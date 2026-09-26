from datetime import timedelta
import secrets

from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.html import escape
from django.db.models import Count, Q, OuterRef, Subquery, F
from django.utils import timezone
from rest_framework import generics, permissions, serializers, status, viewsets
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from apps.users.permissions import IsAdminOrModerator

from .models import ArcanaTransaction, AvatarDirectoryEntry, Category, ChatMessage, ContactRequest, DemonicFormEntry, Post, PrivateMessage, Reaction, SitePage, Topic
from .avatar_directory import clean_avatar_name, scenario_avatar
from .permissions import IsAuthorOrModeratorOrReadOnly, IsTopicNotLocked
from .rewards import award_publication
from .lottery import draw_for_user, lottery_status
from .reply_emails import send_topic_reply_emails
from .private_message_emails import send_private_message_email
from .serializers import (
    CategoryDetailSerializer,
    CategorySerializer,
    ChatMessageSerializer,
    DemonicFormEntrySerializer,
    PostCreateSerializer,
    PostSerializer,
    PrivateMessageSerializer,
    ReactionSerializer,
    SitePageSerializer,
    TopicCreateSerializer,
    TopicDetailSerializer,
    TopicSerializer,
)


class ContactRequestSerializer(serializers.Serializer):
    kind = serializers.ChoiceField(choices=ContactRequest.Kind.choices)
    email = serializers.EmailField(required=False, allow_blank=True)
    message = serializers.CharField(max_length=3000, min_length=10)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), required=False)

    def validate(self, attrs):
        if attrs['kind'] == ContactRequest.Kind.REPORT and not attrs.get('post'):
            raise serializers.ValidationError({'post': 'Indiquez le message à signaler.'})
        if attrs['kind'] != ContactRequest.Kind.REPORT and attrs.get('post'):
            raise serializers.ValidationError({'post': 'Ce champ est réservé aux signalements.'})
        request = self.context['request']
        email = request.user.email if request.user.is_authenticated else attrs.get('email', '')
        if not email:
            raise serializers.ValidationError({'email': 'Indiquez une adresse pour recevoir une réponse.'})
        attrs['email'] = email.strip().lower()
        return attrs


class ContactRequestView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ContactRequestSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        if request.user.is_authenticated and data['kind'] != ContactRequest.Kind.REPORT:
            ava = get_user_model().objects.filter(username__iexact='Ava Bartholomé', is_active=True).first()
            if ava and ava.pk != request.user.pk:
                subject = {
                    ContactRequest.Kind.PRIVACY: 'Demande concernant mes données',
                    ContactRequest.Kind.REPORT: 'Signalement d’un message',
                    ContactRequest.Kind.GENERAL: 'Question à l’administration',
                }[data['kind']]
                if PrivateMessage.objects.filter(
                    sender=request.user, recipient=ava, subject=subject,
                    created_at__gte=timezone.now() - timedelta(minutes=1),
                ).exists():
                    return Response({'detail': 'Une demande vient déjà d’être envoyée. Réessayez dans une minute.'}, status=429)
                body = data['message']
                if data.get('post'):
                    post = data['post']
                    body = f"Message signalé : {request.build_absolute_uri(f'/topics/{post.topic.slug}')} (message n° {post.pk})\n\n{body}"
                pm = PrivateMessage.objects.create(sender=request.user, recipient=ava, subject=subject, body=body)
                transaction.on_commit(lambda: send_private_message_email(pm.pk))
                return Response({'detail': 'Votre message privé a été envoyé à Ava Bartholomé.'}, status=201)
        if ContactRequest.objects.filter(
            email__iexact=data['email'],
            created_at__gte=timezone.now() - timedelta(minutes=1),
        ).exists():
            return Response({'detail': 'Une demande vient déjà d’être envoyée. Réessayez dans une minute.'}, status=429)
        ContactRequest.objects.create(
            **data, author=request.user if request.user.is_authenticated else None,
        )
        return Response({'detail': 'Votre demande a été transmise à l’administration.'}, status=201)


