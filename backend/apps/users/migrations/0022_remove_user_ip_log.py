from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [('users', '0021_user_show_in_staff_team')]

    operations = [migrations.DeleteModel(name='UserIPLog')]
