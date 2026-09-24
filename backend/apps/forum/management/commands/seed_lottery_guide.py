"""Install the optional activity lottery in Contextes et animations."""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.forum.models import Category, Post, Topic


GUIDE = """<section style="max-width:850px;margin:auto;padding:1.5rem;background:#151024;color:#e9def4;border:1px solid #6b5489;border-radius:12px;line-height:1.8">
<h2 style="color:#f5d76e">✦ La loterie des Arcana Flouz</h2>
<p>Vos scènes de RP peuvent vous offrir un petit bonus d'Arcana Flouz. La participation est facultative et gratuite.</p>
<h3 style="color:#c4b5fd">Comment obtenir un tirage ?</h3>
<p>Publiez un message de RP de <strong>plus de 100 mots</strong> dans un lieu de jeu. Revenez ensuite sur cette page et cliquez sur « Tenter ma chance ». Un message publié au cours des sept derniers jours est nécessaire. Un seul tirage est possible tous les sept jours ; le message utilisé ne peut pas servir une seconde fois.</p>
<p>Le tirage rapporte toujours un bonus : <strong>5, 10, 15, 20 ou 30 Arcana Flouz</strong>. Les gains de 5 ou 10 sont plus fréquents que les plus gros lots. Ce bonus s'ajoute aux 10 Arcana Flouz déjà accordés pour un message de plus de 100 mots.</p>
<p>Le résultat est enregistré et les Arcana Flouz sont crédités directement sur votre compte.</p>
</section>"""


class Command(BaseCommand):
    help = 'Crée le sujet de la loterie des Arcana Flouz.'

    @transaction.atomic
    def handle(self, *args, **options):
        category = Category.objects.get(slug='contextes-et-animations')
        founder = get_user_model().objects.filter(role='fondatrice').first()
        if founder is None:
            raise ValueError('Compte fondatrice introuvable.')
        topic, created = Topic.objects.get_or_create(
            slug='loterie-des-arcana-flouz',
            defaults={'title': '✦ Loterie des Arcana Flouz', 'category': category,
                      'author': founder, 'is_pinned': True},
        )
        if topic.category_id != category.pk:
            raise ValueError('Le sujet de la loterie existe dans une autre rubrique.')
        if created or not topic.posts.exists():
            Post.objects.create(topic=topic, author=founder, content=GUIDE, is_trusted_html=True)
        self.stdout.write(self.style.SUCCESS('Loterie présente dans Contextes et animations.'))
