from django.core.management.base import BaseCommand

from apps.forum.models import Category


CATEGORIES = [
    # ── Catégories principales ──────────────────────────────────────────────
    {
        "name": "Bienvenue à Nexus Arcana",
        "slug": "bienvenue-san-francisco",
        "description": "Entrez dans le crossover, créez votre personnage et découvrez les scénarios disponibles.",
        "order": 1,
    },
    {
        "name": "Scénarios à prendre",
        "slug": "scenarios-a-prendre",
        "description": "Personnages et histoires disponibles à incarner.",
        "order": 2,
    },
    {
        "name": "Modèle fiche de présentation",
        "slug": "modele-fiche-de-presentation",
        "description": "Template officiel pour créer votre personnage.",
        "order": 3,
    },
    {
        "name": "Fiches en attente de validation",
        "slug": "fiches-de-presentation-terminees",
        "description": "Présentations en cours de validation, ouvertes aux messages de bienvenue.",
        "order": 4,
    },
    # ── Règlement & Grimoire ────────────────────────────────────────────────
    {
        "name": "Règlement magique et grimoires ancestraux",
        "slug": "reglement-magique",
        "description": "Les lois et savoirs fondamentaux du Nexus Arcana.",
        "order": 5,
    },
    {
        "name": "Règlement du forum",
        "slug": "reglement-du-forum",
        "description": "Les lois fondamentales du Cercle.",
        "order": 6,
    },
    {
        "name": "Créatures et races",
        "slug": "creatures-et-races",
        "description": "Encyclopédie des êtres magiques.",
        "order": 7,
    },
    {
        "name": "Factions",
        "slug": "factions",
        "description": "Alliances, clans et ordres secrets.",
        "order": 8,
    },
    {
        "name": "Bottin des avatars",
        "slug": "bottin-des-avatars",
        "description": "Registre officiel des célébrités.",
        "order": 9,
    },
    {
        "name": "Bottin des formes démoniaques",
        "slug": "bottin-des-formes-demoniaques",
        "description": "Répertoire des apparences démoniaques.",
        "order": 10,
    },
    {
        "name": "Contextes et animations",
        "slug": "contextes-et-animations",
        "description": "Événements et fils narratifs actifs.",
        "order": 11,
    },
    # ── Liens magiques ──────────────────────────────────────────────────────
    {
        "name": "Liens magiques",
        "slug": "liens-magiques",
        "description": "Recherches de partenaires RP et fiches personnages.",
        "order": 12,
    },
    {
        "name": "Recherche de RP",
        "slug": "recherche-de-rp",
        "description": "Trouvez des partenaires pour vos aventures roleplay.",
        "order": 13,
    },
    {
        "name": "Fiche personnage",
        "slug": "fiche-personnage",
        "description": "Carnets récapitulatifs des personnages validés, tenus à jour par leurs joueurs.",
        "order": 14,
    },
    {
        "name": "Demande de partenaire RP",
        "slug": "demande-partenaire-rp",
        "description": "Postez vos annonces pour trouver un partenaire de roleplay.",
        "order": 15,
    },
    # ── Ma situation magique ─────────────────────────────────────────────────
    {
        "name": "Ma situation magique",
        "slug": "ma-situation-magique",
        "description": "Choisissez votre lieu de vie à travers les villes du Nexus et découvrez les objets magiques.",
        "order": 16,
    },
    {
        "name": "Agence immobilière",
        "slug": "agence-immobiliere",
        "description": "Choisissez votre lieu de vie à San Francisco, Mystic Falls, La Nouvelle-Orléans ou Beacon Hills.",
        "order": 17,
    },
    {
        "name": "La boutique magique",
        "slug": "boutique-magique",
        "description": "Achetez des objets magiques, potions et cristaux.",
        "order": 18,
    },
    # ── Une question ? ──────────────────────────────────────────────────────
    {
        "name": "Une question ?",
        "slug": "une-question",
        "description": "Posez vos questions, signalez une absence ou contactez l'équipe.",
        "order": 16,
    },
    {
        "name": "Questions invités",
        "slug": "questions-invites",
        "description": "Vous n'êtes pas encore membre ? Posez vos questions ici.",
        "order": 17,
    },
    {
        "name": "Questions membres",
        "slug": "questions-membres",
        "description": "Vous êtes membre du Cercle ? Posez vos questions à l'équipe.",
        "order": 18,
    },
    {
        "name": "Nous signaler une absence",
        "slug": "signaler-absence",
        "description": "Prévenez l'équipe de votre absence ou retour.",
        "order": 19,
    },
    # ── Quartiers résidentiels ───────────────────────────────────────────────
    {
        "name": "Quartiers résidentiels",
        "slug": "quartiers-residentiels",
        "description": "Les quartiers de San Francisco où se déroulent vos aventures RP.",
        "order": 20,
    },
    {
        "name": "Prescott Street",
        "slug": "prescott-street",
        "description": "La rue emblématique du Nexus Arcana.",
        "order": 21,
    },
    {
        "name": "Tenderloin",
        "slug": "tenderloin",
        "description": "Un quartier populaire aux ruelles animées.",
        "order": 22,
    },
    {
        "name": "Bayview-Hunters",
        "slug": "bayview-hunters",
        "description": "Quartier industriel en bord de baie.",
        "order": 23,
    },
    {
        "name": "Noe Valley",
        "slug": "noe-valley",
        "description": "Quartier résidentiel paisible aux maisons victoriennes.",
        "order": 24,
    },
    {
        "name": "Presidio Heights",
        "slug": "presidio-heights",
        "description": "Quartier huppé surplombant la baie de San Francisco.",
        "order": 25,
    },
    {
        "name": "Bayview",
        "slug": "bayview",
        "description": "Quartier en bord de baie, entre passé industriel et renouveau.",
        "order": 26,
    },
]


class Command(BaseCommand):
    help = "Crée toutes les catégories du forum si elles n'existent pas déjà."

    def handle(self, *args, **options):
        created_count = 0
        for data in CATEGORIES:
            obj, created = Category.objects.get_or_create(
                slug=data["slug"],
                defaults={
                    "name": data["name"],
                    "description": data["description"],
                    "order": data["order"],
                },
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"  ✓ Créée : {obj.name}"))
                created_count += 1
            else:
                if data["slug"] == "fiche-personnage" and obj.description != data["description"]:
                    obj.description = data["description"]
                    obj.save(update_fields=["description"])
                self.stdout.write(f"  — Déjà existante : {obj.name}")

        self.stdout.write(
            self.style.SUCCESS(f"\n{created_count} catégorie(s) créée(s) sur {len(CATEGORIES)} au total.")
        )
