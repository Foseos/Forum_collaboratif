from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from apps.forum.models import ChatMessage


class ChatTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='chat-reader')
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_only_messages_from_last_24_hours_are_displayed(self):
        now = timezone.now()
        old = ChatMessage.objects.create(author=self.user, content='old')
        recent = ChatMessage.objects.create(author=self.user, content='recent')
        ChatMessage.objects.filter(pk=old.pk).update(created_at=now - timedelta(hours=24, seconds=1))
        ChatMessage.objects.filter(pk=recent.pk).update(created_at=now - timedelta(hours=23))
        with patch('apps.forum.views.timezone.now', return_value=now):
            response = self.client.get('/api/chat/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual([row['id'] for row in response.data], [recent.pk])
        self.client.post('/api/chat/', {'content': 'new'})
        self.assertTrue(ChatMessage.objects.filter(pk=old.pk).exists())

    def test_all_messages_in_window_remain_readable(self):
        for i in range(51):
            ChatMessage.objects.create(author=self.user, content=str(i))
        self.assertEqual(len(self.client.get('/api/chat/').data), 51)

    def test_presence_excludes_forum_only_and_expired_members(self):
        User = get_user_model()
        now = timezone.now()
        active = User.objects.create_user(username='active', chat_last_seen=now)
        User.objects.create_user(username='expired', chat_last_seen=now - timedelta(seconds=46))
        User.objects.create_user(username='forum-only', last_seen=now)
        User.objects.create_user(username='disabled', chat_last_seen=now, is_active=False)
        with patch('apps.forum.views.timezone.now', return_value=now):
            response = self.client.post('/api/chat/presence/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual({row['id'] for row in response.data}, {self.user.pk, active.pk})
        self.user.refresh_from_db()
        self.assertEqual(self.user.chat_last_seen, now)

    def test_presence_requires_authentication(self):
        self.client.force_authenticate(user=None)
        self.assertIn(self.client.post('/api/chat/presence/').status_code, [401, 403])
