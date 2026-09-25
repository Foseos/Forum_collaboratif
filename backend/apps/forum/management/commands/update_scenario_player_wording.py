"""Uniformise la mention du joueur dans les scénarios déjà publiés."""

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.forum.models import Post


REPLACEMENTS = (
    ("des joueuses", "des joueurs"),
    ("les joueuses", "les joueurs"),
    ("aux joueuses", "aux joueurs"),
    ("leurs joueuses", "leurs joueurs"),
    ("sa joueuse", "son joueur"),
    ("la joueuse", "le joueur"),
    ("une joueuse", "un joueur"),
)


class Command(BaseCommand):
    help = "Remplace les formulations au féminin concernant les joueurs dans les fiches scénarios."

    def handle(self, *args, **options):
        changed = 0
        with transaction.atomic():
            posts = Post.objects.select_for_update().filter(topic__category__slug="scenarios-a-prendre")
            for post in posts:
                content = post.content
                for old, new in REPLACEMENTS:
                    content = content.replace(old, new)
                if content != post.content:
                    post.content = content
                    post.save(update_fields=["content"])
                    changed += 1
        self.stdout.write(self.style.SUCCESS(f"Fiches corrigées : {changed}"))
