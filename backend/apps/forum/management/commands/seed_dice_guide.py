"""Installe le guide du dé dans Contextes et animations."""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.forum.models import Category, Post, Topic


GUIDE = """<section style="max-width:850px;margin:auto;padding:1.5rem;background:#151024;color:#e9def4;border:1px solid #6b5489;border-radius:12px;line-height:1.8">
<h2 style="color:#f5d76e">🎲 Le Dé du destin</h2>
<p>Dans les contextes et animations, le dé aide à faire avancer une scène lorsque son issue est incertaine. Son usage est facultatif dans les jeux libres. L'équipe peut indiquer qu'un lancer est attendu dans une animation particulière.</p>
<h3 style="color:#c4b5fd">Comment jouer ?</h3>
<p>Décrivez l'action que votre personnage tente dans le sujet concerné, puis utilisez « Lancer le dé à six faces ». Le résultat est publié sous votre nom et reste visible. Un nouveau lancer peut être fait après trente secondes.</p>
<table style="width:100%;border-collapse:collapse"><thead><tr><th style="text-align:left;color:#f5d76e">Résultat</th><th style="text-align:left;color:#f5d76e">Piste narrative</th></tr></thead><tbody>
<tr><td>1–2</td><td>L'action échoue ou crée une complication.</td></tr>
<tr><td>3–4</td><td>L'action réussit partiellement, avec une conséquence à jouer.</td></tr>
<tr><td>5–6</td><td>L'action réussit.</td></tr>
</tbody></table>
<p>Exemple : près du Nemeton, un personnage cherche un indice. Sur 3, il le trouve, mais son passage attire l'attention d'une créature.</p>
<p><strong>Le dé ne décide jamais à lui seul des blessures graves, de la mort, des actions ou des émotions d'un autre personnage.</strong> Les joueurs interprètent le résultat ensemble ; le staff tranche les situations d'animation qui nécessitent une précision.</p>
</section>"""


class Command(BaseCommand):
    help = 'Crée le sujet de présentation du Dé du destin.'

    @transaction.atomic
    def handle(self, *args, **options):
        category = Category.objects.get(slug='contextes-et-animations')
        founder = get_user_model().objects.filter(role='fondatrice').first()
        if founder is None:
            raise ValueError('Compte fondatrice introuvable.')
        topic, created = Topic.objects.get_or_create(
            slug='le-de-du-destin',
            defaults={'title': '🎲 Le Dé du destin — mode d’emploi', 'category': category,
                      'author': founder, 'is_pinned': True},
        )
        if topic.category_id != category.pk:
            raise ValueError('Le sujet du dé existe dans une autre rubrique.')
        if created or not topic.posts.exists():
            Post.objects.create(topic=topic, author=founder, content=GUIDE, is_trusted_html=True)
        self.stdout.write(self.style.SUCCESS('Dé du destin présent dans Contextes et animations.'))
