"""Liens de confirmation à durée limitée pour l'inscription et les adresses."""

from urllib.parse import quote

from django.conf import settings
from django.core import signing
from django.core.mail import send_mail


TOKEN_AGE = 24 * 60 * 60


def make_token(user, purpose):
    email = user.email if purpose == 'registration' else user.pending_email
    return signing.dumps({'id': user.pk, 'email': email, 'purpose': purpose}, salt='account-email-confirmation')


def read_token(token, purpose):
    if not isinstance(token, str) or not token or purpose not in ('registration', 'change'):
        return None
    try:
        data = signing.loads(token, salt='account-email-confirmation', max_age=TOKEN_AGE)
    except (signing.BadSignature, signing.SignatureExpired):
        return None
    if data.get('purpose') != purpose:
        return None
    return data


def send_confirmation(user, purpose):
    email = user.email if purpose == 'registration' else user.pending_email
    token = quote(make_token(user, purpose), safe='')
    url = f"{settings.FORUM_URL.rstrip('/')}/confirmation-email?type={purpose}&jeton={token}"
    if purpose == 'registration':
        subject = 'Confirmez votre inscription à Nexus Arcana'
        message = (f'Bonjour {user.username},\n\nConfirmez votre adresse pour activer votre compte :\n'
                   f'{url}\n\nCe lien est valable 24 heures et ne peut être utilisé qu’une fois.\n')
    else:
        subject = 'Confirmez votre nouvelle adresse sur Nexus Arcana'
        message = (f'Bonjour {user.username},\n\nConfirmez votre nouvelle adresse :\n'
                   f'{url}\n\nVotre adresse actuelle restera active jusqu’à cette confirmation. '
                   'Le lien est valable 24 heures et ne peut être utilisé qu’une fois.\n')
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])


def notify_previous_email(user, new_email):
    if not user.email:
        return
    send_mail(
        'Demande de changement d’adresse sur Nexus Arcana',
        f'Bonjour {user.username},\n\nUn changement vers {new_email} a été demandé pour votre compte. '
        'Si vous n’en êtes pas à l’origine, contactez le staff. Votre adresse actuelle reste active jusqu’à confirmation.\n',
        settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True,
    )