class ContactRequestAdminView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role not in ('admin', 'fondatrice'):
            return Response(status=403)
        if request.query_params.get('counts') == '1':
            pending = ContactRequest.objects.filter(is_resolved=False)
            return Response({
                'reports': pending.filter(kind=ContactRequest.Kind.REPORT).count(),
                'questions': pending.exclude(kind=ContactRequest.Kind.REPORT).count(),
            })
        requests = ContactRequest.objects.select_related('post__topic', 'author')
        if request.query_params.get('kind') == 'report':
            requests = requests.filter(kind=ContactRequest.Kind.REPORT)
        elif request.query_params.get('kind') == 'other':
            requests = requests.exclude(kind=ContactRequest.Kind.REPORT)
        requests = requests[:100]
        return Response([{
            'id': item.pk,
            'kind': item.kind,
            'email': item.email,
            'message': item.message,
            'post_id': item.post_id,
            'topic_slug': item.post.topic.slug if item.post else None,
            'author': item.author.username if item.author else None,
            'is_resolved': item.is_resolved,
            'created_at': item.created_at,
        } for item in requests])

    def patch(self, request):
        if request.user.role not in ('admin', 'fondatrice'):
            return Response(status=403)
        item = generics.get_object_or_404(ContactRequest, pk=request.data.get('id'))
        if not isinstance(request.data.get('is_resolved'), bool):
            return Response({'is_resolved': ['Indiquez vrai ou faux.']}, status=400)
        item.is_resolved = request.data['is_resolved']
        item.save(update_fields=['is_resolved'])
        return Response({'id': item.pk, 'is_resolved': item.is_resolved})


# Ces rubriques restent accessibles avant validation afin qu'un nouveau membre
# puisse lire les règles, demander de l'aide et soumettre sa fiche.
NON_RP_CATEGORY_SLUGS = {
    'bienvenue-san-francisco', 'scenarios-a-prendre', 'modele-fiche-de-presentation',
    'fiches-de-presentation-terminees', 'fiche-personnage', 'reglement-magique',
    'reglement-du-forum', 'creatures-et-races', 'factions', 'bottin-des-avatars',
    'bottin-des-formes-demoniaques', 'contextes-et-animations', 'liens-magiques',
    'recherche-de-rp', 'demande-partenaire-rp', 'une-question', 'questions-invites',
    'questions-membres', 'signaler-absence', 'ma-situation-magique',
    'demande-double-compte', 'partenariats-et-arcades', 'jeu-des-prenoms',
    'demande-de-partenariats', 'grimoire-des-pouvoirs',
}


def requires_validated_character(category):
    return category.slug not in NON_RP_CATEGORY_SLUGS


def is_staff(user):
    return user.is_authenticated and user.role in ('admin', 'fondatrice', 'moderator')


class PartnershipGuestThrottle(AnonRateThrottle):
    rate = '3/day'


class PartnershipRequestSerializer(serializers.Serializer):
    forum_name = serializers.CharField(max_length=120)
    forum_url = serializers.URLField(max_length=500)
    concept = serializers.CharField(max_length=2000)
    opened_at = serializers.CharField(max_length=100, required=False, allow_blank=True)
    partnership_type = serializers.ChoiceField(choices=['fiches', 'boutons', 'les deux'])
    reciprocal_url = serializers.URLField(max_length=500, required=False, allow_blank=True)
    presentation = serializers.CharField(max_length=3000, required=False, allow_blank=True)
    button_url = serializers.URLField(max_length=500, required=False, allow_blank=True)
    message = serializers.CharField(max_length=2000, required=False, allow_blank=True)
    website = serializers.CharField(required=False, allow_blank=True)  # Champ piège antispam.


