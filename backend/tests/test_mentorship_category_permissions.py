from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from apps.forum.models import Category, Topic


class MentorshipCategoryPermissionTests(APITestCase):
    def setUp(self):
        self.category, _ = Category.objects.get_or_create(
            slug="parrainage", defaults={"name": "Parrainage"}
        )
        self.url = "/api/categories/parrainage/topics/"
        self.payload = {
            "title": "Parrainage — Alex & Camille",
            "first_post_content": "Bienvenue dans notre parrainage.",
        }

    def test_regular_member_cannot_open_mentorship(self):
        user = get_user_model().objects.create_user(username="member-mentorship", password="test")
        self.client.force_authenticate(user)
        response = self.client.post(self.url, self.payload, format="json")
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Topic.objects.filter(category=self.category).exists())

    def test_administration_can_open_mentorship(self):
        for role in ("admin", "fondatrice"):
            with self.subTest(role=role):
                user = get_user_model().objects.create_user(
                    username=f"mentorship-{role}", password="test", role=role
                )
                self.client.force_authenticate(user)
                response = self.client.post(self.url, {
                    **self.payload, "title": f"Parrainage — {role}"
                }, format="json")
                self.assertEqual(response.status_code, 201)
