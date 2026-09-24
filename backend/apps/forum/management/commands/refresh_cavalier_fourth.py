"""Refresh the fourth faculties of Mort, Famine and Pestilence in the guide."""

from html import escape

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.forum.models import Topic
from faction_role_powers import FACTION_ROLES


OLD = {
    'Mort': ('Empreinte funèbre', 'Perçoit des traces fragmentaires laissées par une mort récente dans un lieu ou sur un objet. Ne révèle ni l’identité certaine du défunt ni la cause complète du décès ; les indices d’intrigue viennent du maître du jeu.'),
    'Famine': ('Adaptation au manque', 'Supporte temporairement la faim, la soif et l’épuisement mieux qu’un être ordinaire pendant trois tours de RP. Ne restaure pas les réserves perdues et ne dispense pas de se nourrir ensuite.'),
    'Pestilence': ('Perception des afflictions', 'Détecte une maladie ou une contamination active à proximité et en distingue les signes généraux. N’identifie pas à coup sûr sa cause, ne révèle aucun secret médical et ne la guérit pas.'),
}


class Command(BaseCommand):
    help = 'Actualise les quatrièmes facultés de trois Cavaliers.'

    @transaction.atomic
    def handle(self, *args, **options):
        post = Topic.objects.get(slug='guide-des-factions-et-alliances').posts.order_by('created_at').first()
        if post is None:
            raise ValueError('Guide des factions sans texte.')
        content = post.content
        roles = {role['name']: role for role in FACTION_ROLES["Les cavaliers de l'apocalypse"]}
        for name, (old_name, old_description) in OLD.items():
            power = roles[name]['powers'][3]
            old = f"<strong style='color:#e2d9f3;'>{escape(old_name)}</strong> — {escape(old_description)}"
            new = f"<strong style='color:#e2d9f3;'>{escape(power['name'])}</strong> — {escape(power['description'])}"
            if new in content:
                continue
            if content.count(old) != 1:
                raise ValueError(f'Ancienne faculté introuvable ou ambiguë : {name}')
            content = content.replace(old, new, 1)
        if content != post.content:
            post.content = content
            post.save(update_fields=['content'])
        self.stdout.write(self.style.SUCCESS('Quatrièmes facultés actualisées.'))
