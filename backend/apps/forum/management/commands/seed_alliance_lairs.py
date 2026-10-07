"""Create RP locations for the five covens and two crossover alliances."""

from django.core.management.base import BaseCommand

from apps.forum.models import Category


LAIRS = (
    ("Maison de la Seconde Soif", "repaire-maison-seconde-soif", "Refuge du coven d'Hérétiques de Mélissandre Barden, à Mystic Falls."),
    ("Chambre des Murmures", "repaire-chambre-murmures", "Salle de travail du coven de Belisama Vaskov, consacré à l'Expression."),
    ("Héritiers du Vide", "repaire-heritiers-vide", "Lieu de réunion des siphonneurs de Florie Delacroix."),
    ("Veilleurs du Voile", "repaire-veilleurs-voile", "Maison de rites du coven de Sélène Beauchamp, à La Nouvelle-Orléans."),
    ("Cercle des Terres Perdues", "repaire-cercle-terres-perdues", "Campement actuel des Voyageurs de Moira Osborne ; son emplacement peut évoluer en RP."),
    ("Meute de Beacon Hills", "repaire-meute-beacon-hills", "Point de ralliement de la meute près de la réserve et du Nemeton."),
    ("Gardiens de Mystic Falls", "repaire-gardiens-mystic-falls", "Quartier général de l'alliance chargée de protéger Mystic Falls."),
)


class Command(BaseCommand):
    help = "Crée les repaires RP des covens et des alliances crossover."

    def handle(self, *args, **options):
        parent, _ = Category.objects.update_or_create(
            slug="repaires-des-alliances",
            defaults={
                "name": "Repaires des alliances",
                "description": "Lieux de rencontre et refuges des covens, de la Meute de Beacon Hills et des Gardiens de Mystic Falls.",
                "order": 300,
            },
        )
        for order, (name, slug, description) in enumerate(LAIRS, start=301):
            Category.objects.update_or_create(
                slug=slug,
                defaults={"name": name, "description": description, "order": order, "parent": parent},
            )
        self.stdout.write(self.style.SUCCESS("Les sept repaires RP sont disponibles."))
