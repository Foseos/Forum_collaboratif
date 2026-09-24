from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_add_nature_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='camp',
            field=models.CharField(blank=True, default='', help_text='Alignement moral du personnage (ex : Bien, Mal, Neutre)', max_length=50, verbose_name='Camp'),
        ),
        migrations.AddField(
            model_name='user',
            name='metier',
            field=models.CharField(blank=True, default='', max_length=150, verbose_name='Métier'),
        ),
    ]
