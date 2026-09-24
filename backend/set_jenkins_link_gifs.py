import json
from pathlib import Path
from urllib.request import Request, urlopen
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from apps.forum.models import Topic

GIFS = {
    'Billie Jenkins': 'https://media1.tenor.com/m/j6fvPWb2bgUAAAAd/billie-jenkins-charmed-billie.gif',
    'Christy Jenkins': 'https://media.tenor.com/woIQfcrj8jAAAAAM/christy-jenkins-pyrokinesis.gif',
    'Paige Matthews': 'https://zupimages.net/up/26/38/m4he.gif',
    'Piper Halliwell': 'https://zupimages.net/up/26/38/3fgr.gif',
    'Phoebe Halliwell': 'https://zupimages.net/up/26/38/zka2.gif',
}
for name, url in GIFS.items():
    with urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=30) as response:
        assert response.read(6) in (b'GIF87a', b'GIF89a'), name + ': image GIF non reçue'
    print(name + ' : GIF accessible.')

with transaction.atomic():
    topics = list(Topic.objects.select_for_update().filter(slug__in=['billie-jenkins','christie-jenkins'], category__slug='scenarios-a-prendre'))
    assert len(topics) == 2
    backup = [{'topic_id': t.pk, 'scenario_link_cards': t.scenario_link_cards} for t in topics]
    folder = Path(settings.BASE_DIR)/'data/scenario_backups'
    folder.mkdir(parents=True, exist_ok=True)
    (folder/('jenkins-gifs-'+timezone.now().strftime('%Y%m%dT%H%M%S%f')+'.json')).write_text(json.dumps(backup,ensure_ascii=False),encoding='utf-8')
    for topic in topics:
        cards = [dict(c) for c in topic.scenario_link_cards]
        assert len(cards) == 4
        for card in cards:
            matches = [url for name,url in GIFS.items() if card['title'].startswith(name)]
            assert len(matches) == 1
            card['gif'] = matches[0]
        topic.scenario_link_cards = cards
        topic.save(update_fields=['scenario_link_cards'])
        topic.refresh_from_db()
        assert topic.scenario_link_cards == cards
        print(topic.title + ' : quatre GIF enregistrés, textes conservés.')
