from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def link_existing_forms(apps, schema_editor):
    Form = apps.get_model("forum", "DemonicFormEntry")
    User = apps.get_model(*settings.AUTH_USER_MODEL.split("."))
    for form in Form.objects.all():
        user = User.objects.filter(username__iexact=form.character.strip()).first()
        if user and not Form.objects.filter(character_user_id=user.pk).exists():
            form.character_user_id = user.pk
            form.save(update_fields=["character_user"])


class Migration(migrations.Migration):
    dependencies = [
        ("forum", "0025_contact_request"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="demonicformentry",
            name="character",
            field=models.CharField(max_length=150),
        ),
        migrations.AddField(
            model_name="demonicformentry",
            name="character_user",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="demonic_form",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RunPython(link_existing_forms, migrations.RunPython.noop),
    ]
