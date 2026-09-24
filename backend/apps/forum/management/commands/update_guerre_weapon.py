"""Replace Guerre's fourth faculty in the published faction guide."""

from html import escape

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.forum.models import Topic
from faction_role_powers import FACTION_ROLES


OLD = ('<strong style="color:#e2d9f3;">Tenacité guerrière</strong> — '
       'Résiste mieux à la fatigue et à la douleur pendant deux tours de RP au cœur d’un affrontement. '
       'Les blessures demeurent et cette résistance ne garantit ni victoire ni survie.')


class Command(BaseCommand):
    help = 'Donne la matérialisation d’armes au Cavalier Guerre.'

    @transaction.atomic
    def handle(self, *args, **options):
        post = Topic.objects.get(slug='guide-des-factions-et-alliances').posts.order_by('created_at').first()
        if post is None:
            raise ValueError('Guide des factions sans texte.')
        power = FACTION_ROLES["Les cavaliers de l'apocalypse"][0]['powers'][3]
        new = f"<strong style='color:#e2d9f3;'>{escape(power['name'])}</strong> — {escape(power['description'])}"
        old = OLD.replace('style="color:#e2d9f3;"', "style='color:#e2d9f3;'")
        if new in post.content:
            self.stdout.write('La faculté de Guerre est déjà à jour.')
            return
        if post.content.count(old) != 1:
            raise ValueError('Ancienne faculté de Guerre introuvable ou ambiguë.')
        post.content = post.content.replace(old, new, 1)
        post.save(update_fields=['content'])
        self.stdout.write(self.style.SUCCESS('Matérialisation d’armes ajoutée à Guerre.'))
