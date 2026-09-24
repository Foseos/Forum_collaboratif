from django.urls import path
from .post_images import PostImageUploadView

from .views import (
    AvatarDirectoryEntryDetailView, AvatarDirectoryView, CategoryViewSet, ChatMessageView, ChatPresenceView, DemonicFormDirectoryView, DemonicFormEntryDetailView, ForumStatsView, MyRPView,
    PMDetailView, PMInboxView, PMMarkReadView, PMSendView, PMSentView, PMUnreadCountView,
    PostViewSet, ReactionToggleView, SitePageView, TopicViewSet, UserParticipatedTopicsView,
    PartnershipRequestView, PartnershipApproveView,
    DiceRollView, LotteryDrawView, ArcanaHistoryView, NextStepsView,
)

# Category URLs
category_list = CategoryViewSet.as_view({"get": "list", "post": "create"})
category_detail = CategoryViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)

# Topic URLs
topic_list = TopicViewSet.as_view({"get": "list", "post": "create"})
topic_list_flat = TopicViewSet.as_view({"get": "list"})
topic_detail = TopicViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)

# Post URLs
post_list = PostViewSet.as_view({"get": "list", "post": "create"})
post_detail = PostViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)

urlpatterns = [
    path('posts/images/', PostImageUploadView.as_view(), name='post-image-upload'),
    path('arcana/history/', ArcanaHistoryView.as_view(), name='arcana-history'),
    path('next-steps/', NextStepsView.as_view(), name='next-steps'),
    path('lottery/draw/', LotteryDrawView.as_view(), name='lottery-draw'),
    path('partnership-requests/', PartnershipRequestView.as_view(), name='partnership-request'),
    path('partnership-requests/<slug:slug>/approve/', PartnershipApproveView.as_view(), name='partnership-approve'),
    path("demonic-forms/", DemonicFormDirectoryView.as_view(), name="demonic-form-directory"),
    path("demonic-forms/<int:pk>/", DemonicFormEntryDetailView.as_view(), name="demonic-form-entry"),
    path("avatars/", AvatarDirectoryView.as_view(), name="avatar-directory"),
    path("avatars/<int:pk>/", AvatarDirectoryEntryDetailView.as_view(), name="avatar-directory-entry"),
    # Categories
    path("categories/", category_list, name="category-list"),
    path("categories/<slug:slug>/", category_detail, name="category-detail"),
    # Topics (nested under categories)
    path(
        "categories/<slug:category_slug>/topics/",
        topic_list,
        name="topic-list",
    ),
    # Topics (flat list, filterable by ?author=<id>)
    path("topics/", topic_list_flat, name="topic-list-flat"),
    # Topics (participated by current user)
    path("topics/participated/", UserParticipatedTopicsView.as_view(), name="topic-participated"),
    path("topics/my-rp/", MyRPView.as_view(), name="my-rp"),
    # Topics (direct access)
    path("topics/<slug:slug>/", topic_detail, name="topic-detail"),
    path("topics/<slug:slug>/roll/", DiceRollView.as_view(), name="topic-dice-roll"),
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
    # Chat
    path("chat/", ChatMessageView.as_view(), name="chat-messages"),
    path("chat/presence/", ChatPresenceView.as_view(), name="chat-presence"),
    # Pages éditables (règlement, etc.)
    path("pages/<slug:slug>/", SitePageView.as_view(), name="site-page"),
    # Stats globales du forum
    path("stats/", ForumStatsView.as_view(), name="forum-stats"),
    # Messages privés
    path("messages/", PMInboxView.as_view(), name="pm-inbox"),
    path("messages/sent/", PMSentView.as_view(), name="pm-sent"),
    path("messages/send/", PMSendView.as_view(), name="pm-send"),
    path("messages/unread/", PMUnreadCountView.as_view(), name="pm-unread"),
    path("messages/<int:pk>/", PMDetailView.as_view(), name="pm-detail"),
    path("messages/<int:pk>/read/", PMMarkReadView.as_view(), name="pm-read"),
]
