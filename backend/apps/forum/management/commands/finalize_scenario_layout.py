"""Tidy the creation note and credits on the completed scenario sheets."""

import json
import re
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.forum.models import Topic


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        topics = Topic.objects.select_for_update().filter(category__slug="scenarios-a-prendre")
        changes = []
        for topic in topics:
            post = topic.posts.select_for_update().order_by("created_at", "pk").first()
            if not post or 'data-completed-scenario="1"' not in post.content:
                continue
            content = post.content
            marker = '<section style="margin:1rem 0;padding:1rem;border:1px solid #574477;border-radius:8px;"><h2 style="font-size:1.1rem;color:#c4b5fd;">Capacités à la création</h2>'
            if marker not in content:
                raise ValueError("Note de création absente : " + topic.slug)
            content = content.replace('</p></div>' + marker, '</p>' + marker, 1)
            if not content.endswith('</section>'):
                raise ValueError("Fin de fiche inattendue : " + topic.slug)
            content += '</div>'
            content = re.sub(r'Crédits :\s+avatar, images, GIFs et ressources à renseigner\.', "Crédits : auteur de l'avatar non indiqué dans la fiche d'origine.", content)
            changes.append((post, content))
        backup_dir = Path(settings.BASE_DIR) / "data" / "scenario_backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        (backup_dir / ("scenario-layout-" + timezone.now().strftime("%Y%m%dT%H%M%S%f") + ".json")).write_text(
            json.dumps([{"post_id": post.pk, "content": post.content} for post, _ in changes], ensure_ascii=False), encoding="utf-8"
        )
        for post, content in changes:
            post.content = content
            post.save(update_fields=["content", "is_edited", "updated_at"])
        self.stdout.write(self.style.SUCCESS(f"Mise en page finalisée pour {len(changes)} scénarios."))
