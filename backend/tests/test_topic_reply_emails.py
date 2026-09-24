from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import override_settings
from rest_framework.test import APITestCase

from apps.forum.models import Category, Post, Topic


@override_settings(FORUM_URL="https://nexus.example")
class TopicReplyEmailTests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.alice = User.objects.create_user(username="alice", email="alice@example.com", password="pass")
        self.bob = User.objects.create_user(username="bob", email="bob@example.com", password="pass")
        self.carol = User.objects.create_user(username="carol", email="carol@example.com", password="pass")
        self.silent = User.objects.create_user(username="silent", email="", password="pass")
        self.outsider = User.objects.create_user(username="outsider", email="outsider@example.com", password="pass")
        category = Category.objects.create(name="Questions", slug="questions-membres")
        self.topic = Topic.objects.create(title="Les secrets de Mystic Falls", category=category, author=self.alice)
        Post.objects.create(topic=self.topic, author=self.alice, content="Premier message")
        Post.objects.create(topic=self.topic, author=self.alice, content="Autre message")
        Post.objects.create(topic=self.topic, author=self.silent, content="Je suis là")

    @patch("apps.forum.reply_emails.send_mail")
    def test_reply_emails_each_prior_participant_once_with_topic_title_and_link(self, send_mail):
        self.client.force_authenticate(self.bob)
        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(
                f"/api/topics/{self.topic.slug}/posts/", {"content": "Une réponse"}, format="json"
            )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(send_mail.call_count, 1)
        args = send_mail.call_args.args
        self.assertIn(self.topic.title, args[0])
        self.assertIn("https://nexus.example/topics/les-secrets-de-mystic-falls", args[1])
        self.assertEqual(args[3], ["alice@example.com"])

        self.client.force_authenticate(self.carol)
        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(
                f"/api/topics/{self.topic.slug}/posts/", {"content": "Encore une réponse"}, format="json"
            )
        self.assertEqual(response.status_code, 201)
        recipients = [call.args[3][0] for call in send_mail.call_args_list[1:]]
        self.assertCountEqual(recipients, ["alice@example.com", "bob@example.com"])
        self.assertNotIn("outsider@example.com", recipients)
        self.assertNotIn("carol@example.com", recipients)
