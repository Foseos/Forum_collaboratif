"""Rules for the optional Arcana Flouz activity lottery."""

from datetime import timedelta
import secrets

from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone

from .models import Category, LotteryDraw, Post
from .arcana import credit
from .rewards import count_message_words


RP_ROOTS = {'san-francisco', 'mystic-falls', 'la-nouvelle-orleans', 'beacon-hills',
            'les-enfers', 'les-cieux', 'dimensions-alternatives', 'continents'}
PRIZES = (5, 5, 5, 10, 10, 10, 15, 15, 20, 30)


def rp_category_ids():
    categories = list(Category.objects.values('id', 'slug', 'parent_id'))
    # San Francisco's location categories were created without parent links;
    # their reserved order range identifies those RP locations.
    selected = {row['id'] for row in categories if row['slug'] in RP_ROOTS}
    selected.update(Category.objects.filter(order__gte=100, order__lt=300).values_list('id', flat=True))
    while True:
        expanded = selected | {row['id'] for row in categories if row['parent_id'] in selected}
        if expanded == selected:
            return selected
        selected = expanded


def lottery_status(user, now=None):
    now = now or timezone.now()
    last = LotteryDraw.objects.filter(user=user).first()
    next_at = last.created_at + timedelta(days=7) if last else None
    if next_at and now < next_at:
        return {'available': False, 'reason': 'Prochain tirage possible dans sept jours après le précédent.',
                'next_at': next_at}, None
    since = max(now - timedelta(days=7), last.created_at if last else now - timedelta(days=7))
    posts = Post.objects.filter(
        author=user, topic__category_id__in=rp_category_ids(),
        created_at__gt=since, dice_result__isnull=True,
    ).exclude(lottery_draw__isnull=False).order_by('-created_at')
    qualifying_post = next((post for post in posts if count_message_words(post.content) > 100), None)
    if qualifying_post is None:
        return {'available': False, 'reason': 'Publiez un message de RP de plus de 100 mots pour obtenir un tirage.',
                'next_at': None}, None
    return {'available': True, 'reason': 'Un tirage est disponible.', 'next_at': None}, qualifying_post


@transaction.atomic
def draw_for_user(user):
    locked_user = get_user_model().objects.select_for_update().get(pk=user.pk)
    state, qualifying_post = lottery_status(locked_user)
    if not state['available']:
        return None, state['reason']
    prize = PRIZES[secrets.randbelow(len(PRIZES))]
    draw = LotteryDraw.objects.create(user=locked_user, qualifying_post=qualifying_post, prize=prize)
    credit(locked_user.pk, prize, f'Loterie : {qualifying_post.topic.title[:175]}')
    return draw, None
