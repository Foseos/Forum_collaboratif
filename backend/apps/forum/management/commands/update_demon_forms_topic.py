"""Actualise uniquement les règles du bottin des formes démoniaques."""

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

from apps.forum.management.commands.seed_reglement_topics import CONTENT_FORMES
from apps.forum.models import Category, Post, Topic


class Command(BaseCommand):
    help = "Rappelle le choix obligatoire d'une forme pour les démons."

    def handle(self, *args, **options):
        category = Category.objects.filter(slug="bottin-des-formes-demoniaques").first()
        author = get_user_model().objects.filter(role__in=["admin", "fondatrice"]).order_by("id").first()
        if category is None or author is None:
            raise CommandError("Rubrique ou compte administrateur introuvable.")
        topic, _ = Topic.objects.get_or_create(
            category=category,
            slug="reglement-et-reservations-formes-demoniaques",
            defaults={
                "title": "Règlement & Réservations — Formes Démoniaques",
                "author": author,
                "is_pinned": True,
            },
        )
        post = topic.posts.order_by("created_at", "id").first()
        if post is None:
            Post.objects.create(topic=topic, author=author, content=CONTENT_FORMES, is_trusted_html=True)
        elif "chaque <strong style=\"color:#e2d9f3;\">personnage démon</strong>" not in post.content:
            note = "<p>Chaque personnage démon choisit et décrit sa forme démoniaque dans sa fiche, puis la déclare ici avant de la jouer. Cette forme n'ajoute aucun pouvoir.</p>"
            post.content = note + post.content
            post.save(update_fields=["content"])
        self.stdout.write(self.style.SUCCESS("Règles des formes démoniaques actualisées."))
