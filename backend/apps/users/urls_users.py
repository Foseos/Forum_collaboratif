from django.urls import path

from .views import ProfileView, UserDetailView, UserListView

urlpatterns = [
    path("me/", ProfileView.as_view(), name="user-profile"),
    path("", UserListView.as_view(), name="user-list"),
    path("<int:pk>/", UserDetailView.as_view(), name="user-detail"),
]
