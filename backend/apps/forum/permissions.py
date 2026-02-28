from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrModeratorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        return obj.author == request.user or request.user.is_moderator


class IsTopicNotLocked(BasePermission):
    message = "Ce sujet est verrouillé."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        topic_slug = view.kwargs.get("topic_slug")
        if topic_slug:
            from .models import Topic
            try:
                topic = Topic.objects.get(slug=topic_slug)
                return not topic.is_locked or (
                    request.user.is_authenticated and request.user.is_moderator
                )
            except Topic.DoesNotExist:
                return True
        return True
