"""Replace clock-based shop durations with RP turns in the live catalogue."""

import re

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.forum.models import Topic


CHANGES = {
    "Potion d'invisibilité": [
        ('pendant 1 heure', 'pendant 3 tours de RP'),
        ('une heure en RP', 'trois tours de RP'),
    ],
    'Potion de guérison': [
        ('en quelques minutes', 'en 1 tour de RP'),
        ('sur quelques minutes de la scène', 'sur un tour de RP'),
    ],
    'Élixir de vérité': [
        ("Force la personne qui l'ingère à dire la vérité pendant 1 heure.",
         "Agit pendant 2 tours de RP, avec l'accord du joueur concerné."),
        ('une heure en RP', 'deux tours de RP'),
    ],
    "Potion d'immunité magique": [
        ('pendant 6 heures', 'pendant 3 tours de RP'),
        ('six heures en RP', 'trois tours de RP'),
    ],
    'Potion de sommeil profond': [
        ('un sommeil de 8 heures sans rêves', 'un sommeil de 2 tours de RP, avec l’accord du joueur concerné'),
        ('un sommeil de huit heures en RP', 'un sommeil de deux tours de RP'),
    ],
    'Orbe du Destin': [
        ('Une activation par mois en RP ; consigner sa date. La vision porte sur les quarante-huit heures à venir.',
         'Une activation par intrigue ; la vision concerne un événement à venir de cette intrigue, défini avec le maître du jeu.'),
    ],
    'Anneau des Éléments': [
        ('pendant 30 minutes', 'pendant 3 tours de RP'),
        ('trente minutes de maîtrise temporaire en RP', 'trois tours de RP de maîtrise temporaire'),
    ],
}

INTRO = ('<p style="margin: 0 0 1.5rem; font-size: 0.82rem; color: #c4b5d4; line-height: 1.6; text-align: center;">'
         'Les effets temporaires se comptent en <strong>tours de RP</strong> : un tour correspond à une intervention de chaque personnage directement concerné dans la scène. Le tour d’utilisation compte comme le premier.</p>')


class Command(BaseCommand):
    help = 'Exprime les durées de la boutique en tours de RP.'

    @transaction.atomic
    def handle(self, *args, **options):
        post = Topic.objects.get(slug='catalogue-boutique-magique').posts.order_by('created_at').first()
        if post is None:
            raise ValueError('Catalogue sans texte.')
        content = post.content
        found = set()

        def update_row(match):
            row = match.group(0)
            for name, changes in CHANGES.items():
                if name not in row:
                    continue
                found.add(name)
                for old, new in changes:
                    if old not in row and new not in row:
                        raise ValueError(f'Texte inattendu dans {name} : {old}')
                    row = row.replace(old, new)
                return row
            return row

        content = re.sub(r'<tr\b[^>]*>.*?</tr>', update_row, content, flags=re.S | re.I)
        if found != set(CHANGES):
            raise ValueError(f'Objets absents : {set(CHANGES) - found}')
        if INTRO not in content:
            anchor = '<!-- ══ POTIONS ══ -->'
            if anchor not in content:
                raise ValueError('Emplacement de la note introuvable.')
            content = content.replace(anchor, INTRO + '\n\n' + anchor, 1)
        if content != post.content:
            post.content = content
            post.save(update_fields=['content'])
        self.stdout.write(self.style.SUCCESS('Durées de la boutique exprimées en tours de RP.'))
