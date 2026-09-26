from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.cache import cache
from rest_framework.test import APITestCase

from apps.forum.models import Category, Topic


class PartnershipRequestTests(APITestCase):
    def setUp(self):
        cache.clear()
        User = get_user_model()
        self.founder = User.objects.create_user(username='partnership-founder', password='test', role='fondatrice')
        self.member = User.objects.create_user(username='partnership-member', password='test')
        call_command('seed_partnerships', verbosity=0)
        self.payload = {
            'forum_name': 'Les Chroniques du Nord',
            'forum_url': 'https://example.org/',
            'concept': 'Un univers fantastique',
            'partnership_type': 'les deux',
        }

    def test_guide_and_partner_category_are_created_once(self):
        call_command('seed_partnerships', verbosity=0)
        self.assertEqual(Topic.objects.filter(slug='proposer-un-partenariat').count(), 1)
        self.assertTrue(Topic.objects.get(slug='proposer-un-partenariat').is_locked)
        self.assertTrue(Category.objects.filter(slug='nos-partenaires').exists())

    def test_guest_can_submit_and_staff_can_accept(self):
        response = self.client.post('/api/partnership-requests/', self.payload, format='json')
        self.assertEqual(response.status_code, 201)
        topic = Topic.objects.get(slug=response.data['slug'])
        self.assertEqual(topic.category.slug, 'demande-de-partenariats')
        self.assertIn('Demande invitée', topic.title)
        self.assertIn('Les Chroniques du Nord', topic.posts.first().content)
        self.client.force_authenticate(self.member)
        self.assertEqual(self.client.post(f'/api/partnership-requests/{topic.slug}/approve/').status_code, 403)
        self.client.force_authenticate(self.founder)
        self.assertEqual(self.client.post(f'/api/partnership-requests/{topic.slug}/approve/').status_code, 200)
        topic.refresh_from_db()
        self.assertEqual(topic.category.slug, 'nos-partenaires')
        self.assertTrue(topic.is_locked)

    def test_unapproved_member_cannot_publish_directly_among_partners(self):
        self.client.force_authenticate(self.member)
        response = self.client.post('/api/categories/nos-partenaires/topics/', {
            'title': 'Faux partenaire', 'first_post_content': 'Texte',
        }, format='json')
        self.assertEqual(response.status_code, 403)

    def test_request_fields_are_escaped(self):
        response = self.client.post('/api/partnership-requests/', {
            **self.payload, 'forum_name': '<script>alert(1)</script>',
        }, format='json')
        self.assertEqual(response.status_code, 201)
        content = Topic.objects.get(slug=response.data['slug']).posts.first().content
        self.assertNotIn('<script>', content)
