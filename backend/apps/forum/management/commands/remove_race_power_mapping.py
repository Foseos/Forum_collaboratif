"""Retire la liste qui attribue des pouvoirs aux races dans le grimoire publié."""

import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from apps.forum.models import Topic
from .expand_grimoire import DIRECTORY_MARKER, POWER_DIRECTORY


class Command(BaseCommand):
    help = "Retire les affinités par race du bottin des pouvoirs, sans modifier l'encyclopédie."

    @transaction.atomic
    def handle(self, *args, **options):
        topic = Topic.objects.select_for_update().get(slug="liste-des-pouvoirs-magiques")
        post = topic.posts.select_for_update().order_by("created_at", "pk").first()
        if post is None:
            raise CommandError("Le bottin des pouvoirs ne contient aucun message.")

        content = post.content
        heading = "XVI. Affinités et limites selon les races"
        updated = content
        if heading in content:
            heading_at = content.index(heading)
            start_marker = '\n<div style="margin:1.4rem 0; border:1px solid rgba(244,114,182,0.28)'
            start = content.rfind(start_marker, 0, heading_at)
            end_marker = '</div><section data-power-progression="creation-max-4"'
            end = content.find(end_marker, heading_at)
            if start < 0 or end < 0 or content[start:heading_at].count("<h2") != 1:
                raise CommandError("Structure inattendue : le bottin n'a pas été modifié.")
            end += len("</div>")
            updated = content[:start] + content[end:]

        updated = updated.replace(
            "Un personnage possède les dons liés à sa race et à son histoire, jamais l'intégralité des capacités de sa lignée.",
            "Ce catalogue présente des possibilités, jamais des dons automatiquement acquis.",
        )
        updated = updated.replace(
            "Copie de pouvoirs ★ · Métamorphose de masse ★",
            "Métamorphose de masse ★",
        )
        updated = updated.replace(">Contrôle végétal</td>", ">Phytokinésie (contrôle végétal)</td>")
        updated = updated.replace(">Contrôle de l'eau</td>", ">Aquakinésie (contrôle de l'eau)</td>")
        directory_start = updated.find(DIRECTORY_MARKER)
        if directory_start >= 0:
            progression_start = updated.find('<section data-power-progression="creation-max-4"', directory_start)
            if progression_start < 0:
                raise CommandError("Fin du répertoire introuvable : le bottin n'a pas été modifié.")
            updated = updated[:directory_start] + POWER_DIRECTORY + updated[progression_start:]
        if updated == content:
            self.stdout.write("La liste par race est déjà absente du bottin.")
            return

        backup_dir = Path(settings.BASE_DIR) / "data" / "scenario_backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup_path = backup_dir / ("grimoire-races-" + timezone.now().strftime("%Y%m%dT%H%M%S%f") + ".json")
        backup_path.write_text(json.dumps({"topic_id": topic.pk, "post_id": post.pk, "content": content}, ensure_ascii=False), encoding="utf-8")

        post.content = updated
        post.save(update_fields=["content", "is_edited", "updated_at"])
        self.stdout.write(self.style.SUCCESS("Liste des pouvoirs par race retirée du bottin."))
