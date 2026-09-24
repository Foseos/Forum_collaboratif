from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.forum.models import Category, Post, Topic


GUIDE_HTML = """
<article style="max-width:760px;margin:auto;padding:1.8rem;background:#0d0a1a;color:#e2d9f3;border:1px solid rgba(167,139,250,.35);border-radius:10px;font-family:Georgia,serif;line-height:1.75;">
  <p style="margin:0;color:#a78bfa;font-size:.7rem;letter-spacing:.2em;text-transform:uppercase;">✦ Bienvenue à Nexus Arcana ✦</p>
  <h2 style="margin:.4rem 0 1rem;color:#f5d76e;font-weight:normal;">Le parrainage</h2>
  <p>Faire ses premiers pas dans quatre univers réunis peut soulever beaucoup de questions. Le parrainage permet à un nouveau membre de trouver un repère auprès d'un joueur qui connaît déjà le forum.</p>
  <h3 style="color:#f5d76e;">Comment commencer ?</h3>
  <ol style="padding-left:1.4rem;">
    <li>Un nouveau membre et un parrain ou une marraine se mettent d'accord pour avancer ensemble.</li>
    <li>Ils contactent l'administration, qui ouvre un sujet dans cette rubrique avec leurs deux noms dans le titre.</li>
    <li>Ils peuvent ensuite répondre dans ce même sujet pour poser des questions, partager des liens utiles et suivre leurs premières pistes de jeu.</li>
  </ol>
  <h3 style="color:#f5d76e;">À quoi peut servir ce sujet ?</h3>
  <p>Découvrir le contexte, comprendre les rubriques, préparer une fiche, trouver un premier RP ou simplement demander où chercher une information. Il n'y a ni durée imposée ni obligation de jouer ensemble. Le staff reste disponible si une question dépasse le cadre du parrainage.</p>
  <div style="margin-top:1.3rem;padding:1rem;border-left:3px solid #a78bfa;background:rgba(167,139,250,.1);">
    <strong style="color:#f5d76e;">À savoir</strong><br>
    Les sujets de cette rubrique sont publics. Pour une question personnelle, utilisez plutôt la messagerie privée ou contactez l'équipe du staff.
  </div>
</article>
""".strip()


class Command(BaseCommand):
    help = "Crée la sous-rubrique Parrainage et son guide dans Bienvenue à Nexus Arcana."

    @transaction.atomic
    def handle(self, *args, **options):
        parent = Category.objects.filter(slug="bienvenue-san-francisco").first()
        author = get_user_model().objects.filter(username="Ava Bartholomé").first()
        if parent is None or author is None:
            raise CommandError("La rubrique Bienvenue ou le compte d'Ava Bartholomé est introuvable.")

        category, _ = Category.objects.get_or_create(
            slug="parrainage",
            defaults={
                "name": "Parrainage",
                "description": "Un sujet par binôme pour accueillir et accompagner les nouveaux membres.",
                "parent": parent,
                "order": 26,
            },
        )
        topic, created = Topic.objects.get_or_create(
            category=category,
            slug="guide-du-parrainage",
            defaults={
                "title": "✦ Guide du parrainage",
                "author": author,
                "is_pinned": True,
                "is_locked": True,
            },
        )
        if created:
            Post.objects.create(topic=topic, author=author, content=GUIDE_HTML, is_trusted_html=True)
        else:
            first_post = topic.posts.order_by("created_at", "pk").first()
            if first_post:
                first_post.content = GUIDE_HTML
                first_post.save(update_fields=["content"])
        self.stdout.write(self.style.SUCCESS("Parrainage prêt."))
