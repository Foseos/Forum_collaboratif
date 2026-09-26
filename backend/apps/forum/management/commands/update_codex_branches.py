"""Refresh the generated race directory while preserving the rules appended to it."""

import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from apps.forum.models import Topic
from expand_race_directory import render


def render_from_source():
    return render()


class Command(BaseCommand):
    help = "Actualise le bottin des créatures sans effacer les règles ajoutées après celui-ci."

    @transaction.atomic
    def handle(self, *args, **options):
        topic = Topic.objects.select_for_update().get(slug="encyclopedie-des-creatures-et-races")
        post = topic.posts.select_for_update().order_by("created_at", "pk").first()
        if post is None:
            raise CommandError("L'encyclopédie ne contient aucun message.")
        if not post.content.startswith('<div data-nexus-race-directory="1"'):
            raise CommandError("Le début du bottin est introuvable.")
        headings = ("Proposer une nouvelle branche", "Proposer une branche ou un profil")
        heading_position = next((post.content.find(value) for value in headings if value in post.content), -1)
        if heading_position < 0:
            raise CommandError("La fin du bottin est introuvable.")
        ending = "</section></div>"
        ending_position = post.content.find(ending, heading_position)
        if ending_position < 0:
            raise CommandError("La fin du bottin est introuvable.")
        suffix = post.content[ending_position + len(ending):]
        updated_content = render_from_source() + suffix
        updated_title = "Bottin des créatures et des profils"
        if updated_content == post.content and topic.title == updated_title:
            self.stdout.write("Le bottin est déjà à jour.")
            return

        backup_dir = Path(settings.BASE_DIR) / "data" / "scenario_backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup_path = backup_dir / ("codex-branches-" + timezone.now().strftime("%Y%m%dT%H%M%S%f") + ".json")
        backup_path.write_text(json.dumps({
            "topic_id": topic.pk, "title": topic.title, "post_id": post.pk,
            "content": post.content,
        }, ensure_ascii=False), encoding="utf-8")
        post.content = updated_content
        post.save(update_fields=["content", "is_edited", "updated_at"])
        topic.title = updated_title
        topic.save(update_fields=["title"])
        self.stdout.write(self.style.SUCCESS("Bottin actualisé ; règles complémentaires conservées."))
