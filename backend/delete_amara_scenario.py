from pathlib import Path
from django.conf import settings
from django.core import serializers
from django.db import transaction
from django.db.models.deletion import Collector
from django.utils import timezone
from apps.forum.models import Topic
with transaction.atomic():
    topic=Topic.objects.select_for_update().get(slug='amara-asteri',category__slug='scenarios-a-prendre')
    assert topic.title.casefold().startswith('amara'), 'Titre inattendu'
    title=topic.title
    pk=topic.pk
    collector=Collector(using='default')
    collector.collect([topic])
    objects=[obj for group in collector.data.values() for obj in group]
    objects.extend(obj for query in collector.fast_deletes for obj in query)
    folder=Path(settings.BASE_DIR)/'data/deleted_scenario_backups'
    folder.mkdir(parents=True,exist_ok=True)
    backup=folder/('amara-'+timezone.now().strftime('%Y%m%dT%H%M%S%f')+'.json')
    backup.write_text(serializers.serialize('json',objects),encoding='utf-8')
    print('Sauvegarde :',backup.name)
    print(topic.delete())
    assert not Topic.objects.filter(pk=pk).exists()
    print(title+' : scénario supprimé et absence vérifiée.')
