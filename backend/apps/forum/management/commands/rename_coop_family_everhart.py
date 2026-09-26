"""Renomme Coop et ses filles Everhart dans les scénarios publiés."""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.forum.models import Post, Topic


class Command(BaseCommand):
    help = "Remplace Swann par Everhart dans les fiches, les liens et l'URL de Coop."

    def handle(self, *args, **options):
        with transaction.atomic():
            coop = Topic.objects.select_for_update().filter(slug="coop-swann").first()
            if coop and Topic.objects.filter(slug="coop-everhart").exclude(pk=coop.pk).exists():
                raise CommandError("L'adresse coop-everhart est déjà utilisée.")
            if not coop:
                coop = Topic.objects.select_for_update().filter(slug="coop-everhart").first()
            if not coop:
                raise CommandError("Le scénario de Coop est introuvable.")

            updated_posts = 0
            for post in Post.objects.select_for_update().filter(content__icontains="Swann"):
                content = post.content.replace("Swann", "Everhart")
                if content != post.content:
                    post.content = content
                    post.save(update_fields=["content"])
                    updated_posts += 1

            updated_links = 0
            for topic in Topic.objects.select_for_update().filter(category__slug="scenarios-a-prendre"):
                cards = topic.scenario_link_cards or []
                changed = False
                for card in cards:
                    for key in ("title", "text"):
                        value = card.get(key)
                        if isinstance(value, str) and "Swann" in value:
                            card[key] = value.replace("Swann", "Everhart")
                            changed = True
                if changed:
                    topic.scenario_link_cards = cards
                    topic.save(update_fields=["scenario_link_cards"])
                    updated_links += 1

            coop.title = "Coop Everhart"
            coop.slug = "coop-everhart"
            coop.save(update_fields=["title", "slug"])

        self.stdout.write(self.style.SUCCESS(
            f"Famille Everhart mise à jour : {updated_posts} fiches, {updated_links} ensembles de liens."
        ))
