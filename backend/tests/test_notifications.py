from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.forum.models import Category, Post, Topic
from apps.notifications.models import Notification

User = get_user_model()


class NotificationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="user", password="UserPass123!"
        )
        self.other_user = User.objects.create_user(
            username="other", password="OtherPass123!"
        )
        self.category = Category.objects.create(name="Tech", slug="tech")
        self.topic = Topic.objects.create(
            title="Test", slug="test",
            category=self.category, author=self.user,
        )

    def test_notification_created_on_reply(self):
        Post.objects.create(
            topic=self.topic, author=self.other_user, content="Reply"
        )
        self.assertEqual(
            Notification.objects.filter(recipient=self.user).count(), 1
        )

    def test_no_self_notification(self):
        Post.objects.create(
            topic=self.topic, author=self.user, content="My own reply"
        )
        self.assertEqual(
            Notification.objects.filter(recipient=self.user).count(), 0
        )

    def test_list_notifications(self):
        Notification.objects.create(
            recipient=self.user,
            sender=self.other_user,
            notification_type="new_post",
            message="Test notification",
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/notifications/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_mark_notification_read(self):
        notif = Notification.objects.create(
            recipient=self.user,
            notification_type="new_post",
            message="Test",
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f"/api/notifications/{notif.pk}/read/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        notif.refresh_from_db()
        self.assertTrue(notif.is_read)

    def test_mark_all_read(self):
        for i in range(3):
            Notification.objects.create(
                recipient=self.user,
                notification_type="new_post",
                message=f"Test {i}",
            )
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/api/notifications/read-all/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Notification.objects.filter(recipient=self.user, is_read=False).count(), 0
        )

    def test_unread_count(self):
        for i in range(3):
            Notification.objects.create(
                recipient=self.user,
                notification_type="new_post",
                message=f"Test {i}",
            )
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/notifications/unread-count/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["unread_count"], 3)
