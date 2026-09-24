from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Case, IntegerField, Value, When
from django.utils.html import escape
from django.utils import timezone
from datetime import timedelta
import re
from html import unescape
from django.utils.html import strip_tags
from smtplib import SMTPException
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import AdminProfileSerializer, ProfileSerializer, RegisterSerializer, TrackedTokenObtainPairSerializer, UserSerializer
from .ip_tracking import prune_ip_logs, record_ip_event
from .models import UserIPLog
from apps.forum.models import Category, Post, Topic
from .validation_emails import send_character_validation_email
from .email_confirmation import read_token, send_confirmation, notify_previous_email
from .password_recovery import send_reset_link, user_for_reset
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class TrackedTokenObtainPairView(TokenObtainPairView):
    serializer_class = TrackedTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                user = serializer.save()
                send_confirmation(user, 'registration')
                user.last_confirmation_sent_at = timezone.now()
                user.save(update_fields=['last_confirmation_sent_at'])
                record_ip_event(user, request, UserIPLog.Event.REGISTRATION)
        except (SMTPException, OSError):
            return Response({'detail': 'Le service e-mail est indisponible. Aucun compte n’a été créé ; réessayez plus tard.'}, status=503)
        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )


class ConfirmEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        purpose = request.data.get('type')
        data = read_token(request.data.get('jeton', ''), purpose)
        if not data:
            return Response({'detail': 'Ce lien est invalide ou a expiré.'}, status=400)
        with transaction.atomic():
            user = User.objects.select_for_update().filter(pk=data.get('id')).first()
            if user is None:
                return Response({'detail': 'Ce lien est invalide ou a déjà été utilisé.'}, status=400)
            if purpose == 'registration':
                if user.is_active or user.email != data['email']:
                    return Response({'detail': 'Ce lien a déjà été utilisé.'}, status=400)
                user.is_active = True
                user.save(update_fields=['is_active'])
            elif purpose == 'change':
                if not user.is_active or not user.pending_email or user.pending_email != data['email']:
                    return Response({'detail': 'Ce lien a déjà été utilisé.'}, status=400)
                if User.objects.filter(email__iexact=user.pending_email).exclude(pk=user.pk).exists():
                    return Response({'detail': 'Cette adresse est désormais utilisée par un autre compte.'}, status=400)
                user.email = user.pending_email
                user.pending_email = ''
                user.save(update_fields=['email', 'pending_email'])
            else:
                return Response({'detail': 'Ce lien est invalide.'}, status=400)
        return Response({'detail': 'Adresse e-mail confirmée.'})


class ResendConfirmationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            with transaction.atomic():
                user = User.objects.select_for_update().filter(username=request.data.get('username', '')).first()
                if user and not user.is_active and user.check_password(request.data.get('password', '')):
                    last = user.last_confirmation_sent_at
                    if not last or timezone.now() - last >= timedelta(minutes=2):
                        send_confirmation(user, 'registration')
                        user.last_confirmation_sent_at = timezone.now()
                        user.save(update_fields=['last_confirmation_sent_at'])
        except (SMTPException, OSError):
            return Response({'detail': 'Le service e-mail est momentanément indisponible.'}, status=503)
        return Response({'detail': 'Si ce compte attend une confirmation, un nouveau lien a été envoyé.'})


class RequestEmailChangeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        if not user.check_password(request.data.get('password', '')):
            return Response({'password': ['Mot de passe incorrect.']}, status=400)
        field = serializers.EmailField()
        try:
            new_email = field.run_validation(request.data.get('email', '')).strip().lower()
        except serializers.ValidationError as exc:
            return Response({'email': exc.detail}, status=400)
        if User.objects.filter(email__iexact=new_email).exists():
            return Response({'email': ['Cette adresse est déjà utilisée par un autre compte.']}, status=400)
        try:
            with transaction.atomic():
                user = User.objects.select_for_update().get(pk=user.pk)
                last = user.last_confirmation_sent_at
                if last and timezone.now() - last < timedelta(minutes=2):
                    return Response({'detail': 'Veuillez attendre deux minutes avant un nouvel envoi.'}, status=429)
                user.pending_email = new_email
                user.save(update_fields=['pending_email'])
                send_confirmation(user, 'change')
                user.last_confirmation_sent_at = timezone.now()
                user.save(update_fields=['last_confirmation_sent_at'])
                notify_previous_email(user, new_email)
        except (SMTPException, OSError):
            return Response({'detail': 'Le service e-mail est momentanément indisponible.'}, status=503)
        return Response({'detail': 'Un lien de confirmation a été envoyé à la nouvelle adresse.'})


class PasswordResetRequestView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            with transaction.atomic():
                user = User.objects.select_for_update().filter(username=request.data.get('username', '')).first()
                if user and user.is_active and user.email:
                    last = user.last_password_reset_sent_at
                    if not last or timezone.now() - last >= timedelta(minutes=2):
                        send_reset_link(user)
                        user.last_password_reset_sent_at = timezone.now()
                        user.save(update_fields=['last_password_reset_sent_at'])
        except (SMTPException, OSError):
            return Response({'detail': 'Le service e-mail est momentanément indisponible.'}, status=503)
        return Response({'detail': 'Si ce compte existe, un lien de réinitialisation a été envoyé à son adresse e-mail.'})


