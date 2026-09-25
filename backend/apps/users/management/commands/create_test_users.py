"""
Commande de création d'utilisateurs de test répartis dans les groupes du forum.
Usage : python manage.py create_test_users
"""
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

User = get_user_model()

TEST_USERS = [
    # ── Le Pouvoir des Quatre ─────────────────────────────────────────────
    {
        "username": "Piper_Halliwell",
        "email": "piper@cercle.fr",
        "pseudo": "Piper des Flammes",
        "groupe": "Le Pouvoir des Quatre",
        "race": "Sorcière",
        "sexe": "feminin",
        "age_personnage": "32 ans",
        "pouvoirs": "Ralentissement du temps, explosion moléculaire",
        "lieu_residence": "Manor Halliwell, San Francisco",
        "bio": "Aînée des sœurs Halliwell, gardienne du foyer et du Livre des Ombres.",
        "situation": "Mariée, mère de deux enfants",
    },
    {
        "username": "Paige_Matthews",
        "email": "paige@cercle.fr",
        "pseudo": "Paige l'Orbe",
        "groupe": "Le Pouvoir des Quatre",
        "race": "Sorcière / Être de Lumière",
        "sexe": "feminin",
        "age_personnage": "26 ans",
        "pouvoirs": "Télékinésie orbitale, orbage",
        "lieu_residence": "San Francisco",
        "bio": "Quatrième sœur Charmed, demi-être de lumière au tempérament fougueux.",
        "situation": "Célibataire",
    },
    # ── Être de Lumière ───────────────────────────────────────────────────
    {
        "username": "Auriel_Bright",
        "email": "auriel@cercle.fr",
        "pseudo": "Auriel",
        "groupe": "Être de Lumière",
        "race": "Être de Lumière",
        "sexe": "masculin",
        "age_personnage": "Immortel (apparence : 35 ans)",
        "pouvoirs": "Guérison, orbage, bouclier de lumière",
        "lieu_residence": "Les Sphères célestes",
        "bio": "Guide et protecteur assigné aux sorcières du Cercle depuis des siècles.",
        "situation": "Lié à sa charge",
    },
    {
        "username": "Samuel_Veil",
        "email": "samuel@cercle.fr",
        "pseudo": "Sam le Veilleur",
        "groupe": "Être de Lumière",
        "race": "Être de Lumière",
        "sexe": "masculin",
        "age_personnage": "Immortel (apparence : 42 ans)",
        "pouvoirs": "Orbage, guérison, prescience",
        "lieu_residence": "Les Royaumes supérieurs",
        "bio": "Ancien être de lumière reconverti en sentinelle des frontières entre les mondes.",
        "situation": "Missionné par les Anciens",
    },
    # ── Sorcier ───────────────────────────────────────────────────────────
    {
        "username": "Nathanael_Storm",
        "email": "nathanael@cercle.fr",
        "pseudo": "Nath l'Orageux",
        "groupe": "Sorcier",
        "race": "Sorcier",
        "sexe": "masculin",
        "age_personnage": "28 ans",
        "pouvoirs": "Télékinésie, manipulation des éléments",
        "lieu_residence": "Bibliothèque secrète, Lyon",
        "bio": "Érudit de la magie runique, spécialiste des grimoires anciens.",
        "situation": "Apprenti des Fondateurs",
    },
    {
        "username": "Cassandra_Vex",
        "email": "cassandra@cercle.fr",
        "pseudo": "Cass la Mausolée",
        "groupe": "Sorcier",
        "race": "Sorcière",
        "sexe": "feminin",
        "age_personnage": "24 ans",
        "pouvoirs": "Divination, lancement de sorts",
        "lieu_residence": "Nouvelle-Orléans",
        "bio": "Héritière d'une lignée de voyantes, capable de lire les fils du destin.",
        "situation": "En exil volontaire",
    },
    {
        "username": "Marcus_Blackthorn",
        "email": "marcus@cercle.fr",
        "pseudo": "Marcus de la Nuit",
        "groupe": "Sorcier",
        "race": "Sorcier",
        "sexe": "masculin",
        "age_personnage": "45 ans",
        "pouvoirs": "Magie noire maîtrisée, boucliers",
        "lieu_residence": "Manoir des Ombres, Écosse",
        "bio": "Ancien pratiquant de magie sombre reconverti, enseigne l'équilibre entre les forces.",
        "situation": "Maître enseignant",
    },
    # ── Fée ───────────────────────────────────────────────────────────────
    {
        "username": "Sylvana_Dew",
        "email": "sylvana@cercle.fr",
        "pseudo": "Sylvana",
        "groupe": "Fée",
        "race": "Fée",
        "sexe": "feminin",
        "age_personnage": "Plusieurs siècles (apparence : 19 ans)",
        "pouvoirs": "Magie naturelle, communication avec les plantes",
        "lieu_residence": "Forêt de Brocéliande",
        "bio": "Gardienne de la forêt ancestrale, protège l'équilibre de la nature magique.",
        "situation": "Gardienne solitaire",
    },
    {
        "username": "Iris_Petal",
        "email": "iris@cercle.fr",
        "pseudo": "Iris",
        "groupe": "Fée",
        "race": "Fée",
        "sexe": "feminin",
        "age_personnage": "Plusieurs siècles (apparence : 22 ans)",
        "pouvoirs": "Illusions florales, charmes de protection",
        "lieu_residence": "Jardin enchanté, Irlande",
        "bio": "Fée des jardins, tisse des sortilèges de paix et de guérison pour les innocents.",
        "situation": "Alliée des sorcières",
    },
    # ── Vampire ───────────────────────────────────────────────────────────
    {
        "username": "Viktor_Noir",
        "email": "viktor@cercle.fr",
        "pseudo": "Viktor",
        "groupe": "Vampire",
        "race": "Vampire",
        "sexe": "masculin",
        "age_personnage": "Immortel (apparence : 38 ans, né en 1642)",
        "pouvoirs": "Force surhumaine, vitesse, hypnose",
        "lieu_residence": "Château de Valmont, Carpates",
        "bio": "L'un des vampires les plus anciens d'Europe, observe les conflits entre bien et mal depuis des siècles.",
        "situation": "Neutre, observateur",
        "compte_bancaire": 15000,
    },
    {
        "username": "Seraphine_Blood",
        "email": "seraphine@cercle.fr",
        "pseudo": "Séraphine",
        "groupe": "Vampire",
        "race": "Vampire",
        "sexe": "feminin",
        "age_personnage": "Immortelle (apparence : 27 ans, née en 1889)",
        "pouvoirs": "Séduction mystique, vol, régénération",
        "lieu_residence": "Appartement secret, Paris",
        "bio": "Chasseuse de démons, utilise sa nature de vampire pour protéger les innocents.",
        "situation": "Alliée ambiguë",
    },
    # ── Démon ─────────────────────────────────────────────────────────────
    {
        "username": "Shax_Vengeance",
        "email": "shax@cercle.fr",
        "pseudo": "Shax",
        "groupe": "Démon",
        "race": "Démon",
        "sexe": "masculin",
        "age_personnage": "Immémorial",
        "pouvoirs": "Vents tranchants, invisibilité, téléportation",
        "lieu_residence": "Inframonde",
        "bio": "Assassin de la Source, envoyé pour éliminer les sorcières Charmed.",
        "situation": "Agent de la Source",
    },
    {
        "username": "Barbas_Terreur",
        "email": "barbas@cercle.fr",
        "pseudo": "Barbas",
        "groupe": "Démon",
        "race": "Démon",
        "sexe": "masculin",
        "age_personnage": "Immémorial",
        "pouvoirs": "Lecture des peurs, projection des pires cauchemars",
        "lieu_residence": "Limbes de la peur",
        "bio": "Démon de la peur, capable de plonger ses victimes dans leurs terreurs les plus profondes.",
        "situation": "Indépendant",
    },
    # ── Loup-garou ────────────────────────────────────────────────────────
    {
        "username": "Fenris_Moon",
        "email": "fenris@cercle.fr",
        "pseudo": "Fenris",
        "groupe": "Loup-garou",
        "race": "Loup-garou",
        "sexe": "masculin",
        "age_personnage": "31 ans",
        "pouvoirs": "Transformation lupine, force, régénération rapide",
        "lieu_residence": "Forêts du Nord, Norvège",
        "bio": "Alpha de sa meute, cherche à maintenir la paix entre sa communauté et le monde des sorcières.",
        "situation": "Alpha de meute",
    },
    # ── Hybride ───────────────────────────────────────────────────────────
    {
        "username": "Eliara_Dusk",
        "email": "eliara@cercle.fr",
        "pseudo": "Eliara",
        "groupe": "Hybride",
        "race": "Sorcière / Fée",
        "sexe": "feminin",
        "age_personnage": "23 ans",
        "pouvoirs": "Magie runique, magie de la nature, aura de protection",
        "lieu_residence": "Lisière de la Forêt Enchantée",
        "bio": "Née d'une sorcière et d'une fée, sa double nature lui confère des pouvoirs rares mais instables.",
        "situation": "En quête de maîtrise",
    },
    # ── Les veilleurs de l'aube ────────────────────────────────────────────
    {
        "username": "Eos_Sentinel",
        "email": "eos@cercle.fr",
        "pseudo": "Eos",
        "groupe": "Les veilleurs de l'aube",
        "race": "Sorcier",
        "sexe": "feminin",
        "age_personnage": "38 ans",
        "pouvoirs": "Prescience, boucliers de lumière",
        "lieu_residence": "Tour de l'Aube, Avignon",
        "bio": "Cheffe de section des Veilleurs, coordonne la surveillance des brèches entre les mondes.",
        "situation": "En mission active",
    },
    {
        "username": "Dawner_Bright",
        "email": "dawner@cercle.fr",
        "pseudo": "Dawner",
        "groupe": "Les veilleurs de l'aube",
        "race": "Être de Lumière",
        "sexe": "masculin",
        "age_personnage": "Immortel (apparence : 30 ans)",
        "pouvoirs": "Vision nocturne totale, communication télépathique",
        "lieu_residence": "Poste de guet des Alpes",
        "bio": "Ancien être de lumière ayant rejoint les Veilleurs pour mieux protéger le monde des mortels.",
        "situation": "Éclaireur de première ligne",
    },
    # ── Les Fondateurs ────────────────────────────────────────────────────
    {
        "username": "Laury Evans",
        "email": "laury.evans@cercle.fr",
        "pseudo": "Laury Evans",
        "groupe": "Les Fondateurs",
        "race": "Sorcier",
        "sexe": "feminin",
        "age_personnage": "29 ans",
        "pouvoirs": "Magie ancienne, divination, invocation des arcanes primordiaux",
        "lieu_residence": "Siège des Fondateurs, Genève",
        "bio": "Membre éminente du Conseil des Fondateurs, Laury Evans est une sorcière d'élite dont la maîtrise des arcanes anciens en fait l'une des gardiennes les plus redoutées des lois magiques.",
        "situation": "Conseillère active des Fondateurs",
        "metier": "Gardienne des lois magiques",
        "camp": "Bien",
        "nature": "Sorcière de haut rang",
    },
    # ── Élfe ─────────────────────────────────────────────────────────────
    {
        "username": "Aelindra_Silver",
        "email": "aelindra@cercle.fr",
        "pseudo": "Aelindra",
        "groupe": "Elfe",
        "race": "Elfe",
        "sexe": "feminin",
        "age_personnage": "Millénaire (apparence : 25 ans)",
        "pouvoirs": "Archerie magique, communion avec la nature, perception accrue",
        "lieu_residence": "Bois Argentés, Bretagne",
        "bio": "Archère et gardienne des frontières, veille à ce qu'aucune entité démoniaque ne franchisse les lisières.",
        "situation": "Gardienne des lisières",
    },
]

