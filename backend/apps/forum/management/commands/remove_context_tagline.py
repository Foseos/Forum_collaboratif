"""Remove the misleading season-one closing sentence from the live page."""

from django.core.management.base import BaseCommand

from apps.forum.models import SitePage


TAGLINE = '<p style="margin-bottom:0;color:#c4b5d4;font-style:italic;">Le Nexus s’est éveillé. Les portes sont ouvertes. À vous de décider ce qui les traversera.</p>'


class Command(BaseCommand):
    help = 'Retire la conclusion trompeuse du contexte publié.'

    def handle(self, *args, **options):
        page = SitePage.objects.get(slug='home-context')
        if TAGLINE not in page.content:
            self.stdout.write('La phrase est déjà absente du contexte.')
            return
        page.content = page.content.replace(TAGLINE, '', 1)
        page.save(update_fields=['content'])
        self.stdout.write(self.style.SUCCESS('Phrase retirée du contexte.'))
