from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("forum", "0006_add_category_parent"),
    ]

    operations = [
        migrations.AddField(
            model_name="topic",
            name="scenario_status",
            field=models.CharField(
                choices=[("free", "Libre"), ("reserved", "Réservé"), ("played", "Joué")],
                default="free",
                help_text="Statut réservé aux scénarios à prendre.",
                max_length=10,
            ),
        ),
    ]
