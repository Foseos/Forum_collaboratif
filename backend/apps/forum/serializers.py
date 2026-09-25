import re

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Category, ChatMessage, DemonicFormEntry, Post, PrivateMessage, Reaction, SitePage, Topic
from .html_safety import sanitize_member_html

User = get_user_model()


class DemonicFormEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = DemonicFormEntry
        fields = ["id", "name", "image_url", "character"]
        read_only_fields = ["id"]


class AuthorSerializer(serializers.ModelSerializer):
    messages_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id", "username", "avatar", "avatar_name", "signature", "profile_gif_url",
            "pseudo", "groupe", "race", "role", "fiche_status",
            "sexe", "nature", "camp",
            "situation", "metier", "age_personnage",
            "pouvoirs", "lieu_residence", "quartier_residentiel", "credits",
            "compte_bancaire", "double_compte",
            "date_joined", "messages_count",
        ]

    def get_messages_count(self, obj):
        return obj.posts.count()


class ReactionSerializer(serializers.ModelSerializer):
    user = AuthorSerializer(read_only=True)

    class Meta:
        model = Reaction
        fields = ["id", "user", "reaction_type", "created_at"]
        read_only_fields = ["id", "user", "created_at"]


class ReactionCountSerializer(serializers.Serializer):
    reaction_type = serializers.CharField()
    count = serializers.IntegerField()


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    content = serializers.SerializerMethodField()
    reactions_count = serializers.SerializerMethodField()
    user_reactions = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id", "author", "content", "dice_result", "created_at", "updated_at",
            "is_edited", "reactions_count", "user_reactions",
        ]
        read_only_fields = ["id", "author", "created_at", "updated_at", "is_edited"]

    def get_reactions_count(self, obj):
        counts = {}
        for reaction in obj.reactions.all():
            counts[reaction.reaction_type] = counts.get(reaction.reaction_type, 0) + 1
        return counts

    def get_content(self, obj):
        if obj.is_trusted_html:
            return obj.content
        return sanitize_member_html(obj.content)

    def get_user_reactions(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return list(
                obj.reactions.filter(user=request.user).values_list(
                    "reaction_type", flat=True
                )
            )
        return []


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "content"]
        read_only_fields = ["id"]

    def validate_content(self, value):
        request = self.context.get('request')
        if request and request.user.role in ('admin', 'fondatrice'):
            return value
        return sanitize_member_html(value)


class TopicSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    post_count = serializers.IntegerField(read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)
    category_slug = serializers.CharField(source="category.slug", read_only=True)
    first_image = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = [
            "id", "title", "slug", "category", "category_name", "category_slug", "author",
            "is_pinned", "is_locked", "scenario_status", "scenario_avatar_name", "scenario_links", "scenario_link_cards", "post_count", "created_at", "updated_at",
            "first_image",
        ]
        read_only_fields = [
            "id", "slug", "author", "category", "post_count", "created_at", "updated_at",
        ]

    def validate_is_locked(self, value):
        request = self.context.get('request')
        if not request or request.user.role not in ('admin', 'fondatrice'):
            raise serializers.ValidationError("Seule l’administration peut verrouiller un sujet.")
        if value and self.instance and self.instance.category.slug == 'scenarios-a-prendre':
            raise serializers.ValidationError("Les scénarios restent ouverts aux réponses.")
        return value

    def validate_is_pinned(self, value):
        request = self.context.get('request')
        if not request or request.user.role not in ('admin', 'fondatrice'):
            raise serializers.ValidationError("Seule l’administration peut épingler un sujet.")
        return value

    def validate_scenario_status(self, value):
        request = self.context.get("request")
        if request and request.method not in ("GET", "HEAD", "OPTIONS"):
            if not request.user.is_authenticated or request.user.role not in ("admin", "fondatrice"):
                raise serializers.ValidationError("Seuls les administrateurs peuvent modifier le statut d'un scénario.")
        return value

    def validate_scenario_avatar_name(self, value):
        request = self.context.get("request")
        if not request or request.user.role not in ("admin", "fondatrice"):
            raise serializers.ValidationError("Seule l’administration peut modifier l’avatar d’un scénario.")
        if self.instance and self.instance.category.slug != "scenarios-a-prendre":
            raise serializers.ValidationError("Ce sujet n’est pas un scénario.")
        from .avatar_directory import clean_avatar_name
        value = clean_avatar_name(value)
        if not value:
            raise serializers.ValidationError("Indiquez une célébrité.")
        return value

    def validate_scenario_links(self, value):
        request = self.context.get("request")
        if request and request.method not in ("GET", "HEAD", "OPTIONS"):
            if not request.user.is_authenticated or request.user.role not in ("admin", "fondatrice"):
                raise serializers.ValidationError("Seuls les administrateurs peuvent modifier les liens d'un scénario.")
        return value

    def validate_scenario_link_cards(self, value):
        request = self.context.get("request")
        if request and request.method not in ("GET", "HEAD", "OPTIONS"):
            if not request.user.is_authenticated or request.user.role not in ("admin", "fondatrice"):
                raise serializers.ValidationError("Seuls les administrateurs peuvent modifier les liens d'un scénario.")
        if not isinstance(value, list):
            raise serializers.ValidationError("Les liens doivent être une liste de cartes.")
        return value

    def get_first_image(self, obj):
        first_post = obj.posts.order_by("created_at").first()
        if first_post:
            content = first_post.content if first_post.is_trusted_html else sanitize_member_html(first_post.content)
            m = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', content)
            if m:
                return m.group(1)
        return None


