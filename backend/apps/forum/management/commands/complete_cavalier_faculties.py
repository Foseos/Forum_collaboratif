"""Add the fourth faculty to each Cavalier in the published faction guide."""

from html import escape
import re

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.forum.models import Topic
from faction_role_powers import FACTION_ROLES


class Command(BaseCommand):
    help = 'Complète les quatre facultés des Cavaliers dans la fiche des factions.'

    @transaction.atomic
    def handle(self, *args, **options):
        roles = FACTION_ROLES["Les cavaliers de l'apocalypse"]
        if len(roles) != 4 or any(len(role['powers']) != 4 for role in roles):
            raise ValueError('Chaque Cavalier doit posséder exactement quatre facultés dans la source.')
        post = Topic.objects.get(slug='guide-des-factions-et-alliances').posts.order_by('created_at').first()
        if post is None:
            raise ValueError('Guide des factions sans texte.')
        content = post.content
        for role in roles:
            title = f"{role['symbol']} {role['name']}"
            pattern = re.compile(r'(<h3\b[^>]*>' + re.escape(title) + r'</h3>\s*<ul\b[^>]*>)(.*?)(</ul>)', re.S)
            matches = list(pattern.finditer(content))
            if len(matches) != 1:
                raise ValueError(f'Encart introuvable ou ambigu : {role["name"]}')
            match = matches[0]
            body = match.group(2)
            fourth = role['powers'][3]
            if fourth['name'] not in body:
                if body.count('<li ') != 3:
                    raise ValueError(f'Nombre de facultés inattendu : {role["name"]}')
                addition = ("<li style='margin:.4rem 0;'><strong style='color:#e2d9f3;'>"
                            f"{escape(fourth['name'])}</strong> — {escape(fourth['description'])}</li>")
                content = content[:match.start(3)] + addition + content[match.start(3):]
        content = content.replace(
            'Les quatre facultés de chaque Gardien sont définies ci-dessous ; une quatrième faculté reste à préciser pour chaque Cavalier.',
            'Les quatre facultés de chaque Gardien et de chaque Cavalier sont définies ci-dessous.',
        ).replace(
            'Les Gardiens disposent désormais de leurs quatre facultés ; la quatrième de chaque Cavalier reste à définir.',
            'Les Gardiens et les Cavaliers disposent chacun de leurs quatre facultés définies.',
        )
        if content != post.content:
            post.content = content
            post.save(update_fields=['content'])
        self.stdout.write(self.style.SUCCESS('Quatrième faculté ajoutée aux quatre Cavaliers.'))
