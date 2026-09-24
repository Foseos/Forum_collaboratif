from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('users', '0018_user_mail_cooldowns')]

    operations = [
        migrations.AddField(model_name='user', name='email_topic_replies',
                            field=models.BooleanField(default=True, verbose_name='E-mails de réponse aux sujets')),
    ]
