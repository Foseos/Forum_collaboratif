"""Avertit le destinataire après la création d'un message privé."""

import logging

from django.conf import settings
from django.core.mail import send_mail

from .models import PrivateMessage


logger = logging.getLogger(__name__)


def send_private_message_email(message_id):
    pm = PrivateMessage.objects.select_related('sender', 'recipient').filter(pk=message_id).first()
    if pm is None or not pm.recipient.is_active or not pm.recipient.email.strip():
        return

    sender_name = pm.sender.username
    recipient_name = pm.recipient.username
    subject = f'[Nexus Arcana] Nouveau message privé de {sender_name}'
    message = (
        f'Bonjour {recipient_name},\n\n'
        f'Vous avez reçu un nouveau message privé de {sender_name} sur Nexus Arcana.\n\n'
        f'Objet : {pm.subject or "(Sans objet)"}\n\n'
        f'Lire votre message : {settings.FORUM_URL.rstrip("/")}/messageries\n\n'
        '— L’équipe de Nexus Arcana'
    )
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [pm.recipient.email.strip()])
    except Exception:
        logger.exception('Échec de l’envoi du courriel pour le message privé %s', pm.pk)
