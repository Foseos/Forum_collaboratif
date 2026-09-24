from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.forum.models import Category, LotteryDraw, Post, Topic


class LotteryTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='lottery-player', compte_bancaire=10)
        self.root = Category.objects.create(name='Mystic Falls', slug='mystic-falls')
        self.place = Category.objects.create(name='Place de Mystic Falls', slug='place-mystic-falls', parent=self.root)
        self.topic = Topic.objects.create(title='Rencontre en ville', category=self.place, author=self.user)
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_eligible_rp_gives_bonus_once(self):
        Post.objects.create(topic=self.topic, author=self.user, content='magie ' * 101)
        with patch('apps.forum.lottery.secrets.randbelow', return_value=9):
            response = self.client.post('/api/lottery/draw/')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['prize'], 30)
        self.user.refresh_from_db()
        self.assertEqual(self.user.compte_bancaire, 40)
        self.assertEqual(LotteryDraw.objects.count(), 1)
        self.assertEqual(self.client.post('/api/lottery/draw/').status_code, 400)

    def test_unqualified_post_does_not_grant_bonus(self):
        Post.objects.create(topic=self.topic, author=self.user, content='magie ' * 100)
        self.assertEqual(self.client.post('/api/lottery/draw/').status_code, 400)
        self.assertEqual(LotteryDraw.objects.count(), 0)
        self.user.refresh_from_db()
        self.assertEqual(self.user.compte_bancaire, 10)

    def test_non_rp_post_does_not_qualify(self):
        guide_category = Category.objects.create(name='Règlement', slug='reglement')
        guide = Topic.objects.create(title='Guide', category=guide_category, author=self.user)
        Post.objects.create(topic=guide, author=self.user, content='magie ' * 101)
        self.assertEqual(self.client.post('/api/lottery/draw/').status_code, 400)

    def test_san_francisco_location_qualifies(self):
        location = Category.objects.create(name='Le Quake', slug='le-quake', order=120)
        scene = Topic.objects.create(title='Une soirée', category=location, author=self.user)
        Post.objects.create(topic=scene, author=self.user, content='magie ' * 101)
        self.assertEqual(self.client.post('/api/lottery/draw/').status_code, 201)

    def test_authentication_required(self):
        self.client.force_authenticate(user=None)
        self.assertIn(self.client.post('/api/lottery/draw/').status_code, (401, 403))
