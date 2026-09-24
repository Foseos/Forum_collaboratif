"""Notifications par mail pour les membres ayant déjà écrit dans un sujet."""

import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from .models import Post


logger = logging.getLogger(__name__)


def send_topic_reply_emails(topic, replying_author_id):
    participant_ids = (
        Post.objects.filter(topic=topic)
        .exclude(author_id=replying_author_id)
        .values_list("author_id", flat=True)
        .distinct()
    )
    participants = get_user_model().objects.filter(
        pk__in=participant_ids, is_active=True, email_topic_replies=True
    ).exclude(email="")
    if not participants.exists():
        return

    subject = f"[Nexus Arcana] Nouvelle réponse dans « {topic.title} »"
    topic_url = f"{settings.FORUM_URL.rstrip('/')}/topics/{topic.slug}"
    sent_to = set()
    for participant in participants:
        address = participant.email.strip()
        if not address or address.lower() in sent_to:
            continue
        sent_to.add(address.lower())
        name = participant.username
        message = (
            f"Bonjour {name},\n\n"
            f"Une nouvelle réponse a été publiée dans le sujet « {topic.title} » "
            "auquel vous avez participé.\n\n"
            f"Lire le sujet : {topic_url}\n\n"
            "— L'équipe de Nexus Arcana"
        )
        try:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [address])
        except Exception:
            logger.exception("Échec de l'envoi d'un mail de réponse pour le sujet %s", topic.pk)
