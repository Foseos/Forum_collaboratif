from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('users', '0022_remove_user_ip_log')]

    operations = [
        migrations.AddField(
            model_name='user',
            name='power_progression',
            field=models.JSONField(blank=True, default=list,
                                   help_text='Au plus cinq pouvoirs de base, avec deux évolutions par pouvoir.',
                                   verbose_name='Pouvoirs de base et évolutions validés'),
        ),
    ]
