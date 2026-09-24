from django.core.management.base import BaseCommand

from apps.forum.models import Category


CROSSOVER_CITIES = [
    # Mystic Falls — The Vampire Diaries & Legacies
    ("Mystic Falls", "mystic-falls", "Une ville de secrets, de lignées et de magie ancestrale.", 70),
    ("Centre de Mystic Falls", "centre-mystic-falls", "La place, le Mystic Grill et les rues où tout le monde se croise.", 71),
    ("École Salvatore", "ecole-salvatore", "Un refuge pour les jeunes créatures surnaturelles.", 72),
    ("Cimetière et l'église des Fell", "cimetiere-eglise-fell", "Des sépultures anciennes et des archives familiales.", 73),
    ("Les bois de Mystic Falls", "bois-mystic-falls", "Le Wickery Bridge, les cascades et les sentiers hantés.", 74),
    ("Quartier résidentiel de Mystic Falls", "quartier-residentiel-mystic-falls", "Maisons de familles fondatrices, rues tranquilles et secrets derrière chaque portail.", 75),
    ("Rues historiques de Mystic Falls", "rues-historiques-mystic-falls", "Maisons anciennes, jardins clos et histoires des familles de la ville.", 75),
    ("Abords du lycée de Mystic Falls", "abords-lycee-mystic-falls", "Maisons et appartements proches de la vie scolaire.", 75),
    ("Campagne de Mystic Falls", "campagne-mystic-falls", "Fermes, domaines et logements à l'écart du centre.", 75),
    # La Nouvelle-Orléans — The Originals
    ("La Nouvelle-Orléans", "la-nouvelle-orleans", "Une ville de musique, de pactes et de rivalités surnaturelles.", 76),
    ("Le Vieux Carré", "vieux-carre", "Le French Quarter, Jackson Square et les nuits sans fin.", 77),
    ("Le Bayou", "bayou", "Eaux sombres, rites anciens et territoires sauvages.", 78),
    ("Garden District", "garden-district", "Demeures ancestrales et jardins jalousement gardés.", 79),
    ("Les quais et les entrepôts", "quais-entrepots", "Le port, les marchés nocturnes et les repaires discrets.", 80),
    ("Quartiers résidentiels de La Nouvelle-Orléans", "quartiers-residentiels-nouvelle-orleans", "Maisons créoles, demeures anciennes et résidences à l'abri des regards.", 81),
    ("Faubourg Marigny", "faubourg-marigny", "Maisons colorées, musique et vie de quartier.", 81),
    ("Bywater", "bywater", "Ateliers, anciennes bâtisses et espaces à réinventer.", 81),
    # Beacon Hills — Teen Wolf
    ("Beacon Hills", "beacon-hills", "Une ville où le surnaturel rôde derrière chaque ombre.", 82),
    ("Centre-ville de Beacon Hills", "centre-beacon-hills", "Le lycée, le commissariat et la clinique vétérinaire.", 83),
    ("La réserve de Beacon Hills", "reserve-beacon-hills", "Le Nemeton, les sentiers et les vestiges de la maison Hale.", 84),
    ("Eichen House et l'hôpital", "eichen-house-hopital", "Couloirs médicaux, secrets enfermés et esprits troublés.", 85),
    ("Les environs", "environs-beacon-hills", "Routes isolées, terrains de crosse et lieux oubliés.", 86),
    ("Quartiers résidentiels de Beacon Hills", "quartiers-residentiels-beacon-hills", "Rues calmes, lotissements en lisière de forêt et maisons pleines de souvenirs.", 87),
    ("Abords du lycée de Beacon Hills", "abords-lycee-beacon-hills", "Rues familiales et lieux de rencontre des jeunes habitants.", 87),
    ("Hauteurs de Beacon Hills", "hauteurs-beacon-hills", "Rues résidentielles plus calmes à l'écart du centre.", 87),
    ("Lisière de la réserve de Beacon Hills", "lisiere-reserve-beacon-hills", "Chalets et maisons isolées près des sentiers forestiers.", 87),
    ("Périphérie de Beacon Hills", "peripherie-beacon-hills", "Ateliers, motels et habitations de passage.", 87),
]


class Command(BaseCommand):
    help = "Crée les espaces RP de Mystic Falls, La Nouvelle-Orléans et Beacon Hills."

    def handle(self, *args, **options):
        created_count = 0
        city = None
        for name, slug, description, order in CROSSOVER_CITIES:
            if slug in ('mystic-falls', 'la-nouvelle-orleans', 'beacon-hills'):
                parent = None
            else:
                parent = city
            category, created = Category.objects.get_or_create(
                slug=slug,
                defaults={"name": name, "description": description, "order": order, "parent": parent},
            )
            if category.parent_id != (parent.pk if parent else None):
                category.parent = parent
                category.save(update_fields=['parent'])
            if parent is None:
                city = category
            created_count += int(created)

        Category.objects.filter(slug='quais-entrepots').update(
            name='Rives du Mississippi',
            description='Quais, port et entrepôts réhabilités au bord du fleuve.',
        )

        self.stdout.write(
            self.style.SUCCESS(f"{created_count} espace(s) RP crossover créé(s).")
        )
