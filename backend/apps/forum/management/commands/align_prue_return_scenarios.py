"""Align the Halliwell scenarios with Prue's 2006 return."""

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.forum.models import Topic


CHANGES = {
    'andy-trudeau': (
        "Lorsque les Fondateurs accordèrent à Prue le don inouï du retour à la vie, les plans supérieurs consentirent à ce qu'Andy revienne avec elle. Ils se retrouvèrent à San Francisco, deux revenants dans un monde qui avait continué sans eux.",
        "Lorsque les Fondateurs proposèrent à Prue de revenir pour aider les Halliwell face à un danger futur, elle accepta. Ils permirent alors à Andy, toujours être de lumière, de la rejoindre sur Terre. Prue et lui se retrouvèrent à San Francisco, dans un monde qui avait continué sans eux. Leur réunion ne leur rendait pas les années perdues, mais leur laissait la liberté de construire la suite ensemble.",
    ),
    'paige-matthews-charmed-one': (
        "Elle rencontre également sa sœur Prue, suite à sa résurrection en 2006",
        "En 2006, elle rencontre enfin Prue, revenue à la vie après avoir accepté la proposition des Fondateurs. Ces retrouvailles ouvrent une relation à construire entre les deux sœurs, sans effacer la place que Paige s'est faite parmi les Halliwell.",
    ),
    'piper-halliwell-charmed-one': (
        "Lorsque Prue revint à la vie en fin d'année 2006, Piper redevint celle qu'elle était, une seconde fille de sororité, mais elle n'en restait pas moins la fille pleine de caractère qu'elle était devenue suite à la mort de son aînée.",
        "Lorsque Prue revint à la vie à la fin de 2006, après avoir accepté la proposition des Fondateurs, Piper retrouva sa sœur aînée sans redevenir celle qu'elle était avant sa mort. Les années où elle avait porté la famille l'avaient changée. Toutes deux durent réapprendre à être sœurs, et l'arrivée de Prue ne remit pas en cause la place de Paige.",
    ),
    'phoebe-halliwell-charmed-one': (
        "Aujourd’hui, Phoebe est une sorcière puissante et expérimentée, une mère dévouée",
        "Le retour de Prue en 2006, accepté par celle-ci après la proposition des Fondateurs, offrit à Phoebe la chance de retrouver son aînée. Leurs retrouvailles ne remplacèrent pas les années vécues avec Paige : leur famille comptait désormais quatre sœurs, avec des liens à reconstruire.\n\nAujourd’hui, Phoebe est une sorcière puissante et expérimentée, une mère dévouée",
    ),
}


class Command(BaseCommand):
    help = 'Harmonise les scénarios liés au retour de Prue.'

    @transaction.atomic
    def handle(self, *args, **options):
        posts = {}
        for slug, (old, new) in CHANGES.items():
            post = Topic.objects.get(slug=slug).posts.order_by('created_at').first()
            if post is None or (post.content.count(old) != 1 and new not in post.content):
                raise ValueError(f'Passage introuvable ou ambigu : {slug}. Aucune modification.')
            posts[slug] = post
        changed = []
        for slug, (old, new) in CHANGES.items():
            post = posts[slug]
            if new not in post.content:
                post.content = post.content.replace(old, new, 1)
                post.save(update_fields=['content'])
                changed.append(slug)
        self.stdout.write(self.style.SUCCESS(f"Scénarios harmonisés : {', '.join(changed) or 'déjà à jour'}."))
