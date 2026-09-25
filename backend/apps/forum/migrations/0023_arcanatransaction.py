from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def opening_balances(apps, schema_editor):
    User = apps.get_model('users', 'User')
    Transaction = apps.get_model('forum', 'ArcanaTransaction')
    Transaction.objects.bulk_create([
        Transaction(user_id=user.id, amount=user.compte_bancaire,
                    balance_after=user.compte_bancaire, reason='Solde initial')
        for user in User.objects.exclude(compte_bancaire=0).iterator()
    ])


class Migration(migrations.Migration):
    dependencies = [
        ('forum', '0022_lotterydraw'),
        ('users', '0002_user_age_personnage_user_avatar_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArcanaTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('balance_after', models.IntegerField()),
                ('reason', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arcana_transactions', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-created_at', '-id']},
        ),
        migrations.RunPython(opening_balances, migrations.RunPython.noop),
    ]
