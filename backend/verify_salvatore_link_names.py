import json
from pathlib import Path
from django.db import transaction
from apps.forum.models import Topic
items=json.loads(Path('salvatore_scenario_data.json').read_text(encoding='utf-8-sig'))
with transaction.atomic():
 for d in items:
  t=Topic.objects.select_for_update().get(slug=d['slug'])
  cards=[dict(c) for c in t.scenario_link_cards]
  assert len(cards)==len(d['links'])
  for c,(name,label,body) in zip(cards,d['links']):
   assert c['title']==label and c['text']==body
   c['title']=name+' — '+label
  t.scenario_link_cards=cards;t.save(update_fields=['scenario_link_cards'])
  t.refresh_from_db();assert t.scenario_link_cards==cards
  print(t.title+': noms des cinq relations vérifiés.')
