from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from apps.forum.models import SitePage


User = get_user_model()


CONTENT = """
<div style="font-family:Georgia,serif;line-height:1.75;color:#d8d1e5;">
  <p style="margin:0 0 .4rem;color:#d8b4fe;font-size:.68rem;font-weight:700;letter-spacing:.18em;">✦ SAISON 1 · LES PORTES DU NEXUS ✦</p>
  <h2 style="margin:.1rem 0 1rem;color:#f5d76e;font-weight:normal;font-style:italic;">Quand les mondes surnaturels se reconnaissent enfin.</h2>
  <p>Une même nuit, les lumières de <strong style="color:#e2d9f3;">San Francisco</strong> ont vacillé, le Nemeton de <strong style="color:#e2d9f3;">Beacon Hills</strong> s’est réveillé, les cimetières de <strong style="color:#e2d9f3;">La Nouvelle-Orléans</strong> ont chanté et les cloches de <strong style="color:#e2d9f3;">Mystic Falls</strong> ont sonné sans qu’aucune main ne les touche. Au centre de ces signes, une onde de magie ancienne a redessiné le monde.</p>
  <p>Les sorcières appellent ce phénomène le <strong style="color:#f5d76e;">Nexus Arcana</strong>. Les vampires y sentent une faim qui ne leur appartient pas. Les loups entendent l’appel dans leurs os. Les Banshees voient des morts qui n’ont pas encore eu lieu. Les pouvoirs des Charmed Ones, les traditions des covens, la magie des Originels et les forces du Nemeton répondent tous à la même pulsation.</p>
  <div style="margin:1.1rem 0;padding:1rem;border-left:2px solid #a78bfa;background:rgba(124,58,237,.09);"><strong style="display:block;margin-bottom:.35rem;color:#d8b4fe;letter-spacing:.08em;font-size:.76rem;">LE POINT DE DÉPART</strong>Les quatre villes sont désormais voisines. La Convergence les a réunies dans une même région : routes, gares et trajets ordinaires permettent d’aller de San Francisco à Beacon Hills, Mystic Falls ou La Nouvelle-Orléans. Elles gardent leur identité, mais leurs frontières se touchent — et les personnages peuvent s’y croiser librement.</div>
  <p>Quelques failles magiques subsistent et restent dangereuses, mais elles ne sont plus nécessaires pour voyager. À mesure qu’elles se multiplient, des créatures oubliées réapparaissent et des alliances autrefois impensables deviennent nécessaires. Quelqu’un — ou quelque chose — semble nourrir le Nexus. Les premiers indices désignent quatre points d’ancrage : le Manoir Halliwell, l’ancienne propriété des Lockwood, les terres du cimetière Saint-Louis et le Nemeton.</p>
  <p><strong style="color:#f5d76e;">Cette saison 1 est celle des rencontres et des premiers choix.</strong> Protéger sa ville ou explorer l’inconnu ? Fermer les failles ou en utiliser le pouvoir ? Les personnages peuvent conserver, adapter ou réinventer leur parcours canonique : aucune fin de série n’est imposée. Seuls comptent les secrets qu’ils choisissent de porter et les conséquences de leurs actes.</p>
</div>
""".strip()


class Command(BaseCommand):
    help = "Installe le contexte de la saison 1 : Les Portes du Nexus."

    def handle(self, *args, **options):
        author = User.objects.filter(role__in=["fondatrice", "admin"]).first()
        if not author:
            raise CommandError("Aucun compte administrateur n'est disponible.")
        SitePage.objects.update_or_create(
            slug="home-context",
            defaults={"content": CONTENT, "updated_by": author},
        )
        self.stdout.write(self.style.SUCCESS("Contexte de la saison 1 installé."))
