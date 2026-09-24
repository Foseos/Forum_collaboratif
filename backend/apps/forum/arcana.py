"""Record every Arcana Flouz balance change made by the forum."""

from django.contrib.auth import get_user_model
from django.db.models import F

from .models import ArcanaTransaction


def credit(user_id, amount, reason):
    get_user_model().objects.filter(pk=user_id).update(compte_bancaire=F('compte_bancaire') + amount)
    balance = get_user_model().objects.values_list('compte_bancaire', flat=True).get(pk=user_id)
    return ArcanaTransaction.objects.create(user_id=user_id, amount=amount,
                                            balance_after=balance, reason=reason)
