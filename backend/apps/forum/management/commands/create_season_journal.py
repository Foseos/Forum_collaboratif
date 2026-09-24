from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.forum.models import Category, Post, Topic


JOURNAL_HTML = """
<article style="max-width:780px;margin:auto;padding:2rem;color:#e2d9f3;background:#0d0a1a;border:1px solid rgba(167,139,250,.35);border-radius:12px;font-family:Georgia,serif;line-height:1.75;">
  <p style="margin:0;color:#c4a7ef;font-size:.7rem;letter-spacing:.22em;text-transform:uppercase;">✦ Archives du Nexus · Saison 1 ✦</p>
  <h2 style="margin:.5rem 0;color:#f5d76e;font-size:2rem;font-weight:normal;">Le journal des Portes du Nexus</h2>
  <p style="margin-top:0;color:#c5b8d7;font-style:italic;">Un fil pour suivre ce que le monde sait, ce qu'il soupçonne et ce qui reste à découvrir.</p>

  <div style="margin:1.5rem 0;padding:1rem 1.2rem;background:rgba(167,139,250,.1);border-left:3px solid #a78bfa;border-radius:4px;">
    <strong style="color:#f5d76e;">Comment lire ce journal</strong><br>
    Les faits ci-dessous constituent le point de départ commun de la saison. Les mystères ne sont pas des réponses cachées à deviner hors jeu : ils pourront évoluer au rythme des intrigues et des RP. Ce journal sera mis à jour lorsque des événements marquants deviendront connus de tous.
  </div>

  <h3 style="color:#f5d76e;border-bottom:1px solid rgba(167,139,250,.3);padding-bottom:.35rem;">I · La nuit où tout a changé</h3>
  <p>Une même nuit, les lumières de San Francisco ont vacillé. À Beacon Hills, le Nemeton s'est réveillé. Les cimetières de La Nouvelle-Orléans ont semblé chanter et les cloches de Mystic Falls ont sonné sans qu'aucune main ne les touche. Une onde de magie ancienne a traversé les quatre villes. On nomme ce bouleversement <strong style="color:#f5d76e;">la Convergence</strong>.</p>

  <h3 style="color:#f5d76e;border-bottom:1px solid rgba(167,139,250,.3);padding-bottom:.35rem;">II · Le monde depuis la Convergence</h3>
  <p>San Francisco, Mystic Falls, La Nouvelle-Orléans et Beacon Hills se trouvent désormais dans une même région. Des routes et des trajets ordinaires permettent de passer de l'une à l'autre. Chacune garde son histoire et son identité, mais les rencontres entre leurs habitants sont maintenant possibles au quotidien.</p>
  <p>Quelques failles magiques subsistent. Elles sont dangereuses et ne sont pas nécessaires pour voyager. Des créatures oubliées réapparaissent, tandis que des pouvoirs et des traditions issus de mondes différents semblent répondre à une même pulsation.</p>

  <h3 style="color:#f5d76e;border-bottom:1px solid rgba(167,139,250,.3);padding-bottom:.35rem;">III · Les quatre points d'ancrage possibles</h3>
  <p>Les premiers indices attirent l'attention sur quatre lieux : <strong>le Manoir Halliwell</strong> à San Francisco, <strong>l'ancienne propriété des Lockwood</strong> à Mystic Falls, <strong>les terres du cimetière Saint-Louis</strong> à La Nouvelle-Orléans et <strong>le Nemeton</strong> à Beacon Hills. Leur rôle exact reste inconnu.</p>

  <h3 style="color:#f5d76e;border-bottom:1px solid rgba(167,139,250,.3);padding-bottom:.35rem;">IV · Questions encore ouvertes</h3>
  <ul style="padding-left:1.3rem;">
    <li>Quelle force a provoqué la Convergence ?</li>
    <li>Pourquoi ces quatre lieux semblent-ils liés au Nexus ?</li>
    <li>Quelles conséquences auront les failles qui subsistent ?</li>
    <li>Les nouvelles alliances résisteront-elles aux anciens conflits ?</li>
  </ul>
  <p>Aucune faction ni aucun personnage ne possède encore toutes les réponses. Les découvertes faites en jeu pourront enrichir ce journal lorsqu'elles deviendront publiques.</p>

  <div style="margin-top:1.6rem;padding:1rem 1.2rem;border:1px solid rgba(245,215,110,.3);border-radius:8px;">
    <strong style="color:#f5d76e;">Où en sommes-nous ?</strong><br>
    La saison 1 en est à ses premières rencontres. Les personnages peuvent enquêter, protéger leurs proches, explorer les villes ou choisir de rester prudents face à l'inconnu. Les événements futurs seront ajoutés ici, dans l'ordre où ils entreront dans l'histoire commune.
  </div>
</article>
""".strip()


class Command(BaseCommand):
    help = "Crée le journal officiel de la saison 1 dans Contextes et animations."

    @transaction.atomic
    def handle(self, *args, **options):
        category = Category.objects.filter(slug="contextes-et-animations").first()
        author = get_user_model().objects.filter(username="Ava Bartholomé").first()
        if category is None or author is None:
            raise CommandError("La rubrique ou le compte d'Ava Bartholomé est introuvable.")

        topic, created = Topic.objects.get_or_create(
            category=category,
            slug="journal-de-la-saison-1",
            defaults={
                "title": "✦ Journal de la saison 1 — Les Portes du Nexus",
                "author": author,
                "is_pinned": True,
                "is_locked": True,
            },
        )
        if created:
            Post.objects.create(topic=topic, author=author, content=JOURNAL_HTML, is_trusted_html=True)
        self.stdout.write(self.style.SUCCESS("Journal créé." if created else "Journal déjà présent ; contenu conservé."))
