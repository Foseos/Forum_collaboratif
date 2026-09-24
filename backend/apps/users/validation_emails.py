"""Courriel envoyé au membre après validation de sa fiche de présentation."""

import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from apps.forum.models import Topic


logger = logging.getLogger(__name__)


def send_character_validation_email(member_id, topic_id):
    member = get_user_model().objects.filter(pk=member_id, is_active=True).first()
    topic = Topic.objects.filter(pk=topic_id).first()
    if not member or not member.email or not topic:
        return

    name = member.username
    title = topic.title.replace("\r", " ").replace("\n", " ")
    subject = f"[Nexus Arcana] Votre fiche « {title} » est validée"
    link = f"{settings.FORUM_URL.rstrip('/')}/topics/{topic.slug}"
    message = (
        f"Bonjour {name},\n\n"
        f"La fondatrice a validé votre fiche « {title} ». "
        "Son message de validation est disponible dans le sujet.\n\n"
        f"Consulter votre fiche : {link}\n\n"
        "Vous pouvez désormais participer aux RP du forum.\n\n"
        "— L'équipe de Nexus Arcana"
    )
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [member.email])
    except Exception:
        logger.exception("Échec de l'envoi du mail de validation pour la fiche %s", topic_id)
