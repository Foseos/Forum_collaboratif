from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("forum", "0009_topic_scenario_links"),
    ]

    operations = [
        migrations.AddField(
            model_name="topic",
            name="scenario_link_cards",
            field=models.JSONField(
                blank=True,
                default=list,
                help_text="Cartes GIF et textes de survol pour les liens du scénario.",
            ),
        ),
    ]
