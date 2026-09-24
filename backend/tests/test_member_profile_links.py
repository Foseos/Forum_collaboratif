from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.forum.models import Category, Topic


class MemberProfileLinksTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="profil-test", fiche_status="validated")
        self.client = APIClient()
        presentation, _ = Category.objects.get_or_create(slug="fiches-validees-et-archivees", defaults={"name": "Archives"})
        recap, _ = Category.objects.get_or_create(slug="fiche-personnage", defaults={"name": "Fiche personnage"})
        self.presentation = Topic.objects.create(title="Présentation", slug="presentation-test", category=presentation, author=self.user)
        self.recap = Topic.objects.create(title="Carnet", slug="carnet-test", category=recap, author=self.user)

    def test_public_profile_links_to_own_validated_sheets(self):
        response = self.client.get(f"/api/users/{self.user.pk}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["presentation_topic_slug"], self.presentation.slug)
        self.assertEqual(response.data["recap_topic_slug"], self.recap.slug)
        self.client.force_authenticate(self.user)
        own = self.client.get("/api/users/me/")
        self.assertEqual(own.data["presentation_topic_slug"], self.presentation.slug)
        self.assertEqual(own.data["recap_topic_slug"], self.recap.slug)

    def test_player_can_change_rp_availability(self):
        self.client.force_authenticate(self.user)
        response = self.client.patch("/api/users/me/", {"rp_availability": "open"})
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.rp_availability, "open")
        self.assertEqual(self.client.get(f"/api/users/{self.user.pk}/").data["rp_availability"], "open")

    def test_unvalidated_sheet_is_not_exposed_as_validated(self):
        self.user.fiche_status = "pending"
        self.user.save(update_fields=["fiche_status"])
        response = self.client.get(f"/api/users/{self.user.pk}/")
        self.assertIsNone(response.data["presentation_topic_slug"])
        self.assertIsNone(response.data["recap_topic_slug"])
