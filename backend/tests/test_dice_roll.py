from unittest.mock import patch

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from apps.forum.models import Category, Post, Topic


class DiceRollTests(APITestCase):
    def setUp(self):
        self.member = get_user_model().objects.create_user(username='dice-player', password='test')
        self.category = Category.objects.create(name='Contextes et animations', slug='contextes-et-animations')
        self.topic = Topic.objects.create(title='Une enquête', category=self.category, author=self.member)
        Post.objects.create(topic=self.topic, author=self.member, content='Départ')
        self.url = f'/api/topics/{self.topic.slug}/roll/'

    @patch('apps.forum.views.send_topic_reply_emails')
    @patch('apps.forum.views.secrets.randbelow', return_value=3)
    def test_roll_is_visible_and_immutable(self, _random, _emails):
        self.client.force_authenticate(self.member)
        response = self.client.post(self.url, {'intention': 'Chercher un indice'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['dice_result'], 4)
        post = Post.objects.get(pk=response.data['id'])
        self.assertIn('Chercher un indice', post.content)
        self.assertEqual(self.client.patch(f'/api/posts/{post.pk}/', {'content': 'Autre résultat'}).status_code, 403)
        self.assertEqual(self.client.delete(f'/api/posts/{post.pk}/').status_code, 403)
        self.assertEqual(self.client.post(self.url, {'intention': 'Encore'}).status_code, 429)

    def test_roll_requires_login_and_animation_category(self):
        self.assertEqual(self.client.post(self.url, {'intention': 'Chercher'}).status_code, 401)
        other = Category.objects.create(name='Autre', slug='autre')
        self.topic.category = other
        self.topic.save(update_fields=['category'])
        self.client.force_authenticate(self.member)
        self.assertEqual(self.client.post(self.url, {'intention': 'Chercher'}).status_code, 400)

    def test_lottery_topic_has_no_dice_roll(self):
        lottery = Topic.objects.create(
            title='Loterie des Arcana Flouz', slug='loterie-des-arcana-flouz',
            category=self.category, author=self.member,
        )
        self.client.force_authenticate(self.member)
        response = self.client.post(f'/api/topics/{lottery.slug}/roll/', {'intention': 'Tenter ma chance'})
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Post.objects.filter(topic=lottery).exists())
