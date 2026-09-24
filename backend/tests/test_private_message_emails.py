from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import override_settings
from rest_framework.test import APITestCase

from apps.forum.models import PrivateMessage


@override_settings(FORUM_URL='https://nexus.example')
class PrivateMessageEmailTests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.sender = User.objects.create_user(username='sender-pm', email='sender@example.com', password='test')
        self.recipient = User.objects.create_user(username='recipient-pm', email='recipient@example.com', password='test')
        self.sender.pseudo = 'Autre nom'
        self.sender.save(update_fields=['pseudo'])
        self.client.force_authenticate(self.sender)

    @patch('apps.forum.private_message_emails.send_mail')
    def test_recipient_gets_email_after_private_message_is_saved(self, send_mail):
        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post('/api/messages/send/', {
                'recipient': self.recipient.pk,
                'subject': 'Notre prochain RP',
                'body': 'Bonjour !',
            }, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(PrivateMessage.objects.filter(sender=self.sender, recipient=self.recipient).exists())
        self.assertEqual(send_mail.call_count, 1)
        subject, body, _, recipients = send_mail.call_args.args
        self.assertIn(self.sender.username, subject)
        self.assertNotIn('Autre nom', subject)
        self.assertIn('Notre prochain RP', body)
        self.assertIn('https://nexus.example/messageries', body)
        self.assertEqual(recipients, ['recipient@example.com'])

    @patch('apps.forum.private_message_emails.send_mail')
    def test_no_email_without_recipient_address(self, send_mail):
        self.recipient.email = ''
        self.recipient.save(update_fields=['email'])
        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post('/api/messages/send/', {
                'recipient': self.recipient.pk, 'subject': 'Salut', 'body': 'Bonjour',
            }, format='json')
        self.assertEqual(response.status_code, 201)
        send_mail.assert_not_called()
