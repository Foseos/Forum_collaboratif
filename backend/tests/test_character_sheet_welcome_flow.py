from django.contrib.auth import get_user_model
from django.core.management import call_command
from unittest.mock import patch
from rest_framework.test import APITestCase

from apps.forum.models import Category, Post, Topic
from apps.notifications.models import Notification


class CharacterSheetWelcomeFlowTests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.author = User.objects.create_user(username='fiche-author', email='author@example.com', password='test-password')
        self.guest = User.objects.create_user(username='fiche-guest', password='test-password')
        self.admin = User.objects.create_user(username='fiche-admin', password='test-password', role='admin')
        self.founder = User.objects.create_user(username='fiche-founder', password='test-password', role='fondatrice')
        Category.objects.create(name='Bienvenue à Nexus Arcana', slug='bienvenue-san-francisco')
        self.pending = Category.objects.create(name='Fiches en attente de validation', slug='fiches-de-presentation-terminees')

    def test_sheet_is_visible_and_welcomes_are_allowed_until_admin_validation(self):
        self.client.force_authenticate(self.author)
        response = self.client.post(
            '/api/categories/fiches-de-presentation-terminees/topics/',
            {'title': 'Présentation de Mira', 'first_post_content': '<p>Ma fiche</p>'},
            format='json',
        )
        self.assertEqual(response.status_code, 201)
        topic = Topic.objects.get(pk=response.data['id'])
        first_post = topic.posts.first()
        self.assertEqual(topic.category, self.pending)
        self.assertFalse(topic.is_locked)

        self.client.force_authenticate(self.guest)
        self.assertEqual(self.client.get(f'/api/topics/{topic.slug}/').status_code, 200)
        self.assertEqual(self.client.patch(f'/api/posts/{first_post.pk}/', {'content': 'Autre fiche'}, format='json').status_code, 403)
        reply = self.client.post(f'/api/topics/{topic.slug}/posts/', {'content': 'Bienvenue !'}, format='json')
        self.assertEqual(reply.status_code, 201)

        self.client.force_authenticate(self.admin)
        validation = self.client.patch(f'/api/users/{self.author.pk}/', {'fiche_status': 'validated'}, format='json')
        self.assertEqual(validation.status_code, 200)
        topic.refresh_from_db()
        self.assertEqual(topic.category.slug, 'fiches-validees-et-archivees')
        self.assertTrue(topic.is_locked)
        validation_post = topic.posts.order_by('-created_at').first()
        self.assertEqual(validation_post.author, self.founder)
        self.assertIn('Ta fiche est validée', validation_post.content)
        self.assertIn('href="/categories/fiches-validees-et-archivees"', validation_post.content)
        self.assertNotIn('Ta présentation reste ici', validation_post.content)
        self.assertIn('href="/categories/fiche-personnage"', validation_post.content)
        self.assertIn('href="/topics/demande-de-partenaire-de-rp"', validation_post.content)
        self.assertIn('href="/topics/agence-immobiliere-demande-de-logement"', validation_post.content)
        self.assertIn('disponibles à tout moment', validation_post.content)
        self.assertIn('— Ava Bartholomé', validation_post.content)
        self.assertTrue(Notification.objects.filter(
            recipient=self.author, sender=self.founder,
            message__contains='a été validée par la fondatrice',
        ).exists())

        self.client.force_authenticate(self.author)
        self.assertEqual(self.client.patch(f'/api/posts/{first_post.pk}/', {'content': 'Changement'}, format='json').status_code, 403)
        self.assertEqual(self.client.post(f'/api/topics/{topic.slug}/posts/', {'content': 'Encore'}, format='json').status_code, 403)

    @patch('apps.users.validation_emails.send_mail')
    def test_validation_email_names_topic_and_validation_is_not_repeated(self, send_mail):
        self.client.force_authenticate(self.author)
        created = self.client.post('/api/categories/fiches-de-presentation-terminees/topics/', {
            'title': 'Présentation de Mira', 'first_post_content': 'Ma fiche',
        }, format='json')
        self.assertEqual(created.status_code, 201)
        topic = Topic.objects.get(pk=created.data['id'])

        self.client.force_authenticate(self.admin)
        with self.captureOnCommitCallbacks(execute=True):
            validated = self.client.patch(f'/api/users/{self.author.pk}/', {
                'fiche_status': 'validated',
            }, format='json')
        self.assertEqual(validated.status_code, 200)
        self.assertEqual(send_mail.call_count, 1)
        subject, body, _, recipients = send_mail.call_args.args
        self.assertIn(topic.title, subject)
        self.assertIn(f'/topics/{topic.slug}', body)
        self.assertEqual(recipients, ['author@example.com'])

        repeated = self.client.patch(f'/api/users/{self.author.pk}/', {
            'fiche_status': 'validated',
        }, format='json')
        self.assertEqual(repeated.status_code, 200)
        self.assertEqual(topic.posts.filter(author=self.founder).count(), 1)
        self.assertEqual(send_mail.call_count, 1)

    def test_parent_and_unvalidated_recap_category_cannot_hold_character_sheet_topic(self):
        self.client.force_authenticate(self.author)
        response = self.client.post('/api/categories/bienvenue-san-francisco/topics/', {
            'title': 'Fiche mal placée', 'first_post_content': 'Présentation',
        }, format='json')
        self.assertEqual(response.status_code, 403)
        Category.objects.create(name='Fiche personnage', slug='fiche-personnage')
        alternate = self.client.post('/api/categories/fiche-personnage/topics/', {
            'title': 'Autre fiche mal placée', 'first_post_content': 'Présentation',
        }, format='json')
        self.assertEqual(alternate.status_code, 403)
        self.assertFalse(Topic.objects.exists())

    def test_validated_member_can_create_one_editable_recap_topic(self):
        Category.objects.create(name='Fiche personnage', slug='fiche-personnage')
        self.author.fiche_status = 'validated'
        self.author.save(update_fields=['fiche_status'])
        self.client.force_authenticate(self.author)
        response = self.client.post('/api/categories/fiche-personnage/topics/', {
            'title': 'Mira — carnet de personnage',
            'first_post_content': '<p>Mes liens et mes RP</p>',
        }, format='json')
        self.assertEqual(response.status_code, 201)
        post = Topic.objects.get(pk=response.data['id']).posts.first()
        self.assertEqual(self.client.patch(f'/api/posts/{post.pk}/', {
            'content': '<p>Mes liens actualisés</p>',
        }, format='json').status_code, 200)
        duplicate = self.client.post('/api/categories/fiche-personnage/topics/', {
            'title': 'Mira — second carnet', 'first_post_content': 'Un autre carnet',
        }, format='json')
        self.assertEqual(duplicate.status_code, 403)

    def test_official_recap_model_is_pinned_locked_and_does_not_take_admin_slot(self):
        Category.objects.create(name='Fiche personnage', slug='fiche-personnage')
        call_command('seed_recap_model', verbosity=0)
        model = Topic.objects.get(slug='modele-fiche-personnage')
        self.assertTrue(model.is_pinned)
        self.assertTrue(model.is_locked)
        self.assertIn('Parcours en jeu', model.posts.first().content)
        self.client.force_authenticate(self.admin)
        response = self.client.post('/api/categories/fiche-personnage/topics/', {
            'title': 'Carnet personnel', 'first_post_content': 'Mes liens',
        }, format='json')
        self.assertEqual(response.status_code, 201)

    def test_archive_cannot_receive_a_new_topic_directly(self):
        Category.objects.get_or_create(slug='fiches-validees-et-archivees', defaults={'name': 'Fiches validées & archivées'})
        self.author.fiche_status = 'validated'
        self.author.save(update_fields=['fiche_status'])
        self.client.force_authenticate(self.author)
        response = self.client.post('/api/categories/fiches-validees-et-archivees/topics/', {
            'title': 'Fiche sans validation', 'first_post_content': 'Présentation',
        }, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Topic.objects.exists())

    def test_author_cannot_move_or_unlock_a_topic(self):
        archive, _ = Category.objects.get_or_create(slug='fiches-validees-et-archivees', defaults={'name': 'Fiches validées & archivées'})
        topic = Topic.objects.create(title='Fiche en cours', category=self.pending, author=self.author)
        Post.objects.create(topic=topic, author=self.author, content='Ma fiche')
        self.client.force_authenticate(self.author)
        self.assertEqual(self.client.patch(f'/api/topics/{topic.slug}/', {'category': archive.pk}, format='json').status_code, 403)
        self.assertEqual(self.client.patch(f'/api/topics/{topic.slug}/', {'is_locked': True}, format='json').status_code, 400)
        topic.refresh_from_db()
        self.assertEqual(topic.category, self.pending)
        self.assertFalse(topic.is_locked)

    def test_member_html_is_sanitized_on_write_and_read(self):
        self.client.force_authenticate(self.author)
        response = self.client.post('/api/categories/fiches-de-presentation-terminees/topics/', {
            'title': 'Présentation HTML',
            'first_post_content': '<p style="color:red" onclick="alert(1)">Texte</p><script>alert(2)</script><img src="javascript:alert(3)" onerror="alert(4)">',
        }, format='json')
        self.assertEqual(response.status_code, 201)
        topic = Topic.objects.get(pk=response.data['id'])
        post = topic.posts.first()
        self.assertIn('color:red', post.content)
        self.assertNotIn('onclick', post.content)
        self.assertNotIn('<script', post.content)
        self.assertNotIn('javascript:', post.content)
        self.assertNotIn('onerror', post.content)

        # Un ancien message non nettoyé doit également être sûr à la lecture.
        post.content = '<p onmouseover="alert(1)">Ancien texte</p>'
        post.save(update_fields=['content'])
        shown = self.client.get(f'/api/topics/{topic.slug}/posts/').data['results'][0]['content']
        self.assertIn('Ancien texte', shown)
        self.assertNotIn('onmouseover', shown)
