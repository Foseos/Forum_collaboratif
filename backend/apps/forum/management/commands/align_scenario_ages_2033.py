"""Harmonise les identités des scénarios avec la chronologie 2033."""

import html
import json
import re
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.forum.models import Topic
from apps.forum.scenario_ages_2033 import SCENARIO_AGES


FLAGS = re.I | re.S
DT_FIELD = re.compile(r'(<dt\b[^>]*>)(.*?)(</dt>\s*<dd\b[^>]*>)(.*?)(</dd>)', FLAGS)
ROW_FIELD = re.compile(r'(<tr\b[^>]*>\s*<td\b[^>]*>)(.*?)(</td>\s*<td\b[^>]*>)(.*?)(</td>\s*</tr>)', FLAGS)
PAR_FIELD = re.compile(r'(<p\b[^>]*>\s*)(Âge|Date de naissance)\s*:\s*(.*?)(</p>)', FLAGS)


def label_text(value):
    return html.unescape(re.sub(r'<[^>]+>', '', value)).strip().casefold()


def replace_identity_fields(content, age, birth):
    """Modifie uniquement les deux champs d'identité, quel que soit leur balisage."""
    age = html.escape(age)
    birth = html.escape(birth)
    # Corrige la seule fiche de type paragraphe si une exécution antérieure a
    # concaténé sa valeur à l'étiquette au lieu de conserver les deux-points.
    content = content.replace('ÂgeVingt-cinq à trente ans · date exacte au choix28 ans en 2033 · cadet d’Abigael',
                              'Âge : 28 ans en 2033 · cadet d’Abigael')
    for pattern, kind in ((DT_FIELD, 'dl'), (ROW_FIELD, 'table'), (PAR_FIELD, 'paragraph')):
        matches = list(pattern.finditer(content))
        age_matches = [m for m in matches if label_text(m.group(2)) in ('âge', 'age')]
        if len(age_matches) != 1:
            continue
        birth_matches = [m for m in matches if label_text(m.group(2)) in ('date de naissance', 'naissance')]
        if len(birth_matches) > 1:
            raise ValueError('Plusieurs champs de naissance dans une fiche.')

        def field_value(m, new_value):
            if kind == 'paragraph':
                return m.group(1) + m.group(2) + ' : ' + new_value + m.group(4)
            return m.group(1) + m.group(2) + m.group(3) + new_value + m.group(5)

        age_match = age_matches[0]
        edits = [(age_match.start(), age_match.end(), field_value(age_match, age))]
        if birth_matches:
            m = birth_matches[0]
            edits.append((m.start(), m.end(), field_value(m, birth)))
        else:
            if kind == 'paragraph':
                new_field = age_match.group(1) + 'Date de naissance : ' + birth + age_match.group(4)
            else:
                new_field = (age_match.group(1) + 'Date de naissance' + age_match.group(3)
                             + birth + age_match.group(5))
            edits.append((age_match.end(), age_match.end(), new_field))
        for start, end, replacement in sorted(edits, reverse=True):
            content = content[:start] + replacement + content[end:]
        if kind == 'table' and 'Henry Mitchell a cinquante-trois ans' in content:
            content = content.replace('Henry Mitchell a cinquante-trois ans', 'Henry Mitchell a soixante ans')
        return content
    raise ValueError('Champ Âge introuvable ou ambigu dans la fiche.')


class Command(BaseCommand):
    help = 'Ajoute et harmonise les âges et dates de naissance des scénarios pour 2033.'

    @transaction.atomic
    def handle(self, *args, **options):
        topics = list(Topic.objects.select_for_update().filter(category__slug='scenarios-a-prendre'))
        slugs = {topic.slug for topic in topics}
        if slugs != set(SCENARIO_AGES):
            raise ValueError(f'Inventaire incomplet : sans repère {slugs - set(SCENARIO_AGES)} ; '
                             f'sans scénario {set(SCENARIO_AGES) - slugs}')
        changes = []
        for topic in topics:
            post = topic.posts.select_for_update().order_by('created_at', 'pk').first()
            if post is None:
                raise ValueError(f'Fiche sans message : {topic.slug}')
            content = replace_identity_fields(post.content, *SCENARIO_AGES[topic.slug])
            if content != post.content:
                changes.append((post, content))
        if changes:
            backup_dir = Path(settings.BASE_DIR) / 'data' / 'scenario_backups'
            backup_dir.mkdir(parents=True, exist_ok=True)
            backup_path = backup_dir / ('scenario-ages-2033-' + timezone.now().strftime('%Y%m%dT%H%M%S%f') + '.json')
            backup_path.write_text(json.dumps([
                {'post_id': post.pk, 'content': post.content} for post, _ in changes
            ], ensure_ascii=False), encoding='utf-8')
            for post, content in changes:
                post.content = content
                post.save(update_fields=['content', 'is_edited', 'updated_at'])
        self.stdout.write(self.style.SUCCESS(f'{len(changes)} fiches de scénario harmonisées pour 2033.'))
