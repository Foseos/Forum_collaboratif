from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase


class DemonicFormsAndProfileGifTests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.member = User.objects.create_user(username="demon-member", password="pass")
        self.admin = User.objects.create_user(username="form-admin", password="pass", role="admin")

    def test_demonic_form_directory_is_public_and_admin_managed(self):
        self.assertEqual(self.client.get("/api/demonic-forms/").data, [])
        payload = {
            "name": "L'Ombre cendrée",
            "image_url": "https://example.com/form.gif",
            "character": "Ava Bartholomé",
        }
        self.client.force_authenticate(self.member)
        self.assertEqual(self.client.post("/api/demonic-forms/", payload, format="json").status_code, 403)

        self.client.force_authenticate(self.admin)
        created = self.client.post("/api/demonic-forms/", payload, format="json")
        self.assertEqual(created.status_code, 201)
        entry_id = created.data["id"]
        updated = self.client.patch(f"/api/demonic-forms/{entry_id}/", {
            "image_url": "https://example.com/new.gif",
        }, format="json")
        self.assertEqual(updated.status_code, 200)

        self.client.force_authenticate(self.member)
        listing = self.client.get("/api/demonic-forms/")
        self.assertEqual(len(listing.data), 1)
        self.assertEqual(listing.data[0]["character"], "Ava Bartholomé")
        self.assertEqual(listing.data[0]["image_url"], "https://example.com/new.gif")
        self.assertEqual(self.client.delete(f"/api/demonic-forms/{entry_id}/").status_code, 403)

    def test_member_can_set_profile_gif_visible_on_public_profile(self):
        self.client.force_authenticate(self.member)
        updated = self.client.patch("/api/users/me/", {
            "profile_gif_url": "https://example.com/portrait.gif",
        }, format="json")
        self.assertEqual(updated.status_code, 200)
        self.assertEqual(updated.data["profile_gif_url"], "https://example.com/portrait.gif")
        self.client.force_authenticate(user=None)
        public = self.client.get(f"/api/users/{self.member.pk}/")
        self.assertEqual(public.status_code, 200)
        self.assertEqual(public.data["profile_gif_url"], "https://example.com/portrait.gif")
