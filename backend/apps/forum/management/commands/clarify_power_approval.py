"""State that every post-creation power and evolution requires staff approval."""

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.forum.models import Topic


NOTICE = (
    '<aside data-universal-staff-approval="1" style="margin:1rem 0;padding:1rem;'
    'border:1px solid rgba(245,215,110,.5);border-radius:8px;'
    'background:rgba(245,215,110,.07);color:#e2d9f3;line-height:1.7">'
    '<strong style="color:#f5d76e">Ajouts et évolutions des pouvoirs</strong><br>'
    'Quatre pouvoirs de base maximum à la création, puis un cinquième achetable : cinq au total. '
    'Chaque pouvoir de base peut recevoir deux évolutions maximum, achetées séparément. '
    'Aucun sixième pouvoir de base ni troisième évolution d’un même pouvoir. '
    'Tout achat doit être approuvé par le staff avant utilisation en RP, même s’il figure déjà dans le grimoire. '
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
            marker = 'data-universal-staff-approval="1"'
            if marker in post.content:
                start = post.content.find('<aside ', max(0, post.content.find(marker) - 15))
                end = post.content.find('</aside>', start) + len('</aside>')
                if start < 0 or end < len('</aside>'):
                    raise ValueError(f'Encadré de validation malformé : {slug}')
                updated = post.content[:start] + NOTICE + post.content[end:]
            else:
                updated = NOTICE + post.content
            if updated != post.content:
                post.content = updated
                post.save(update_fields=['content'])
                changed.append(slug)
        self.stdout.write(self.style.SUCCESS(f"Règle affichée : {', '.join(changed) or 'déjà en place'}."))
