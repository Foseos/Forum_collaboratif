from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase

from apps.users.ip_tracking import client_ip, prune_ip_logs
from apps.users.models import UserIPLog


class UserIPHistoryTests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.admin = User.objects.create_user(username='ip-admin', password='StrongTestPassword!24', role='admin')
        self.member = User.objects.create_user(username='ip-member', password='StrongTestPassword!24')

    def test_registration_and_successful_login_are_recorded(self):
        response = self.client.post('/api/auth/register/', {
            'username': 'new-ip-member', 'email': 'new@example.com',
            'password': 'StrongTestPassword!24', 'password_confirm': 'StrongTestPassword!24',
        }, format='json', REMOTE_ADDR='192.0.2.10')
        self.assertEqual(response.status_code, 201)
        newcomer = get_user_model().objects.get(username='new-ip-member')
        self.assertTrue(UserIPLog.objects.filter(user=newcomer, ip_address='192.0.2.10', event='registration').exists())
        self.assertEqual(self.client.post('/api/auth/login/', {
            'username': 'new-ip-member', 'password': 'wrong',
        }, format='json', REMOTE_ADDR='192.0.2.11').status_code, 401)
        self.assertFalse(UserIPLog.objects.filter(user=newcomer, event='login').exists())
        self.assertEqual(self.client.post('/api/auth/login/', {
            'username': 'new-ip-member', 'password': 'StrongTestPassword!24',
        }, format='json', REMOTE_ADDR='192.0.2.11').status_code, 200)
        self.assertTrue(UserIPLog.objects.filter(user=newcomer, ip_address='192.0.2.11', event='login').exists())

    def test_history_is_admin_only_and_shows_shared_accounts(self):
        UserIPLog.objects.create(user=self.member, ip_address='192.0.2.15', event='login')
        other = get_user_model().objects.create_user(username='ip-other', password='StrongTestPassword!24')
        UserIPLog.objects.create(user=other, ip_address='192.0.2.15', event='registration')
        url = f'/api/users/{self.member.pk}/ip-history/'
        self.assertEqual(self.client.get(url).status_code, 401)
        self.client.force_authenticate(self.member)
        self.assertEqual(self.client.get(url).status_code, 403)
        self.client.force_authenticate(self.admin)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['entries'][0]['ip_address'], '192.0.2.15')
        self.assertEqual(response.data['shared_accounts'][0]['id'], other.pk)

    def test_retention_and_untrusted_forwarded_header(self):
        old = UserIPLog.objects.create(user=self.member, ip_address='192.0.2.20', event='login')
        UserIPLog.objects.filter(pk=old.pk).update(created_at=timezone.now() - timedelta(days=181))
        prune_ip_logs()
        self.assertFalse(UserIPLog.objects.filter(pk=old.pk).exists())
        class Request:
            META = {'REMOTE_ADDR': '192.0.2.21', 'HTTP_X_REAL_IP': '192.0.2.99'}
        with patch('apps.users.ip_tracking.socket.gethostbyname', return_value='172.18.0.4'):
            self.assertEqual(client_ip(Request()), '192.0.2.21')
            Request.META['REMOTE_ADDR'] = '172.18.0.4'
            self.assertEqual(client_ip(Request()), '192.0.2.99')
