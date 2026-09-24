from django.db import migrations, models


def validate_existing_users(apps, schema_editor):
    User = apps.get_model("users", "User")
    User.objects.filter(fiche_status="pending").update(fiche_status="validated")


class Migration(migrations.Migration):

    dependencies = [("users", "0010_user_quartier_residentiel_user_credits")]

    operations = [
        migrations.AddField(
            model_name="user",
            name="fiche_status",
            field=models.CharField(choices=[("pending", "En attente"), ("validated", "Validée"), ("rejected", "À corriger")], default="pending", max_length=12, verbose_name="Statut de fiche"),
        ),
        migrations.RunPython(validate_existing_users, migrations.RunPython.noop),
    ]
