"""Prépare les rubriques et le guide public des partenariats."""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from apps.forum.models import Category, Post, Topic


GUIDE = '''<div style="max-width:760px;margin:auto;padding:1.5rem;border:1px solid rgba(245,215,110,.35);border-radius:10px;background:#100c1d;color:#e2d9f3;line-height:1.8">
<p style="margin:0;color:#a78bfa;font-size:.75rem;letter-spacing:.18em;text-transform:uppercase">✦ Nexus Arcana · Rencontres entre univers ✦</p>
<h2 style="color:#f5d76e;margin:.4rem 0 1rem">Proposer un partenariat</h2>
<p>Nous aimons découvrir d’autres communautés et construire des échanges durables. Les forums récents sont les bienvenus : nous étudions chaque proposition pour son univers, sa présentation et l’envie de faire vivre le partenariat.</p>
<p><strong>Comment faire ?</strong> Ouvrez une demande au nom de votre forum dans cette rubrique. Vous pouvez utiliser le formulaire sans créer de compte. Le staff répondra dans votre sujet. Une proposition acceptée sera ensuite visible dans <a href="/categories/nos-partenaires" style="color:#f5d76e">Nos partenaires</a>.</p>
<p>Présentez votre forum, son adresse, son concept, sa date d’ouverture, le type d’échange souhaité (fiches, boutons ou les deux), ainsi que le lien vers notre affichage chez vous s’il est déjà en place. Vous pouvez joindre votre fiche et votre bouton. Aucun nombre minimum de membres ou de messages n’est exigé.</p>
<p style="margin-bottom:0">Une question avant de vous lancer ? Le staff est disponible pour en discuter dans votre sujet.</p>
</div>'''


class Command(BaseCommand):
    help = "Crée les rubriques de partenariat et leur guide épinglé."

    def handle(self, *args, **options):
        author = get_user_model().objects.filter(role='fondatrice', is_active=True).first()
        author = author or get_user_model().objects.filter(role='admin', is_active=True).first()
        if author is None:
            raise CommandError('Un compte fondatrice ou administrateur actif est nécessaire.')
        requests, _ = Category.objects.get_or_create(
            slug='demande-de-partenariats',
            defaults={'name': 'Demande de partenariats', 'order': 302},
        )
        requests.description = 'Présentez votre forum et échangez avec le staff autour d’un partenariat.'
        requests.save(update_fields=['description'])
        partners, _ = Category.objects.get_or_create(
            slug='nos-partenaires',
            defaults={'name': 'Nos partenaires', 'description': 'Les communautés partenaires de Nexus Arcana.', 'order': 303},
        )
        guide, _ = Topic.objects.get_or_create(
            category=requests, slug='proposer-un-partenariat',
            defaults={'title': 'Proposer un partenariat', 'author': author},
        )
        guide.title = 'Proposer un partenariat'
        guide.is_pinned = True
        guide.is_locked = True
        guide.save(update_fields=['title', 'is_pinned', 'is_locked'])
        post = guide.posts.order_by('created_at', 'id').first()
        if post is None:
            Post.objects.create(topic=guide, author=author, content=GUIDE, is_trusted_html=True)
        else:
            post.content = GUIDE
            post.is_trusted_html = True
            post.save(update_fields=['content', 'is_trusted_html'])
        self.stdout.write(self.style.SUCCESS(f'Partenariats prêts : {requests.name}, {partners.name}, guide épinglé.'))
