from django.db import migrations


def rename_welcome_category(apps, schema_editor):
    Category = apps.get_model("forum", "Category")
    Category.objects.filter(slug="bienvenue-san-francisco").update(
        name="Bienvenue à Nexus Arcana",
        description="Entrez dans le crossover, créez votre personnage et découvrez les scénarios disponibles.",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("forum", "0007_topic_scenario_status"),
    ]

    operations = [
        migrations.RunPython(rename_welcome_category, migrations.RunPython.noop),
    ]
