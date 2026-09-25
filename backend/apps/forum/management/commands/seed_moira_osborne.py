"""Publie la dirigeante du Cercle des Terres Perdues sans écraser sa fiche."""

from html import escape

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.forum.models import Category, Post, Topic


TITLE = "Moira Osborne"
SLUG = "moira-osborne"
ACTOR = "Zoë Kravitz"
PORTRAIT = (
    "https://upload.wikimedia.org/wikipedia/commons/thumb/0/01/"
    "Zo%C3%AB_Kravitz_%2842814396185%29_%28cropped%29.jpg/"
    "500px-Zo%C3%AB_Kravitz_%2842814396185%29_%28cropped%29.jpg"
)
PHOTO_SOURCE = "https://commons.wikimedia.org/wiki/File:Zo%C3%AB_Kravitz_(42814396185)_(cropped).jpg"
LINKS = [
    (
        "Bonnie Bennett", "bonnie-bennett",
        "Moira aimerait échanger avec elle sur les effets de la Convergence à Mystic Falls. Bonnie choisira elle-même la place qu'elle souhaite lui accorder.",
        "https://media.tenor.com/SgwzIqg9Z_QAAAAC/bonnie-bennett.gif",
    ),
    (
        "Belisama Vaskov", "belisama-vaskov",
        "Deux dirigeantes de covens aux pratiques différentes : leur curiosité mutuelle peut ouvrir une collaboration ou une dispute de méthode.",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Sarah_Paulson_at_the_2024_Toronto_International_Film_Festival_2_%28cropped%29.jpg/500px-Sarah_Paulson_at_the_2024_Toronto_International_Film_Festival_2_%28cropped%29.jpg",
    ),
    (
        "Sélène Beauchamp", "selene-beauchamp",
        "Moira cherche un lieu où son coven pourrait séjourner à La Nouvelle-Orléans ; Sélène peut devenir une interlocutrice, sans accord préétabli.",
        "https://media.tenor.com/KAIBDVzia8IAAAAM/caitriona-balfe-cait.gif",
    ),
]


