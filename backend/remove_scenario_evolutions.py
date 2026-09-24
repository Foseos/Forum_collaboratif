import json
import re
from pathlib import Path
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from apps.forum.models import Post


def clean(content):
    content = content.replace('II. Quatre pouvoirs et leurs évolutions', 'II. Pouvoirs de base')
    content = re.sub(r'(<p\b[^>]*>)Quatre pouvoirs de base à la création\.[^<]*</p>', r'\1Quatre pouvoirs de base à la création.</p>', content)
    content = re.sub(r'<p\b[^>]*>Évolution [12],[^<]*</p>', '', content)
    content = content.replace(' ; les manifestations majeures sont des évolutions à valider.', '.')
    content = content.replace('Une tempête, un gel massif ou un effet temporel véritable nécessite une évolution explicitement validée.', 'Ces pouvoirs de base ne permettent ni tempête, ni gel massif, ni effet temporel véritable.')
    content = content.replace('Les capacités majeures, les effets sur le temps et toute évolution doivent respecter le grimoire et la fiche validée.', 'Les pouvoirs doivent respecter le grimoire et la fiche validée.')
    return content.replace(' Les évolutions de pouvoirs suivent le grimoire.', '')


with transaction.atomic():
    changes = []
    for post in Post.objects.select_for_update().filter(topic__category__slug='scenarios-a-prendre', content__icontains='volution').select_related('topic'):
        updated = clean(post.content)
        if updated != post.content:
            base_before = re.findall(r'<p\b[^>]*>Base — [^<]*</p>', post.content)
            assert base_before == re.findall(r'<p\b[^>]*>Base — [^<]*</p>', updated)
            changes.append((post, updated))
    folder = Path(settings.BASE_DIR) / 'data/scenario_backups'
    folder.mkdir(parents=True, exist_ok=True)
    (folder / ('remove-evolutions-' + timezone.now().strftime('%Y%m%dT%H%M%S%f') + '.json')).write_text(json.dumps([dict(post_id=p.pk, content=p.content) for p, _ in changes], ensure_ascii=False), encoding='utf-8')
    for post, updated in changes:
        post.content = updated
        post.save(update_fields=['content', 'is_edited', 'updated_at'])
        post.refresh_from_db()
        assert post.content == updated
        print(post.topic.title + ' : évolutions retirées.')
    assert not Post.objects.filter(topic__category__slug='scenarios-a-prendre', content__regex=r'Évolution [12],').exists()
    print(str(len(changes)) + ' fiches mises à jour et vérifiées.')
