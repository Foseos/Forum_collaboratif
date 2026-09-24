from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from apps.forum.models import AvatarDirectoryEntry, Category, Post, Topic


class AvatarDirectoryPermissionsTests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.member = User.objects.create_user(username="member-avatar", password="test-password", avatar_name="Old Actor")
        self.admin = User.objects.create_user(username="admin-avatar", password="test-password", role="admin")
        self.moderator = User.objects.create_user(username="moderator-avatar", password="test-password", role="moderator")
        category = Category.objects.create(name="Scénarios à prendre", slug="scenarios-a-prendre")
        self.scenario = Topic.objects.create(title="Scenario Avatar", category=category, author=self.admin)
        self.post = Post.objects.create(topic=self.scenario, author=self.admin, content="<p>Ft Original Actor</p>")

    def test_member_cannot_change_avatar_name_through_own_profile(self):
        self.client.force_authenticate(self.member)
        response = self.client.patch("/api/users/me/", {"avatar_name": "New Actor"}, format="json")
        self.assertEqual(response.status_code, 400)
        self.member.refresh_from_db()
        self.assertEqual(self.member.avatar_name, "Old Actor")

    def test_admin_can_change_avatar_name(self):
        self.client.force_authenticate(self.admin)
        response = self.client.patch(f"/api/users/{self.member.pk}/", {"avatar_name": "New Actor"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.member.refresh_from_db()
        self.assertEqual(self.member.avatar_name, "New Actor")

    def test_moderator_cannot_change_scenario_avatar(self):
        self.client.force_authenticate(self.moderator)
        response = self.client.patch(f"/api/posts/{self.post.pk}/", {"content": "<p>Ft New Actor</p>"}, format="json")
        self.assertEqual(response.status_code, 403)
        self.post.refresh_from_db()
        self.assertIn("Original Actor", self.post.content)

    def test_only_admin_can_add_character_to_avatar_directory(self):
        payload = {"character": "Nouveau personnage", "avatar": "New Actor", "status": "taken"}
        self.client.force_authenticate(self.member)
        self.assertEqual(self.client.post("/api/avatars/", payload, format="json").status_code, 403)
        self.client.force_authenticate(self.moderator)
        self.assertEqual(self.client.post("/api/avatars/", payload, format="json").status_code, 403)
        self.client.force_authenticate(self.admin)
        self.assertEqual(self.client.post("/api/avatars/", payload, format="json").status_code, 201)
        self.assertEqual(AvatarDirectoryEntry.objects.count(), 1)
        listing = self.client.get("/api/avatars/").data["entries"]
        self.assertTrue(any(item["character"] == "Nouveau personnage" for item in listing))

    def test_admin_can_recast_scenario_and_change_its_status(self):
        payload = {"scenario_avatar_name": "New Actor", "scenario_status": "reserved"}
        self.client.force_authenticate(self.moderator)
        denied = self.client.patch(f"/api/topics/{self.scenario.slug}/", payload, format="json")
        self.assertIn(denied.status_code, (400, 403))

        self.client.force_authenticate(self.admin)
        response = self.client.patch(f"/api/topics/{self.scenario.slug}/", payload, format="json")
        self.assertEqual(response.status_code, 200)
        self.scenario.refresh_from_db()
        self.post.refresh_from_db()
        self.assertEqual(self.scenario.scenario_status, "reserved")
        self.assertEqual(self.scenario.scenario_avatar_name, "New Actor")
        self.assertIn("Ft New Actor", self.post.content)
        listing = self.client.get("/api/avatars/").data["entries"]
        entry = next(item for item in listing if item["scenario_slug"] == self.scenario.slug)
        self.assertEqual((entry["avatar"], entry["scenario_status"]), ("New Actor", "reserved"))
