"""Publish the faction guide without touching the other rules topics."""

import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from apps.forum.management.commands.seed_reglement_topics import CONTENT_FACTIONS
from apps.forum.models import Topic


class Command(BaseCommand):
    help = "Met à jour le guide des factions et alliances."

    @transaction.atomic
    def handle(self, *args, **options):
        topic = Topic.objects.select_for_update().get(slug="guide-des-factions-et-alliances")
        post = topic.posts.select_for_update().order_by("created_at", "pk").first()
        if not post:
            raise CommandError("La fiche Factions et alliances est introuvable.")
        if post.content == CONTENT_FACTIONS:
            self.stdout.write("Le guide est déjà à jour.")
            return
        backup_dir = Path(settings.BASE_DIR) / "data" / "scenario_backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        (backup_dir / ("factions-guide-" + timezone.now().strftime("%Y%m%dT%H%M%S%f") + ".json")).write_text(
            json.dumps({"topic_id": topic.pk, "post_id": post.pk, "content": post.content}, ensure_ascii=False), encoding="utf-8"
        )
        post.content = CONTENT_FACTIONS
        post.save(update_fields=["content", "is_edited", "updated_at"])
        self.stdout.write(self.style.SUCCESS("Guide Factions et alliances mis à jour."))
