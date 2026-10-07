from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('forum', '0026_link_demonic_forms_to_users'),
        ('users', '0023_user_power_progression'),
    ]

    operations = [
        migrations.CreateModel(
            name='PowerPurchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(choices=[('fifth', 'Cinquième pouvoir'), ('evolution', 'Évolution')], max_length=12)),
                ('power_name', models.CharField(max_length=120)),
                ('evolution_name', models.CharField(blank=True, default='', max_length=120)),
                ('cost', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('approved_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='approved_power_purchases', to=settings.AUTH_USER_MODEL)),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='power_purchases', to=settings.AUTH_USER_MODEL)),
                ('request_post', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='power_purchase', to='forum.post')),
                ('transaction', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='power_purchase', to='forum.arcanatransaction')),
            ],
        ),
    ]
