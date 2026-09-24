from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
import re

from apps.forum.models import Category, Post, Topic

User = get_user_model()

FICHE_CONTENT = """<div style="font-family: Georgia, 'Times New Roman', serif; background: #0d0a1a; color: #e2d9f3; padding: 2rem; border-radius: 10px; border: 1px solid rgba(124,58,237,0.3); max-width: 720px; margin: 0 auto;">

<!-- EN-TÊTE : nom à gauche, image à droite -->
<table style="width: 100%; border-collapse: collapse; margin-bottom: 1.75rem; padding-bottom: 1.5rem; border-bottom: 1px solid rgba(124,58,237,0.2);">
<tr>
  <td style="vertical-align: top; padding-right: 1.5rem;">
    <p style="margin: 0 0 0.5rem; font-size: 0.58rem; letter-spacing: 0.38em; text-transform: uppercase; color: #6d28d9;">✦ Nexus Arcana · Livre des Ombres ✦</p>
    <h1 style="margin: 0 0 0.6rem; font-size: 2rem; font-weight: normal; font-style: italic; color: #f5d76e; letter-spacing: 0.04em; line-height: 1.2;">Prénom(s)<br>Nom</h1>
    <p style="margin: 0 0 1rem; font-size: 0.82rem; color: #a78bfa; font-style: italic; letter-spacing: 0.06em;">Race · Camp</p>
    <p style="margin: 0; font-size: 0.75rem; color: #4b3a6b; font-style: italic; line-height: 1.7;">"Une citation ou accroche qui définit votre personnage en quelques mots."</p>
  </td>
  <td style="vertical-align: top; width: 210px; text-align: center;">
    <!-- Remplacez src par l'URL de votre image de personnage -->
    <img src="/Image_de_base_photo_de_profil.jpg" alt="Prénom NOM" style="width:200px;height:320px;object-fit:cover;border-radius:6px;border:2px solid rgba(124,58,237,0.35);display:block;margin:0 auto;">
    <p style="margin: 0.35rem 0 0; font-size: 0.6rem; color: #3d2d5e; font-style: italic;">Prénom NOM — célébrité jouée</p>
  </td>
</tr>
</table>

<!-- BOX I : IDENTITÉ -->
<div style="margin-bottom: 1.2rem; border: 1px solid rgba(124,58,237,0.28); border-radius: 7px; overflow: hidden;">
  <div style="background: linear-gradient(90deg, rgba(109,40,217,0.3), rgba(109,40,217,0.08)); padding: 0.45rem 1rem; border-bottom: 1px solid rgba(124,58,237,0.25);">
    <h2 style="margin: 0; font-size: 0.6rem; letter-spacing: 0.3em; text-transform: uppercase; color: #a78bfa; font-weight: normal;">◈ I. Identité</h2>
  </div>
  <div style="padding: 0.6rem 1rem;">
    <table style="width: 100%; border-collapse: collapse;">
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; width: 42%; border-bottom: 1px solid rgba(124,58,237,0.08);">Âge</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">XX ans</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(124,58,237,0.08);">Date de naissance</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">JJ Mois AAAA</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(124,58,237,0.08);">Sexe</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">Féminin / Masculin / Autre</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(124,58,237,0.08);">Orientation sexuelle</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">...</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(124,58,237,0.08);">Situation familiale</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">Célibataire / Marié(e) / Veuf(ve) / ...</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(124,58,237,0.08);">Race</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">Sorcière / Démon / ...</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(124,58,237,0.08);">Camp</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">Bien / Neutre / Mal</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0;">Métier</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3;">...</td></tr>
    </table>
  </div>
</div>

<!-- DÉMONS UNIQUEMENT : supprimez cet encart entier pour les autres races. -->
<div style="margin-bottom: 1.2rem; border: 1px solid rgba(185,120,139,0.45); border-radius: 7px; overflow: hidden; background: #17101f;">
  <div style="padding: 0.5rem 1rem; border-bottom: 1px solid rgba(185,120,139,0.3); background: rgba(185,120,139,0.1);">
    <h2 style="margin: 0; font-size: 0.65rem; letter-spacing: 0.22em; text-transform: uppercase; color: #d3aab6; font-weight: normal;">◈ Forme démoniaque · si Démon</h2>
  </div>
  <div style="padding: 1rem; text-align: center;">
    <p style="margin: 0 0 0.35rem; color: #f5d76e; font-size: 1rem;">[Nom de la forme]</p>
    <p style="margin: 0 0 0.85rem; color: #c4b5d4; font-size: 0.82rem; line-height: 1.6;">[Décrivez son apparence. Elle doit aussi être déclarée au bottin des formes démoniaques.]</p>
    <!-- Remplacez uniquement l'adresse src par celle de votre image ou de votre GIF ; supprimez l'image si vous n'en souhaitez pas. -->
    <img src="/demon-form-placeholder.svg" alt="Image ou GIF de la forme démoniaque" style="display: block; width: 180px; max-width: 100%; height: 110px; object-fit: cover; border-radius: 6px; margin: 0 auto; border: 1px solid rgba(185,120,139,0.4);">
  </div>
</div>

<!-- BOX II : POUVOIRS -->
<div style="margin-bottom: 1.2rem; border: 1px solid rgba(124,58,237,0.28); border-radius: 7px; overflow: hidden;">
  <div style="background: linear-gradient(90deg, rgba(109,40,217,0.3), rgba(109,40,217,0.08)); padding: 0.45rem 1rem; border-bottom: 1px solid rgba(124,58,237,0.25);">
    <h2 style="margin: 0; font-size: 0.6rem; letter-spacing: 0.3em; text-transform: uppercase; color: #a78bfa; font-weight: normal;">◈ II. Pouvoirs Magiques &amp; Aptitudes</h2>
  </div>
  <div style="padding: 0.85rem 1rem 0.75rem;">
    <p style="margin: 0 0 0.4rem; font-size: 0.78rem; font-weight: 600; color: #c4b5fd;">⚡ Pouvoirs actifs :</p>
    <ul style="margin: 0; padding-left: 1.3rem; line-height: 1.85; font-size: 0.87rem; color: #c4b5d4;">
      <li><strong style="color: #e2d9f3;">Nom du pouvoir</strong> — Description et limites du pouvoir</li>
      <li><strong style="color: #e2d9f3;">Nom du pouvoir</strong> — Description et limites du pouvoir</li>
      <li><strong style="color: #e2d9f3;">Nom du pouvoir</strong> — Description et limites du pouvoir</li>
      <li><strong style="color: #e2d9f3;">Nom du pouvoir</strong> — Description et limites du pouvoir</li>
      <li><strong style="color: #e2d9f3;">Nom du pouvoir</strong> — Description et limites du pouvoir</li>
    </ul>
  </div>
</div>

<!-- BOX III : CARACTÈRE -->
<div style="margin-bottom: 1.2rem; border: 1px solid rgba(124,58,237,0.28); border-radius: 7px; overflow: hidden;">
  <div style="background: linear-gradient(90deg, rgba(109,40,217,0.3), rgba(109,40,217,0.08)); padding: 0.45rem 1rem; border-bottom: 1px solid rgba(124,58,237,0.25);">
    <h2 style="margin: 0; font-size: 0.6rem; letter-spacing: 0.3em; text-transform: uppercase; color: #a78bfa; font-weight: normal;">◈ III. Âme &amp; Caractère</h2>
  </div>
  <div style="padding: 1rem;">
    <p style="margin: 0; line-height: 1.9; color: #c4b5d4; text-align: justify; font-size: 0.9rem;">[Décrivez la personnalité de votre personnage : ses traits dominants, ses habitudes, ses valeurs, ses peurs, ses forces et faiblesses. Comment se comporte-t-il face aux autres ? Quel est son rapport à la magie, au destin, à la trahison ? Comment réagit-il sous pression ? Minimum 15 lignes.]</p>
  </div>
</div>

<!-- BOX IV : HISTOIRE -->
<div style="margin-bottom: 1.2rem; border: 1px solid rgba(124,58,237,0.28); border-radius: 7px; overflow: hidden;">
  <div style="background: linear-gradient(90deg, rgba(109,40,217,0.3), rgba(109,40,217,0.08)); padding: 0.45rem 1rem; border-bottom: 1px solid rgba(124,58,237,0.25);">
    <h2 style="margin: 0; font-size: 0.6rem; letter-spacing: 0.3em; text-transform: uppercase; color: #a78bfa; font-weight: normal;">◈ IV. Mémoire des Âges · Histoire</h2>
  </div>
  <div style="padding: 1rem;">
    <p style="margin: 0; line-height: 1.9; color: #c4b5d4; text-align: justify; font-size: 0.9rem;">[Racontez l'histoire complète de votre personnage : ses origines, les événements qui l'ont façonné, les épreuves traversées, et ce qui l'a conduit dans l'une des villes du Nexus. Comment a-t-il découvert le monde magique ? Quels secrets porte-t-il ? Quelles cicatrices l'invisible lui a-t-il laissées ? Minimum 30 lignes.]</p>
  </div>
</div>

<!-- BOX V : HORS PERSONNAGE -->
<div style="border: 1px solid rgba(245,215,110,0.22); border-radius: 7px; overflow: hidden;">
  <div style="background: linear-gradient(90deg, rgba(245,215,110,0.12), rgba(245,215,110,0.03)); padding: 0.45rem 1rem; border-bottom: 1px solid rgba(245,215,110,0.2);">
    <h2 style="margin: 0; font-size: 0.6rem; letter-spacing: 0.3em; text-transform: uppercase; color: #f5d76e; font-weight: normal;">◈ V. Hors Personnage</h2>
  </div>
  <div style="padding: 0.6rem 1rem;">
    <table style="width: 100%; border-collapse: collapse;">
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; width: 50%; border-bottom: 1px solid rgba(245,215,110,0.07);">Pseudonyme sur le forum</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(245,215,110,0.07);">...</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(245,215,110,0.07);">Âge</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(245,215,110,0.07);">...</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(245,215,110,0.07);">Comment avez-vous connu le forum ?</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(245,215,110,0.07);">...</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(245,215,110,0.07);">Crédits</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(245,215,110,0.07);">Avatar, images, GIFs…</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0;">Souhaitez-vous un parrain / une marraine ?</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3;">Oui / Non</td></tr>
    </table>
  </div>
</div>

<p style="text-align: center; margin: 1.25rem 0 0; font-size: 0.58rem; color: #2d1f4a; font-style: italic; letter-spacing: 0.18em;">✦ Fiche soumise à la validation du Nexus Arcana ✦</p>
</div>"""


