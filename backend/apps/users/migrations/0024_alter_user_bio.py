from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('users', '0023_user_power_progression')]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True),
        ),
    ]
