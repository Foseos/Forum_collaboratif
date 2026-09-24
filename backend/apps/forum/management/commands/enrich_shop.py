import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from apps.forum.models import Post, Topic
from apps.forum.shop_details import ITEM_DETAILS, enrich_catalogue


class Command(BaseCommand):
    help = 'Enrichit les objets existants sans changer leurs prix ni les commandes.'

    def add_arguments(self, parser):
        parser.add_argument('--apply', action='store_true')

    @transaction.atomic
    def handle(self, *args, **options):
        topic = Topic.objects.get(slug='catalogue-boutique-magique')
        post = Post.objects.select_for_update().filter(topic=topic).order_by('created_at', 'pk').first()
        if not post:
            raise CommandError('Catalogue introuvable.')
        updated, found = enrich_catalogue(post.content)
        missing = set(ITEM_DETAILS) - set(found)
        if missing or len(found) != len(set(found)):
            raise CommandError(f'Catalogue inattendu. Objets absents : {sorted(missing)}')
        if updated == post.content:
            self.stdout.write('Catalogue déjà enrichi : aucune modification.')
            return
        if options['apply']:
            backup_dir = Path(settings.BASE_DIR) / 'data' / 'boutique_backups'
            backup_dir.mkdir(parents=True, exist_ok=True)
            backup_path = backup_dir / (timezone.now().strftime('%Y%m%dT%H%M%S%f') + '.json')
            backup_path.write_text(json.dumps({'post_id': post.pk, 'content': post.content}, ensure_ascii=False), encoding='utf-8')
            post.content = updated
            post.save(update_fields=['content', 'updated_at', 'is_edited'])
            post.refresh_from_db()
            if post.content != updated:
                raise CommandError('Échec de la vérification après enregistrement.')
        self.stdout.write(f'{len(found)} objets : ' + ('enrichis et vérifiés.' if options['apply'] else 'prêts à enrichir.'))