class Command(BaseCommand):
    help = "Crée le sujet modèle de fiche de présentation (épinglé, verrouillé) avec son contenu HTML."

    def handle(self, *args, **options):
        # 1. Récupérer la catégorie
        try:
            category = Category.objects.get(slug="modele-fiche-de-presentation")
        except Category.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    "Catégorie 'modele-fiche-de-presentation' introuvable. "
                    "Lancez d'abord : python manage.py seed_categories"
                )
            )
            return

        # 2. Récupérer un utilisateur admin/fondatrice
        author = (
            User.objects.filter(role__in=["fondatrice", "admin"]).first()
            or User.objects.filter(is_superuser=True).first()
        )
        if not author:
            self.stdout.write(
                self.style.ERROR(
                    "Aucun utilisateur admin trouvé. "
                    "Créez d'abord un compte admin ou fondatrice."
                )
            )
            return

        # 3. Créer le sujet (idempotent)
        topic, created = Topic.objects.get_or_create(
            category=category,
            slug="modele-de-fiche-de-presentation",
            defaults={
                "title": "Modèle de fiche de présentation",
                "author": author,
                "is_pinned": True,
                "is_locked": True,
            },
        )

        if created:
            Post.objects.create(
                topic=topic,
                author=author,
                content=FICHE_CONTENT,
                is_trusted_html=True,
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"  ✓ Sujet créé : « {topic.title} » (auteur : {author.username})"
                )
            )
        else:
            post = topic.posts.order_by('created_at', 'pk').first()
            if post:
                old = "ce qui l'a conduit à San Francisco"
                new = "ce qui l'a conduit dans l'une des villes du Nexus"
                if old in post.content:
                    post.content = post.content.replace(old, new)
                if '◈ Forme démoniaque · si Démon' not in post.content:
                    post.content = re.sub(
                        r'\s*<!-- DÉMONS UNIQUEMENT : supprimez ces trois lignes pour les autres races\. -->\s*'
                        r'(?:<tr><td[^>]*>.*?</tr>\s*){3}',
                        '\n', post.content, count=1, flags=re.S,
                    )
                    post.content = re.sub(
                        r'\s*<tr><td[^>]*>Forme démoniaque \(si Démon\)</td>.*?</tr>',
                        '', post.content, count=1, flags=re.S,
                    )
                    start = FICHE_CONTENT.index('<!-- DÉMONS UNIQUEMENT : supprimez cet encart')
                    end = FICHE_CONTENT.index('<!-- BOX II : POUVOIRS -->', start)
                    new_block = FICHE_CONTENT[start:end]
                    anchor = '<!-- BOX II : POUVOIRS -->'
                    if anchor not in post.content:
                        raise ValueError('Section des pouvoirs introuvable dans le modèle publié.')
                    post.content = post.content.replace(anchor, new_block + anchor, 1)
                post.save(update_fields=['content', 'updated_at'])
                self.stdout.write(f"  — Sujet déjà existant : « {topic.title} »")
            else:
                Post.objects.create(topic=topic, author=author, content=FICHE_CONTENT, is_trusted_html=True)
                self.stdout.write(self.style.SUCCESS("  ✓ Message du modèle restauré."))
