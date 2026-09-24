"""Actualise les deux facultés modifiées dans le guide publié des factions."""

from django.core.management.base import BaseCommand, CommandError

from apps.forum.models import Topic
from faction_role_powers import FACTION_ROLES


class Command(BaseCommand):
    help = 'Met à jour la nécromancie de Mort et la disette magique de Famine.'

    def handle(self, *args, **options):
        topic = Topic.objects.filter(slug='guide-des-factions-et-alliances', category__slug='factions').first()
        if topic is None:
            raise CommandError('Le guide des factions est introuvable.')
        post = topic.posts.order_by('created_at', 'pk').first()
        if post is None:
            raise CommandError('Le guide des factions est vide.')
        roles = {role['name']: role for role in FACTION_ROLES["Les cavaliers de l'apocalypse"]}
        necromancy = next(power for power in roles['Mort']['powers'] if power['name'] == 'Nécromancie')
        famine = next(power for power in roles['Famine']['powers'] if power['name'] == 'Disette magique')
        replacements = [
            (
                'Nécromancie</strong> — Communique avec les morts et peut rappeler temporairement certains esprits dans le monde des vivants.',
                f"Nécromancie</strong> — {necromancy['description']}",
            ),
            (
                'Décomposition</strong> — Accélère le pourrissement de la nourriture, des plantes, des potions et de certains ingrédients magiques.',
                f"{famine['name']}</strong> — {famine['description']}",
            ),
        ]
        content = post.content
        for old, new in replacements:
            if new in content:
                continue
            if content.count(old) != 1:
                raise CommandError(f'Passage attendu introuvable ou en double : {old[:40]}')
            content = content.replace(old, new, 1)
        if content != post.content:
            post.content = content
            post.save(update_fields=['content', 'updated_at'])
        self.stdout.write(self.style.SUCCESS('Pouvoirs de Mort et de Famine mis à jour dans le guide.'))
