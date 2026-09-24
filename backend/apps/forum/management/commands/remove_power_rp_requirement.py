"""Remove the RP proof requirement from published power progression rules."""

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.forum.models import Topic


REPLACEMENTS = (
    ('Présentez la capacité souhaitée, ses limites et un RP justificatif ; l’achat et la fiche sont mis à jour après validation.',
     'Présentez la capacité souhaitée et ses limites ; aucun RP justificatif n’est demandé. L’achat et la fiche sont mis à jour après validation.'),
    ('Présentez à la boutique l’effet demandé, ses limites et un RP justificatif.',
     'Présentez à la boutique l’effet demandé et ses limites.'),
    ('une justification en RP et la validation du staff',
     'la validation du staff'),
    ('avec justification en RP et validation du staff',
     'avec validation du staff'),
    ('Les évolutions marquées <span style="color: #f5d76e;">★</span> nécessitent une validation explicite.',
     'Les évolutions marquées <span style="color: #f5d76e;">★</span> demandent un encadrement particulier ; toutes les évolutions nécessitent l’approbation du staff.'),
)


class Command(BaseCommand):
    help = 'Retire l’obligation d’un RP justificatif pour les pouvoirs.'

    @transaction.atomic
    def handle(self, *args, **options):
        slugs = ('catalogue-boutique-magique', 'reglement-officiel-du-forum',
                 'encyclopedie-des-creatures-et-races', 'liste-des-pouvoirs-magiques')
        changed = []
        for slug in slugs:
            post = Topic.objects.get(slug=slug).posts.order_by('created_at').first()
            if post is None:
                raise ValueError(f'Sujet sans contenu : {slug}')
            content = post.content
            for old, new in REPLACEMENTS:
                content = content.replace(old, new)
            if content != post.content:
                post.content = content
                post.save(update_fields=['content'])
                changed.append(slug)
        self.stdout.write(self.style.SUCCESS(f"Règle actualisée : {', '.join(changed) or 'déjà à jour'}."))
