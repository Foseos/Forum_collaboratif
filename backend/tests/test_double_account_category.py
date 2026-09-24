from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from apps.forum.models import Category, Topic


class DoubleAccountCategoryTests(APITestCase):
    def test_category_is_under_welcome_and_accepts_form_topic(self):
        category = Category.objects.get(slug='demande-double-compte')
        self.assertEqual(category.parent.slug, 'bienvenue-san-francisco')
        user = get_user_model().objects.create_user(username='second-character', password='test')
        self.client.force_authenticate(user)
        response = self.client.post('/api/categories/demande-double-compte/topics/', {
            'title': 'Demande de double compte — Elara',
            'first_post_content': 'Nom : Elara',
        }, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Topic.objects.filter(pk=response.data['id'], category=category).exists())
