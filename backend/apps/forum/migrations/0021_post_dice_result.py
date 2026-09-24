from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('forum', '0020_attach_double_account_to_welcome')]

    operations = [
        migrations.AddField(model_name='post', name='dice_result',
                            field=models.PositiveSmallIntegerField(blank=True, editable=False, null=True)),
    ]
