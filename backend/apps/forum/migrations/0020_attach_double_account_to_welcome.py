from django.db import migrations


def attach_category(apps, schema_editor):
    Category = apps.get_model('forum', 'Category')
    parent, _ = Category.objects.get_or_create(
        slug='bienvenue-san-francisco',
        defaults={'name': 'Bienvenue à Nexus Arcana', 'order': 1},
    )
    Category.objects.filter(slug='demande-double-compte').update(parent=parent)


class Migration(migrations.Migration):
    dependencies = [('forum', '0019_double_account_category')]
    operations = [migrations.RunPython(attach_category, migrations.RunPython.noop)]