class PartnershipRequestView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [PartnershipGuestThrottle]

    @transaction.atomic
    def post(self, request):
        serializer = PartnershipRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        if data.get('website'):
            return Response({'detail': 'Demande invalide.'}, status=status.HTTP_400_BAD_REQUEST)
        category = Category.objects.filter(slug='demande-de-partenariats').first()
        if category is None:
            return Response({'detail': 'La rubrique des partenariats est indisponible.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        author = request.user if request.user.is_authenticated else get_user_model().objects.filter(role='fondatrice', is_active=True).first()
        if author is None:
            return Response({'detail': 'La demande invitée est momentanément indisponible.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        lines = [
            ('Forum', data['forum_name']), ('Adresse', data['forum_url']),
            ('Univers et concept', data['concept']), ('Ouverture', data.get('opened_at', '')),
            ('Échange souhaité', data['partnership_type']),
            ('Notre affichage chez vous', data.get('reciprocal_url', '')),
            ('Votre fiche de partenariat', data.get('presentation', '')),
            ('Votre bouton', data.get('button_url', '')),
            ('Un mot pour le staff', data.get('message', '')),
        ]
        body = '<p><em>Demande envoyée par un invité.</em></p>' if not request.user.is_authenticated else ''
        body += ''.join(f'<p><strong>{escape(label)} :</strong> {escape(value)}</p>' for label, value in lines if value)
        prefix = 'Demande invitée' if not request.user.is_authenticated else 'Partenariat'
        topic = Topic.objects.create(title=f"{prefix} — {data['forum_name']}", category=category, author=author)
        Post.objects.create(topic=topic, author=author, content=body, is_trusted_html=False)
        return Response({'slug': topic.slug}, status=status.HTTP_201_CREATED)


class PartnershipApproveView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request, slug):
        if not is_staff(request.user):
            return Response({'detail': 'Action réservée au staff.'}, status=status.HTTP_403_FORBIDDEN)
        topic = generics.get_object_or_404(Topic, slug=slug, category__slug='demande-de-partenariats')
        if topic.slug == 'proposer-un-partenariat':
            return Response({'detail': 'Le guide ne peut pas être déplacé.'}, status=status.HTTP_400_BAD_REQUEST)
        destination = generics.get_object_or_404(Category, slug='nos-partenaires')
        topic.category = destination
        topic.is_locked = True
        topic.save(update_fields=['category', 'is_locked', 'updated_at'])
        return Response({'slug': topic.slug, 'category': destination.slug})


class IsAdminOrFondatrice(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role in ('admin', 'fondatrice')


class DemonicFormDirectoryView(generics.ListCreateAPIView):
    queryset = DemonicFormEntry.objects.all()
    serializer_class = DemonicFormEntrySerializer
    permission_classes = [IsAdminOrFondatrice]
    pagination_class = None


class DemonicFormEntryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DemonicFormEntry.objects.all()
    serializer_class = DemonicFormEntrySerializer
    permission_classes = [IsAdminOrFondatrice]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    lookup_field = "slug"
    search_fields = ["name", "description"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CategoryDetailSerializer
        return CategorySerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminOrModerator()]
        return [permissions.AllowAny()]


class AvatarDirectoryEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = AvatarDirectoryEntry
        fields = ("id", "avatar", "character", "status", "url", "negotiable")

    def validate_avatar(self, value):
        value = clean_avatar_name(value)
        if not value:
            raise serializers.ValidationError("Indiquez une célébrité.")
        return value

    def validate_url(self, value):
        if value and (not value.startswith("/") or value.startswith("//")):
            raise serializers.ValidationError("Utilisez un lien interne commençant par /.")
        return value


class AvatarDirectoryView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        User = get_user_model()
        entries = []
        for member in User.objects.filter(is_active=True).exclude(avatar_name="").only(
            "id", "username", "pseudo", "avatar_name", "fiche_status"
        ):
            entries.append({
                "avatar": clean_avatar_name(member.avatar_name),
                "character": member.username,
                "status": "taken" if member.fiche_status == "validated" else "pending",
                "url": f"/membres/{member.pk}",
                "kind": "member",
                "member_id": member.pk,
            })

        missing_scenarios = []
        scenarios = Topic.objects.filter(category__slug="scenarios-a-prendre").prefetch_related("posts")
        for topic in scenarios:
            post = next(iter(topic.posts.all()), None)
            actor = topic.scenario_avatar_name or scenario_avatar(post.content if post else "")
            if not actor:
                missing_scenarios.append({"character": topic.title, "url": f"/topics/{topic.slug}"})
                continue
            entries.append({
                "avatar": actor,
                "character": topic.title,
                "status": "taken" if topic.scenario_status == "played" else "scenario",
                "url": f"/topics/{topic.slug}",
                "kind": "scenario",
                "scenario_status": topic.scenario_status,
                "scenario_slug": topic.slug,
                "negotiable": "négociable" in (post.content or "").lower(),
            })

        for manual in AvatarDirectoryEntry.objects.all():
            entries.append({
                "id": manual.pk,
                "avatar": manual.avatar,
                "character": manual.character,
                "status": manual.status,
                "url": manual.url,
                "kind": "manual",
                "negotiable": manual.negotiable,
            })

        entries = [entry for entry in entries if entry["avatar"]]
        entries.sort(key=lambda entry: (entry["avatar"].casefold(), entry["character"].casefold()))
        return Response({"entries": entries, "missing_scenarios": missing_scenarios})

    def post(self, request, *args, **kwargs):
        if not IsAdminOrFondatrice().has_permission(request, self):
            return Response({"detail": "Réservé à l’administration."}, status=status.HTTP_403_FORBIDDEN)
        serializer = AvatarDirectoryEntrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AvatarDirectoryEntryDetailView(generics.GenericAPIView):
    permission_classes = [IsAdminOrFondatrice]

    def patch(self, request, pk):
        entry = generics.get_object_or_404(AvatarDirectoryEntry, pk=pk)
        serializer = AvatarDirectoryEntrySerializer(entry, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        entry = generics.get_object_or_404(AvatarDirectoryEntry, pk=pk)
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TopicViewSet(viewsets.ModelViewSet):
    lookup_field = "slug"
    search_fields = ["title"]
    filterset_fields = ["is_pinned", "is_locked", "author"]

    def get_queryset(self):
        queryset = Topic.objects.annotate(post_count=Count("posts")).order_by(
            "-is_pinned", "-created_at", "-pk"
        )
        category_slug = self.kwargs.get("category_slug")
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
            if category_slug == "scenarios-a-prendre":
                queryset = queryset.order_by("-is_pinned", "created_at", "pk")
        return queryset

    def get_serializer_class(self):
        if self.action == "create":
            return TopicCreateSerializer
        if self.action == "retrieve":
            return TopicDetailSerializer
        return TopicSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticated()]
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthorOrModeratorOrReadOnly()]
        return [permissions.AllowAny()]

    @transaction.atomic
    def perform_create(self, serializer):
        category_slug = self.kwargs.get("category_slug")
        category = Category.objects.get(slug=category_slug)
        if category.slug == 'bienvenue-san-francisco':
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Créez votre fiche dans la rubrique des présentations.")
        if category.slug == 'parrainage' and self.request.user.role not in ('admin', 'fondatrice'):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Seule l'administration peut ouvrir un sujet de parrainage.")
        if category.slug == 'fiche-personnage':
            from rest_framework.exceptions import PermissionDenied
            if self.request.user.fiche_status != 'validated' and not is_staff(self.request.user):
                raise PermissionDenied("Votre fiche doit être validée avant de publier un récapitulatif.")
            if Topic.objects.filter(author=self.request.user, category=category).exclude(slug='modele-fiche-personnage').exists():
                raise PermissionDenied("Vous avez déjà un récapitulatif : mettez à jour ce sujet.")
        if category.slug == 'modele-fiche-de-presentation' and self.request.user.role not in ('admin', 'fondatrice'):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Le modèle de fiche est publié par l’administration.")
        if category.slug == 'fiches-validees-et-archivees':
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Les fiches sont archivées après validation par l’administration.")
        if category.slug == 'nos-partenaires' and not is_staff(self.request.user):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Les partenaires sont ajoutés après acceptation par le staff.")
        if category.slug == 'fiches-de-presentation-terminees' and self.request.user.role not in ('admin', 'fondatrice'):
            from rest_framework.exceptions import PermissionDenied
            if self.request.user.fiche_status == 'validated':
                raise PermissionDenied("Votre fiche est déjà validée.")
            if Topic.objects.filter(author=self.request.user, category=category).exists():
                raise PermissionDenied("Vous avez déjà une fiche en attente : modifiez-la dans son sujet.")
        if category.slug == 'scenarios-a-prendre' and self.request.user.role not in ('admin', 'fondatrice'):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Seuls les administrateurs peuvent créer un scénario et réserver son avatar.")
        if requires_validated_character(category) and not is_staff(self.request.user) and self.request.user.fiche_status != 'validated':
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Votre fiche doit être validée avant de créer un sujet RP.")
        topic = serializer.save(author=self.request.user, category=category)
        award_publication(topic.posts.get())

    @transaction.atomic
    def perform_update(self, serializer):
        if 'category' in self.request.data:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Le déplacement d’un sujet se fait uniquement depuis l’administration.")
        if serializer.instance.category.slug in ('fiches-de-presentation-terminees', 'fiches-validees-et-archivees'):
            from rest_framework.exceptions import PermissionDenied
            if serializer.instance.is_locked and self.request.user.role not in ('admin', 'fondatrice'):
                raise PermissionDenied("Une fiche archivée ne peut plus être modifiée.")
            if self.request.user.role not in ('admin', 'fondatrice') and any(
                field in serializer.validated_data for field in ('category', 'is_locked')
            ):
                raise PermissionDenied("Seule l’administration peut déplacer ou verrouiller une fiche.")
        if serializer.instance.category.slug == 'scenarios-a-prendre' and self.request.user.role not in ('admin', 'fondatrice'):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Seuls les administrateurs peuvent modifier un scénario du bottin.")
        if 'scenario_avatar_name' in serializer.validated_data:
            topic = serializer.instance
            first_post = topic.posts.order_by('created_at', 'pk').first()
            previous = topic.scenario_avatar_name or scenario_avatar(first_post.content if first_post else '')
            replacement = serializer.validated_data['scenario_avatar_name']
            if first_post and previous and previous != replacement and previous in first_post.content:
                first_post.content = first_post.content.replace(previous, replacement)
                first_post.save(update_fields=['content', 'updated_at'])
        serializer.save()

    def perform_destroy(self, instance):
        if instance.category.slug in ('fiches-de-presentation-terminees', 'fiches-validees-et-archivees'):
            from rest_framework.exceptions import PermissionDenied
            if self.request.user.role not in ('admin', 'fondatrice'):
                raise PermissionDenied("Seule l’administration peut supprimer une fiche de présentation.")
        if instance.category.slug == 'scenarios-a-prendre' and self.request.user.role not in ('admin', 'fondatrice'):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Seuls les administrateurs peuvent supprimer un scénario du bottin.")
        instance.delete()


class PostViewSet(viewsets.ModelViewSet):
    search_fields = ["content"]
    permission_classes = [IsAuthorOrModeratorOrReadOnly, IsTopicNotLocked]

    def get_queryset(self):
        queryset = Post.objects.select_related("author").prefetch_related("reactions")
        topic_slug = self.kwargs.get("topic_slug")
        if topic_slug:
            queryset = queryset.filter(topic__slug=topic_slug)
        return queryset

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return PostCreateSerializer
        return PostSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticated(), IsTopicNotLocked()]
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthorOrModeratorOrReadOnly()]
        return [permissions.AllowAny()]

    def _protect_scenario_sheet(self, post):
        if post.topic.category.slug != 'scenarios-a-prendre':
            return
        first_post = post.topic.posts.order_by('created_at', 'pk').first()
        if first_post and first_post.pk == post.pk and self.request.user.role not in ('admin', 'fondatrice'):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Seule l’administration peut modifier la fiche d’un scénario.")

    def perform_update(self, serializer):
        if serializer.instance.dice_result is not None:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Un lancer de dé ne peut pas être modifié.")
        if serializer.instance.topic.is_locked and self.request.user.role not in ('admin', 'fondatrice'):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Ce sujet est archivé et ne peut plus être modifié.")
        self._protect_scenario_sheet(serializer.instance)
        serializer.save(is_trusted_html=self.request.user.role in ('admin', 'fondatrice'))

    def perform_destroy(self, instance):
        if instance.dice_result is not None:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Un lancer de dé ne peut pas être supprimé.")
        if instance.topic.is_locked and self.request.user.role not in ('admin', 'fondatrice'):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Ce sujet est archivé et ne peut plus être modifié.")
        self._protect_scenario_sheet(instance)
        instance.delete()

    @transaction.atomic
    def perform_create(self, serializer):
        topic_slug = self.kwargs.get("topic_slug")
        topic = Topic.objects.get(slug=topic_slug)
        if topic.is_locked:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Ce sujet est archivé et ne peut plus recevoir de réponses.")
        if requires_validated_character(topic.category) and not is_staff(self.request.user) and self.request.user.fiche_status != 'validated':
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Votre fiche doit être validée avant de répondre dans les zones RP.")
        post = serializer.save(
            author=self.request.user, topic=topic,
            is_trusted_html=self.request.user.role in ('admin', 'fondatrice'),
        )

        award_publication(post)
        transaction.on_commit(lambda: send_topic_reply_emails(topic, post.author_id))


