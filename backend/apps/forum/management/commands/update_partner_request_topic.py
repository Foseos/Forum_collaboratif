"""Actualise le sujet officiel de recherche de partenaires RP sans toucher aux réponses."""

from django.core.management.base import BaseCommand, CommandError

from apps.forum.models import Topic


CONTENT = """<div style="font-family:Georgia,'Times New Roman',serif;background:#0d0a1a;color:#e2d9f3;padding:2rem;border:1px solid rgba(124,58,237,.35);border-radius:10px;max-width:760px;margin:auto;line-height:1.7">
  <p style="margin:0;text-align:center;color:#a78bfa;font-size:.7rem;letter-spacing:.25em;text-transform:uppercase">✦ Nexus Arcana · Recherche de RP ✦</p>
  <h1 style="margin:.35rem 0 1rem;text-align:center;color:#f5d76e;font-weight:normal;font-style:italic;font-size:1.8rem">Trouver un partenaire de RP</h1>
  <p style="margin:0 0 1.4rem;text-align:center">Une rencontre imprévue, une enquête, une alliance fragile ou une rivalité à construire ? Décrivez votre idée ici pour trouver quelqu’un avec qui l’écrire, dans la ville qui convient à vos personnages.</p>

  <div style="border:1px solid rgba(124,58,237,.3);border-radius:7px;padding:1rem 1.2rem;margin-bottom:1.2rem">
    <h2 style="margin:0 0 .5rem;color:#a78bfa;font-size:1rem;font-weight:normal">Comment proposer un RP ?</h2>
    <p style="margin:0">Répondez à ce sujet avec une annonce par <strong>idée de RP</strong>. Vous pouvez la laisser ouverte à plusieurs personnes ou préciser le type de partenaire recherché. Quand vous avez trouvé, modifiez votre message pour indiquer <strong>« Trouvé »</strong> ; si l’idée est de nouveau disponible, indiquez <strong>« Ouvert »</strong>. Les intéressés peuvent répondre ici ou vous écrire en privé.</p>
  </div>

  <div style="border:1px solid rgba(245,215,110,.4);border-radius:7px;overflow:hidden">
    <h2 style="margin:0;padding:.6rem 1rem;background:rgba(245,215,110,.1);color:#f5d76e;font-size:.9rem;font-weight:normal;letter-spacing:.08em">Modèle d’annonce à reprendre</h2>
    <div style="padding:1rem 1.2rem">
      <p style="margin:0 0 .7rem"><strong style="color:#f5d76e">Statut :</strong> Ouvert / Trouvé</p>
      <p style="margin:0 0 .7rem"><strong style="color:#f5d76e">Mon personnage :</strong> [Nom et lien vers sa fiche, si vous le souhaitez]</p>
      <p style="margin:0 0 .7rem"><strong style="color:#f5d76e">Ville et lieu :</strong> [San Francisco, Beacon Hills, Mystic Falls, La Nouvelle-Orléans ou lieu à définir]</p>
      <p style="margin:0 0 .7rem"><strong style="color:#f5d76e">Idée de départ :</strong> [La situation qui lance la scène et ce que vous aimeriez explorer]</p>
      <p style="margin:0 0 .7rem"><strong style="color:#f5d76e">Partenaire(s) recherché(s) :</strong> [Libre à tous, lien particulier, faction, nombre de joueurs…]</p>
      <p style="margin:0 0 .7rem"><strong style="color:#f5d76e">Ambiance :</strong> [Enquête, action, quotidien, tension, romance… selon vos envies]</p>
      <p style="margin:0 0 .7rem"><strong style="color:#f5d76e">Rythme de réponse :</strong> [Votre disponibilité approximative]</p>
      <p style="margin:0"><strong style="color:#f5d76e">Pour me contacter :</strong> [Réponse dans ce sujet ou message privé]</p>
    </div>
  </div>
  <p style="margin:1.2rem 0 0;text-align:center;color:#a78bfa;font-style:italic;font-size:.85rem">Le modèle est un guide : adaptez-le à votre idée et discutez des détails ensemble avant de commencer.</p>
</div>"""


class Command(BaseCommand):
    help = "Met à jour la présentation de la recherche de partenaires RP."

    def handle(self, *args, **options):
        topic = Topic.objects.filter(slug="demande-de-partenaire-de-rp").first()
        if topic is None:
            raise CommandError("Sujet de recherche de partenaires introuvable.")
        post = topic.posts.order_by("created_at").first()
        if post is None:
            raise CommandError("Premier message du sujet introuvable.")
        post.content = CONTENT
        post.is_trusted_html = True
        post.save(update_fields=["content", "is_trusted_html"])
        self.stdout.write(self.style.SUCCESS("Présentation des recherches de RP actualisée."))
