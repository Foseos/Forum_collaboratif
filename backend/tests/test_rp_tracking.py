from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from apps.forum.models import Category, Topic, Post


class RPTrackingTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='reader')
        self.partner = get_user_model().objects.create_user(username='partner')
        self.category = Category.objects.create(name='RP', slug='rp')
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def topic(self, title, joined=True, locked=False, category=None):
        topic = Topic.objects.create(title=title, author=self.partner, category=category or self.category, is_locked=locked)
        if joined:
            Post.objects.create(topic=topic, author=self.user, content='Ma réponse')
        Post.objects.create(topic=topic, author=self.partner, content='La suite')
        return topic

    def test_filters_and_last_author(self):
        waiting = self.topic('À reprendre')
        mine = self.topic('Répondu')
        Post.objects.create(topic=mine, author=self.user, content='Encore')
        locked = self.topic('Verrouillé', locked=True)
        self.topic('Pas mon RP', joined=False)
        non_rp = Category.objects.create(name='Fiches', slug='fiche-personnage')
        self.topic('Fiche', category=non_rp)
        response = self.client.get('/api/topics/my-rp/?status=waiting')
        self.assertEqual(response.status_code, 200)
        self.assertEqual([row['id'] for row in response.data['results']], [waiting.pk])
        self.assertEqual(response.data['results'][0]['post_count'], 2)
        self.assertTrue(response.data['results'][0]['awaiting_reply'])
        response = self.client.get('/api/topics/my-rp/?status=active')
        self.assertEqual({row['id'] for row in response.data['results']}, {waiting.pk, mine.pk})
        response = self.client.get('/api/topics/my-rp/?status=locked')
        self.assertEqual([row['id'] for row in response.data['results']], [locked.pk])

    def test_account_cannot_be_overridden_by_query_parameter(self):
        self.topic('Privé au suivi du partenaire', joined=False)
        response = self.client.get(f'/api/topics/my-rp/?user_id={self.partner.pk}')
        self.assertEqual(response.data['count'], 0)

    def test_login_required(self):
        self.client.force_authenticate(None)
        self.assertIn(self.client.get('/api/topics/my-rp/').status_code, [401, 403])