class PasswordResetConfirmView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user = user_for_reset(request.data.get('uid'), request.data.get('jeton'))
        if user is None:
            return Response({'detail': 'Ce lien est invalide ou a expiré.'}, status=400)
        password = request.data.get('password', '')
        if password != request.data.get('password_confirm'):
            return Response({'password_confirm': ['Les mots de passe ne correspondent pas.']}, status=400)
        try:
            validate_password(password, user)
        except Exception as exc:
            return Response({'password': list(exc.messages)}, status=400)
        with transaction.atomic():
            user = User.objects.select_for_update().get(pk=user.pk)
            if not user_for_reset(request.data.get('uid'), request.data.get('jeton')):
                return Response({'detail': 'Ce lien a déjà été utilisé.'}, status=400)
            user.set_password(password)
            user.save(update_fields=['password'])
        return Response({'detail': 'Mot de passe modifié. Vous pouvez vous connecter.'})


class UserIPHistoryView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        if request.user.role not in ('admin', 'fondatrice'):
            return Response({'detail': 'Réservé à l’administration.'}, status=status.HTTP_403_FORBIDDEN)
        member = generics.get_object_or_404(User, pk=pk)
        prune_ip_logs()
        entries = list(UserIPLog.objects.filter(user=member).values('ip_address', 'event', 'created_at')[:100])
        ips = {entry['ip_address'] for entry in entries}
        shared = []
        if ips:
            for other in User.objects.filter(ip_logs__ip_address__in=ips).exclude(pk=member.pk).distinct().order_by('username')[:100]:
                shared_ips = sorted(set(UserIPLog.objects.filter(user=other, ip_address__in=ips).values_list('ip_address', flat=True)))
                shared.append({'id': other.pk, 'name': other.username, 'shared_ips': shared_ips})
        return Response({'entries': entries, 'shared_accounts': shared})


class LinkedAccountsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        if request.user.role not in ('admin', 'fondatrice'):
            return Response({'detail': 'Réservé à l’administration.'}, status=403)
        member = generics.get_object_or_404(User, pk=pk)
        return Response({
            'main_account': member.main_account_id,
            'linked_accounts': list(member.linked_accounts.values('id', 'username')),
        })

    def patch(self, request, pk):
        if request.user.role not in ('admin', 'fondatrice'):
            return Response({'detail': 'Réservé à l’administration.'}, status=403)
        member = generics.get_object_or_404(User, pk=pk)
        primary_id = request.data.get('main_account')
        if primary_id in (None, ''):
            member.main_account = None
        else:
            primary = User.objects.filter(pk=primary_id).first()
            if primary is None or primary.pk == member.pk or primary.main_account_id or member.linked_accounts.exists():
                return Response({'detail': 'Choisissez un autre compte principal sans rattachement existant.'}, status=400)
            member.main_account = primary
        member.save(update_fields=['main_account'])
        return self.get(request, pk)


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class PresenceView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.user.last_seen = timezone.now()
        request.user.save(update_fields=['last_seen'])
        return Response({'last_seen': request.user.last_seen})


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    pagination_class = None  # tous les membres en une seule requête
    search_fields = ["username", "email"]
    filterset_fields = ["groupe", "race", "role", "sexe"]

    def get_queryset(self):
        return User.objects.annotate(
            role_order=Case(
                When(role='fondatrice', then=Value(0)),
                When(role='admin', then=Value(1)),
                When(role='moderator', then=Value(2)),
                When(role='user', then=Value(3)),
                default=Value(99),
                output_field=IntegerField(),
            )
        ).order_by('role_order', 'date_joined')


class ActivityAlertsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role not in ('admin', 'fondatrice'):
            return Response({'detail': 'Réservé à l’administration.'}, status=403)

        now = timezone.now()
        cutoff = now - timedelta(days=30)
        members = list(User.objects.filter(is_active=True, role='user', fiche_status='validated').only('id', 'username', 'date_joined'))
        member_ids = [member.id for member in members]
        latest = {}
        # Les textes mis en forme comptent pour leurs mots visibles uniquement.
        posts = Post.objects.filter(author_id__in=member_ids).order_by('-created_at').values('author_id', 'content', 'created_at')
        for post in posts.iterator():
            author_id = post['author_id']
            if author_id in latest:
                continue
            content = unescape(strip_tags(post['content']))
            if len(re.findall(r"\b[\w]+(?:[’'-][\w]+)*\b", content, flags=re.UNICODE)) > 150:
                latest[author_id] = post['created_at']

        alerts = []
        for member in members:
            last_long_post = latest.get(member.id)
            reference = last_long_post or member.date_joined
            if reference <= cutoff:
                alerts.append({
                    'id': member.id,
                    'username': member.username,
                    'last_qualifying_post': last_long_post,
                    'days_without_qualifying_post': (now - reference).days,
                })
        alerts.sort(key=lambda item: (-item['days_without_qualifying_post'], item['username'].casefold()))
        return Response({'count': len(alerts), 'members': alerts})


