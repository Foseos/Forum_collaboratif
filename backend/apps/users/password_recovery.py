"""Réinitialisation du mot de passe par lien temporaire à usage unique."""

from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes


token_generator = PasswordResetTokenGenerator()


def send_reset_link(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_generator.make_token(user)
    url = f"{settings.FORUM_URL.rstrip('/')}/reinitialiser-mot-de-passe?uid={uid}&jeton={token}"
    send_mail(
        'Réinitialisez votre mot de passe Nexus Arcana',
        f'Bonjour {user.username},\n\nPour choisir un nouveau mot de passe, ouvrez ce lien :\n'
        f'{url}\n\nSi vous n’avez rien demandé, ignorez ce message. Le lien expire automatiquement.\n',
        settings.DEFAULT_FROM_EMAIL, [user.email],
    )


def user_for_reset(uid, token):
    if not isinstance(uid, str) or not isinstance(token, str) or not uid or not token:
        return None
    try:
        from django.contrib.auth import get_user_model
        pk = force_str(urlsafe_base64_decode(uid))
        user = get_user_model().objects.get(pk=pk, is_active=True)
    except (TypeError, ValueError, OverflowError, UnicodeDecodeError, get_user_model().DoesNotExist):
        return None
    return user if token_generator.check_token(user, token) else None
