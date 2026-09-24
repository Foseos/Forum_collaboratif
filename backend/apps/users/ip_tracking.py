"""Journal d'IP limité aux inscriptions et aux connexions réussies."""

import ipaddress
import socket
from datetime import timedelta

from django.utils import timezone

from .models import UserIPLog


RETENTION_DAYS = 180


def client_ip(request):
    remote = request.META.get('REMOTE_ADDR', '')
    try:
        remote_ip = ipaddress.ip_address(remote)
    except ValueError:
        return None
    # Seul le proxy nginx du service frontend peut fournir l'adresse réelle.
    try:
        proxy_ip = ipaddress.ip_address(socket.gethostbyname('frontend'))
    except (OSError, ValueError):
        proxy_ip = None
    if proxy_ip and remote_ip == proxy_ip:
        forwarded = request.META.get('HTTP_X_REAL_IP', '')
        try:
            return ipaddress.ip_address(forwarded).compressed
        except ValueError:
            pass
    return remote_ip.compressed


def prune_ip_logs():
    UserIPLog.objects.filter(created_at__lt=timezone.now() - timedelta(days=RETENTION_DAYS)).delete()


def record_ip_event(user, request, event):
    ip = client_ip(request)
    if ip:
        UserIPLog.objects.create(user=user, ip_address=ip, event=event)
    prune_ip_logs()
