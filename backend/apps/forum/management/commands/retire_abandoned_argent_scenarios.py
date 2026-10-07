"""Retire two abandoned scenario topics while keeping a local recovery copy."""

from pathlib import Path

from django.conf import settings
from django.core import serializers
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.forum.models import Topic


SLUGS = ('nymea-argent', 'briseis-argent')


class Command(BaseCommand):
    help = 'Retire les scénarios abandonnés Nyméa et Briséis Argent.'

    def handle(self, *args, **options):
        with transaction.atomic():
            topics = list(
                Topic.objects.select_for_update()
                .filter(slug__in=SLUGS, category__slug='scenarios-a-prendre')
                .order_by('pk')
            )
            if not topics:
                self.stdout.write('Ces deux scénarios sont déjà retirés.')
                return

            posts = [post for topic in topics for post in topic.posts.order_by('pk')]
            backup_dir = Path(settings.BASE_DIR) / 'data' / 'scenario_backups'
            backup_dir.mkdir(parents=True, exist_ok=True)
            backup_path = backup_dir / (
                'retired-argent-scenarios-'
                + timezone.now().strftime('%Y%m%dT%H%M%S%f')
                + '.json'
            )
            backup_path.write_text(
                serializers.serialize('json', [*topics, *posts], indent=2),
                encoding='utf-8',
            )
            for topic in topics:
                topic.delete()
            self.stdout.write(self.style.SUCCESS(
                f'{len(topics)} scénarios retirés ; copie locale : {backup_path}'
            ))
