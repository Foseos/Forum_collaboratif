from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("forum", "0008_rename_welcome_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="topic",
            name="scenario_links",
            field=models.TextField(
                blank=True,
                default="",
                help_text="Liens, relations et pistes de jeu du scénario.",
            ),
        ),
    ]
