from django.core.management.base import BaseCommand

from apps.users.ip_tracking import prune_ip_logs


class Command(BaseCommand):
    help = 'Supprime les traces IP de plus de 180 jours.'

    def handle(self, *args, **options):
        prune_ip_logs()
        self.stdout.write('Traces IP expirées supprimées.')
