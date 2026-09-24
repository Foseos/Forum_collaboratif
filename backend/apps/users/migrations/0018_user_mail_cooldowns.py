from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("users", "0017_user_main_account")]

    operations = [
        migrations.AddField(model_name="user", name="last_confirmation_sent_at",
                            field=models.DateTimeField(blank=True, null=True)),
        migrations.AddField(model_name="user", name="last_password_reset_sent_at",
                            field=models.DateTimeField(blank=True, null=True)),
    ]
