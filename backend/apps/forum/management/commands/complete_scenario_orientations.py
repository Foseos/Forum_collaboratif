"""Ajoute l'orientation sexuelle aux scénarios qui n'ont pas encore ce champ."""

import json
import re
from html import escape
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from apps.forum.models import Topic


DEFAULT = "Au choix du joueur, dans le respect des liens déjà établis"
ORIENTATIONS = {
    "abigael-jameson-caine": DEFAULT,
    "briseis-argent": DEFAULT,
    "chris-argent": DEFAULT,
    "isaac-lahey": DEFAULT,
    "isabella-montana": DEFAULT,
    "jackson-whittemore": (
        "Attirance pour les hommes établie avec Ethan ; relation passée avec Lydia. "
        "L'étiquette choisie par le joueur respecte ces deux liens."
    ),
    "jordan-parrish": DEFAULT,
    "kate-argent": DEFAULT,
    "kira-yukimura": DEFAULT,
    "liam-dunbar": DEFAULT,
    "malia-tate": DEFAULT,
    "nymea-argent": DEFAULT,
    "parker-caine": DEFAULT,
    "vivienne-montana": DEFAULT,
    "waverly-jameson": DEFAULT,
}

DL_FIELD = re.compile(
    r'(<dt\b[^>]*>)Vie sentimentale(</dt>\s*<dd\b[^>]*>)(.*?)(</dd>)',
    re.IGNORECASE | re.DOTALL,
)
PARAGRAPH_FIELD = re.compile(
    r'(<p\b[^>]*>)Vie sentimentale\s*:\s*(.*?)(</p>)',
    re.IGNORECASE | re.DOTALL,
)


def add_orientation(content, value):
    if "orientation sexuelle" in content.casefold():
        return content
    matches = list(DL_FIELD.finditer(content))
    if len(matches) == 1:
        match = matches[0]
        new_field = (
            match.group(1) + "Orientation sexuelle" + match.group(2)
            + escape(value) + match.group(4)
        )
    else:
        matches = list(PARAGRAPH_FIELD.finditer(content))
        if len(matches) != 1:
            raise ValueError("Rubrique « Vie sentimentale » absente ou ambiguë.")
        match = matches[0]
        new_field = match.group(1) + "Orientation sexuelle : " + escape(value) + match.group(3)
    return content[:match.start()] + new_field + content[match.start():]


class Command(BaseCommand):
    help = "Complète les orientations manquantes des scénarios sans modifier les autres champs."

    def handle(self, *args, **options):
        with transaction.atomic():
            topics = list(Topic.objects.select_for_update().filter(category__slug="scenarios-a-prendre"))
            changes = []
            for topic in topics:
                post = topic.posts.select_for_update().order_by("created_at", "id").first()
                if post is None:
                    raise CommandError(f"Fiche sans message : {topic.title}")
                if "orientation sexuelle" in post.content.casefold():
                    continue
                value = ORIENTATIONS.get(topic.slug)
                if value is None:
                    raise CommandError(f"Orientation à définir pour : {topic.title}")
                try:
                    content = add_orientation(post.content, value)
                except ValueError as exc:
                    raise CommandError(f"{topic.title} : {exc}") from exc
                changes.append((post, content))

            if changes:
                backup_dir = Path(settings.BASE_DIR) / "data" / "scenario_backups"
                backup_dir.mkdir(parents=True, exist_ok=True)
                backup_file = backup_dir / (
                    "scenario-orientations-" + timezone.now().strftime("%Y%m%dT%H%M%S%f") + ".json"
                )
                backup_file.write_text(
                    json.dumps([{"post_id": post.pk, "content": post.content} for post, _ in changes], ensure_ascii=False),
                    encoding="utf-8",
                )
                for post, content in changes:
                    post.content = content
                    post.save(update_fields=["content", "is_edited", "updated_at"])
            self.stdout.write(self.style.SUCCESS(f"{len(changes)} fiches complétées."))
