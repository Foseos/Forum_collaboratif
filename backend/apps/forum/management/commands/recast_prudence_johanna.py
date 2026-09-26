"""Attribue Emma Watson à Prudence Johanna et actualise les liens visuels."""

import re

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.forum.models import Topic


PORTRAIT = "https://upload.wikimedia.org/wikipedia/commons/f/f9/Emma_Watson_ONU_2017.jpg"
LINK_GIF = "https://media1.tenor.com/m/Rx-rtspGFXoAAAAd/emma-watson.gif"
PHOTO_SOURCE = "https://commons.wikimedia.org/wiki/File:Emma_Watson_ONU_2017.jpg"
OLD_PORTRAIT = "https://zupimages.net/up/26/39/yqne.png"
PREVIOUS_PORTRAIT = "https://upload.wikimedia.org/wikipedia/commons/2/2e/Emma_Watson_2017_%28cropped%29.jpg"


class Command(BaseCommand):
    help = "Actualise la fiche et le bottin de Prudence Johanna avec Emma Watson."

    def handle(self, *args, **options):
        with transaction.atomic():
            topic = Topic.objects.select_for_update().filter(slug="prudence-johanna-halliwell").first()
            if not topic:
                raise CommandError("Le scénario de Prudence Johanna est introuvable.")
            post = topic.posts.select_for_update().order_by("id").first()
            if not post:
                raise CommandError("La fiche de Prudence Johanna est introuvable.")

            content = post.content.replace(OLD_PORTRAIT, PORTRAIT).replace(PREVIOUS_PORTRAIT, PORTRAIT)
            content = re.sub(
                r'(<img\s+src=")[^"]+(")',
                lambda match: f"{match.group(1)}{PORTRAIT}{match.group(2)}",
                content,
                count=1,
                flags=re.IGNORECASE,
            )
            content = content.replace('alt="Prénom NOM"', 'alt="Prudence Johanna Halliwell, incarnée par Emma Watson"')
            content = content.replace("Ft Kristen Stewart", "Ft Emma Watson")
            content = content.replace(
                "Prettyvacantavatars - TUMBLR",
                "Photo principale : ONU Brasil / Wikimedia Commons (CC BY 3.0)",
            )
            content = content.replace(
                'Photo : FR / Wikimedia Commons, CC BY-SA 4.0',
                'Photo : ONU Brasil / Wikimedia Commons, CC BY 3.0',
            )
            content = content.replace(
                'https://commons.wikimedia.org/wiki/File:Emma_Watson_2017_(cropped).jpg',
                PHOTO_SOURCE,
            )
            credit = (
                f' <a href="{PHOTO_SOURCE}" target="_blank" rel="noopener noreferrer" '
                'style="color:#c4b5fd;">Photo : ONU Brasil / Wikimedia Commons, CC BY 3.0</a>.'
            )
            marker = "Ft Emma Watson (négociable - échange avec le staff)</p>"
            if marker in content:
                content = content.replace(marker, f"Ft Emma Watson (négociable - échange avec le staff).{credit}</p>")
            if content != post.content:
                post.content = content
                post.save(update_fields=["content"])

            if topic.scenario_avatar_name != "Emma Watson":
                topic.scenario_avatar_name = "Emma Watson"
                topic.save(update_fields=["scenario_avatar_name"])

            linked = 0
            for related in Topic.objects.select_for_update().filter(category__slug="scenarios-a-prendre"):
                cards = related.scenario_link_cards or []
                changed = False
                for card in cards:
                    title = card.get("title", "")
                    if ("Prudence Johanna" in title or "P.J Halliwell" in title) and card.get("gif") != LINK_GIF:
                        card["gif"] = LINK_GIF
                        changed = True
                if changed:
                    related.scenario_link_cards = cards
                    related.save(update_fields=["scenario_link_cards"])
                    linked += 1

        self.stdout.write(self.style.SUCCESS(f"Prudence Johanna : Emma Watson ; {linked} fiches liées actualisées."))