class TopicCreateSerializer(serializers.ModelSerializer):
    first_post_content = serializers.CharField(write_only=True)

    class Meta:
        model = Topic
        # 'category' est injecté par perform_create via category_slug, pas envoyé par le client
        fields = ["id", "title", "slug", "first_post_content"]
        read_only_fields = ["id", "slug"]

    def validate_first_post_content(self, value):
        request = self.context.get('request')
        if request and request.user.role in ('admin', 'fondatrice'):
            return value
        return sanitize_member_html(value)

    def create(self, validated_data):
        content = validated_data.pop("first_post_content")
        topic = Topic.objects.create(**validated_data)
        Post.objects.create(
            topic=topic,
            author=topic.author,
            content=content,
            is_trusted_html=topic.author.role in ('admin', 'fondatrice'),
        )
        return topic


class TopicDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    post_count = serializers.IntegerField(read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)
    category_slug = serializers.CharField(source="category.slug", read_only=True)
    first_post_id = serializers.SerializerMethodField()

    def get_first_post_id(self, obj):
        return obj.posts.order_by("created_at", "pk").values_list("pk", flat=True).first()

    class Meta:
        model = Topic
        fields = [
            "id", "title", "slug", "category", "category_name", "category_slug", "author",
            "is_pinned", "is_locked", "scenario_status", "scenario_avatar_name", "scenario_links", "scenario_link_cards", "first_post_id", "post_count", "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "slug", "author", "post_count", "created_at", "updated_at",
        ]


class CategorySerializer(serializers.ModelSerializer):
    topic_count = serializers.IntegerField(read_only=True)
    post_count = serializers.IntegerField(read_only=True)
    last_post = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "order", "parent", "topic_count", "post_count", "last_post"]
        read_only_fields = ["id", "slug"]

    def get_last_post(self, obj):
        last = Post.objects.filter(topic__category=obj).order_by('-created_at').select_related('author', 'topic').first()
        if not last:
            return None
        request = self.context.get('request')
        avatar_url = None
        if last.author.avatar:
            avatar_url = request.build_absolute_uri(last.author.avatar.url) if request else last.author.avatar.url
        return {
            'topic_title': last.topic.title,
            'topic_slug': last.topic.slug,
            'author_pseudo': last.author.pseudo or last.author.username,
            'author_avatar': avatar_url,
            'created_at': last.created_at,
        }


class CategoryDetailSerializer(CategorySerializer):
    latest_topics = serializers.SerializerMethodField()

    class Meta(CategorySerializer.Meta):
        fields = CategorySerializer.Meta.fields + ["latest_topics"]

    def get_latest_topics(self, obj):
        topics = obj.topics.all()[:5]
        return TopicSerializer(topics, many=True, context=self.context).data


class ChatMessageSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_pseudo = serializers.CharField(source='author.pseudo', read_only=True)
    author_avatar = serializers.SerializerMethodField()

    def get_author_avatar(self, obj):
        if obj.author.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.author.avatar.url)
            return obj.author.avatar.url
        return None

    class Meta:
        model = ChatMessage
        fields = ['id', 'author_username', 'author_pseudo', 'author_avatar', 'content', 'created_at']
        read_only_fields = ['id', 'author_username', 'author_pseudo', 'author_avatar', 'created_at']


class SitePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SitePage
        fields = ['slug', 'content', 'updated_at']
        read_only_fields = ['slug', 'updated_at']


class PrivateMessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    sender_avatar = serializers.SerializerMethodField()
    recipient_username = serializers.CharField(source='recipient.username', read_only=True)
    recipient_avatar = serializers.SerializerMethodField()

    class Meta:
        model = PrivateMessage
        fields = [
            'id', 'sender', 'sender_username', 'sender_avatar',
            'recipient', 'recipient_username', 'recipient_avatar',
            'subject', 'body', 'is_read', 'created_at',
        ]
        read_only_fields = [
            'id', 'sender', 'sender_username', 'sender_avatar',
            'recipient_username', 'recipient_avatar', 'is_read', 'created_at',
        ]

    def get_sender_avatar(self, obj):
        if obj.sender.avatar:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.sender.avatar.url) if request else obj.sender.avatar.url
        return None

    def get_recipient_avatar(self, obj):
        if obj.recipient.avatar:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.recipient.avatar.url) if request else obj.recipient.avatar.url
        return None

    def validate_recipient(self, value):
        request = self.context.get('request')
        if request and value == request.user:
            raise serializers.ValidationError("Vous ne pouvez pas vous envoyer un message.")
        return value
