from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.forum.models import Category, Post, Topic
from apps.forum.rewards import count_message_words


class RPRewardTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='writer', fiche_status='validated', compte_bancaire=30
        )
        root = Category.objects.create(name='Mystic Falls', slug='mystic-falls')
        self.category = Category.objects.create(name='Lieu RP', slug='lieu-rp', parent=root)
        self.topic = Topic.objects.create(title='Rencontre', category=self.category, author=self.user)
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_threshold_for_first_posts_and_replies(self):
        expected = 30
        for count in (99, 100, 101, 150):
            for first in (True, False):
                with self.subTest(count=count, first=first):
                    content = ' '.join(['magie'] * count)
                    if first:
                        response = self.client.post('/api/categories/lieu-rp/topics/', {
                            'title': f'Sujet {count}', 'first_post_content': content,
                        })
                    else:
                        response = self.client.post('/api/topics/rencontre/posts/', {'content': content})
                    self.assertEqual(response.status_code, 201)
                    if count > 100:
                        expected += 10
                    self.user.refresh_from_db()
                    self.assertEqual(self.user.compte_bancaire, expected)

    def test_html_entities_and_formatting(self):
        content = '<p>' + '&nbsp;'.join(['magie'] * 101) + '</p>'
        self.assertEqual(count_message_words(content), 101)
        self.assertEqual(count_message_words("<p>Bon<strong>jour</strong> l’ami</p><p>arc-en-ciel ! ✨</p>"), 3)
        self.assertEqual(count_message_words('<img alt="un long texte"><style>du texte caché</style><!-- commentaire -->'), 0)
        response = self.client.post('/api/topics/rencontre/posts/', {'content': content})
        self.assertEqual(response.status_code, 201)
        self.user.refresh_from_db()
        self.assertEqual(self.user.compte_bancaire, 40)

    def test_edit_does_not_reward_again(self):
        content = 'magie ' * 101
        response = self.client.post('/api/topics/rencontre/posts/', {'content': content})
        for _ in range(2):
            edited = self.client.patch(f"/api/posts/{response.data['id']}/", {'content': content + 'encore'})
            self.assertEqual(edited.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.compte_bancaire, 40)

    def test_database_balance_is_used_even_when_user_object_is_stale(self):
        get_user_model().objects.filter(pk=self.user.pk).update(compte_bancaire=70)
        response = self.client.post('/api/topics/rencontre/posts/', {'content': 'magie ' * 101})
        self.assertEqual(response.status_code, 201)
        self.user.refresh_from_db()
        self.assertEqual(self.user.compte_bancaire, 80)

    def test_reward_failure_rolls_back_publication(self):
        with patch('apps.forum.views.award_publication', side_effect=RuntimeError('failure')):
            with self.assertRaises(RuntimeError):
                self.client.post('/api/topics/rencontre/posts/', {'content': 'magie ' * 101})
        self.assertEqual(Post.objects.count(), 0)

    def test_rejected_publication_has_no_reward(self):
        response = self.client.post('/api/topics/rencontre/posts/', {'content': ''})
        self.assertEqual(response.status_code, 400)
        self.user.refresh_from_db()
        self.assertEqual(self.user.compte_bancaire, 30)

    def test_long_non_rp_posts_do_not_reward(self):
        welcome = Category.objects.create(name='Parrainage', slug='parrainage')
        guide = Topic.objects.create(title='Questions', category=welcome, author=self.user)
        content = 'magie ' * 101

        reply = self.client.post(f'/api/topics/{guide.slug}/posts/', {'content': content})
        Category.objects.create(name='Fiche personnage', slug='fiche-personnage')
        first = self.client.post('/api/categories/fiche-personnage/topics/', {
            'title': 'Présentation', 'first_post_content': content,
        })

        self.assertEqual(reply.status_code, 201)
        self.assertEqual(first.status_code, 201)
        self.user.refresh_from_db()
        self.assertEqual(self.user.compte_bancaire, 30)