class DiceRollView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request, slug):
        topic = generics.get_object_or_404(Topic.objects.select_for_update().select_related('category'), slug=slug)
        if topic.category.slug != 'contextes-et-animations':
            return Response({'detail': 'Les dés sont réservés à Contexte et animations.'}, status=400)
        if topic.slug == 'loterie-des-arcana-flouz':
            return Response({'detail': 'Le Dé du destin ne se lance pas dans la loterie.'}, status=400)
        if topic.is_locked:
            return Response({'detail': 'Ce sujet est verrouillé.'}, status=400)
        intention = str(request.data.get('intention', '')).strip()
        if not intention or len(intention) > 280:
            return Response({'intention': ['Décrivez l’action en 280 caractères maximum.']}, status=400)
        last = Post.objects.filter(topic=topic, author=request.user, dice_result__isnull=False).order_by('-created_at').first()
        if last and timezone.now() - last.created_at < timedelta(seconds=30):
            return Response({'detail': 'Attendez trente secondes avant un autre lancer.'}, status=429)
        post = Post.objects.create(
            topic=topic, author=request.user,
            content=f"Action tentée : {escape(intention)}", dice_result=secrets.randbelow(6) + 1,
        )
        transaction.on_commit(lambda: send_topic_reply_emails(topic, post.author_id))
        return Response(PostSerializer(post, context={'request': request}).data, status=201)


