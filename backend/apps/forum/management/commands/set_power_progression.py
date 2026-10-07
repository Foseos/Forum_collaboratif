"""Align the published power rules with the five-base-power ceiling."""

import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from apps.forum.models import Topic
from .clarify_power_approval import NOTICE


RULE_SECTION = (
    '<section data-power-progression="creation-max-5" style="margin:1rem 0;padding:1rem;'
    'border:1px solid rgba(245,215,110,.35);border-radius:8px;line-height:1.8;">'
    '<h2 style="color:#f5d76e;font-size:1rem;">Création et progression des capacités</h2>'
    '<p><strong>Quatre pouvoirs de base maximum à la création.</strong> '
    'Cette limite vaut pour toutes les espèces, y compris les hybrides, tribrides et Originels. '
    'Un cinquième pouvoir de base peut être acheté ensuite : cinq est le plafond total, '
    'tous héritages confondus.</p>'
    '<p>Chaque effet surnaturel distinct, actif ou passif, compte comme un pouvoir de base. '
    'La force, la vitesse, la régénération, les sens accrus, une immunité ou la transformation '
    'sont des capacités distinctes. Un intitulé général ne permet pas de cumuler plusieurs dons. '
    'La nature, l’âge ou les exploits de la série ne débloquent rien automatiquement. '
    'Les humains ne reçoivent pas de pouvoirs magiques : leurs aptitudes restent humaines.</p>'
    '<p><strong>Chaque pouvoir de base peut recevoir deux évolutions maximum :</strong> '
    'base → évolution 1 → évolution 2. Chaque évolution fait l’objet d’un achat et d’une validation '
    'distincts. Une évolution améliore le pouvoir concerné ; elle ne crée pas un nouveau pouvoir de base. '
    'Aucun sixième pouvoir de base ni troisième évolution d’un même pouvoir ne peut être acheté.</p>'
    '<p>Présentez à la boutique le cinquième pouvoir ou l’évolution souhaitée et ses limites. '
    'Le staff valide, débite les Arcana Flouz et met à jour la fiche avant utilisation. '
    'Aucun RP justificatif n’est demandé. Le cinquième pouvoir de base coûte 600 Arcana Flouz ; '
    'chaque évolution coûte 300 Arcana Flouz, quel que soit le nombre d’achats précédents.</p></section>'
)

OLD_INTRO = (
    "À la création, chaque personnage choisit quatre capacités maximum, actives et passives comprises, "
    "cohérentes avec sa nature et validées dans sa fiche. Les capacités et évolutions supplémentaires "
    "s'acquièrent ensuite en jeu selon les règles de la boutique."
)
NEW_INTRO = (
    "À la création, chaque personnage choisit quatre pouvoirs de base maximum, actifs et passifs compris, "
    "cohérents avec sa nature et validés dans sa fiche. Un cinquième pouvoir de base peut être acheté "
    "ensuite, sans dépasser cinq au total. Chacun peut recevoir deux évolutions maximum, achetées et "
    "validées séparément."
)
OLD_CROSSOVER = (
    "quatre capacités maximum à la création, tous héritages confondus. Les capacités manquantes et "
    "les améliorations s’achètent en Arcana Flouz, avec validation du staff."
)
NEW_CROSSOVER = (
    "quatre pouvoirs de base maximum à la création, puis un cinquième achetable : cinq au total, "
    "tous héritages confondus. Chaque pouvoir de base peut recevoir deux évolutions achetées "
    "séparément, avec validation du staff."
)


def update_content(slug, content):
    if slug in ('reglement-officiel-du-forum', 'catalogue-boutique-magique'):
        markers = ('data-power-progression="creation-max-4"',
                   'data-power-progression="creation-max-5"')
        matches = [marker for marker in markers if marker in content]
        if len(matches) != 1:
            raise CommandError(f'Bloc de progression introuvable ou en double : {slug}')
        start = content.find('<section ', max(0, content.find(matches[0]) - 15))
        end = content.find('</section>', start) + len('</section>')
        if start < 0 or end < len('</section>'):
            raise CommandError(f'Bloc de progression malformé : {slug}')
        content = content[:start] + RULE_SECTION + content[end:]
    else:
        if OLD_INTRO in content:
            content = content.replace(OLD_INTRO, NEW_INTRO, 1)
        elif NEW_INTRO not in content:
            raise CommandError('Introduction du grimoire introuvable.')
        if OLD_CROSSOVER in content:
            content = content.replace(OLD_CROSSOVER, NEW_CROSSOVER, 1)
        elif NEW_CROSSOVER not in content:
            raise CommandError('Règle du crossover introuvable dans le grimoire.')

    marker = 'data-universal-staff-approval="1"'
    if slug in ('liste-des-pouvoirs-magiques', 'catalogue-boutique-magique'):
        if marker not in content:
            raise CommandError(f'Encadré de validation introuvable : {slug}')
        start = content.find('<aside ', max(0, content.find(marker) - 15))
        end = content.find('</aside>', start) + len('</aside>')
        if start < 0 or end < len('</aside>'):
            raise CommandError(f'Encadré de validation malformé : {slug}')
        content = content[:start] + NOTICE + content[end:]
    return content


class Command(BaseCommand):
    help = 'Fixe quatre pouvoirs de base au départ, un cinquième achetable et deux évolutions par pouvoir.'

    def handle(self, *args, **options):
        with transaction.atomic():
            changed = []
            for slug in ('reglement-officiel-du-forum', 'catalogue-boutique-magique',
                         'liste-des-pouvoirs-magiques'):
                topic = Topic.objects.filter(slug=slug).first()
                if topic is None:
                    raise CommandError(f'Sujet introuvable : {slug}')
                post = topic.posts.select_for_update().order_by('created_at', 'pk').first()
                if post is None:
                    raise CommandError(f'Sujet sans contenu : {slug}')
                updated = update_content(slug, post.content)
                if updated == post.content:
                    continue
                backup_dir = Path(settings.BASE_DIR) / 'data' / 'scenario_backups'
                backup_dir.mkdir(parents=True, exist_ok=True)
                backup_path = backup_dir / (f'power-progression-{slug}-' +
                                           timezone.now().strftime('%Y%m%dT%H%M%S%f') + '.json')
                backup_path.write_text(json.dumps({'topic_id': topic.pk, 'post_id': post.pk,
                                                  'content': post.content}, ensure_ascii=False),
                                       encoding='utf-8')
                post.content = updated
                post.save(update_fields=['content', 'updated_at', 'is_edited'])
                changed.append(slug)
            self.stdout.write(self.style.SUCCESS(f"Règle publiée : {', '.join(changed) or 'déjà à jour'}."))
