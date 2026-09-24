from django.db import migrations, models


def hide_primerose(apps, schema_editor):
    User = apps.get_model('users', 'User')
    User.objects.filter(username__iexact='Primerose Halliwell').update(show_in_staff_team=False)


class Migration(migrations.Migration):
    dependencies = [('users', '0020_user_rp_availability')]

    operations = [
        migrations.AddField(
            model_name='user',
            name='show_in_staff_team',
            field=models.BooleanField(default=True, verbose_name='Afficher dans la team du staff'),
        ),
        migrations.RunPython(hide_primerose, migrations.RunPython.noop),
    ]
