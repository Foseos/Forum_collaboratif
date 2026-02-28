from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Category, Post, Reaction, Topic

User = get_user_model()


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "avatar"]


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
    reactions_count = serializers.SerializerMethodField()
    user_reactions = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id", "author", "content", "created_at", "updated_at",
            "is_edited", "reactions_count", "user_reactions",
        ]
        read_only_fields = ["id", "author", "created_at", "updated_at", "is_edited"]

    def get_reactions_count(self, obj):
        counts = {}
        for reaction in obj.reactions.all():
            counts[reaction.reaction_type] = counts.get(reaction.reaction_type, 0) + 1
        return counts

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


class TopicSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    post_count = serializers.IntegerField(read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Topic
        fields = [
            "id", "title", "slug", "category", "category_name", "author",
            "is_pinned", "is_locked", "post_count", "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "slug", "author", "post_count", "created_at", "updated_at",
        ]


class TopicCreateSerializer(serializers.ModelSerializer):
    first_post_content = serializers.CharField(write_only=True)

    class Meta:
        model = Topic
        fields = ["id", "title", "category", "first_post_content"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        content = validated_data.pop("first_post_content")
        topic = Topic.objects.create(**validated_data)
        Post.objects.create(
            topic=topic,
            author=validated_data["author"],
            content=content,
        )
        return topic


class TopicDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    post_count = serializers.IntegerField(read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Topic
        fields = [
            "id", "title", "slug", "category", "category_name", "author",
            "is_pinned", "is_locked", "post_count", "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "slug", "author", "post_count", "created_at", "updated_at",
        ]


class CategorySerializer(serializers.ModelSerializer):
    topic_count = serializers.IntegerField(read_only=True)
    post_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "order", "topic_count", "post_count"]
        read_only_fields = ["id", "slug"]


class CategoryDetailSerializer(CategorySerializer):
    latest_topics = serializers.SerializerMethodField()

    class Meta(CategorySerializer.Meta):
        fields = CategorySerializer.Meta.fields + ["latest_topics"]

    def get_latest_topics(self, obj):
        topics = obj.topics.all()[:5]
        return TopicSerializer(topics, many=True, context=self.context).data
