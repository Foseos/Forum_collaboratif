"""Align the published Chimera entry with the Teen Wolf continuity."""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.forum.models import Topic


REPLACEMENTS = (
    (
        "Nature composite dont les origines sont fixées avant le jeu.",
        "Dans Teen Wolf, les Chimères sont issues des expériences des Médecins de l’Effroi. Leurs traits surnaturels ont été assemblés artificiellement : elles ne sont pas des hybrides nés de deux lignées.",
    ),
    (
        "Une seule branche pour toutes les chimères, quelle que soit la combinaison de leurs traits. Les origines et les capacités propres au personnage sont détaillées dans sa fiche.",
        "Une seule branche pour les Chimères issues de ces expériences. Les traits réunis, les capacités et les limites propres au personnage sont détaillés dans sa fiche.",
    ),
    ("Chimères · 1 branches ou profils", "Chimères · 1 branche ou profil"),
)


class Command(BaseCommand):
    help = "Actualise la fiche Chimères dans le bottin publié."

    def handle(self, *args, **options):
        with transaction.atomic():
            topic = Topic.objects.select_for_update().get(slug="encyclopedie-des-creatures-et-races")
            post = topic.posts.select_for_update().order_by("created_at", "pk").first()
            if post is None:
                raise CommandError("Le sujet du bottin ne contient aucun message.")

            content = post.content
            for old, new in REPLACEMENTS:
                if old not in content and new not in content:
                    raise CommandError(f"Texte attendu absent du bottin : {old}")
                content = content.replace(old, new, 1)

            if content != post.content:
                post.content = content
                post.save(update_fields=["content", "is_edited", "updated_at"])
                self.stdout.write(self.style.SUCCESS("Fiche Chimères du bottin actualisée."))
            else:
                self.stdout.write("Fiche Chimères déjà à jour.")
