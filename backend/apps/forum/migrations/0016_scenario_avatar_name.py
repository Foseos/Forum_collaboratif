from django.db import migrations, models


def fill_halliwell_avatars(apps, schema_editor):
    Topic = apps.get_model('forum', 'Topic')
    Topic.objects.filter(slug='peyton-halliwell', category__slug='scenarios-a-prendre').update(
        scenario_avatar_name='Ester Exposito',
    )
    Topic.objects.filter(slug='melinda-halliwell', category__slug='scenarios-a-prendre').update(
        scenario_avatar_name='Ella Purnell',
    )


class Migration(migrations.Migration):
    dependencies = [('forum', '0015_rename_pending_character_sheets')]
    operations = [
        migrations.AddField(
            model_name='topic', name='scenario_avatar_name',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.RunPython(fill_halliwell_avatars, migrations.RunPython.noop),
    ]
