from django.db import migrations


def rename_pending_category(apps, schema_editor):
    Category = apps.get_model('forum', 'Category')
    Category.objects.filter(slug='fiches-de-presentation-terminees').update(
        name='Fiches en attente de validation',
        description='Présentations en cours de validation, ouvertes aux messages de bienvenue.',
    )


class Migration(migrations.Migration):
    dependencies = [('forum', '0014_avatardirectoryentry')]
    operations = [migrations.RunPython(rename_pending_category, migrations.RunPython.noop)]
