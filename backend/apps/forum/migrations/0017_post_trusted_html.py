from django.db import migrations, models


def trust_existing_staff_posts(apps, schema_editor):
    Post = apps.get_model('forum', 'Post')
    Post.objects.filter(author__role__in=['admin', 'fondatrice']).update(is_trusted_html=True)


class Migration(migrations.Migration):
    dependencies = [('forum', '0016_scenario_avatar_name')]
    operations = [
        migrations.AddField(
            model_name='post', name='is_trusted_html',
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(trust_existing_staff_posts, migrations.RunPython.noop),
    ]
