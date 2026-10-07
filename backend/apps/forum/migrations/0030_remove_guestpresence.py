from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [('forum', '0029_guestpresence')]

    operations = [
        migrations.DeleteModel(name='GuestPresence'),
    ]
