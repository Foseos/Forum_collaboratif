"""Harmonise les passages de Prudence sur Jensen et corrige Coop."""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.forum.models import Topic


OLD_JENSEN_PASSAGE = (
    "Elle n’a aucun a priori sur Jensen : \n"
    "- elle accepte naturellement sa nature\n"
    "- mais doit apprendre à lui laisser une vraie place"
)
NEW_JENSEN_PASSAGE = (
    "Prudence ne juge pas Jensen sur sa nature et reconnaît sa place dans la famille. "
    "Son arrivée bouscule pourtant le rôle d’aînée qu’elle occupait depuis des années. "
    "Elle apprend progressivement à partager cette place avec lui, sans renoncer à leur construire un lien."
)
OLD_JENSEN_LINK = (
    "J’ai du mal à accepter mon grand frère Jensen, car cela veut dire que je dois lui céder "
    "ma place d'aînée, que j’ai tenue pendant de nombreuses années. J'apprends à le connaître, "
    "même si je n'ai pas d'a priori à son sujet."
)
NEW_JENSEN_LINK = (
    "L’arrivée de mon grand frère Jensen bouscule la place d’aînée que j’ai occupée pendant des années. "
    "Je ne juge pas sa nature, mais j’ai besoin de temps pour partager ce rôle et apprendre à le connaître."
)
COOP_FIXES = (
    ("Perite fille sérieuse", "Petite fille sérieuse"),
    ("Il co-parenté avec Phoebe avec une dignité", "Il partage leur éducation avec Phoebe, avec une dignité"),
    ("arranger tout par l'amour", "tout arranger par l'amour"),
)


class Command(BaseCommand):
    help = "Corrige les textes déjà publiés de Prudence Johanna et Coop."

    def handle(self, *args, **options):
        with transaction.atomic():
            prudence = Topic.objects.select_for_update().filter(slug="prudence-johanna-halliwell").first()
            coop = Topic.objects.select_for_update().filter(slug="coop-everhart").first()
            if not prudence or not coop:
                raise CommandError("Une des fiches de la famille Everhart est introuvable.")

            prudence_post = prudence.posts.select_for_update().order_by("id").first()
            coop_post = coop.posts.select_for_update().order_by("id").first()
            if not prudence_post or not coop_post:
                raise CommandError("Le contenu d'une des fiches est introuvable.")

            updated = 0
            content = prudence_post.content.replace(OLD_JENSEN_PASSAGE, NEW_JENSEN_PASSAGE)
            if content != prudence_post.content:
                prudence_post.content = content
                prudence_post.save(update_fields=["content"])
                updated += 1

            cards = prudence.scenario_link_cards or []
            for card in cards:
                if "Jensen" in card.get("title", "") and card.get("text") == OLD_JENSEN_LINK:
                    card["text"] = NEW_JENSEN_LINK
                    prudence.scenario_link_cards = cards
                    prudence.save(update_fields=["scenario_link_cards"])
                    updated += 1
                    break

            content = coop_post.content
            for old, new in COOP_FIXES:
                content = content.replace(old, new)
            if content != coop_post.content:
                coop_post.content = content
                coop_post.save(update_fields=["content"])
                updated += 1

        self.stdout.write(self.style.SUCCESS(f"Éléments corrigés : {updated}"))
