"""Replace the resurrection item without rewriting the rest of the live shop."""

from html import escape
import re

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.forum.models import Topic
from apps.forum.shop_details import ITEM_DETAILS


OLD_NAME = 'Amulette de Résurrection'
NEW_NAME = 'Boussole des Failles'
OLD_SUMMARY = "Permet de rappeler à la vie un être décédé depuis moins de 24 h. Usage absolument unique — l'amulette se désintègre après."
NEW_SUMMARY = "Repère la direction d'une faille magique active pendant 3 tours de RP et indique si elle s'élargit ou se referme. Ne crée aucun passage."


class Command(BaseCommand):
    help = 'Remplace l’amulette de résurrection par la Boussole des Failles.'

    @transaction.atomic
    def handle(self, *args, **options):
        post = Topic.objects.get(slug='catalogue-boutique-magique').posts.order_by('created_at').first()
        if post is None:
            raise ValueError('Catalogue sans texte.')
        if NEW_NAME in post.content and OLD_NAME not in post.content:
            self.stdout.write('La Boussole des Failles est déjà présente.')
            return
        rows = list(re.finditer(r'<tr\b[^>]*>.*?</tr>', post.content, re.S | re.I))
        targets = [match for match in rows if OLD_NAME in match.group(0)]
        if len(targets) != 1:
            raise ValueError('L’ancienne amulette doit apparaître dans une seule ligne du catalogue.')
        match = targets[0]
        row = match.group(0)
        if row.count(OLD_SUMMARY) != 1 or row.count('4 500 Arcana Flouz') != 1:
            raise ValueError('Description ou prix inattendu ; aucune modification.')
        atmosphere, usage, limits = ITEM_DETAILS[NEW_NAME]
        details = (
            '<details data-shop-details="1" style="margin-top:.7rem;">'
            '<summary style="cursor:pointer;color:#c4b5fd;font-weight:600;">Description &amp; utilisation en RP</summary>'
            '<div style="margin-top:.6rem;line-height:1.7;">'
            f'<p style="margin:0 0 .6rem;font-style:italic;">{escape(atmosphere)}</p>'
            f'<p style="margin:0 0 .6rem;"><strong>Utilisation :</strong> {escape(usage)}</p>'
            f'<p style="margin:0;"><strong>Limites :</strong> {escape(limits)}</p>'
            '</div></details>'
        )
        row = row.replace(OLD_NAME, NEW_NAME, 1).replace(OLD_SUMMARY, NEW_SUMMARY, 1)
        row = row.replace('4 500 Arcana Flouz', '2 000 Arcana Flouz', 1)
        row, count = re.subn(r'<details data-shop-details="1".*?</details>', lambda _: details, row, count=1, flags=re.S)
        if count != 1:
            raise ValueError('Fiche détaillée introuvable ; aucune modification.')
        post.content = post.content[:match.start()] + row + post.content[match.end():]
        post.save(update_fields=['content'])
        self.stdout.write(self.style.SUCCESS('Boussole des Failles publiée à la place de l’amulette.'))
