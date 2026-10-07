from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from apps.forum.models import ArcanaTransaction, Category, Post, PowerPurchase, Topic


class PowerPurchaseApprovalTests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.admin = User.objects.create_user(username='Ava test', password='secret', role='fondatrice')
        self.player = User.objects.create_user(
            username='Joueur test', password='secret', fiche_status='validated', compte_bancaire=1000,
            power_progression=[{'name': f'Pouvoir {i}', 'evolutions': []} for i in range(4)],
        )
        category = Category.objects.create(name='Boutique magique', slug='boutique-magique')
        topic = Topic.objects.create(title='Catalogue', slug='catalogue-boutique-magique', category=category, author=self.admin)
        Post.objects.create(topic=topic, author=self.admin, content='Catalogue officiel')
        self.request_post = Post.objects.create(topic=topic, author=self.player, content='Je demande un cinquième pouvoir.')
        self.url = f'/api/posts/{self.request_post.pk}/power-purchase/'

    def test_fifth_power_debits_once_and_marks_request(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post(self.url, {'kind': 'fifth', 'name': 'Télékinésie'}, format='json')
        self.assertEqual(response.status_code, 201)
        self.player.refresh_from_db()
        self.assertEqual(self.player.compte_bancaire, 400)
        self.assertEqual(self.player.power_progression[4], {'name': 'Télékinésie', 'evolutions': []})
        self.assertEqual(ArcanaTransaction.objects.filter(user=self.player, amount=-600).count(), 1)
        self.assertEqual(PowerPurchase.objects.filter(request_post=self.request_post).count(), 1)
        self.assertEqual(self.client.post(self.url, {'kind': 'fifth', 'name': 'Autre'}, format='json').status_code, 409)
        self.player.refresh_from_db()
        self.assertEqual(self.player.compte_bancaire, 400)

    def test_evolution_respects_limit_and_balance(self):
        self.player.power_progression[0]['evolutions'] = ['Maîtrise 1']
        self.player.save(update_fields=['power_progression'])
        self.client.force_authenticate(self.admin)
        response = self.client.post(self.url, {'kind': 'evolution', 'power_index': 0, 'name': 'Maîtrise 2'}, format='json')
        self.assertEqual(response.status_code, 201)
        self.player.refresh_from_db()
        self.assertEqual(self.player.compte_bancaire, 700)
        self.assertEqual(self.player.power_progression[0]['evolutions'], ['Maîtrise 1', 'Maîtrise 2'])

    def test_player_cannot_approve_own_request(self):
        self.client.force_authenticate(self.player)
        self.assertEqual(self.client.post(self.url, {'kind': 'fifth', 'name': 'Télékinésie'}, format='json').status_code, 403)
        self.assertFalse(PowerPurchase.objects.exists())

    def test_insufficient_balance_changes_nothing(self):
        self.player.compte_bancaire = 500
        self.player.save(update_fields=['compte_bancaire'])
        self.client.force_authenticate(self.admin)
        self.assertEqual(self.client.post(self.url, {'kind': 'fifth', 'name': 'Télékinésie'}, format='json').status_code, 400)
        self.player.refresh_from_db()
        self.assertEqual(self.player.compte_bancaire, 500)
        self.assertEqual(len(self.player.power_progression), 4)
        self.assertFalse(PowerPurchase.objects.exists())
