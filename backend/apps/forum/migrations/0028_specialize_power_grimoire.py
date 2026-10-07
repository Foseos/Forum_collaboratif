import json
import re
from html import escape

from django.db import migrations


OLD_INTRO = (
    "Chaque ligne suit le modèle <strong style=\"color:#e2d9f3;\">"
    "pouvoir de base → évolution → maîtrise</strong>. Les branches sont des pistes : "
    "un personnage n'a pas à toutes les posséder. Les mentions « staff » demandent "
    "une validation avant la fiche ou une évolution jouée."
)
NEW_INTRO = (
    "Chaque pouvoir de base propose des <strong style=\"color:#e2d9f3;\">"
    "options de spécialisation</strong>, et non une progression imposée. "
    "Une option améliore le pouvoir concerné ; elle ne donne pas automatiquement "
    "les autres options. Chaque achat exige la validation du staff."
)
OLD_ENTRIES = {
    "Accélération moléculaire → combustion → pyrokinésie": (
        "Accélération moléculaire → échauffement ciblé → propagation thermique limitée",
        "La chaleur reste liée à la cible et à la portée validées ; ce pouvoir ne donne pas automatiquement la pyrokinésie.",
    ),
    "Boule de feu → jet de flammes → mur de feu": (
        "Boule de feu → précision du projectile → maintien d'une flamme",
        "La précision améliore le tir ; le maintien prolonge une flamme limitée dans le temps. Aucun effet de zone n'est acquis automatiquement.",
    ),
}
ENTRY = re.compile(
    r"<li style='margin:0 0 0\.55rem;'><strong style='color:#e2d9f3;'>([^<]*→[^<]*)</strong> — ([^<]*)</li>"
)


def refresh_power_options(apps, schema_editor):
    Topic = apps.get_model("forum", "Topic")
    Post = apps.get_model("forum", "Post")
    topic = Topic.objects.filter(slug="liste-des-pouvoirs-magiques").first()
    if not topic:
        return
    post = Post.objects.filter(topic_id=topic.pk).order_by("created_at", "pk").first()
    if not post or "<!-- NEXUS-ARCANA-POWER-DIRECTORY -->" not in post.content:
        return

    def replace_entry(match):
        name, description = match.groups()
        if name in OLD_ENTRIES:
            name, description = OLD_ENTRIES[name]
        base, *options = (part.strip() for part in name.split("→"))
        options_attr = escape(json.dumps(options, ensure_ascii=False), quote=True)
        return (
            f"<li data-power-options=\"{options_attr}\" style='margin:0 0 0.55rem;'>"
            f"<strong style='color:#e2d9f3;'>{base}</strong> — "
            f"Pistes de spécialisation : {' ; '.join(options)}. {description}</li>"
        )

    prefix, marker, directory = post.content.partition("<!-- NEXUS-ARCANA-POWER-DIRECTORY -->")
    updated_directory = ENTRY.sub(replace_entry, directory).replace(OLD_INTRO, NEW_INTRO)
    if updated_directory != directory:
        post.content = prefix + marker + updated_directory
        post.save(update_fields=["content", "updated_at"])


class Migration(migrations.Migration):
    dependencies = [("forum", "0027_power_purchase")]

    operations = [migrations.RunPython(refresh_power_options, migrations.RunPython.noop)]
