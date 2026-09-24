from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.forum.models import ArcanaTransaction, Category, Post, Topic


class ProfileExtrasTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.member = User.objects.create_user(username='player', fiche_status='validated')
        self.other = User.objects.create_user(username='other', email='other@example.com')
        self.client = APIClient()
        self.client.force_authenticate(self.member)
        place = Category.objects.create(name='Mystic Falls', slug='mystic-falls')
        self.topic = Topic.objects.create(title='Une scène', category=place, author=self.other)

    def test_history_is_private_and_tracks_rp_reward(self):
        response = self.client.post(f'/api/topics/{self.topic.slug}/posts/', {'content': 'magie ' * 101})
        self.assertEqual(response.status_code, 201)
        history = self.client.get('/api/arcana/history/')
        self.assertEqual(history.status_code, 200)
        self.assertEqual(history.data[0]['amount'], 10)
        self.assertEqual(history.data[0]['balance_after'], 10)
        self.client.force_authenticate(self.other)
        self.assertEqual(self.client.get('/api/arcana/history/').data, [])

    def test_lottery_status_and_bonus_are_recorded(self):
        self.assertFalse(self.client.get('/api/lottery/draw/').data['available'])
        Post.objects.create(topic=self.topic, author=self.member, content='magie ' * 101)
        self.assertTrue(self.client.get('/api/lottery/draw/').data['available'])
        with patch('apps.forum.lottery.secrets.randbelow', return_value=0):
            self.assertEqual(self.client.post('/api/lottery/draw/').status_code, 201)
        self.assertFalse(self.client.get('/api/lottery/draw/').data['available'])
        self.assertTrue(ArcanaTransaction.objects.filter(user=self.member, amount=5).exists())

    def test_reply_email_preference_is_editable(self):
        response = self.client.patch('/api/users/me/', {'email_topic_replies': False})
        self.assertEqual(response.status_code, 200)
        self.member.refresh_from_db()
        self.assertFalse(self.member.email_topic_replies)
