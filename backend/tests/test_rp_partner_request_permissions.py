from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from apps.forum.models import Category, Post, Topic


class RPPartnerRequestPermissionTests(APITestCase):
    def setUp(self):
        self.category, _ = Category.objects.get_or_create(
            slug='recherche-de-rp', defaults={'name': 'Recherche de RP'}
        )
        founder = get_user_model().objects.create_user(
            username='rp-search-founder', role='fondatrice'
        )
        self.topic = Topic.objects.create(
            slug='demande-de-partenaire-de-rp',
            title='Demande de partenaire de RP',
            category=self.category,
            author=founder,
        )

    def test_pending_member_can_read_but_cannot_publish_request(self):
        member = get_user_model().objects.create_user(username='rp-search-pending')
        self.client.force_authenticate(member)

        self.assertEqual(
            self.client.get(f'/api/topics/{self.topic.slug}/').status_code, 200
        )
        response = self.client.post(
            f'/api/topics/{self.topic.slug}/posts/',
            {'content': 'Je recherche un partenaire de RP.'},
            format='json',
        )
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Post.objects.filter(topic=self.topic, author=member).exists())

        response = self.client.post(
            '/api/categories/recherche-de-rp/topics/',
            {'title': 'Recherche directe', 'first_post_content': 'Qui veut jouer ?'},
            format='json',
        )
        self.assertEqual(response.status_code, 403)

    def test_validated_member_can_publish_request(self):
        member = get_user_model().objects.create_user(
            username='rp-search-validated', fiche_status='validated'
        )
        self.client.force_authenticate(member)
        response = self.client.post(
            f'/api/topics/{self.topic.slug}/posts/',
            {'content': 'Je recherche un partenaire de RP.'},
            format='json',
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Post.objects.filter(topic=self.topic, author=member).exists())
