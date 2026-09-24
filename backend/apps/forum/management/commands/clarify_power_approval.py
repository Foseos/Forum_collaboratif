"""State that every post-creation power and evolution requires staff approval."""

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.forum.models import Topic


NOTICE = (
    '<aside data-universal-staff-approval="1" style="margin:1rem 0;padding:1rem;'
    'border:1px solid rgba(245,215,110,.5);border-radius:8px;'
    'background:rgba(245,215,110,.07);color:#e2d9f3;line-height:1.7">'
    '<strong style="color:#f5d76e">Ajouts et évolutions des pouvoirs</strong><br>'
    'Après la création du personnage, tout nouveau pouvoir et toute évolution doivent être '
    'approuvés par le staff avant d’être utilisés en RP, même s’ils figurent déjà dans le grimoire. '
    'Présentez la capacité souhaitée et ses limites ; aucun RP justificatif n’est demandé. L’achat et la fiche sont '
    'mis à jour après validation.'
    '</aside>'
)


class Command(BaseCommand):
    help = 'Affiche la règle de validation dans le grimoire et la boutique.'

    @transaction.atomic
    def handle(self, *args, **options):
        changed = []
        for slug in ('liste-des-pouvoirs-magiques', 'catalogue-boutique-magique'):
            post = Topic.objects.get(slug=slug).posts.order_by('created_at').first()
            if post is None:
                raise ValueError(f'Sujet sans contenu : {slug}')
            if 'data-universal-staff-approval="1"' not in post.content:
                post.content = NOTICE + post.content
                post.save(update_fields=['content'])
                changed.append(slug)
        self.stdout.write(self.style.SUCCESS(f"Règle affichée : {', '.join(changed) or 'déjà en place'}."))
