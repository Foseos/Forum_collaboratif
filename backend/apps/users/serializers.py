from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class UniqueAccountEmailMixin:
    def validate_email(self, value):
        email = value.strip().lower()
        if not email:
            raise serializers.ValidationError("Une adresse e-mail est obligatoire pour chaque compte.")
        if self.instance is not None and self.instance.email.strip().lower() == email:
            return email
        existing = User.objects.filter(email__iexact=email)
        if self.instance is not None:
            existing = existing.exclude(pk=self.instance.pk)
        if existing.exists():
            raise serializers.ValidationError(
                "Cette adresse e-mail est déjà utilisée. Chaque compte, y compris un double compte, doit avoir sa propre adresse."
            )
        return email


# Tous les champs du profil RPG
PROFILE_FIELDS = [
    "id", "username", "email", "role", "show_in_staff_team", "fiche_status", "rp_availability", "avatar", "bio", "signature", "profile_gif_url", "date_joined",
    "last_login", "last_seen",
    "sexe", "race", "nature", "camp", "groupe", "pseudo", "situation", "metier",
    "age_personnage", "pouvoirs", "lieu_residence", "quartier_residentiel", "credits", "compte_bancaire",
    "avatar_name", "double_compte", "email_topic_replies",
]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [field for field in PROFILE_FIELDS if field != 'email']
        read_only_fields = ["id", "role", "show_in_staff_team", "fiche_status", "date_joined", "last_seen", "compte_bancaire"]


class MemberProfileSerializer(UserSerializer):
    presentation_topic_slug = serializers.SerializerMethodField()
    recap_topic_slug = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ["presentation_topic_slug", "recap_topic_slug"]
        read_only_fields = UserSerializer.Meta.read_only_fields + ["presentation_topic_slug", "recap_topic_slug"]

    def get_presentation_topic_slug(self, obj):
        if obj.fiche_status != User.FicheStatus.VALIDATED:
            return None
        from apps.forum.models import Topic
        return Topic.objects.filter(
            author=obj, category__slug="fiches-validees-et-archivees",
        ).order_by("-created_at").values_list("slug", flat=True).first()

    def get_recap_topic_slug(self, obj):
        if obj.fiche_status != User.FicheStatus.VALIDATED:
            return None
        from apps.forum.models import Topic
        return Topic.objects.filter(
            author=obj, category__slug="fiche-personnage",
        ).exclude(slug="modele-fiche-personnage").order_by("-created_at").values_list("slug", flat=True).first()


class RegisterSerializer(UniqueAccountEmailMixin, serializers.ModelSerializer):
    email = serializers.EmailField(required=True, allow_blank=False)
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password_confirm"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password_confirm": "Les mots de passe ne correspondent pas."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        validated_data['is_active'] = False
        user = User.objects.create_user(**validated_data)
        return user


class ProfileSerializer(UniqueAccountEmailMixin, serializers.ModelSerializer):
    """
    Sérialiseur du profil utilisateur.
    Le champ `compte_bancaire` est en lecture seule pour les utilisateurs normaux.
    Seul un admin peut le modifier (via AdminProfileSerializer).
    """

    presentation_topic_slug = serializers.SerializerMethodField()
    recap_topic_slug = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = PROFILE_FIELDS + ["presentation_topic_slug", "recap_topic_slug"]
        read_only_fields = [
            "id", "username", "email", "role", "show_in_staff_team", "fiche_status", "race", "nature", "groupe", "date_joined", "last_seen", "compte_bancaire", "presentation_topic_slug", "recap_topic_slug",
        ]

    def validate(self, attrs):
        protected = {'race', 'nature', 'groupe'} & set(self.initial_data)
        if protected:
            raise serializers.ValidationError({field: 'Attribution réservée à la fondatrice.' for field in protected})
        return super().validate(attrs)

    def get_presentation_topic_slug(self, obj):
        return MemberProfileSerializer.get_presentation_topic_slug(self, obj)

    def get_recap_topic_slug(self, obj):
        return MemberProfileSerializer.get_recap_topic_slug(self, obj)

    def validate_avatar_name(self, value):
        request = self.context.get("request")
        if not request or request.user.role not in ("admin", "fondatrice"):
            raise serializers.ValidationError("Seuls les administrateurs peuvent modifier la célébrité du bottin.")
        return value


class AdminProfileSerializer(UniqueAccountEmailMixin, serializers.ModelSerializer):
    """
    Sérialiseur admin : permet de modifier le compte_bancaire RP
    et le rôle d'un utilisateur.
    """

    class Meta:
        model = User
        fields = PROFILE_FIELDS
        read_only_fields = ["id", "date_joined"]

    def validate(self, attrs):
        request = self.context.get('request')
        if not request or request.user.role != 'fondatrice':
            protected = {
                field for field in ('race', 'nature', 'groupe')
                if field in attrs and getattr(self.instance, field) != attrs[field]
            }
            if protected:
                raise serializers.ValidationError({field: 'Attribution réservée à la fondatrice.' for field in protected})
        return super().validate(attrs)

    def validate_username(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError('Le nom d’utilisateur ne peut pas être vide.')
        if self.instance and value == self.instance.username:
            return value
        request = self.context.get('request')
        if not request or request.user.role != 'fondatrice':
            raise serializers.ValidationError('Seule la fondatrice peut changer un nom d’utilisateur.')
        if User.objects.filter(username__iexact=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError('Ce nom d’utilisateur est déjà utilisé.')
        return value
