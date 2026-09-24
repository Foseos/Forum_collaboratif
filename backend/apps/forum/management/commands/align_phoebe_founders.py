"""Clarify Phoebe's admission to the Founders and half-demon alignment."""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.forum.models import Post, Topic


CHANGES = {
    'phoebe-halliwell-charmed-one': [
        (
            'Elle devient fondatrice à 45 ans arrêtant de vieillir',
            "Quelques années après son remariage avec Cole, Phoebe défend une famille mêlant humains et êtres surnaturels que certains Fondateurs voulaient condamner pour son ascendance. Elle refuse de confondre les origines des enfants avec leurs actes, sans minimiser les dangers liés au monde démoniaque. Son intervention épargne des innocents et évite une crise plus grave. Le Conseil, divisé sur son union avec Cole, reconnaît pourtant la justesse de son jugement et l'admet parmi les Fondateurs à une courte majorité lorsqu'elle a 45 ans. Elle cesse alors de vieillir. Cette nomination ne vaut ni pardon pour les actes passés de Cole ni accès de celui-ci au Conseil, à ses secrets ou à ses décisions. Phoebe se retire de toute délibération le concernant, tandis que plusieurs Fondateurs continuent de contester sa place."
        ),
    ],
    'cole-turner': [
        (
            "Cole fut le premier à s'avancer. Il savait mieux que quiconque ce que signifiait choisir le bien alors que tout vous pousse vers le Mal — et il ne posa aucune condition, n'exigea aucune explication.",
            "Cole fut le premier à s'avancer. Comme tout hybride mi-démon, il peut choisir son camp ; sa propre ascendance est mi-humaine, mi-démoniaque. Son choix du bien n'efface ni son passé ni ses responsabilités. Il ne posa aucune condition à Jensen et n'exigea aucune explication. Le siège de Phoebe parmi les Fondateurs ne lui donne aucun accès à leur Conseil."
        ),
    ],
    'encyclopedie-des-creatures-et-races': [
        (
            'En revanche, les démons, y compris les Êtres des ténèbres, ne peuvent pas rejoindre le camp du Bien : ils peuvent suivre le Mal ou rester neutres.',
            'En revanche, les démons à part entière, y compris les Êtres des ténèbres, ne peuvent pas rejoindre le camp du Bien : ils peuvent suivre le Mal ou rester neutres. Les mi-démons sont des hybrides dont l’autre ascendance peut être humaine ou appartenir à une autre espèce surnaturelle. Ils peuvent choisir le Bien, le Mal ou la neutralité : leur camp dépend de leurs actes, pas de la nature de leur autre parent.'
        ),
        (
            'Un démon peut suivre le Mal ou rester neutre, mais pas rejoindre le camp du Bien. Ses capacités précises doivent figurer dans sa fiche validée.',
            'Un démon à part entière peut suivre le Mal ou rester neutre, mais pas rejoindre le camp du Bien. Un mi-démon peut être issu d’un parent humain, sorcier ou d’une autre espèce ; il peut choisir le Bien, le Mal ou la neutralité quelle que soit cette autre ascendance. Sa lignée ne lui donne aucun pouvoir supplémentaire automatique. Ses capacités précises doivent figurer dans sa fiche validée.'
        ),
    ],
}

PREVIOUS_WORDING = {
    'cole-turner': [
        "Cole fut le premier à s'avancer. Sa part humaine lui donne la liberté de choisir le bien malgré son héritage démoniaque ; ce choix n'efface ni son passé ni ses responsabilités. Il ne posa aucune condition à Jensen et n'exigea aucune explication. Le siège de Phoebe parmi les Fondateurs ne lui donne aucun accès à leur Conseil."
    ],
    'encyclopedie-des-creatures-et-races': [
        'En revanche, les démons à part entière, y compris les Êtres des ténèbres, ne peuvent pas rejoindre le camp du Bien : ils peuvent suivre le Mal ou rester neutres. Les mi-démons font exception : leur part humaine leur permet de choisir le Bien, le Mal ou la neutralité. Ce choix dépend de leurs actes et n’efface pas leur héritage démoniaque.',
        'Un démon à part entière peut suivre le Mal ou rester neutre, mais pas rejoindre le camp du Bien. Un mi-démon, grâce à sa part humaine, peut choisir le Bien, le Mal ou la neutralité ; sa lignée ne lui donne aucun pouvoir supplémentaire automatique. Ses capacités précises doivent figurer dans sa fiche validée.'
    ],
}


class Command(BaseCommand):
    help = "Harmonise l'histoire de Phoebe, Cole et la règle des mi-démons."

    @transaction.atomic
    def handle(self, *args, **options):
        for slug, replacements in CHANGES.items():
            topic = Topic.objects.filter(slug=slug).first()
            post = Post.objects.filter(topic=topic).order_by('created_at').first() if topic else None
            if post is None:
                raise CommandError(f'Sujet introuvable : {slug}')
            content = post.content
            for index, (old, new) in enumerate(replacements):
                if new in content:
                    continue
                if old not in content:
                    previous = PREVIOUS_WORDING.get(slug, [])
                    if index < len(previous) and previous[index] in content:
                        old = previous[index]
                    else:
                        raise CommandError(f'Passage attendu introuvable : {slug} / {old[:55]}')
                content = content.replace(old, new, 1)
            if content != post.content:
                Post.objects.filter(pk=post.pk).update(content=content)
            self.stdout.write(f'Mis à jour : {slug}')
