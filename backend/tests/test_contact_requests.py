from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from apps.forum.models import Category, ContactRequest, Post, PrivateMessage, Topic


class ContactRequestTests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.member = User.objects.create_user(username='report-member', email='member@example.com', password='test')
        self.admin = User.objects.create_user(username='report-admin', email='admin@example.com', password='test', role='admin')
        self.ava = User.objects.create_user(username='Ava Bartholomé', email='ava@example.com', password='test', role='fondatrice')
        category = Category.objects.create(name='Forum', slug='forum-test')
        topic = Topic.objects.create(title='Sujet', category=category, author=self.member)
        self.post = Post.objects.create(topic=topic, author=self.member, content='Message à signaler')

    def test_guest_can_request_data_deletion_without_publication(self):
        response = self.client.post('/api/contact/', {
            'kind': 'privacy', 'email': 'visitor@example.com', 'message': 'Je souhaite supprimer mes données.',
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ContactRequest.objects.count(), 1)
        self.assertIsNone(ContactRequest.objects.first().author)
        self.assertEqual(self.client.get('/api/administration/contact/').status_code, 401)

    def test_report_is_visible_only_to_admin(self):
        self.client.force_authenticate(self.member)
        response = self.client.post('/api/contact/', {
            'kind': 'report', 'post': self.post.pk, 'message': 'Cette image pose un problème de droits.',
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ContactRequest.objects.first().email, 'member@example.com')
        self.assertEqual(PrivateMessage.objects.count(), 0)
        self.assertEqual(self.client.get('/api/administration/contact/').status_code, 403)
        self.client.force_authenticate(self.admin)
        listing = self.client.get('/api/administration/contact/?kind=report')
        self.assertEqual(listing.status_code, 200)
        self.assertEqual(listing.data['results'][0]['post_id'], self.post.pk)
        update = self.client.patch('/api/administration/contact/', {
            'id': listing.data['results'][0]['id'], 'is_resolved': True,
        }, format='json')
        self.assertEqual(update.status_code, 200)
        self.assertTrue(ContactRequest.objects.first().is_resolved)

    def test_member_question_goes_to_ava_private_inbox_only(self):
        self.client.force_authenticate(self.member)
        response = self.client.post('/api/contact/', {
            'kind': 'general', 'message': 'Pouvez-vous m’aider avec ma fiche ?',
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ContactRequest.objects.count(), 0)
        pm = PrivateMessage.objects.get()
        self.assertEqual(pm.sender, self.member)
        self.assertEqual(pm.recipient, self.ava)
        self.assertIn('ma fiche', pm.body)
        self.assertEqual(self.client.post('/api/contact/', {
            'kind': 'general', 'message': 'Pouvez-vous m’aider avec ma fiche ?',
        }).status_code, 429)

    def test_report_requires_existing_post_and_requests_are_rate_limited(self):
        invalid = self.client.post('/api/contact/', {
            'kind': 'report', 'email': 'visitor@example.com', 'post': 999999,
            'message': 'Je signale ce contenu.',
        })
        self.assertEqual(invalid.status_code, 400)
        payload = {'kind': 'privacy', 'email': 'visitor@example.com', 'message': 'Je souhaite supprimer mes données.'}
        self.assertEqual(self.client.post('/api/contact/', payload).status_code, 201)
        self.assertEqual(self.client.post('/api/contact/', payload).status_code, 429)

    def test_admin_counters_include_only_unresolved_requests(self):
        ContactRequest.objects.create(kind='report', email='report@example.com', message='Signalement', post=self.post)
        question = ContactRequest.objects.create(kind='general', email='visitor@example.com', message='Une question')
        self.client.force_authenticate(self.member)
        self.assertEqual(self.client.get('/api/administration/contact/?counts=1').status_code, 403)
        self.client.force_authenticate(self.admin)
        self.assertEqual(self.client.get('/api/administration/contact/?counts=1').data, {'reports': 1, 'questions': 1, 'forum_questions': 0})
        question.is_resolved = True
        question.save(update_fields=['is_resolved'])
        self.assertEqual(self.client.get('/api/administration/contact/?counts=1').data, {'reports': 1, 'questions': 0, 'forum_questions': 0})

    def test_forum_questions_leave_alert_after_staff_reply(self):
        category = Category.objects.create(name='Questions membres', slug='questions-membres')
        topic = Topic.objects.create(title='Besoin d’aide', category=category, author=self.member)
        Post.objects.create(topic=topic, author=self.member, content='Comment commencer ?')
        self.client.force_authenticate(self.admin)
        endpoint = '/api/administration/contact/'
        self.assertEqual(self.client.get(endpoint + '?counts=1').data['forum_questions'], 1)
        self.assertEqual(self.client.get(endpoint + '?kind=forum_questions').data[0]['slug'], topic.slug)
        Post.objects.create(topic=topic, author=self.admin, content='Voici comment commencer.')
        self.assertEqual(self.client.get(endpoint + '?counts=1').data['forum_questions'], 0)

    def test_admin_can_page_through_all_contact_requests(self):
        ContactRequest.objects.bulk_create([
            ContactRequest(kind='general', email=f'visitor{i}@example.com', message='Une question')
            for i in range(27)
        ])
        self.client.force_authenticate(self.admin)
        first = self.client.get('/api/administration/contact/?kind=other&page=1')
        second = self.client.get('/api/administration/contact/?kind=other&page=2')
        self.assertEqual(first.data['count'], 27)
        self.assertEqual(len(first.data['results']), 25)
        self.assertEqual(len(second.data['results']), 2)
