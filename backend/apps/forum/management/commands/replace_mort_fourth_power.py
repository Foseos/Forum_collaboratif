"""Replace Mort's fourth faculty in the published faction guide."""

from html import escape

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.forum.models import Topic
from faction_role_powers import FACTION_ROLES


class Command(BaseCommand):
    help = "Remplace la quatrième faculté du Cavalier de la Mort."

    @transaction.atomic
    def handle(self, *args, **options):
        post = Topic.objects.get(slug="guide-des-factions-et-alliances").posts.order_by("created_at").first()
        if post is None:
            raise ValueError("Guide des factions sans texte.")
        old_name = "Traversée du Voile"
        old_description = (
            "Prend une forme spectrale pendant un tour de RP pour franchir un obstacle physique proche. "
            "Dans cet état, le Cavalier ne peut ni attaquer ni agir sur les vivants ; "
            "les protections magiques et les sceaux restent efficaces."
        )
        power = next(role for role in FACTION_ROLES["Les cavaliers de l'apocalypse"] if role["name"] == "Mort")["powers"][3]
        old = f"<strong style='color:#e2d9f3;'>{escape(old_name)}</strong> — {escape(old_description)}"
        new = f"<strong style='color:#e2d9f3;'>{escape(power['name'])}</strong> — {escape(power['description'])}"
        if new not in post.content:
            if post.content.count(old) != 1:
                raise ValueError("Ancienne faculté introuvable ou ambiguë.")
            post.content = post.content.replace(old, new, 1)
            post.save(update_fields=["content"])
        self.stdout.write(self.style.SUCCESS("Faculté de Mort actualisée."))
