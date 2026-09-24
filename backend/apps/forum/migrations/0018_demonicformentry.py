from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("forum", "0017_post_trusted_html"),
    ]

    operations = [
        migrations.CreateModel(
            name="DemonicFormEntry",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, unique=True)),
                ("image_url", models.URLField(blank=True, max_length=500)),
                ("character", models.CharField(max_length=150, unique=True)),
            ],
            options={"ordering": ["name"]},
        ),
    ]
