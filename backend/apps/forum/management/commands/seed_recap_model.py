"""Publie le modèle officiel du carnet de personnage dans sa rubrique."""

from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from apps.forum.models import Category, Post, Topic


MODEL_SLUG = "modele-fiche-personnage"
TEMPLATE_PATH = Path(__file__).resolve().parents[2] / "data" / "recap_template.html"


class Command(BaseCommand):
    help = "Crée ou actualise le sujet officiel « Modèle fiche personnage »."

    def handle(self, *args, **options):
        category = Category.objects.filter(slug="fiche-personnage").first()
        if category is None:
            raise CommandError("La rubrique Fiche personnage est introuvable.")
        author = get_user_model().objects.filter(role__in=["admin", "fondatrice"]).order_by("id").first()
        if author is None:
            raise CommandError("Aucun administrateur ne peut publier le modèle.")
        content = TEMPLATE_PATH.read_text(encoding="utf-8-sig").strip()
        topic, _ = Topic.objects.get_or_create(
            category=category,
            slug=MODEL_SLUG,
            defaults={"title": "Modèle fiche personnage", "author": author},
        )
        topic.title = "Modèle fiche personnage"
        topic.is_pinned = True
        topic.is_locked = True
        topic.save(update_fields=["title", "is_pinned", "is_locked"])
        post = topic.posts.order_by("created_at", "id").first()
        if post is None:
            Post.objects.create(topic=topic, author=author, content=content, is_trusted_html=True)
        else:
            post.content = content
            post.is_trusted_html = True
            post.save(update_fields=["content", "is_trusted_html"])
        self.stdout.write(self.style.SUCCESS("Sujet « Modèle fiche personnage » prêt."))
