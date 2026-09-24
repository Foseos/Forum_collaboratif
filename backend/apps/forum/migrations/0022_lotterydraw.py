from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [('forum', '0021_post_dice_result'), migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name='LotteryDraw',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prize', models.PositiveSmallIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('qualifying_post', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='lottery_draw', to='forum.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lottery_draws', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-created_at']},
        ),
    ]
