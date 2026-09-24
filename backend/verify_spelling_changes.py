import json
import re
from pathlib import Path
from django.apps import apps

count = 0
for file in Path('data/spelling_backups').glob('*.json'):
    for row in json.loads(file.read_text(encoding='utf-8')):
        obj = apps.get_model(row['model']).objects.get(pk=row['pk'])
        for field, old in row['fields'].items():
            current = getattr(obj, field)
            if field == 'content':
                assert re.findall(r'<[^>]*>', old) == re.findall(r'<[^>]*>', current)
            if field == 'scenario_link_cards':
                assert [c.get('gif') for c in old] == [c.get('gif') for c in current]
        count += 1
print(count, 'vérifications : balisage et images conservés.')
