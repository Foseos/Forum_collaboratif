"""Publie la dirigeante des Héritiers du Vide sans écraser sa fiche."""

from html import escape

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.forum.models import Category, Post, Topic


TITLE = "Florie Delacroix"
SLUG = "florie-delacroix"
ACTOR = "Margot Robbie"
PORTRAIT = (
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/"
    "Margot_Robbie_%2828129125629%29_%28cropped%29.jpg/"
    "500px-Margot_Robbie_%2828129125629%29_%28cropped%29.jpg"
)
PHOTO_SOURCE = "https://commons.wikimedia.org/wiki/File:Margot_Robbie_(28129125629)_(cropped).jpg"
LINKS = [
    (
        "Valérie Tulle", "valerie-tulle",
        "Leurs deux covens accueillent des siphonneurs, mais Florie refuse de confondre sa nature avec celle des Hérétiques. Une entraide reste possible.",
        "https://media.tenor.com/-SrvDzmkULAAAAAC/valerie-tulle-the-vampire-diaries.gif",
    ),
    (
        "Belisama Vaskov", "belisama-vaskov",
        "Florie souhaite comprendre les traces laissées par l’Expression sans exposer les siens à une source de magie qu’ils ne maîtrisent pas.",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Sarah_Paulson_at_the_2024_Toronto_International_Film_Festival_2_%28cropped%29.jpg/500px-Sarah_Paulson_at_the_2024_Toronto_International_Film_Festival_2_%28cropped%29.jpg",
    ),
    (
        "Bonnie Bennett", "bonnie-bennett",
        "Une rencontre à Mystic Falls pourrait ouvrir un échange sur les sources magiques disponibles et les limites que chacune entend poser.",
        "https://media.tenor.com/SgwzIqg9Z_QAAAAC/bonnie-bennett.gif",
    ),
]


