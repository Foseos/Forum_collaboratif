"""Clarifie le passage sur les pouvoirs dans le contexte déjà publié."""

from django.core.management.base import BaseCommand, CommandError

from apps.forum.models import SitePage
from .seed_season_one_context import CONTENT


class Command(BaseCommand):
    help = "Explique simplement que le Nexus brouille les pouvoirs des créatures."

    def handle(self, *args, **options):
        page = SitePage.objects.filter(slug="home-context").first()
        if page is None:
            raise CommandError("Le contexte de la saison 1 est introuvable.")

        old_paragraph = (
            "<p>Les sorciers appellent ce phénomène le <strong style=\"color:#f5d76e;\">Nexus Arcana</strong>. "
            "Les vampires y sentent une faim qui ne leur appartient pas. Les loups entendent l’appel dans leurs os. "
            "Les Banshees voient des morts qui n’ont pas encore eu lieu. Les pouvoirs des Charmed Ones, les traditions "
            "des covens, la magie des Originels et les forces du Nemeton répondent tous à la même pulsation.</p>"
        )
        new_paragraph = next(line.strip() for line in CONTENT.splitlines() if "les pouvoirs des créatures surnaturelles sont brouillés" in line)
        if old_paragraph in page.content:
            page.content = page.content.replace(old_paragraph, new_paragraph)
            page.save(update_fields=["content"])
            self.stdout.write(self.style.SUCCESS("Le contexte publié a été clarifié."))
        elif new_paragraph in page.content:
            self.stdout.write("Le contexte est déjà à jour.")
        else:
            raise CommandError("Le passage d'origine a été modifié : aucune autre partie du contexte n'a été écrasée.")
