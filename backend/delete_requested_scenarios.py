from pathlib import Path
from django.conf import settings
from django.core import serializers
from django.db import transaction
from django.db.models.deletion import Collector
from django.utils import timezone
from apps.forum.models import Topic

TARGETS = {
    89: 'antiana-harden', 88: 'violetviolette-mercury',
    90: 'darius-shane-alias-metus', 92: 'jada-rodrov',
    91: 'thea-oblivion-alias-calista', 94: 'aliyah-al-najjar',
    93: 'viggo-mordor-alias-nyxar', 95: 'vanille-castillo',
    98: 'selene-olyle-alias-medusa', 99: 'blanche-de-constantine',
    103: 'meredith-blossom', 104: 'stefan-reed',
    105: 'belisama-kinn', 106: 'harmony-moretti',
}

with transaction.atomic():
    topics = list(Topic.objects.select_for_update().filter(pk__in=TARGETS, category__slug='scenarios-a-prendre'))
    assert {t.pk: t.slug for t in topics} == TARGETS, 'Target mismatch; nothing deleted.'
    other_ids = set(Topic.objects.exclude(pk__in=TARGETS).values_list('pk', flat=True))
    collector = Collector(using='default')
    collector.collect(topics)
    objects = [obj for group in collector.data.values() for obj in group]
    objects.extend(obj for query in collector.fast_deletes for obj in query)
    folder = Path(settings.BASE_DIR) / 'data/deleted_scenario_backups'
    folder.mkdir(parents=True, exist_ok=True)
    backup = folder / ('requested-14-' + timezone.now().strftime('%Y%m%dT%H%M%S%f') + '.json')
    backup.write_text(serializers.serialize('json', objects), encoding='utf-8')
    print('Backup:', backup.name)
    print(Topic.objects.filter(pk__in=TARGETS, category__slug='scenarios-a-prendre').delete())
    assert not Topic.objects.filter(pk__in=TARGETS).exists()
    assert set(Topic.objects.values_list('pk', flat=True)) == other_ids
    print('14 scénarios supprimés ; autres sujets conservés et vérifiés.')
