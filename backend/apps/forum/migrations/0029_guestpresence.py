from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('forum', '0028_specialize_power_grimoire')]

    operations = [
        migrations.CreateModel(
            name='GuestPresence',
            fields=[
                ('token', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('last_seen', models.DateTimeField(db_index=True)),
            ],
        ),
    ]
