"""Applique aux scénarios publiés les corrections relevées dans l'audit."""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.forum.models import Topic


SLUGS = (
    "valerie-tulle",
    "selene-beauchamp",
    "belisama-vaskov",
    "moira-osborne",
    "florie-delacroix",
    "melissandre-barden",
)


class Command(BaseCommand):
    help = "Corrige l'âge de Sélène et les coquilles des scénarios TVD publiés."

    def handle(self, *args, **options):
        changed = []
        with transaction.atomic():
            for slug in SLUGS:
                topic = Topic.objects.select_for_update().filter(
                    category__slug="scenarios-a-prendre", slug=slug
                ).first()
                if not topic:
                    raise CommandError(f"Scénario introuvable : {slug}")
                post = topic.posts.select_for_update().order_by("id").first()
                if not post:
                    raise CommandError(f"Fiche sans message : {slug}")

                content = post.content.replace("Au choix de le joueur", "Au choix du joueur")
                if slug == "selene-beauchamp":
                    content = content.replace("46 ans en 2033", "50 ans en 2033")
                if slug == "moira-osborne":
                    content = content.replace("TUMBR", "Tumblr")
                if content != post.content:
                    post.content = content
                    post.save(update_fields=["content"])
                    changed.append(slug)

        self.stdout.write(self.style.SUCCESS(f"Scénarios corrigés : {', '.join(changed) or 'aucun'}"))
