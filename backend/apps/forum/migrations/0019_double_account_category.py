from django.db import migrations


def create_double_account_category(apps, schema_editor):
    Category = apps.get_model('forum', 'Category')
    parent = Category.objects.filter(slug='bienvenue-san-francisco').first()
    Category.objects.update_or_create(
        slug='demande-double-compte',
        defaults={
            'name': 'Demande de double compte',
            'description': 'Présentez votre projet de second personnage avec le formulaire dédié.',
            'order': 25,
            'parent': parent,
        },
    )


class Migration(migrations.Migration):
    dependencies = [('forum', '0018_demonicformentry')]
    operations = [migrations.RunPython(create_double_account_category, migrations.RunPython.noop)]
