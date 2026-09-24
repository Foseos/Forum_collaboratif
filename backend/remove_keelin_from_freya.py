import json
from pathlib import Path
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from apps.forum.models import Topic
REPLACE={
'Sa vie avec Keelin et leur enfant lui rappelle qu’elle mérite aussi du repos et des relations où elle n’est pas appelée seulement pour résoudre une crise.':'Sa vie auprès de son fils Nik lui rappelle qu’elle mérite aussi du repos et des relations où elle n’est pas appelée seulement pour résoudre une crise.',
'Sa relation avec Keelin devient une part essentielle de son avenir. Leur mariage et leur fils Nik lui donnent un foyer qui ne se limite pas à la fratrie. Elle doit consacrer à cette vie une présence réelle, et non les instants qui restent entre deux dangers.':'Son fils Nik occupe une place essentielle dans sa vie. Freya veut lui offrir un foyer qui ne se limite pas aux conflits de la fratrie. Elle doit consacrer à cette vie une présence réelle, et non les instants qui restent entre deux dangers. Sa situation amoureuse est au choix du joueur.'}
with transaction.atomic():
 t=Topic.objects.select_for_update().get(slug='freya-mikaelson',category__slug='scenarios-a-prendre')
 post=t.posts.select_for_update().order_by('created_at','pk').first()
 old=post.content;cards=t.scenario_link_cards
 folder=Path(settings.BASE_DIR)/'data/scenario_backups';folder.mkdir(parents=True,exist_ok=True)
 (folder/('freya-without-keelin-'+timezone.now().strftime('%Y%m%dT%H%M%S%f')+'.json')).write_text(json.dumps({'post_id':post.pk,'content':old,'topic_id':t.pk,'cards':cards},ensure_ascii=False),encoding='utf-8')
 content=old
 for before,after in REPLACE.items():
  assert before in content
  content=content.replace(before,after)
 updated=[c for c in cards if not c['title'].startswith('Keelin')]
 assert len(updated)==len(cards)-1
 assert 'keelin' not in (content+json.dumps(updated)).lower()
 post.content=content;post.save(update_fields=['content','is_edited','updated_at'])
 t.scenario_link_cards=updated;t.save(update_fields=['scenario_link_cards'])
 post.refresh_from_db();t.refresh_from_db()
 assert post.content==content and t.scenario_link_cards==updated
 print('Keelin retirée du texte et des liens de Freya ; Nik et les cinq autres liens conservés.')
