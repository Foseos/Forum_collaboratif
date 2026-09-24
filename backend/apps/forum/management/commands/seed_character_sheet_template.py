from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from apps.forum.models import Category, Post, Topic


User = get_user_model()


TEMPLATE = """
<div style="font-family:Georgia,serif;max-width:760px;margin:auto;padding:2rem;border:1px solid rgba(124,58,237,.35);border-radius:10px;background:#0d0a1a;color:#e2d9f3;">
  <p style="margin:0 0 .4rem;text-align:center;color:#a78bfa;font-size:.62rem;letter-spacing:.22em;">✦ NEXUS ARCANA · FICHE PERSONNAGE ✦</p>
  <h1 style="margin:0 0 1.2rem;text-align:center;color:#f5d76e;font-weight:normal;font-style:italic;">Prénom Nom</h1>
  <p style="margin:0 0 1.5rem;text-align:center;color:#c4b5d4;font-style:italic;">« Une citation qui résume votre personnage. »</p>
  <div style="padding:1rem;margin-bottom:1rem;border:1px solid rgba(124,58,237,.25);border-radius:7px;"><h2 style="margin:0 0 .65rem;color:#a78bfa;font-size:.78rem;letter-spacing:.15em;">I. IDENTITÉ</h2><p><strong>Âge :</strong> …<br><strong>Origine / ville :</strong> …<br><strong>Race :</strong> …<br><strong>Groupe / camp :</strong> …<br><strong>Métier :</strong> …<br><strong>Avatar :</strong> …</p></div>
  <div style="padding:1rem;margin-bottom:1rem;border:1px solid rgba(124,58,237,.25);border-radius:7px;"><h2 style="margin:0 0 .65rem;color:#a78bfa;font-size:.78rem;letter-spacing:.15em;">II. POUVOIRS &amp; LIMITES</h2><p><strong>Pouvoirs :</strong> …<br><strong>Forces :</strong> …<br><strong>Faiblesses / contreparties :</strong> …</p></div>
  <div style="padding:1rem;margin-bottom:1rem;border:1px solid rgba(124,58,237,.25);border-radius:7px;"><h2 style="margin:0 0 .65rem;color:#a78bfa;font-size:.78rem;letter-spacing:.15em;">III. CARACTÈRE</h2><p>Décrivez ses qualités, défauts, peurs, ambitions et relations au surnaturel.</p></div>
  <div style="padding:1rem;margin-bottom:1rem;border:1px solid rgba(124,58,237,.25);border-radius:7px;"><h2 style="margin:0 0 .65rem;color:#a78bfa;font-size:.78rem;letter-spacing:.15em;">IV. HISTOIRE</h2><p>Racontez les moments importants de sa vie et ce qui l'amène aujourd'hui à Nexus Arcana.</p></div>
  <div style="padding:1rem;border:1px solid rgba(124,58,237,.25);border-radius:7px;"><h2 style="margin:0 0 .65rem;color:#a78bfa;font-size:.78rem;letter-spacing:.15em;">V. LIENS &amp; PISTES DE RP</h2><p><strong>Liens recherchés :</strong> …<br><strong>Ce que vous aimeriez jouer :</strong> …<br><strong>Crédits :</strong> avatar, images, GIFs et ressources…</p></div>
</div>
""".strip()


class Command(BaseCommand):
    help = "Crée ou actualise le modèle de fiche dans la catégorie Fiche personnage."

    def handle(self, *args, **options):
        try:
            category = Category.objects.get(slug="fiche-personnage")
        except Category.DoesNotExist as exc:
            raise CommandError("La catégorie Fiche personnage est introuvable.") from exc

        author = User.objects.filter(role__in=["fondatrice", "admin"]).first()
        if not author:
            raise CommandError("Aucun compte administrateur n'est disponible.")

        topic, created = Topic.objects.get_or_create(
            category=category,
            slug="modele-fiche-personnage-nexus-arcana",
            defaults={
                "title": "📋 Modèle de fiche personnage — à copier",
                "author": author,
                "is_pinned": True,
                "is_locked": True,
            },
        )
        if not created:
            topic.title = "📋 Modèle de fiche personnage — à copier"
            topic.is_pinned = True
            topic.is_locked = True
            topic.save(update_fields=["title", "is_pinned", "is_locked"])

        post = topic.posts.order_by("created_at").first()
        if post:
            post.content = TEMPLATE
            post.save(update_fields=["content", "updated_at"])
        else:
            Post.objects.create(topic=topic, author=author, content=TEMPLATE)

        category.description = "Publiez votre propre sujet de présentation à partir du modèle proposé."
        category.save(update_fields=["description"])
        self.stdout.write(self.style.SUCCESS("Modèle de fiche personnage prêt."))
