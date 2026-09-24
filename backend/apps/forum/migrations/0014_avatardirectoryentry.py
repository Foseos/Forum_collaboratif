from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("forum", "0013_validated_character_archives_category"),
    ]

    operations = [
        migrations.CreateModel(
            name="AvatarDirectoryEntry",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("avatar", models.CharField(max_length=100)),
                ("character", models.CharField(max_length=150)),
                ("status", models.CharField(choices=[("taken", "Pris"), ("pending", "En attente"), ("scenario", "Scénario")], default="taken", max_length=10)),
                ("url", models.CharField(blank=True, max_length=250)),
                ("negotiable", models.BooleanField(default=False)),
            ],
        ),
    ]
