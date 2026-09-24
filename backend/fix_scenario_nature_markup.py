import json
import re
from html.parser import HTMLParser
from pathlib import Path
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from apps.forum.models import Topic

BROKEN = re.compile(r'(<p\s+style="[^"]*")([^<>]+)(</p>)')

class VisibleText(HTMLParser):
    def __init__(self, content):
        super().__init__()
        self.text=[]
        self.feed(content)
    def handle_data(self,data):
        self.text.append(data)

with transaction.atomic():
    changes=[]
    for topic in Topic.objects.filter(category__slug='scenarios-a-prendre'):
        post=topic.posts.select_for_update().order_by('created_at','pk').first()
        if not post:
            continue
        matches=list(BROKEN.finditer(post.content))
        if not matches:
            continue
        original=post.content
        updated=BROKEN.sub(r'\1>\2\3',original)
        updated=re.sub(r'^\s*<<div\b','<div',updated,count=1)
        # Remove the duplicated cell closure from this copied header only.
        updated=re.sub(r'</td>\s*</td>(\s*<td\b)',r'</td>\1',updated,count=1)
        visible=''.join(VisibleText(updated).text)
        assert all(m.group(2).strip() in visible for m in matches)
        assert re.findall(r'<img\b[^>]*>',original)==re.findall(r'<img\b[^>]*>',updated)
        assert not BROKEN.search(updated)
        changes.append((topic,post,original,updated))
    folder=Path(settings.BASE_DIR)/'data/scenario_backups'
    folder.mkdir(parents=True,exist_ok=True)
    (folder/('nature-markup-'+timezone.now().strftime('%Y%m%dT%H%M%S%f')+'.json')).write_text(json.dumps([dict(topic_id=t.pk,post_id=p.pk,content=old) for t,p,old,new in changes],ensure_ascii=False),encoding='utf-8')
    for topic,post,old,new in changes:
        post.content=new
        post.save(update_fields=['content','is_edited','updated_at'])
        post.refresh_from_db()
        assert post.content==new
        print(topic.title+' : nature visible.')
    print(str(len(changes))+' fiches corrigées et vérifiées.')