def render_sheet():
    frame = "font-family:Georgia,serif;background:#0d0a1a;color:#e2d9f3;padding:clamp(1rem,4vw,2rem);border-radius:10px;max-width:800px;margin:auto;"
    section = "margin:1rem 0;padding:1rem;border:1px solid #574477;border-radius:8px;"
    parts = [
        f'<div data-moira-scenario="1" style="{frame}">',
        '<p style="color:#a78bfa;letter-spacing:.1em;">✦ NEXUS ARCANA · SCÉNARIO À PRENDRE ✦</p>',
        '<div style="display:flex;flex-wrap:wrap;gap:1.5rem;align-items:center;">',
        '<div style="flex:1;min-width:180px;">',
        f'<h1 style="color:#f5d76e;">{TITLE}</h1>',
        '<p>Voyageuse TVD · Dirigeante du Cercle des Terres Perdues · Itinérante</p>',
        '<p style="font-style:italic;">« Voyager n’interdit pas de chercher un endroit où revenir. »</p>',
        '</div><figure style="margin:0;max-width:100%;">',
        f'<img src="{PORTRAIT}" alt="{TITLE}, incarnée par {ACTOR}" style="width:200px;max-width:100%;height:320px;object-fit:cover;border-radius:8px;">',
        f'<figcaption style="max-width:200px;font-size:.75rem;">{TITLE} — Ft {ACTOR}. '
        f'<a href="{PHOTO_SOURCE}" target="_blank" rel="noopener noreferrer" style="color:#c4b5fd;">Photo : Gage Skidmore / Wikimedia Commons, CC BY-SA 2.0</a>.</figcaption>',
        '</figure></div>',
        f'<section style="{section}"><h2 style="color:#c4b5fd;">I. Identité</h2><dl>',
    ]
    for label, value in [
        ("Âge", "45 ans en 2033"),
        ("Date de naissance", "6 juillet 1988"),
        ("Orientation sexuelle", "Au choix de la joueuse"),
        ("Origines", "Lignée de Voyageurs ; lieu de naissance et famille proche à préciser avec la joueuse"),
        ("Nature", "Voyageuse · sorcière TVD"),
        ("Camp", "Au choix de la joueuse ; la survie du Cercle guide nombre de ses décisions"),
        ("Faction", "Le Cercle des Terres Perdues — dirigeante, sous validation de l'administration"),
        ("Résidence", "Itinérante entre les villes de la Convergence"),
        ("Activité", "Organisatrice des déplacements et gardienne des rites du Cercle"),
    ]:
        parts.append(f'<dt style="color:#a78bfa;margin-top:.6rem;">{escape(label)}</dt><dd style="margin:.2rem 0;">{escape(value)}</dd>')
    parts.append(f'</dl></section><section style="{section}"><h2 style="color:#c4b5fd;">II. Quatre capacités de départ</h2>')
    parts.append('<p>Ses quatre capacités occupent ses emplacements de départ. Le Cercle et sa fonction ne lui donnent aucun pouvoir supplémentaire. Toute nouvelle capacité ou évolution demande l’approbation du staff.</p>')
    for name, description in [
        ("Magie collective", "Elle participe à un rituel partagé avec d'autres Voyageurs consentants. La portée du sort dépend du groupe, de la préparation et des sources disponibles ; elle ne peut reproduire seule un grand rituel."),
        ("Lecture des traces", "Elle repère les marques récentes d'un passage magique sur un lieu ou un objet proche. Cette perception ne révèle ni l'identité ni les intentions de ceux qui sont passés."),
        ("Voile de discrétion", "Elle atténue brièvement la signature magique d'un petit groupe immobile. Le mouvement, un sort actif ou une recherche ciblée peuvent défaire ce voile."),
        ("Protection de cercle", "Elle trace une limite rituelle qui réduit l'effet d'une magie mineure entrant dans un espace restreint. Elle doit rester concentrée et une attaque soutenue peut rompre la protection."),
    ]:
        parts.append(f'<div data-base-power="1"><h3 style="color:#f5d76e;font-size:1rem;">{escape(name)}</h3><p>{escape(description)}</p></div>')
    parts.append('<p>Ses rituels demandent de la préparation et ne permettent ni de neutraliser toute magie ni de se déplacer instantanément entre les villes.</p></section>')
    parts.append(f'<section style="{section}"><h2 style="color:#c4b5fd;">III. Histoire</h2>')
    for paragraph in [
        "Moira a grandi au sein d'une lignée de Voyageurs pour qui les routes, les haltes et les départs faisaient partie de la vie quotidienne. Elle a appris les rites collectifs avant de savoir ce que signifiait habiter longtemps au même endroit. Lorsqu'une halte s'est terminée par une rupture avec des sorciers locaux, elle a compris qu'un refuge ne se gagne pas par la seule force d'un sort.",
        "Elle a rassemblé le Cercle des Terres Perdues autour d'un projet plus durable que la survie de la semaine suivante : conserver leurs pratiques, négocier leurs passages et chercher un lieu qui puisse devenir le leur. Certains Voyageurs préfèrent rester mobiles ; d'autres voudraient s'établir tout de suite. Moira dirige leurs échanges, mais ne peut imposer un foyer à ceux qui ne le choisissent pas.",
        "En 2033, la Convergence perturbe plusieurs endroits traversés par le Cercle. Moira relève ces anomalies sans prétendre connaître la puissance à leur origine. Ses voyages l'amènent vers Mystic Falls et La Nouvelle-Orléans, où elle pourrait croiser Bonnie, Belisama ou Sélène. La suite de ces liens appartient aux joueuses concernées.",
    ]:
        parts.append(f'<p style="line-height:1.8;">{escape(paragraph)}</p>')
    parts.append(f'</section><section style="{section}"><h2 style="color:#c4b5fd;">IV. Liens</h2><ul>')
    for name, slug, description, _ in LINKS:
        parts.append(f'<li><a href="/topics/{slug}" style="color:#f5d76e;">{escape(name)}</a> — {escape(description)}</li>')
    parts.append(f'</ul></section><section style="{section}"><h2 style="color:#c4b5fd;">V. Pistes de jeu</h2><ul>')
    for hook in [
        "Choisir avec les membres du Cercle entre une nouvelle route et un lieu où s'établir.",
        "Négocier une halte avec un coven local sans renoncer aux rites des Voyageurs.",
        "Enquêter sur une anomalie de la Convergence trouvée sur le trajet du Cercle.",
    ]:
        parts.append(f'<li>{escape(hook)}</li>')
    parts.append('</ul><p>Les relations, les détails du passé et les évolutions se construisent avec les joueurs concernés et le staff.</p></section></div>')
    return ''.join(parts)


class Command(BaseCommand):
    help = "Publie Moira Osborne sans écraser une fiche déjà modifiée."

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
