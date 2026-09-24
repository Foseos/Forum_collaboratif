import json
from pathlib import Path
from urllib.request import Request,urlopen
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from apps.forum.models import Topic
url='https://media.tenor.com/ZfPfiXgwQ1cAAAAM/niklaus-mikaelson-klaus.gif'
with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=30) as response:
    assert response.read(6) in (b'GIF87a',b'GIF89a')
card={'title':'Niklaus Mikaelson — Persécuteur de plusieurs siècles','gif':url,'text':'Tu voulais sacrifier mon sang de double pour briser ta malédiction. Je suis devenue vampire pour t’échapper, et tu as massacré ma famille en représailles. Pendant des siècles, la peur de te retrouver sur ma route a dicté mes départs, mes mensonges et mes alliances. Je refuse désormais que ma vie se résume à ta menace, mais je sais ce dont tu es capable. Le Nexus peut nous obliger à nous croiser ou à négocier ; il n’efface ni ma méfiance ni ce que tu m’as pris. Une trêve éventuelle devra se construire en jeu, sans pardon ni confiance imposés.'}
with transaction.atomic():
    t=Topic.objects.select_for_update().get(slug='katherine-pierce',category__slug='scenarios-a-prendre')
    original=t.scenario_link_cards
    assert not any(c['title'].startswith(('Niklaus','Klaus')) for c in original),'Un lien existe déjà : à relire avant modification.'
    folder=Path(settings.BASE_DIR)/'data/scenario_backups'
    folder.mkdir(parents=True,exist_ok=True)
    (folder/('katherine-niklaus-'+timezone.now().strftime('%Y%m%dT%H%M%S%f')+'.json')).write_text(json.dumps({'topic_id':t.pk,'scenario_link_cards':original},ensure_ascii=False),encoding='utf-8')
    cards=[dict(c) for c in original]+[card]
    t.scenario_link_cards=cards
    t.save(update_fields=['scenario_link_cards'])
    t.refresh_from_db()
    assert t.scenario_link_cards==cards and t.scenario_link_cards[:-1]==original
    print('Niklaus ajouté avec GIF accessible ; liens précédents conservés. Total :',len(cards))
