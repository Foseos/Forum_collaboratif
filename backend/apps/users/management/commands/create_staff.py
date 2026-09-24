"""
Commande de création des comptes staff (fondatrice, admins, modérateurs).
Usage : python manage.py create_staff
        python manage.py create_staff --reset   (supprime et recrée)
"""
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

User = get_user_model()

STAFF_MEMBERS = [
    {
        "username": "Ava Bartholomé",
        "email": None,
        "pseudo": "",
        "role": "fondatrice",
        "bio": "Fondatrice du Nexus Arcana. Elle veille sur l'équilibre du forum depuis ses origines.",
        "groupe": "",
        "race": "Sorcière",
        "sexe": "feminin",
    },
    {
        "username": "AdminPrincipal",
        "email": "gideon@cercle.fr",
        "pseudo": "Gidéon",
        "role": "admin",
        "bio": "Administrateur principal du Cercle.",
        "groupe": "",
        "race": "Être de Lumière",
        "sexe": "masculin",
    },
    {
        "username": "Modo1",
        "email": "zankou@cercle.fr",
        "pseudo": "Zankou",
        "role": "moderator",
        "bio": "Modérateur, gardien de l'ordre dans l'Inframonde.",
        "groupe": "",
        "race": "Démon",
        "sexe": "masculin",
    },
    {
        "username": "Modo2",
        "email": "leo@cercle.fr",
        "pseudo": "Leo Wyatt",
        "role": "moderator",
        "bio": "Modérateur et être de lumière protecteur.",
        "groupe": "",
        "race": "Être de Lumière",
        "sexe": "masculin",
    },
]

class Command(BaseCommand):
    help = "Crée les comptes staff du forum (fondatrice, admins, modérateurs)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Supprime les comptes staff existants avant de les recréer.",
        )

    def handle(self, *args, **options):
        password = os.environ.get('STAFF_INITIAL_PASSWORD')
        founder_email = os.environ.get('FOUNDER_EMAIL')
        if not password or not founder_email:
            raise CommandError('Définissez STAFF_INITIAL_PASSWORD et FOUNDER_EMAIL avant de créer les comptes du staff.')

        if options["reset"]:
            usernames = [m["username"] for m in STAFF_MEMBERS]
            deleted, _ = User.objects.filter(username__in=usernames).delete()
            self.stdout.write(self.style.WARNING(f"[DEL] {deleted} compte(s) staff supprimé(s)."))

        created = 0
        skipped = 0

        for data in STAFF_MEMBERS:
            username = data["username"]

            if User.objects.filter(username=username).exists():
                self.stdout.write(f"  [SKIP] {username} existe déjà.")
                skipped += 1
                continue

            user = User(
                username=username,
                email=founder_email if data['role'] == 'fondatrice' else data['email'],
                pseudo=data.get("pseudo", ""),
                role=data["role"],
                bio=data.get("bio", ""),
                groupe=data.get("groupe", ""),
                race=data.get("race", ""),
                sexe=data.get("sexe", ""),
                is_staff=(data["role"] in ("fondatrice", "admin")),
                is_superuser=(data["role"] == "fondatrice"),
            )
            user.set_password(password)
            user.save()

            self.stdout.write(
                self.style.SUCCESS(f"  [OK] {username} ({data['role']}) — {data['pseudo']}")
            )
            created += 1

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(f"[DONE] {created} compte(s) créé(s), {skipped} ignoré(s).")
        )
