from django.db import migrations


def unlock_scenarios(apps, schema_editor):
    Topic = apps.get_model('forum', 'Topic')
    Topic.objects.filter(category__slug='scenarios-a-prendre', is_locked=True).update(is_locked=False)


class Migration(migrations.Migration):
    dependencies = [
        ('forum', '0023_arcanatransaction'),
    ]

    operations = [
        migrations.RunPython(unlock_scenarios, migrations.RunPython.noop),
    ]
