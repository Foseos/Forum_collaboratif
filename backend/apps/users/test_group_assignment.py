from django.test import TestCase
from rest_framework.test import APIClient

from .models import User


class GroupAssignmentPermissionsTests(TestCase):
    def setUp(self):
        self.founder = User.objects.create_user(username='Fondatrice test', password='pass', role='fondatrice')
        self.admin = User.objects.create_user(username='Admin test', password='pass', role='admin')
        self.member = User.objects.create_user(username='Membre test', password='pass', role='user')
        self.client = APIClient()

    def test_member_cannot_assign_own_faction_species_or_specialty(self):
        self.client.force_authenticate(user=self.member)
        response = self.client.patch('/api/users/me/', {
            'groupe': 'Les Fondateurs', 'race': 'Fée', 'nature': 'Fée lumineuse',
        }, format='json')
        self.assertEqual(response.status_code, 400)
        self.member.refresh_from_db()
        self.assertEqual((self.member.groupe, self.member.race, self.member.nature), ('', '', ''))

    def test_other_admin_cannot_assign_faction_or_species(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(f'/api/users/{self.member.pk}/', {
            'groupe': 'Les Fondateurs', 'race': 'Fée', 'nature': 'Fée lumineuse',
        }, format='json')
        self.assertEqual(response.status_code, 400)
        self.member.refresh_from_db()
        self.assertEqual((self.member.groupe, self.member.race, self.member.nature), ('', '', ''))

    def test_founder_can_assign_faction_species_and_specialty(self):
        self.client.force_authenticate(user=self.founder)
        response = self.client.patch(f'/api/users/{self.member.pk}/', {
            'groupe': 'Les Fondateurs', 'race': 'Fée', 'nature': 'Fée lumineuse',
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.member.refresh_from_db()
        self.assertEqual((self.member.groupe, self.member.race, self.member.nature),
                         ('Les Fondateurs', 'Fée', 'Fée lumineuse'))
