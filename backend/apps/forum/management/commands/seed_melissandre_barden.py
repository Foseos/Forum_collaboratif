"""Publie la dirigeante de la Maison de la Seconde Soif sans écraser sa fiche."""

from html import escape

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.forum.models import Category, Post, Topic


TITLE = "Mélissandre Barden"
SLUG = "melissandre-barden"
ACTOR = "Eva Green"
PORTRAIT = "https://upload.wikimedia.org/wikipedia/commons/5/59/Eva_Green_%28Headshot%29.jpg"
PHOTO_SOURCE = "https://commons.wikimedia.org/wiki/File:Eva_Green_(Headshot).jpg"
LINKS = [
    (
        "Valérie Tulle", "valerie-tulle",
        "L'expérience de Valérie au sein des Hérétiques est précieuse pour la Maison. Mélissandre lui propose une place sans présumer de sa réponse.",
        "https://media.tenor.com/-SrvDzmkULAAAAAC/valerie-tulle-the-vampire-diaries.gif",
    ),
    (
        "Mary Louise", "mary-louise",
        "Mélissandre aimerait que Mary Louise et Nora trouvent refuge auprès des leurs, à leurs propres conditions.",
        "https://media.tenor.com/b2MsZTkCAYoAAAAC/mary-louise-the-vampire-diaries.gif",
    ),
    (
        "Florie Delacroix", "florie-delacroix",
        "Leurs covens ont le siphonnage en commun, mais leurs natures diffèrent. Elles peuvent choisir la coopération ou défendre des méthodes opposées.",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Margot_Robbie_%2828129125629%29_%28cropped%29.jpg/500px-Margot_Robbie_%2828129125629%29_%28cropped%29.jpg",
    ),
]


