from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("users", "0019_user_email_topic_replies")]

    operations = [
        migrations.AddField(
            model_name="user",
            name="rp_availability",
            field=models.CharField(
                choices=[("open", "Ouvert aux RP"), ("discuss", "À discuter"), ("unavailable", "Indisponible")],
                default="discuss", max_length=12, verbose_name="Disponibilité RP",
            ),
        ),
    ]
