"""Inventaire des âges et naissances figurant dans les scénarios."""

import html
import re

from apps.forum.models import Topic
from apps.forum.scenario_ages_2033 import SCENARIO_AGES
from apps.forum.management.commands.align_scenario_ages_2033 import replace_identity_fields


def plain(value):
    return html.unescape(re.sub(r'<[^>]+>', ' ', value)).strip()


topics = list(Topic.objects.filter(category__slug='scenarios-a-prendre').order_by('title'))
slugs = {topic.slug for topic in topics}
print('Inventaire :', len(topics), 'fiches,', len(SCENARIO_AGES), 'repères ; écarts :', slugs ^ set(SCENARIO_AGES))
for topic in topics:
    post = topic.posts.order_by('created_at', 'pk').first()
    content = post.content if post else ''
    try:
        replace_identity_fields(content, *SCENARIO_AGES[topic.slug])
    except Exception as exc:
        print('ERREUR', topic.slug, exc)
    fields = {}
    for label, value in re.findall(r'<dt[^>]*>(.*?)</dt>\s*<dd[^>]*>(.*?)</dd>', content, re.I | re.S):
        fields[plain(label).lower()] = plain(value)
    for label, value in re.findall(r'<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>', content, re.I | re.S):
        fields.setdefault(plain(label).lower(), plain(value))
    age = fields.get('âge', fields.get('age', ''))
    birth = fields.get('date de naissance', fields.get('naissance', ''))
    if not age:
        match = re.search(r'<p[^>]*>\s*Âge\s*:\s*(.*?)</p>', content, re.I | re.S)
        age = plain(match.group(1)) if match else ''
    if not birth:
        match = re.search(r'<p[^>]*>\s*Date de naissance\s*:\s*(.*?)</p>', content, re.I | re.S)
        birth = plain(match.group(1)) if match else ''
    print(f'{topic.slug}\t{age or "[absent]"}\t{birth or "[absent]"}')
