"""Remove the obsolete exclusive powers section from the live grimoire."""

import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from apps.forum.models import Topic


class Command(BaseCommand):
    help = "Supprime le bloc des pouvoirs exclusifs du Grimoire sans toucher aux autres sections."

    @transaction.atomic
    def handle(self, *args, **options):
        topic = Topic.objects.select_for_update().get(slug="liste-des-pouvoirs-magiques")
        post = topic.posts.select_for_update().order_by("created_at", "pk").first()
        if post is None:
            raise CommandError("Le Grimoire ne contient aucun message.")

        start_marker = "<!-- SECTION : POUVOIRS EXCLUSIFS"
        end_marker = "<!-- NOTE DE BAS DE PAGE -->"
        start = post.content.find(start_marker)
        if start < 0:
            self.stdout.write("Le bloc des pouvoirs exclusifs est déjà absent.")
            return
        end = post.content.find(end_marker, start)
        if end < 0:
            raise CommandError("Fin du bloc introuvable : aucune modification effectuée.")

        backup_dir = Path(settings.BASE_DIR) / "data" / "scenario_backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup_path = backup_dir / (
            "exclusive-powers-" + timezone.now().strftime("%Y%m%dT%H%M%S%f") + ".json"
        )
        backup_path.write_text(
            json.dumps({"topic_id": topic.pk, "post_id": post.pk, "content": post.content}, ensure_ascii=False),
            encoding="utf-8",
        )

        post.content = post.content[:start] + post.content[end:]
        post.save(update_fields=["content", "is_edited", "updated_at"])
        self.stdout.write(self.style.SUCCESS("Bloc des pouvoirs exclusifs supprimé du Grimoire."))
