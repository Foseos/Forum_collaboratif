from django.db.models import Count
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response

from apps.users.permissions import IsAdminOrModerator

from .models import Category, Post, Reaction, Topic
from .permissions import IsAuthorOrModeratorOrReadOnly, IsTopicNotLocked
from .serializers import (
    CategoryDetailSerializer,
    CategorySerializer,
    PostCreateSerializer,
    PostSerializer,
    ReactionSerializer,
    TopicCreateSerializer,
    TopicDetailSerializer,
    TopicSerializer,
)


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


class TopicViewSet(viewsets.ModelViewSet):
    lookup_field = "slug"
    search_fields = ["title"]
    filterset_fields = ["is_pinned", "is_locked", "author"]

    def get_queryset(self):
        queryset = Topic.objects.annotate(post_count=Count("posts"))
        category_slug = self.kwargs.get("category_slug")
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
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

    def perform_create(self, serializer):
        category_slug = self.kwargs.get("category_slug")
        category = Category.objects.get(slug=category_slug)
        serializer.save(author=self.request.user, category=category)


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

    def perform_create(self, serializer):
        topic_slug = self.kwargs.get("topic_slug")
        topic = Topic.objects.get(slug=topic_slug)
        serializer.save(author=self.request.user, topic=topic)


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
