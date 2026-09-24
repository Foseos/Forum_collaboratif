from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0013_user_chat_last_seen"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="profile_gif_url",
            field=models.URLField(blank=True, default="", help_text="URL directe d'un petit GIF affiché sous le portrait du personnage.", max_length=500),
        ),
    ]
