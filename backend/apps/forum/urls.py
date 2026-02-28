from django.urls import path

from .views import CategoryViewSet, PostViewSet, ReactionToggleView, TopicViewSet

# Category URLs
category_list = CategoryViewSet.as_view({"get": "list", "post": "create"})
category_detail = CategoryViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)

# Topic URLs
topic_list = TopicViewSet.as_view({"get": "list", "post": "create"})
topic_detail = TopicViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)

# Post URLs
post_list = PostViewSet.as_view({"get": "list", "post": "create"})
post_detail = PostViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)

urlpatterns = [
    # Categories
    path("categories/", category_list, name="category-list"),
    path("categories/<slug:slug>/", category_detail, name="category-detail"),
    # Topics (nested under categories)
    path(
        "categories/<slug:category_slug>/topics/",
        topic_list,
        name="topic-list",
    ),
    # Topics (direct access)
    path("topics/<slug:slug>/", topic_detail, name="topic-detail"),
    # Posts (nested under topics)
    path(
        "topics/<slug:topic_slug>/posts/",
        post_list,
        name="post-list",
    ),
    # Posts (direct access)
    path("posts/<int:pk>/", post_detail, name="post-detail"),
    # Reactions
    path(
        "posts/<int:post_id>/reactions/",
        ReactionToggleView.as_view(),
        name="reaction-toggle",
    ),
]