def render_sheet():
    frame = "font-family:Georgia,serif;background:#0d0a1a;color:#e2d9f3;padding:clamp(1rem,4vw,2rem);border-radius:10px;max-width:800px;margin:auto;"
    section = "margin:1rem 0;padding:1rem;border:1px solid #574477;border-radius:8px;"
    parts = [
        f'<div data-melissandre-scenario="1" style="{frame}">',
        '<p style="color:#a78bfa;letter-spacing:.1em;">✦ NEXUS ARCANA · SCÉNARIO À PRENDRE ✦</p>',
        '<div style="display:flex;flex-wrap:wrap;gap:1.5rem;align-items:center;">',
        '<div style="flex:1;min-width:180px;">',
        f'<h1 style="color:#f5d76e;">{TITLE}</h1>',
        '<p>Hérétique TVD · Dirigeante de la Maison de la Seconde Soif · Mystic Falls</p>',
        '<p style="font-style:italic;">« Notre seconde vie mérite davantage qu’une seconde solitude. »</p>',
        '</div><figure style="margin:0;max-width:100%;">',
        f'<img src="{PORTRAIT}" alt="{TITLE}, incarnée par {ACTOR}" style="width:200px;max-width:100%;height:320px;object-fit:cover;border-radius:8px;">',
        f'<figcaption style="max-width:200px;font-size:.75rem;">{TITLE} — Ft {ACTOR}. '
        f'<a href="{PHOTO_SOURCE}" target="_blank" rel="noopener noreferrer" style="color:#c4b5fd;">Photo : Dan Shao / Wikimedia Commons, CC BY-SA 2.0</a>.</figcaption>',
        '</figure></div>',
        f'<section style="{section}"><h2 style="color:#c4b5fd;">I. Identité</h2><dl>',
    ]
    for label, value in [
        ("Âge", "48 ans depuis sa naissance ; transformée à 25 ans"),
        ("Date de naissance", "14 février 1985"),
        ("Transformation", "2010, à préciser avec le joueur"),
        ("Orientation sexuelle", "Au choix du joueur"),
        ("Origines", "Famille et lieu de naissance à préciser avec le joueur"),
        ("Nature", "Hérétique TVD · vampire siphonneuse"),
        ("Camp", "Au choix du joueur"),
        ("Faction", "La Maison de la Seconde Soif — dirigeante, sous validation de l’administration"),
        ("Résidence", "Mystic Falls"),
        ("Activité", "Organise l’accueil et la protection des Hérétiques de la Maison"),
    ]:
        parts.append(f'<dt style="color:#a78bfa;margin-top:.6rem;">{escape(label)}</dt><dd style="margin:.2rem 0;">{escape(value)}</dd>')
    parts.append(f'</dl></section><section style="{section}"><h2 style="color:#c4b5fd;">II. Quatre capacités de départ</h2>')
    parts.append('<p>Ses quatre capacités occupent ses emplacements de départ. Sa nature, son coven et sa fonction ne lui donnent aucun pouvoir supplémentaire. Toute nouvelle capacité ou évolution demande l’approbation du staff.</p>')
    for name, description in [
        ("Siphonnage", "Par contact, elle absorbe une quantité limitée de magie d’une source accessible, y compris de son propre vampirisme. Cette énergie s’épuise et ne permet pas d’annuler tout sort."),
        ("Sort de protection", "Elle convertit la magie siphonnée en une protection brève contre une attaque limitée. Maintenir cette protection consomme sa réserve."),
        ("Sens vampiriques", "Son ouïe et son odorat dépassent ceux d’une humaine, sans lui révéler automatiquement la nature ou les intentions d’autrui."),
        ("Guérison vampirique", "Son corps récupère plus vite de blessures ordinaires. Les atteintes graves et les vulnérabilités des vampires restent dangereuses."),
    ]:
        parts.append(f'<div data-base-power="1"><h3 style="color:#f5d76e;font-size:1rem;">{escape(name)}</h3><p>{escape(description)}</p></div>')
    parts.append('<p>Mélissandre demeure soumise à la soif et aux vulnérabilités des vampires. Sa réserve magique dépend des sources qu’elle siphonne ; elle ne crée pas de magie de façon autonome.</p></section>')
    parts.append(f'<section style="{section}"><h2 style="color:#c4b5fd;">III. Histoire</h2>')
    for paragraph in [
        "Née siphonneuse, Mélissandre a appris jeune à dissimuler ses gestes au milieu de sorciers qui redoutaient ce qu’elle pouvait leur prendre. Elle s’est longtemps tenue à l’écart de leurs cercles, jusqu’à ce qu’une transformation en vampire change à la fois sa faim et son rapport à la magie.",
        "La possibilité de siphonner son propre vampirisme ne l’a jamais délivrée de la soif. Elle a fondé la Maison de la Seconde Soif pour que les Hérétiques puissent partager leurs connaissances et s’entraider sans devoir reproduire les loyautés d’une ancienne famille. Chacun garde sa liberté de rejoindre la Maison ou de s’en éloigner.",
        "En 2033, la Convergence attire de nouveaux êtres surnaturels à Mystic Falls et rend certains équilibres plus fragiles. Mélissandre cherche à protéger les siens sans prétendre connaître la puissance à l’origine du phénomène. Son chemin peut croiser celui de Valérie, Mary Louise ou Florie ; leurs relations dépendront des joueurs concernés.",
    ]:
        parts.append(f'<p style="line-height:1.8;">{escape(paragraph)}</p>')
    parts.append(f'</section><section style="{section}"><h2 style="color:#c4b5fd;">IV. Liens</h2><ul>')
    for name, slug, description, _ in LINKS:
        parts.append(f'<li><a href="/topics/{slug}" style="color:#f5d76e;">{escape(name)}</a> — {escape(description)}</li>')
    parts.append(f'</ul></section><section style="{section}"><h2 style="color:#c4b5fd;">V. Pistes de jeu</h2><ul>')
    for hook in [
        "Accueillir une Hérétique qui refuse toute autorité et lui laisser le choix de rester.",
        "Négocier avec les Héritiers du Vide l’accès à une source magique sans confondre leurs deux covens.",
        "Faire face à une crise de soif au sein de la Maison tout en préservant la confiance entre ses membres.",
    ]:
        parts.append(f'<li>{escape(hook)}</li>')
    parts.append('</ul><p>Les relations, les détails du passé et les évolutions se construisent avec les joueurs concernés et le staff.</p></section></div>')
    return ''.join(parts)


class Command(BaseCommand):
    help = "Publie Mélissandre Barden sans écraser une fiche déjà modifiée."

    def handle(self, *args, **options):
        category = Category.objects.filter(slug="scenarios-a-prendre").first()
        author = get_user_model().objects.filter(role="fondatrice").order_by("id").first()
        if not category or not author:
            raise CommandError("La catégorie Scénarios ou le compte fondatrice est introuvable.")
        with transaction.atomic():
            topic, created = Topic.objects.get_or_create(
                category=category,
                slug=SLUG,
                defaults={
                    "title": TITLE,
                    "author": author,
                    "scenario_avatar_name": ACTOR,
                    "scenario_link_cards": [
                        {"gif": gif, "title": name, "text": description}
                        for name, _, description, gif in LINKS
                    ],
                    "is_locked": False,
                },
            )
            if created:
                Post.objects.create(topic=topic, author=author, content=render_sheet(), is_trusted_html=True)
                self.stdout.write(self.style.SUCCESS(f"Scénario publié : {TITLE}"))
            else:
                self.stdout.write(f"Scénario existant conservé : {topic.title}")
