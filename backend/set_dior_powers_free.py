import json
import re
from pathlib import Path
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from apps.forum.models import Topic

with transaction.atomic():
    topic = Topic.objects.get(slug='dior-montana', category__slug='scenarios-a-prendre')
    post = topic.posts.select_for_update().order_by('created_at', 'pk').first()
    original = post.content
    content, count = re.subn(r'<div data-base-power="1">.*?</div>', '', original, flags=re.S)
    assert count == 4
    heading = 'II. Pouvoirs de base</h2></div><div style="padding:1rem;">'
    assert heading in content
    content = content.replace(heading, heading + '<p style="margin:0 0 .9rem;line-height:1.85;"><strong>Les quatre pouvoirs de base de Dior sont au choix du joueur</strong>, en cohérence avec sa nature de sorcière, le grimoire et la validation du staff.</p>', 1)
    content = content.replace('avec les quatre pouvoirs de base décrits ici.', 'avec quatre pouvoirs de base au choix du joueur.')
    content = content.replace('Les quatre dons décrits restent des pouvoirs de départ aux effets limités', 'Les quatre dons choisis restent des pouvoirs de départ aux effets limités')
    folder = Path(settings.BASE_DIR) / 'data/scenario_backups'
    folder.mkdir(parents=True, exist_ok=True)
    (folder / ('dior-free-powers-' + timezone.now().strftime('%Y%m%dT%H%M%S%f') + '.json')).write_text(json.dumps({'post_id': post.pk, 'content': original}, ensure_ascii=False), encoding='utf-8')
    post.content = content
    post.save(update_fields=['content', 'is_edited', 'updated_at'])
    post.refresh_from_db()
    assert post.content == content
    print('Dior : quatre pouvoirs au choix, descriptions imposées retirées et références harmonisées.')
