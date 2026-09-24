from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("users", "0012_user_last_seen")]
    operations = [
        migrations.AddField(
            model_name="user",
            name="chat_last_seen",
            field=models.DateTimeField(null=True, blank=True, db_index=True),
        ),
    ]
