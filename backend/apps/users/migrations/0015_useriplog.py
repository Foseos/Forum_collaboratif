from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [('users', '0014_user_profile_gif_url')]

    operations = [
        migrations.CreateModel(
            name='UserIPLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField()),
                ('event', models.CharField(choices=[('registration', 'Inscription'), ('login', 'Connexion')], max_length=12)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ip_logs', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.AddIndex(model_name='useriplog', index=models.Index(fields=['ip_address', 'created_at'], name='users_iplog_ip_created_idx')),
    ]