class Command(BaseCommand):
    help = "Crée des utilisateurs de test répartis dans les groupes du forum."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Supprime les utilisateurs de test existants avant de les recréer.",
        )

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError("La création de comptes de test est réservée au développement.")
        password = os.environ.get("TEST_USERS_PASSWORD")
        if not password:
            raise CommandError("Définissez TEST_USERS_PASSWORD pour créer les comptes de test.")

        if options["reset"]:
            deleted, _ = User.objects.filter(
                email__endswith="@cercle.fr"
            ).delete()
            self.stdout.write(self.style.WARNING(f"[DEL] {deleted} utilisateur(s) supprime(s)."))

        created_count = 0
        skipped_count = 0

        for data in TEST_USERS:
            username = data["username"]

            if User.objects.filter(username=username).exists():
                self.stdout.write(f"  [SKIP] {username} existe deja.")
                skipped_count += 1
                continue

            user = User(
                username=username,
                email=data.get("email", f"{username.lower()}@cercle.fr"),
                pseudo=data.get("pseudo", ""),
                groupe=data.get("groupe", ""),
                race=data.get("race", ""),
                sexe=data.get("sexe", ""),
                age_personnage=data.get("age_personnage", ""),
                pouvoirs=data.get("pouvoirs", ""),
                lieu_residence=data.get("lieu_residence", ""),
                bio=data.get("bio", ""),
                situation=data.get("situation", ""),
                metier=data.get("metier", ""),
                camp=data.get("camp", ""),
                nature=data.get("nature", ""),
                compte_bancaire=data.get("compte_bancaire", 0),
            )
            user.set_password(password)
            user.save()

            self.stdout.write(
                self.style.SUCCESS(f"  [OK] {username} -> {data.get('groupe', '-')}")
            )
            created_count += 1

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"[DONE] {created_count} utilisateur(s) cree(s), {skipped_count} ignore(s)."
            )
        )
        self.stdout.write("[PWD] Mot de passe défini par TEST_USERS_PASSWORD.")