class LotteryDrawView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        state, _ = lottery_status(request.user)
        return Response(state)

    def post(self, request):
        draw, error = draw_for_user(request.user)
        if error:
            return Response({'detail': error}, status=400)
        return Response({'prize': draw.prize, 'qualifying_topic': draw.qualifying_post.topic.title,
                         'created_at': draw.created_at}, status=201)


class ArcanaHistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        entries = ArcanaTransaction.objects.filter(user=request.user)[:50]
        return Response([{'amount': entry.amount, 'balance_after': entry.balance_after,
                          'reason': entry.reason, 'created_at': entry.created_at} for entry in entries])


class NextStepsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'recap': Topic.objects.filter(author=user, category__slug='fiche-personnage').exists(),
            'housing': Post.objects.filter(author=user, topic__slug='agence-immobiliere-demande-de-logement').exists(),
            'rp_search': (Post.objects.filter(author=user, topic__slug='demande-de-partenaire-de-rp').exists()
                          or Topic.objects.filter(author=user, category__slug='recherche-de-rp').exists()),
        })


class ReactionToggleView(generics.CreateAPIView, generics.DestroyAPIView):
    serializer_class = ReactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reaction.objects.filter(post_id=self.kwargs["post_id"])

    def create(self, request, *args, **kwargs):
        post_id = self.kwargs["post_id"]
        reaction_type = request.data.get("reaction_type", "like")

        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response(
                {"detail": "Post non trouvé."}, status=status.HTTP_404_NOT_FOUND
            )

        reaction, created = Reaction.objects.get_or_create(
            post=post,
            user=request.user,
            reaction_type=reaction_type,
        )

        if not created:
            reaction.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = self.get_serializer(reaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ChatMessageView(generics.ListCreateAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None  # retourne un tableau JSON simple, sans pagination

    def get_queryset(self):
        return ChatMessage.objects.select_related('author').filter(
            created_at__gte=timezone.now() - timedelta(hours=24)
        ).order_by('-created_at', '-id')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ChatPresenceView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        now = timezone.now()
        User = get_user_model()
        User.objects.filter(pk=request.user.pk).update(chat_last_seen=now)
        members = User.objects.filter(
            is_active=True, chat_last_seen__gte=now - timedelta(seconds=45)
        ).order_by('username')
        return Response([
            {'id': member.pk, 'username': member.username,
             'pseudo': member.pseudo,
             'avatar': request.build_absolute_uri(member.avatar.url) if member.avatar else None}
            for member in members
        ])


class ForumStatsView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        User = get_user_model()
        cutoff = timezone.now() - timedelta(hours=48)

        member_count = User.objects.count()
        message_count = Post.objects.count()

        newest = User.objects.order_by('-date_joined').first()
        newest_member = None
        if newest:
            avatar_url = newest.avatar.url if newest.avatar else None
            if avatar_url and request.build_absolute_uri:
                avatar_url = request.build_absolute_uri(avatar_url)
            newest_member = {
                'username': newest.username,
                'pseudo': getattr(newest, 'pseudo', ''),
                'avatar': avatar_url,
                'date_joined': newest.date_joined,
            }

        recent_qs = User.objects.filter(last_login__gte=cutoff).order_by('-last_login')[:20]
        recent_members = []
        for u in recent_qs:
            avatar_url = u.avatar.url if u.avatar else None
            if avatar_url and request.build_absolute_uri:
                avatar_url = request.build_absolute_uri(avatar_url)
            recent_members.append({
                'username': u.username,
                'pseudo': getattr(u, 'pseudo', ''),
                'avatar': avatar_url,
                'last_login': u.last_login,
            })

        return Response({
            'member_count': member_count,
            'message_count': message_count,
            'newest_member': newest_member,
            'recent_members': recent_members,
        })


class SitePageView(generics.RetrieveUpdateAPIView):
    serializer_class = SitePageSerializer
    permission_classes = [IsAdminOrFondatrice]
    lookup_field = 'slug'

    def get_object(self):
        slug = self.kwargs['slug']
        obj, _ = SitePage.objects.get_or_create(slug=slug)
        return obj

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


# ── Messages privés ──────────────────────────────────────────────────

class PMInboxView(generics.ListAPIView):
    serializer_class = PrivateMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PrivateMessage.objects.filter(
            recipient=self.request.user,
            is_deleted_by_recipient=False,
        ).select_related('sender', 'recipient')


class PMSentView(generics.ListAPIView):
    serializer_class = PrivateMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PrivateMessage.objects.filter(
            sender=self.request.user,
            is_deleted_by_sender=False,
        ).select_related('sender', 'recipient')


class PMSendView(generics.CreateAPIView):
    serializer_class = PrivateMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        pm = serializer.save(sender=self.request.user)
        transaction.on_commit(lambda: send_private_message_email(pm.pk))


class PMDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = PrivateMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return PrivateMessage.objects.filter(
            Q(sender=user) | Q(recipient=user)
        ).select_related('sender', 'recipient')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.recipient == request.user and not instance.is_read:
            instance.is_read = True
            instance.save(update_fields=['is_read'])
        return Response(self.get_serializer(instance).data)

    def perform_destroy(self, instance):
        user = self.request.user
        if instance.sender == user:
            instance.is_deleted_by_sender = True
        if instance.recipient == user:
            instance.is_deleted_by_recipient = True
        instance.save()


class PMMarkReadView(generics.UpdateAPIView):
    serializer_class = PrivateMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PrivateMessage.objects.filter(recipient=self.request.user)

    def patch(self, request, *args, **kwargs):
        msg = self.get_object()
        msg.is_read = not msg.is_read
        msg.save(update_fields=['is_read'])
        return Response({'is_read': msg.is_read})


class PMUnreadCountView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        count = PrivateMessage.objects.filter(
            recipient=request.user,
            is_read=False,
            is_deleted_by_recipient=False,
        ).count()
        return Response({'unread': count})


class UserParticipatedTopicsView(generics.ListAPIView):
    serializer_class = TopicSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return (
                Topic.objects.filter(posts__author_id=user_id)
                .distinct()
                .annotate(post_count=Count("posts"))
                .order_by('-created_at')
            )
        if self.request.user.is_authenticated:
            return (
                Topic.objects.filter(posts__author=self.request.user)
                .distinct()
                .annotate(post_count=Count("posts"))
                .order_by('-created_at')
            )
        return Topic.objects.none()


class MyRPView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        latest = Post.objects.filter(topic_id=OuterRef('pk')).order_by('-created_at', '-pk')
        joined = Post.objects.filter(author=self.request.user).values('topic_id')
        queryset = Topic.objects.filter(
            Q(pk__in=joined) | Q(author=self.request.user)
        ).exclude(category__slug__in=NON_RP_CATEGORY_SLUGS).select_related('category').annotate(
            post_count=Count('posts'),
            last_author_id=Subquery(latest.values('author_id')[:1]),
            last_author_name=Subquery(latest.values('author__username')[:1]),
            last_activity=Subquery(latest.values('created_at')[:1]),
        ).order_by(F('last_activity').desc(nulls_last=True), '-pk')
        selection = self.request.query_params.get('status')
        if selection == 'waiting':
            queryset = queryset.filter(is_locked=False, last_author_id__isnull=False).exclude(last_author_id=self.request.user.pk)
        elif selection == 'active':
            queryset = queryset.filter(is_locked=False)
        elif selection == 'locked':
            queryset = queryset.filter(is_locked=True)
        return queryset

    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.get_queryset())
        result = [{
            'id': topic.pk, 'title': topic.title, 'slug': topic.slug,
            'category': topic.category.name, 'is_locked': topic.is_locked,
            'post_count': topic.post_count, 'last_author': topic.last_author_name,
            'last_activity': topic.last_activity,
            'awaiting_reply': not topic.is_locked and topic.last_author_id is not None and topic.last_author_id != request.user.pk,
        } for topic in page]
        return self.get_paginated_response(result)
