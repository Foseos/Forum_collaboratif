from django.urls import path

from .views import ActivityAlertsView, ChangePasswordView, LinkedAccountsView, PresenceView, ProfileView, UserDetailView, UserListView

urlpatterns = [
    path("me/", ProfileView.as_view(), name="user-profile"),
    path("me/change-password/", ChangePasswordView.as_view(), name="user-change-password"),
    path("presence/", PresenceView.as_view(), name="user-presence"),
    path("activity-alerts/", ActivityAlertsView.as_view(), name="user-activity-alerts"),
    path("<int:pk>/linked-accounts/", LinkedAccountsView.as_view(), name="user-linked-accounts"),
    path("", UserListView.as_view(), name="user-list"),
    path("<int:pk>/", UserDetailView.as_view(), name="user-detail"),
]