def render_sheet():
    frame = "font-family:Georgia,serif;background:#0d0a1a;color:#e2d9f3;padding:clamp(1rem,4vw,2rem);border-radius:10px;max-width:800px;margin:auto;"
    section = "margin:1rem 0;padding:1rem;border:1px solid #574477;border-radius:8px;"
    parts = [
        f'<div data-florie-scenario="1" style="{frame}">',
        '<p style="color:#a78bfa;letter-spacing:.1em;">✦ NEXUS ARCANA · SCÉNARIO À PRENDRE ✦</p>',
        '<div style="display:flex;flex-wrap:wrap;gap:1.5rem;align-items:center;">',
        '<div style="flex:1;min-width:180px;">',
        f'<h1 style="color:#f5d76e;">{TITLE}</h1>',
        '<p>Siphonneuse TVD · Dirigeante des Héritiers du Vide · Mystic Falls</p>',
        '<p style="font-style:italic;">« Le vide n’est pas une faute. Il nous appartient de choisir ce que nous en faisons. »</p>',
        '</div><figure style="margin:0;max-width:100%;">',
        f'<img src="{PORTRAIT}" alt="{TITLE}, incarnée par {ACTOR}" style="width:200px;max-width:100%;height:320px;object-fit:cover;border-radius:8px;">',
        f'<figcaption style="max-width:200px;font-size:.75rem;">{TITLE} — Ft {ACTOR}. '
        f'<a href="{PHOTO_SOURCE}" target="_blank" rel="noopener noreferrer" style="color:#c4b5fd;">Photo : Eva Rinaldi / Wikimedia Commons, CC BY-SA 2.0</a>.</figcaption>',
        '</figure></div>',
        f'<section style="{section}"><h2 style="color:#c4b5fd;">I. Identité</h2><dl>',
    ]
    for label, value in [
        ("Âge", "43 ans en 2033"),
        ("Date de naissance", "8 mars 1990"),
        ("Orientation sexuelle", "Au choix de la joueuse"),
        ("Origines", "Famille et lieu de naissance à préciser avec la joueuse"),
        ("Nature", "Sorcière siphonneuse TVD, non vampirique"),
        ("Camp", "Au choix de la joueuse"),
        ("Faction", "Les Héritiers du Vide — dirigeante, sous validation de l’administration"),
        ("Résidence", "Mystic Falls"),
        ("Activité", "Coordonne les recherches de sources magiques et les accords du coven"),
    ]:
        parts.append(f'<dt style="color:#a78bfa;margin-top:.6rem;">{escape(label)}</dt><dd style="margin:.2rem 0;">{escape(value)}</dd>')
    parts.append(f'</dl></section><section style="{section}"><h2 style="color:#c4b5fd;">II. Quatre capacités de départ</h2>')
    parts.append('<p>Ses quatre capacités occupent ses emplacements de départ. Son rôle et son coven ne lui donnent aucun pouvoir supplémentaire. Toute nouvelle capacité ou évolution demande l’approbation du staff.</p>')
    for name, description in [
        ("Siphonnage", "Par contact, elle absorbe une quantité limitée de magie présente dans un objet enchanté ou chez une personne consentante. Elle ne vole pas définitivement un pouvoir inné et ne produit pas sa propre magie."),
        ("Perception des sources", "Elle distingue la présence d’une source magique proche, sans connaître automatiquement sa nature, sa puissance ni ses dangers."),
        ("Protection empruntée", "En dépensant l’énergie siphonnée, elle érige brièvement une protection contre une attaque magique limitée. La protection cède sous une pression soutenue."),
        ("Stabilisation d’enchantement", "Elle canalise de l’énergie siphonnée pour ralentir la dégradation d’un petit sort ou d’un objet enchanté. Cet effet est temporaire et ne répare pas une magie détruite."),
    ]:
        parts.append(f'<div data-base-power="1"><h3 style="color:#f5d76e;font-size:1rem;">{escape(name)}</h3><p>{escape(description)}</p></div>')
    parts.append('<p>Florie reste une siphonneuse non vampirique : elle ne possède aucune capacité liée au vampirisme et doit trouver une source de magie avant de lancer un sort.</p></section>')
    parts.append(f'<section style="{section}"><h2 style="color:#c4b5fd;">III. Histoire</h2>')
    for paragraph in [
        "Florie a grandi parmi des sorciers qui interprétaient son incapacité à produire sa propre magie comme un manque à cacher. Elle a appris à reconnaître les objets enchantés et à demander la permission avant d’y puiser. Cette discipline lui a donné une place que personne ne lui avait offerte.",
        "Elle a ensuite réuni d’autres siphonneurs non vampiriques. Les Héritiers du Vide partagent des connaissances, recensent les sources disponibles et négocient leur usage avec leurs propriétaires. Florie dirige ces échanges parce qu’elle a gagné leur confiance ; elle doit encore convaincre certains membres que la prudence ne signifie pas renoncer à agir.",
        "En 2033, la Convergence fait apparaître de nouvelles anomalies autour de Mystic Falls. Florie y voit des pistes à étudier, sans prétendre savoir quelle puissance en est à l’origine. Ses recherches peuvent la rapprocher de Valérie, Belisama ou Bonnie, selon les choix des joueuses concernées.",
    ]:
        parts.append(f'<p style="line-height:1.8;">{escape(paragraph)}</p>')
    parts.append(f'</section><section style="{section}"><h2 style="color:#c4b5fd;">IV. Liens</h2><ul>')
    for name, slug, description, _ in LINKS:
        parts.append(f'<li><a href="/topics/{slug}" style="color:#f5d76e;">{escape(name)}</a> — {escape(description)}</li>')
    parts.append(f'</ul></section><section style="{section}"><h2 style="color:#c4b5fd;">V. Pistes de jeu</h2><ul>')
    for hook in [
        "Négocier avec un autre coven l’accès à un lieu ou à un objet chargé de magie.",
        "Aider une jeune siphonneuse à trouver sa place sans lui imposer les choix de Florie.",
        "Enquêter sur une source apparue après la Convergence et décider si son usage est acceptable.",
    ]:
        parts.append(f'<li>{escape(hook)}</li>')
    parts.append('</ul><p>Les relations, les détails du passé et les évolutions se construisent avec les joueurs concernés et le staff.</p></section></div>')
    return ''.join(parts)


class Command(BaseCommand):
    help = "Publie Florie Delacroix sans écraser une fiche déjà modifiée."

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
