"""Clarify why the Founders offered Prue a return to life."""

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.forum.models import Topic


OLD = (
    "En 2006, elle revint à la vie, en guise de cadeau des fondateurs. "
    "Elle revint cependant à la vie avec l’âge qu’elle aurait dû avoir si elle avait continué de vivre, donc à 36 ans. "
)
NEW = (
    "En 2006, les Fondateurs découvrirent qu’un danger futur menaçait l’équilibre magique et que l’expérience de Prue pourrait aider les Halliwell à y faire face. "
    "Ils lui offrirent la possibilité de revenir parmi les vivants, et Prue accepta. "
    "Elle retrouva le monde à l’âge qu’elle aurait eu si elle avait vécu : 36 ans. "
    "Son retour n’effaça ni les années perdues ni la place que Paige avait prise au sein de la famille. "
)


class Command(BaseCommand):
    help = 'Précise la résurrection de Prue dans son scénario.'

    @transaction.atomic
    def handle(self, *args, **options):
        post = Topic.objects.get(slug='prue-halliwell-charmed-one').posts.order_by('created_at').first()
        if post is None:
            raise ValueError('Scénario de Prue sans texte.')
        if NEW in post.content:
            self.stdout.write('Le scénario de Prue est déjà à jour.')
            return
        if post.content.count(OLD) != 1:
            raise ValueError('Passage initial introuvable ou ambigu ; aucune modification.')
        post.content = post.content.replace(OLD, NEW, 1)
        post.save(update_fields=['content'])
        self.stdout.write(self.style.SUCCESS('Résurrection de Prue clarifiée.'))
