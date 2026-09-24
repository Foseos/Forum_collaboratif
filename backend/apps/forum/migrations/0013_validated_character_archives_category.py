from django.db import migrations


def create_archive_category(apps, schema_editor):
    Category = apps.get_model('forum', 'Category')
    Category.objects.get_or_create(
        slug='fiches-validees-et-archivees',
        defaults={
            'name': 'Fiches validées & archivées',
            'description': 'Archives officielles des personnages validés.',
            'order': 90,
        },
    )


class Migration(migrations.Migration):
    dependencies = [('forum', '0012_remove_topic_scenario_profile')]
    operations = [migrations.RunPython(create_archive_category, migrations.RunPython.noop)]