class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = AdminProfileSerializer

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            from .serializers import MemberProfileSerializer
            return MemberProfileSerializer
        return AdminProfileSerializer

    def update(self, request, *args, **kwargs):
        allowed_roles = ('fondatrice', 'admin')
        if not request.user.is_authenticated or request.user.role not in allowed_roles:
            return Response(
                {'detail': 'Seuls les administrateurs peuvent modifier ce profil.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role not in ('fondatrice', 'admin'):
            return Response({'detail': 'Réservé à l’administration.'}, status=403)
        member = self.get_object()
        if member.role != 'user' or member.pk == request.user.pk:
            return Response({'detail': 'Ce compte ne peut pas être supprimé ici.'}, status=403)
        if request.data.get('confirm_username') != member.username:
            return Response({'detail': 'Saisissez le nom exact du personnage pour confirmer.'}, status=400)

        # Les tirages protègent leur message qualifiant : ils doivent être retirés
        # avant la suppression en cascade du compte et de ses sujets.
        from apps.forum.models import LotteryDraw
        with transaction.atomic():
            LotteryDraw.objects.filter(qualifying_post__author=member).delete()
            LotteryDraw.objects.filter(qualifying_post__topic__author=member).delete()
            member.delete()
        return Response(status=204)

    @transaction.atomic
    def perform_update(self, serializer):
        previous_status = serializer.instance.fiche_status
        previous_balance = serializer.instance.compte_bancaire
        validating = previous_status != 'validated' and serializer.validated_data.get('fiche_status') == 'validated'
        founder = None
        if validating:
            founder = User.objects.filter(role='fondatrice', is_active=True).order_by('id').first()
            if founder is None:
                from rest_framework.exceptions import ValidationError
                raise ValidationError({'fiche_status': 'Un compte fondatrice actif est nécessaire pour valider la fiche.'})
        member = serializer.save()
        if member.compte_bancaire != previous_balance:
            from apps.forum.models import ArcanaTransaction
            ArcanaTransaction.objects.create(
                user=member, amount=member.compte_bancaire - previous_balance,
                balance_after=member.compte_bancaire, reason='Ajustement par le staff',
            )

        # Une fiche validée devient une archive de référence : elle ne peut plus
        # être altérée, mais reste visible par toute la communauté.
        if validating:
            archive_category, _ = Category.objects.get_or_create(
                slug='fiches-validees-et-archivees',
                defaults={
                    'name': 'Fiches validées & archivées',
                    'description': 'Archives officielles des personnages validés.',
                    'order': 90,
                },
            )
            fiche = Topic.objects.filter(
                author=member,
                category__slug='fiches-de-presentation-terminees',
            ).order_by('-created_at').first()
            if fiche:
                fiche.category = archive_category
                fiche.is_locked = True
                fiche.save(update_fields=['category', 'is_locked', 'updated_at'])
                name = escape(member.username)
                content = (
                    '<div data-nexus-validation="1" style="padding:1.2rem;border:1px solid rgba(245,215,110,.4);border-radius:8px;background:#0d0a1a;color:#e2d9f3;line-height:1.8">'
                    '<p style="margin:0 0 .4rem;color:#f5d76e;font-size:.75rem;letter-spacing:.15em;text-transform:uppercase">✦ Validation officielle ✦</p>'
                    f'<p style="margin:0 0 .7rem">Bienvenue parmi nous, <strong>{name}</strong> ! Ta fiche est validée.</p>'
                    '<p style="margin:0 0 .7rem">Tu peux désormais prendre part aux RP et faire évoluer ton personnage dans les villes du Nexus. Ta présentation est déplacée dans les <a href="/categories/fiches-validees-et-archivees" style="color:#f5d76e;text-decoration:underline">fiches validées et archivées</a>, où elle reste consultable par les autres joueurs.</p>'
                    '<p style="margin:0 0 .7rem">Pour commencer : <a href="/categories/fiche-personnage" style="color:#f5d76e;text-decoration:underline">publier ta fiche personnage récapitulative</a>, <a href="/topics/demande-de-partenaire-de-rp" style="color:#f5d76e;text-decoration:underline">faire une recherche de RP</a> ou <a href="/topics/agence-immobiliere-demande-de-logement" style="color:#f5d76e;text-decoration:underline">trouver un logement auprès de l’agence immobilière</a>.</p>'
                    '<p style="margin:0 0 .7rem">Nous restons disponibles à tout moment pour répondre à tes questions et t’aider à prendre tes marques. N’hésite pas à contacter l’équipe du staff si tu as besoin d’un coup de main.</p>'
                    '<p style="margin:0;color:#a78bfa;font-style:italic">— Ava Bartholomé</p>'
                    '</div>'
                )
                Post.objects.create(topic=fiche, author=founder, content=content, is_trusted_html=True)
                transaction.on_commit(lambda: send_character_validation_email(member.pk, fiche.pk))
