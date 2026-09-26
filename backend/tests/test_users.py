from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core import mail
from urllib.parse import parse_qs, urlparse
from unittest.mock import patch
from smtplib import SMTPException
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


class UserRegistrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = "/api/auth/register/"

    def test_anonymous_user_cannot_update_profile(self):
        user = User.objects.create_user(username="member", password="StrongPass123!")
        response = self.client.patch("/api/users/me/", {"username": "changed"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        user.refresh_from_db()
        self.assertEqual(user.username, "member")

    def test_register_success(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "StrongPass123!",
            "password_confirm": "StrongPass123!",
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().username, "testuser")
        self.assertFalse(User.objects.first().is_active)
        self.assertEqual(len(mail.outbox), 1)

    def test_confirmation_activates_once_and_then_allows_login(self):
        data = {"username": "new-user", "email": "new@example.com",
                "password": "StrongPass123!", "password_confirm": "StrongPass123!"}
        self.client.post(self.register_url, data)
        self.assertEqual(self.client.post('/api/auth/login/', {
            'username': data['username'], 'password': data['password'],
        }).status_code, 401)
        link = mail.outbox[-1].body.splitlines()[3]
        query = parse_qs(urlparse(link).query)
        payload = {'type': query['type'][0], 'jeton': query['jeton'][0]}
        self.assertEqual(self.client.post('/api/auth/confirm-email/', payload).status_code, 200)
        self.assertEqual(self.client.post('/api/auth/confirm-email/', payload).status_code, 400)
        self.assertEqual(self.client.post('/api/auth/login/', {
            'username': data['username'], 'password': data['password'],
        }).status_code, 200)

    def test_confirmation_resend_has_a_cooldown(self):
        data = {"username": "new-user", "email": "new@example.com",
                "password": "StrongPass123!", "password_confirm": "StrongPass123!"}
        self.client.post(self.register_url, data)
        self.assertEqual(len(mail.outbox), 1)
        self.client.post('/api/auth/resend-confirmation/', {
            'username': data['username'], 'password': data['password'],
        })
        self.assertEqual(len(mail.outbox), 1)

    @patch('apps.users.views.send_confirmation', side_effect=SMTPException('unavailable'))
    def test_registration_rolls_back_when_mail_cannot_be_sent(self, _send):
        response = self.client.post(self.register_url, {
            'username': 'new-user', 'email': 'new@example.com',
            'password': 'StrongPass123!', 'password_confirm': 'StrongPass123!',
        })
        self.assertEqual(response.status_code, 503)
        self.assertFalse(User.objects.filter(username='new-user').exists())

    def test_register_password_mismatch(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "StrongPass123!",
            "password_confirm": "WrongPass123!",
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_duplicate_username(self):
        User.objects.create_user(username="testuser", password="pass123!")
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "StrongPass123!",
            "password_confirm": "StrongPass123!",
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_requires_a_distinct_email_even_for_another_account(self):
        User.objects.create_user(username="first", email="shared@example.com", password="pass123!")
        response = self.client.post(self.register_url, {
            "username": "second", "email": " SHARED@EXAMPLE.COM ",
            "password": "StrongPass123!", "password_confirm": "StrongPass123!",
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_register_requires_email(self):
        response = self.client.post(self.register_url, {
            "username": "second", "password": "StrongPass123!",
            "password_confirm": "StrongPass123!",
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)


class UserAuthenticationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = "/api/auth/login/"
        self.user = User.objects.create_user(
            username="testuser", password="StrongPass123!", email="test@example.com"
        )

    def test_login_success(self):
        data = {"username": "testuser", "password": "StrongPass123!"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_invalid_credentials(self):
        data = {"username": "testuser", "password": "WrongPass"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserProfileTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.profile_url = "/api/users/me/"
        self.user = User.objects.create_user(
            username="testuser", password="StrongPass123!", email="test@example.com"
        )

    def test_get_profile_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "testuser")

    def test_get_profile_unauthenticated(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.profile_url, {"bio": "Hello world"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.bio, "Hello world")

    def test_profile_cannot_take_another_accounts_email(self):
        User.objects.create_user(username="other", email="taken@example.com", password="pass123!")
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.profile_url, {"email": "TAKEN@example.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "test@example.com")

    def test_email_change_requires_password_and_confirmation(self):
        self.client.force_authenticate(user=self.user)
        url = '/api/auth/request-email-change/'
        self.assertEqual(self.client.post(url, {
            'email': 'new@example.com', 'password': 'wrong',
        }).status_code, 400)
        response = self.client.post(url, {
            'email': 'new@example.com', 'password': 'StrongPass123!',
        })
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.pending_email, 'new@example.com')
        link = mail.outbox[0].body.splitlines()[3]
        query = parse_qs(urlparse(link).query)
        payload = {'type': query['type'][0], 'jeton': query['jeton'][0]}
        self.assertEqual(self.client.post('/api/auth/confirm-email/', payload).status_code, 200)
        self.assertEqual(self.client.post('/api/auth/confirm-email/', payload).status_code, 400)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'new@example.com')

    def test_only_staff_can_link_a_secondary_account(self):
        secondary = User.objects.create_user(username='secondary', email='secondary@example.com', password='pass123!')
        url = f'/api/users/{secondary.pk}/linked-accounts/'
        self.client.force_authenticate(user=self.user)
        self.assertEqual(self.client.patch(url, {'main_account': self.user.pk}).status_code, 403)
        staff = User.objects.create_user(username='staff', email='staff@example.com', password='pass123!', role='admin')
        self.client.force_authenticate(user=staff)
        self.assertEqual(self.client.patch(url, {'main_account': self.user.pk}).status_code, 200)
        secondary.refresh_from_db()
        self.assertEqual(secondary.main_account_id, self.user.pk)

    def test_public_member_profile_does_not_expose_email(self):
        response = self.client.get(f'/api/users/{self.user.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('email', response.data)

    def test_password_reset_link_is_single_use_and_requests_are_limited(self):
        url = '/api/auth/password-reset/'
        self.assertEqual(self.client.post(url, {'username': self.user.username}).status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.client.post(url, {'username': self.user.username})
        self.assertEqual(len(mail.outbox), 1)
        link = mail.outbox[0].body.splitlines()[3]
        query = parse_qs(urlparse(link).query)
        payload = {
            'uid': query['uid'][0], 'jeton': query['jeton'][0],
            'password': 'AnotherStrongPass123!',
            'password_confirm': 'AnotherStrongPass123!',
        }
        confirm_url = '/api/auth/password-reset/confirm/'
        self.assertEqual(self.client.post(confirm_url, payload).status_code, 200)
        self.assertEqual(self.client.post(confirm_url, payload).status_code, 400)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('AnotherStrongPass123!'))

    def test_update_avatar(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        self.client.force_authenticate(user=self.user)
        gif_bytes = b'GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
        avatar = SimpleUploadedFile("avatar.gif", gif_bytes, content_type="image/gif")
        response = self.client.patch(self.profile_url, {"avatar": avatar}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(bool(self.user.avatar))



