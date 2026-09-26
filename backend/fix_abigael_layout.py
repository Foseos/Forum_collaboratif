import json
import re
from html.parser import HTMLParser
from pathlib import Path
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from apps.forum.models import Topic


class Text(HTMLParser):
    def __init__(self, content):
        super().__init__()
        self.parts = []
        self.feed(content)

    def handle_data(self, data):
        self.parts.append(data)


with transaction.atomic():
    topic = Topic.objects.select_for_update().get(slug='abigael-jameson-caine')
    post = topic.posts.select_for_update().order_by('created_at', 'pk').first()
    original = post.content
    content = original.replace('<p style="line-height:1.85;margin:0 0 .9rem;"</p>', '')
    content = re.sub(r'<p\b[^>]*>\s*</p>', '', content)
    content = content.replace('<header ', '<div ', 1).replace('</header>', '</div>', 1)
    content = content.replace('<figure style="margin:0;">', '<figure style="margin:0;max-width:100%;">')
    content = content.replace('<figcaption>', '<figcaption style="max-width:200px;font-size:.75rem;margin-top:.5rem;line-height:1.6;">')
    content = content.replace('<h1 style="color:#f5d76e;">', '<h1 style="color:#f5d76e;font-size:2rem;">')
    content = content.replace('<p style="line-height:1.85;margin:0 0 .9rem;">✦', '<p style="text-align:center;color:#a78bfa;font-size:.75rem;letter-spacing:.12em;">✦', 1)

    def section(match):
        title, body = match.groups()
        if title == 'I. Identité':
            fields = re.findall(r'<p\b[^>]*>(.*?)</p>', body, flags=re.S)
            assert len(fields) == 6
            rows = []
            for field in fields:
                label, value = field.split(' : ', 1)
                rows.append('<dt style="color:#a78bfa;font-size:.8rem;margin-top:.65rem;">' + label + '</dt><dd style="margin:.15rem 0 0;">' + value + '</dd>')
            body = '<dl style="margin:0;">' + ''.join(rows) + '</dl>'
        return '<section style="margin:1rem 0;border:1px solid rgba(124,58,237,.3);border-radius:8px;overflow:hidden;"><div style="padding:.65rem 1rem;background:rgba(124,58,237,.16);"><h2 style="margin:0;font-size:1rem;color:#c4b5fd;">' + title + '</h2></div><div style="padding:1rem;">' + body + '</div></section>'

    content, count = re.subn(r'<section\b[^>]*><h2\b[^>]*>(.*?)</h2>(.*?)</section>', section, content, flags=re.S)
    assert count == 5
    # Identity separators become layout; every other word must be retained.
    before = ''.join(Text(original).parts).replace(' : ', '')
    after = ''.join(Text(content).parts).replace(' : ', '')
    assert before == after, 'Unexpected text change'
    assert content.count('data-base-power="1"') == 4
    folder = Path(settings.BASE_DIR) / 'data/scenario_backups'
    folder.mkdir(parents=True, exist_ok=True)
    (folder / ('abigael-layout-' + timezone.now().strftime('%Y%m%dT%H%M%S%f') + '.json')).write_text(json.dumps({'post_id': post.pk, 'content': original, 'links': topic.scenario_link_cards}, ensure_ascii=False), encoding='utf-8')
    post.content = content
    post.save(update_fields=['content', 'is_edited', 'updated_at'])
    post.refresh_from_db()
    assert post.content == content
    print('Présentation harmonisée : 5 sections, texte et portrait conservés, balise défectueuse corrigée.')
