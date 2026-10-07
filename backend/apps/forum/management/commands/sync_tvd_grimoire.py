"""Publie les évolutions TVD sans réécrire le reste du grimoire."""

import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from apps.forum.models import Topic
from .expand_grimoire import (
    DIRECTORY_MARKER, TVD_DIRECTORY, TVD_DIRECTORY_END, TVD_DIRECTORY_MARKER,
)


class Command(BaseCommand):
    help = "Synchronise les pouvoirs et évolutions TVD avec le grimoire publié."

    def handle(self, *args, **options):
        with transaction.atomic():
            topic = Topic.objects.filter(slug="liste-des-pouvoirs-magiques").first()
            if topic is None:
                raise CommandError("Sujet du grimoire introuvable.")
            post = topic.posts.select_for_update().order_by("created_at", "pk").first()
            if post is None:
                raise CommandError("Le grimoire ne contient aucun message.")

            content = post.content
            if DIRECTORY_MARKER not in content:
                raise CommandError("Répertoire détaillé introuvable ; aucune modification effectuée.")
            if TVD_DIRECTORY_MARKER in content:
                before, _, rest = content.partition(TVD_DIRECTORY_MARKER)
                if TVD_DIRECTORY_END not in rest:
                    raise CommandError("Fin de la section TVD introuvable ; aucune modification effectuée.")
                _, _, after = rest.partition(TVD_DIRECTORY_END)
                updated = before + TVD_DIRECTORY + after
            else:
                anchor = '<section data-power-progression="creation-max-4"'
                position = content.find(anchor, content.find(DIRECTORY_MARKER))
                if position < 0:
                    position = content.rfind("</div></div>")
                if position < content.find(DIRECTORY_MARKER):
                    raise CommandError("Fin du répertoire introuvable ; aucune modification effectuée.")
                updated = content[:position] + TVD_DIRECTORY + content[position:]

            if updated == content:
                self.stdout.write("La section TVD est déjà à jour.")
                return

            backup_dir = Path(settings.BASE_DIR) / "data" / "scenario_backups"
            backup_dir.mkdir(parents=True, exist_ok=True)
            backup_path = backup_dir / ("grimoire-tvd-" + timezone.now().strftime("%Y%m%dT%H%M%S%f") + ".json")
            backup_path.write_text(json.dumps({"topic_id": topic.pk, "post_id": post.pk, "content": content}, ensure_ascii=False), encoding="utf-8")
            post.content = updated
            post.save(update_fields=["content", "is_edited", "updated_at"])
            self.stdout.write(self.style.SUCCESS("Évolutions TVD publiées dans le grimoire."))
