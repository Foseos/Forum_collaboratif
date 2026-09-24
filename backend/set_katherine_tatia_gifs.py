import ast,json
from pathlib import Path
from urllib.request import Request,urlopen
from concurrent.futures import ThreadPoolExecutor
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from apps.forum.models import Topic
module=ast.parse(Path('update_elena_link_gifs.py').read_text(encoding='utf-8-sig'))
GIFS=next(ast.literal_eval(n.value) for n in module.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='GIFS' for t in n.targets))
GIFS.update({'Elena Gilbert Salvatore':'https://media1.tenor.com/m/TraCAjZMch8AAAAC/elena-gilbert.gif','Elijah Mikaelson':'https://media1.tenor.com/m/ukDD2pxS79kAAAAC/elijah-mikaelson-elijah.gif','Niklaus Mikaelson':'https://media.tenor.com/ZfPfiXgwQ1cAAAAM/niklaus-mikaelson-klaus.gif'})
names=['Elena Gilbert Salvatore','Stefan Salvatore','Damon Salvatore','Tatia Petrova','Katherine Pierce','Elijah Mikaelson','Niklaus Mikaelson']
def verify(name):
 with urlopen(Request(GIFS[name],headers={'User-Agent':'Mozilla/5.0'}),timeout=30) as response:
  assert response.read(6) in (b'GIF87a',b'GIF89a'),name
 return name
print('GIFs accessibles : '+', '.join(ThreadPoolExecutor(7).map(verify,names)))
with transaction.atomic():
 topics=list(Topic.objects.select_for_update().filter(slug__in=['katherine-pierce','tatia-petrova'],category__slug='scenarios-a-prendre'))
 assert len(topics)==2
 folder=Path(settings.BASE_DIR)/'data/scenario_backups';folder.mkdir(parents=True,exist_ok=True)
 (folder/('katherine-tatia-gifs-'+timezone.now().strftime('%Y%m%dT%H%M%S%f')+'.json')).write_text(json.dumps([{'topic_id':t.pk,'scenario_link_cards':t.scenario_link_cards} for t in topics],ensure_ascii=False),encoding='utf-8')
 for t in topics:
  original=t.scenario_link_cards
  cards=[dict(c) for c in original]
  assert len(cards)==4
  for card in cards:
   matches=[url for name,url in GIFS.items() if card['title'].startswith(name)]
   assert len(matches)==1,card['title']
   card['gif']=matches[0]
  assert all(a['title']==b['title'] and a['text']==b['text'] for a,b in zip(original,cards))
  t.scenario_link_cards=cards;t.save(update_fields=['scenario_link_cards'])
  t.refresh_from_db();assert t.scenario_link_cards==cards
  print(t.title+' : quatre liens avec GIFs enregistrés, textes conservés.')
