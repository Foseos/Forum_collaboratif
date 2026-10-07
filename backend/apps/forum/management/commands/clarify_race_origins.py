"""Clarify the published race directory and power grimoire without resetting posts."""

from html import escape

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.forum.models import Topic


RACE_REPLACEMENTS = (
    (
        'Magie personnelle, sorts et potions dans la continuité Charmed du forum. Les sorciers Charmed ne choisissent aucune branche : chacun définit son camp séparément, selon ses convictions et ses actes.',
        'Nature de sorcière propre à Charmed, distincte de celle des sorcières TVD. Ses pouvoirs personnels s’expriment par sa lignée ; sorts et potions complètent sa pratique. Les sorciers Charmed ne choisissent aucune branche : chacun définit son camp selon ses convictions et ses actes.',
    ),
    (
        'Les pouvoirs précis sont choisis dans la fiche validée. Une lignée familiale ou un apprentissage ne constitue pas une sous-race et ne donne aucun don automatique. Un rituel ne permet pas de contourner les quatre pouvoirs de base validés ou de reproduire librement ceux d’un autre personnage.',
        'Les pouvoirs précis sont choisis dans la fiche validée. Une lignée familiale ou un apprentissage ne donne aucun don automatique. Apprendre un rituel TVD ne change pas la nature du personnage et ne lui transmet pas les aptitudes propres aux sorcières TVD.',
    ),
    (
        'Le choix de branche décrit l’appartenance à un coven ou une pratique indépendante. Les traditions magiques et les aptitudes se précisent séparément dans la fiche.',
        'Nature de sorcière propre à The Vampire Diaries, The Originals et Legacies, distincte de celle des sorcières Charmed. Sa magie passe notamment par la canalisation de sources et les rituels ; le choix de profil décrit l’appartenance à un coven ou une pratique indépendante.',
    ),
    (
        'La magie ancestrale est une tradition et le siphonnage une aptitude, pas des branches liées à l’appartenance. Un siphonneur peut appartenir à un coven ou être indépendant : cette aptitude doit figurer dans ses dons validés. Une source n’est pas inépuisable ; aucun de ces choix ne donne accès automatiquement à toutes les traditions ni ne permet de vider la magie d’un autre joueur sans résolution commune.',
        'La magie ancestrale est une tradition et le siphonnage une aptitude, pas des branches liées à l’appartenance. Un siphonneur peut appartenir à un coven ou être indépendant : cette aptitude doit figurer dans ses dons validés. Une source n’est pas inépuisable. Apprendre un sort Charmed ne transmet ni sa nature ni ses pouvoirs personnels.',
    ),
    (
        'Héritage de vampire et de siphonneur, à distinguer d’un sorcier ordinaire devenu vampire.',
        'Profil de vampire siphonneur issu de The Vampire Diaries, et non espèce indépendante : à distinguer d’un sorcier ordinaire devenu vampire.',
    ),
    (
        'Natures animales distinctes : choisir une forme principale. Les pouvoirs évoqués ci-dessous sont des pistes, jamais des dons automatiques.',
        'Natures animales distinctes : choisir une forme principale. Les pouvoirs évoqués ci-dessous sont des pistes, jamais des dons automatiques. Le WereLion est une adaptation de Nexus Arcana inspirée de Teen Wolf, pas une espèce présentée comme canonique dans la série.',
    ),
    (
        'Affinité lion ; rugissement de garde peut être proposé dans la fiche.',
        'Adaptation du forum : affinité lion ; rugissement de garde peut être proposé dans la fiche.',
    ),
    (
        'Triple héritage exceptionnel de sorcier, vampire et loup-garou. L’éveil éventuel des héritages relève de l’évolution du personnage, pas d’une branche ou d’une sous-race.',
        'Hope Mikaelson est la seule Trybride de Nexus Arcana. Son triple héritage de sorcière, vampire et loup-garou ne constitue pas une nature ouverte à d’autres personnages.',
    ),
    (
        'Quatre pouvoirs au total à la création, répartis entre les héritages validés ; aucun triple quota ni éveil libre en cours de sujet. Les capacités nouvellement éveillées suivent les règles de progression et la validation du staff.',
        'Les capacités de Hope et leurs évolutions suivent sa fiche validée. Aucun autre personnage ne peut choisir la nature de trybride.',
    ),
)

GRIMOIRE_REPLACEMENTS = (
    (
        "capacités de changeforme propres à leur espèce : adaptabilité du coyote, agilité du jaguar, puissance et présence du lion. Une forme animale n'est jamais invulnérable.",
        "capacités de changeforme : adaptabilité du coyote, agilité du jaguar, puissance et présence du lion. Le WereLion est une adaptation de Nexus Arcana inspirée de Teen Wolf. Une forme animale n'est jamais invulnérable.",
    ),
    (
        "Hybrides et Trybrides</strong> — cumulent des héritages mais aussi leurs faiblesses. Les Trybrides sont exceptionnelles et nécessitent l'accord préalable du staff.",
        "Hybrides et Trybride</strong> — les hybrides cumulent des héritages mais aussi leurs faiblesses. Hope Mikaelson est la seule Trybride ; cette nature n'est pas ouverte à d'autres personnages.",
    ),
    (
        "vampires siphonneurs : ils canalisent une magie absorbée, mais leur soif et l'épuisement limitent leur puissance.",
        "profil de vampires siphonneurs, non espèce indépendante : ils canalisent une magie absorbée, mais leur soif et l'épuisement limitent leur puissance.",
    ),
)


class Command(BaseCommand):
    help = "Clarifie les Hérétiques, la Trybride et les WereLions dans les sujets publiés."

    def handle(self, *args, **options):
        with transaction.atomic():
            for slug, replacements, html_escape in (
                ('encyclopedie-des-creatures-et-races', RACE_REPLACEMENTS, True),
                ('liste-des-pouvoirs-magiques', GRIMOIRE_REPLACEMENTS, False),
            ):
                topic = Topic.objects.filter(slug=slug).first()
                if topic is None:
                    raise CommandError(f'Sujet introuvable : {slug}')
                post = topic.posts.select_for_update().order_by('created_at', 'pk').first()
                if post is None:
                    raise CommandError(f'Sujet sans contenu : {slug}')
                content = post.content
                for old, new in replacements:
                    if html_escape:
                        old, new = escape(old), escape(new)
                    if old not in content and new not in content:
                        raise CommandError(f'Texte attendu absent dans {slug} : {old}')
                    content = content.replace(old, new, 1)
                if content != post.content:
                    post.content = content
                    post.save(update_fields=['content', 'is_edited', 'updated_at'])
                self.stdout.write(self.style.SUCCESS(f'Sujet vérifié : {slug}'))
