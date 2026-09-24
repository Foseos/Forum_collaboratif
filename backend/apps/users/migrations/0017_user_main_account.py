from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("users", "0016_user_pending_email")]

    operations = [
        migrations.AddField(
            model_name="user", name="main_account",
            field=models.ForeignKey(blank=True, help_text='Compte principal lié après validation par le staff.',
                                    null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    related_name='linked_accounts', to='users.user'),
        ),
    ]
