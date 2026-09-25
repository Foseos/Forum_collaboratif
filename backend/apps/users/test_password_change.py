from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


class ChangePasswordTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="password_test_user",
            email="password-test@example.com",
            password="OldPassword-7284!",
        )
        self.client = APIClient()
        self.url = "/api/users/me/change-password/"

    def test_authentication_and_current_password_required(self):
        self.assertEqual(self.client.post(self.url, {}).status_code, 401)
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, {
            "current_password": "incorrect",
            "new_password": "NewPassword-8294!",
            "new_password_confirm": "NewPassword-8294!",
        })
        self.assertEqual(response.status_code, 400)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("OldPassword-7284!"))

    def test_change_revokes_existing_token(self):
        old_access = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {old_access}")
        response = self.client.post(self.url, {
            "current_password": "OldPassword-7284!",
            "new_password": "NewPassword-8294!",
            "new_password_confirm": "NewPassword-8294!",
        })
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("NewPassword-8294!"))
        self.assertEqual(self.client.get("/api/users/me/").status_code, 401)
