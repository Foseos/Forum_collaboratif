"""Align the live Grimoire with its current power creation rules."""

import json
import re
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from apps.forum.models import Topic


CHAPTERS = (
    ("VI", "VIII", "Magies et disciplines du crossover"),
    ("VII", "IX", "Vampires, loups et héritages hybrides"),
    ("VIII", "X", "Créatures singulières"),
    ("IX", "XI", "Règles d'évolution et limites"),
    ("X", "XII", "Pouvoirs psychiques, médiumniques et émotionnels"),
    ("XI", "XIII", "Pouvoirs physiques, moléculaires et de soin"),
    ("XII", "XIV", "Éléments, énergie et matière"),
    ("XIII", "XV", "Déplacement, espace et rituels"),
    ("XIV", "XVI", "Pouvoirs innés par race"),
)


class Command(BaseCommand):
    help = "Corrige les règles d'introduction et la numérotation du Grimoire publié."

    @transaction.atomic
    def handle(self, *args, **options):
        topic = Topic.objects.select_for_update().get(slug="liste-des-pouvoirs-magiques")
        post = topic.posts.select_for_update().order_by("created_at", "pk").first()
        if post is None:
            raise CommandError("Le Grimoire ne contient aucun message.")

        content = post.content
        if "<!-- SECTION : POUVOIRS EXCLUSIFS" in content:
            raise CommandError("Le bloc des pouvoirs exclusifs doit être supprimé d'abord.")

        replacements = (
            (
                "Ce grimoire recense l'ensemble des pouvoirs disponibles sur le forum.",
                "Ce grimoire ne recense ni tous les pouvoirs ni toutes leurs évolutions possibles. Vous pouvez proposer un pouvoir ou une évolution au staff et en discuter avec l'équipe avant de l'intégrer à votre fiche ou de l'utiliser en RP.",
            ),
            (
                "Ce grimoire présente des exemples de pouvoirs et d'évolutions possibles ; il ne recense pas toutes les possibilités. Vous pouvez proposer un autre pouvoir au staff et en discuter avec l'équipe avant de l'intégrer à votre fiche ou de l'utiliser en RP.",
                "Ce grimoire ne recense ni tous les pouvoirs ni toutes leurs évolutions possibles. Vous pouvez proposer un pouvoir ou une évolution au staff et en discuter avec l'équipe avant de l'intégrer à votre fiche ou de l'utiliser en RP.",
            ),
            (
                "Chaque pouvoir peut évoluer selon l'expérience acquise en RP et avec l'accord du staff.",
                "Une évolution exige un achat en Arcana Flouz et la validation du staff avant son utilisation ; aucun RP justificatif n’est demandé.",
            ),
            (
                "Les pouvoirs de départ sont libres dans la limite de la cohérence avec votre race et votre camp.",
                "À la création, chaque personnage choisit quatre capacités maximum, actives et passives comprises, cohérentes avec sa nature et validées dans sa fiche. Les capacités et évolutions supplémentaires s'acquièrent ensuite en jeu selon les règles de la boutique.",
            ),
            (
                "Les pouvoirs sans marquage sont libres à la création du personnage (dans la limite de la cohérence de la race et du camp).",
                "Les pouvoirs sans marquage restent soumis au plafond de quatre capacités à la création et à la validation de la fiche.",
            ),
            (
                "Tout abus ou utilisation non validée d'un pouvoir ★ pourra entraîner un recadrage ou une sanction.",
                "Une nouvelle capacité ou une évolution s'acquiert en jeu selon les règles de la boutique ; ce catalogue n'accorde aucun pouvoir automatiquement.",
            ),
        )
        for old, new in replacements:
            content = content.replace(old, new)
        friendly_note = "En cas de doute, échangez avec le staff pour trouver ensemble une manière de jouer votre idée."
        if friendly_note not in content:
            content = content.replace(
                "ce catalogue n'accorde aucun pouvoir automatiquement.",
                "ce catalogue n'accorde aucun pouvoir automatiquement. " + friendly_note,
            )

        for old_number, new_number, title in CHAPTERS:
            content = content.replace(f">{old_number}. {title}</h2>", f">{new_number}. {title}</h2>")
        content = content.replace(
            ">XVI. Pouvoirs innés par race</h2>",
            ">XVI. Affinités et limites selon les races</h2>",
        )

        if content == post.content:
            self.stdout.write("Le Grimoire est déjà à jour.")
            return

        headings = re.findall(r"([IVX]+)\. ([^<]+)</h2>", content)
        numbers = [number for number, _ in headings]
        expected = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV", "XVI"]
        if numbers != expected:
            raise CommandError(f"Numérotation inattendue : {numbers}")

        backup_dir = Path(settings.BASE_DIR) / "data" / "scenario_backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup_path = backup_dir / ("grimoire-reconcile-" + timezone.now().strftime("%Y%m%dT%H%M%S%f") + ".json")
        backup_path.write_text(
            json.dumps({"topic_id": topic.pk, "post_id": post.pk, "content": post.content}, ensure_ascii=False),
            encoding="utf-8",
        )
        post.content = content
        post.save(update_fields=["content", "is_edited", "updated_at"])
        self.stdout.write(self.style.SUCCESS("Grimoire corrigé : règles et chapitres I à XVI."))
