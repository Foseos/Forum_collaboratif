"""Met à jour la fiche publique de l'agence immobilière du Nexus."""

from django.core.management.base import BaseCommand

from apps.forum.models import Category, Topic


HOUSING_GUIDE = """
<div style="max-width:900px;margin:0 auto;color:#e7dcf3;font-family:Georgia,serif;line-height:1.7;">
  <header style="padding:2rem 1.5rem;text-align:center;border:1px solid #9472b4;border-radius:12px;background:linear-gradient(135deg,#37204f,#171122);">
    <p style="margin:0;color:#f1d88d;font-size:.72rem;letter-spacing:.2em;text-transform:uppercase;">Nexus Arcana · Agence immobilière</p>
    <h1 style="margin:.5rem 0;color:#fff0ba;font-size:2rem;">Trouver son lieu de vie</h1>
    <p style="margin:0;color:#ded0ed;">Quatre villes, mille façons d'habiter le crossover.</p>
  </header>

  <section style="margin:1.3rem 0;padding:1.2rem 1.4rem;border:1px solid #69527d;border-radius:10px;background:#21172e;">
    <h2 style="margin:0 0 .6rem;color:#f1d88d;font-size:1.2rem;">Comment s'installer ?</h2>
    <p style="margin:.4rem 0;">Après validation de votre fiche de personnage, répondez à ce sujet avec le formulaire ci-dessous. Votre réponse suffit pour situer votre logement et commencer à l'utiliser en RP.</p>
    <p style="margin:.4rem 0;">Les villes et quartiers proposés sont des pistes d'ambiance, jamais des restrictions de race ou de camp. Vous pouvez choisir un autre quartier, inventer une rue ou proposer une colocation, tant que le lieu reste cohérent avec l'univers. Le staff échangera avec vous seulement si un détail nécessite un ajustement.</p>
    <p style="margin:.4rem 0;">Le budget peut nourrir votre histoire, mais aucun prix ni achat n'est requis pour faire cette demande.</p>
  </section>

  <h2 style="margin:1.7rem 0 .8rem;color:#f1d88d;font-size:1.3rem;">Les villes du Nexus</h2>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:.8rem;">
    <section style="padding:1rem;border:1px solid #765698;border-top:3px solid #b788ea;border-radius:9px;background:#20152c;">
      <h3 style="margin:0 0 .4rem;color:#e5c5ff;">San Francisco</h3>
      <p style="margin:0;">Le cœur de l'héritage Charmed : maisons victoriennes, magie discrète, Manoir et passages vers d'autres mondes.</p>
    </section>
    <section style="padding:1rem;border:1px solid #765698;border-top:3px solid #bf687c;border-radius:9px;background:#20152c;">
      <h3 style="margin:0 0 .4rem;color:#f2b7c5;">Mystic Falls</h3>
      <p style="margin:0;">Une petite ville où les lignées, les souvenirs et les secrets surnaturels se croisent au quotidien.</p>
    </section>
    <section style="padding:1rem;border:1px solid #765698;border-top:3px solid #d3a24c;border-radius:9px;background:#20152c;">
      <h3 style="margin:0 0 .4rem;color:#f2d49e;">La Nouvelle-Orléans</h3>
      <p style="margin:0;">Rues vivantes, vieilles demeures et alliances mouvantes : chaque voisinage a sa propre histoire.</p>
    </section>
    <section style="padding:1rem;border:1px solid #765698;border-top:3px solid #78b98c;border-radius:9px;background:#20152c;">
      <h3 style="margin:0 0 .4rem;color:#bce3c6;">Beacon Hills</h3>
      <p style="margin:0;">Entre quartiers résidentiels et forêt, la ville attire celles et ceux que les mystères du Nemeton appellent.</p>
    </section>
  </div>

  <section style="margin:1.5rem 0;padding:1.2rem 1.4rem;border:1px solid #69527d;border-radius:10px;background:#21172e;">
    <h2 style="margin:0 0 .6rem;color:#f1d88d;font-size:1.2rem;">Quelques ambiances à San Francisco</h2>
    <ul style="margin:0;padding-left:1.2rem;">
      <li><strong>Prescott Street :</strong> maisons victoriennes et présence magique familière.</li>
      <li><strong>Tenderloin :</strong> rues animées, vies entremêlées et anonymat possible.</li>
      <li><strong>Noe Valley :</strong> jardins, familles et tranquillité derrière les façades.</li>
      <li><strong>Presidio Heights :</strong> grandes propriétés, vues sur la baie et apparences soignées.</li>
      <li><strong>Bayview–Hunters Point :</strong> passé industriel, ateliers, entrepôts reconvertis et nouveaux départs.</li>
    </ul>
    <p style="margin:.7rem 0 0;">Ces ambiances n'imposent ni alignement ni type de personnage. Les autres quartiers restent ouverts à vos idées.</p>
  </section>

  <section style="margin:1.5rem 0;padding:1.2rem 1.4rem;border:1px solid #69527d;border-radius:10px;background:#21172e;">
    <h2 style="margin:0 0 .6rem;color:#f1d88d;font-size:1.2rem;">Secteurs de Mystic Falls</h2>
    <ul style="margin:0;padding-left:1.2rem;">
      <li><strong>Le centre-ville :</strong> commerces, cafés et vie locale où les visages finissent toujours par se reconnaître.</li>
      <li><strong>Les rues historiques :</strong> maisons anciennes, jardins clos et histoires de famille transmises de génération en génération.</li>
      <li><strong>Les abords du lycée :</strong> petites maisons et appartements pratiques pour les jeunes adultes et les familles.</li>
      <li><strong>La lisière des bois :</strong> demeures plus isolées, sentiers et voisinage discret.</li>
      <li><strong>La campagne alentour :</strong> fermes, domaines et logements éloignés du centre.</li>
    </ul>
  </section>

  <section style="margin:1.5rem 0;padding:1.2rem 1.4rem;border:1px solid #69527d;border-radius:10px;background:#21172e;">
    <h2 style="margin:0 0 .6rem;color:#f1d88d;font-size:1.2rem;">Quartiers de La Nouvelle-Orléans</h2>
    <ul style="margin:0;padding-left:1.2rem;">
      <li><strong>Le Vieux Carré :</strong> balcons ouvragés, cours intérieures et rues animées jusque tard dans la nuit.</li>
      <li><strong>Le Garden District :</strong> grandes demeures, jardins ombragés et façades chargées d'histoire.</li>
      <li><strong>Faubourg Marigny :</strong> maisons colorées, musique et vie de quartier à quelques rues du centre.</li>
      <li><strong>Bywater :</strong> ateliers, anciennes bâtisses et espaces à réinventer.</li>
      <li><strong>Les rives du Mississippi :</strong> entrepôts réhabilités, quais et logements tournés vers le fleuve.</li>
    </ul>
  </section>

  <section style="margin:1.5rem 0;padding:1.2rem 1.4rem;border:1px solid #69527d;border-radius:10px;background:#21172e;">
    <h2 style="margin:0 0 .6rem;color:#f1d88d;font-size:1.2rem;">Secteurs de Beacon Hills</h2>
    <ul style="margin:0;padding-left:1.2rem;">
      <li><strong>Le centre-ville :</strong> commerces et appartements proches de l'agitation quotidienne.</li>
      <li><strong>Les abords du lycée :</strong> rues résidentielles, maisons familiales et lieux de rencontre des jeunes habitants.</li>
      <li><strong>Les hauteurs résidentielles :</strong> rues plus calmes et maisons à l'écart du centre.</li>
      <li><strong>La lisière de la réserve :</strong> chalets et maisons isolées, près des sentiers et des mystères de la forêt.</li>
      <li><strong>La périphérie :</strong> ateliers, motels et habitations de passage pour ceux qui préfèrent garder leur liberté.</li>
    </ul>
    <p style="margin:.7rem 0 0;">Ces secteurs servent de repères de jeu : chacun peut aussi proposer une autre adresse cohérente avec la ville.</p>
  </section>

  <section style="margin:1.5rem 0;padding:1.3rem;border:1px solid #a786c1;border-radius:10px;background:#291b39;">
    <h2 style="margin:0 0 .5rem;color:#f1d88d;font-size:1.2rem;">Modèle à copier dans votre réponse</h2>
    <p style="margin:0 0 .6rem;">Quelques lignes suffisent ; les détails de votre logement pourront évoluer au fil des RP.</p>
    <pre style="white-space:pre-wrap;overflow-wrap:anywhere;margin:0;padding:1rem;border-radius:7px;background:#140f1d;color:#eee2f6;font:inherit;">Personnage :
Ville :
Quartier ou lieu souhaité :
Type de logement :
Personnes avec qui il vit (facultatif) :
Une phrase sur ce lieu (facultatif) :</pre>
  </section>
</div>
""".strip()


class Command(BaseCommand):
    help = "Publie la version crossover du guide de l'agence immobilière."

    def handle(self, *args, **options):
        category = Category.objects.get(slug="agence-immobiliere")
        category.description = (
            "Choisissez votre lieu de vie à San Francisco, Mystic Falls, "
            "La Nouvelle-Orléans ou Beacon Hills."
        )
        category.save(update_fields=["description"])
        Category.objects.filter(slug="ma-situation-magique").update(
            description="Choisissez votre lieu de vie à travers les villes du Nexus et découvrez les objets magiques."
        )
        topic = Topic.objects.get(slug="agence-immobiliere-demande-de-logement", category=category)
        post = topic.posts.order_by("created_at", "pk").first()
        if not post:
            raise RuntimeError("Le sujet de l'agence ne contient aucun message à mettre à jour.")
        post.content = HOUSING_GUIDE
        post.save(update_fields=["content", "updated_at"])
        self.stdout.write(self.style.SUCCESS("Guide de l'agence immobilière mis à jour."))
