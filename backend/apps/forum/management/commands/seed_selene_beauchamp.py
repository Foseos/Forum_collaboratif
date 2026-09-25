"""Publie le scénario de la dirigeante des Veilleurs du Voile."""

from html import escape

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.forum.models import Category, Post, Topic


TITLE = "Sélène Beauchamp"
SLUG = "selene-beauchamp"
ACTOR = "Caitríona Balfe"
PORTRAIT = (
    "https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/"
    "Caitriona_Balfe_at_the_2024_Toronto_International_Film_Festival_%28cropped%29.jpg/"
    "960px-Caitriona_Balfe_at_the_2024_Toronto_International_Film_Festival_%28cropped%29.jpg"
)
PHOTO_SOURCE = (
    "https://commons.wikimedia.org/wiki/File:"
    "Caitriona_Balfe_at_the_2024_Toronto_International_Film_Festival_(cropped).jpg"
)
LINKS = [
    (
        "Vincent Griffith", "vincent-griffith",
        "Ils défendent tous deux les sorciers de La Nouvelle-Orléans, sans toujours s'accorder sur la place des ancêtres dans leurs décisions.",
    ),
    (
        "Davina Claire", "davina-claire",
        "Sélène connaît le prix des décisions prises au nom d'un coven. Davina peut trouver en elle une alliée ou lui demander des comptes.",
    ),
    (
        "Freya Mikaelson", "freya-mikaelson",
        "Leurs recherches sur les perturbations de la Convergence peuvent se rejoindre, malgré des priorités différentes.",
    ),
]
LINK_GIFS = {
    "Vincent Griffith": "https://media.tenor.com/scAqhVKhcYcAAAAM/vincent-griffith-yusuf-gatewood.gif",
    "Davina Claire": "https://media.tenor.com/AOLeCs-uzRwAAAAM/davina-claire-the-originals.gif",
    "Freya Mikaelson": "https://media.tenor.com/ku_48xedFR8AAAAM/freya-mikaelson-riley-voelkel.gif",
}


def render_sheet():
    frame = "font-family:Georgia,serif;background:#0d0a1a;color:#e2d9f3;padding:clamp(1rem,4vw,2rem);border-radius:10px;max-width:800px;margin:auto;"
    section = "margin:1rem 0;padding:1rem;border:1px solid #574477;border-radius:8px;"
    parts = [
        f'<div data-selene-scenario="1" style="{frame}">',
        '<p style="color:#a78bfa;letter-spacing:.1em;">✦ NEXUS ARCANA · SCÉNARIO À PRENDRE ✦</p>',
        '<div style="display:flex;flex-wrap:wrap;gap:1.5rem;align-items:center;">',
        '<div style="flex:1;min-width:180px;">',
        f'<h1 style="color:#f5d76e;">{TITLE}</h1>',
        '<p>Sorcière TVD · Dirigeante des Veilleurs du Voile · La Nouvelle-Orléans</p>',
        '<p style="font-style:italic;">« Les morts peuvent nous parler. Ils ne doivent pas choisir notre avenir à notre place. »</p>',
        '</div><figure style="margin:0;max-width:100%;">',
        f'<img src="{PORTRAIT}" alt="{TITLE}, incarnée par {ACTOR}" style="width:200px;max-width:100%;height:320px;object-fit:cover;border-radius:8px;">',
        f'<figcaption style="max-width:200px;font-size:.75rem;">{TITLE} — Ft {ACTOR}. '
        f'<a href="{PHOTO_SOURCE}" target="_blank" rel="noopener noreferrer" style="color:#c4b5fd;">Photo : Kevin Payravi / Wikimedia Commons, CC BY-SA 4.0</a>.</figcaption>',
        '</figure></div>',
        f'<section style="{section}"><h2 style="color:#c4b5fd;">I. Identité</h2><dl>',
    ]
    for label, value in [
        ("Âge", "50 ans en 2033"),
        ("Date de naissance", "12 février 1983"),
        ("Orientation sexuelle", "Au choix de la joueuse"),
        ("Origines", "La Nouvelle-Orléans ; famille de sorcières liée aux rites ancestraux"),
        ("Nature", "Sorcière TVD"),
        ("Camp", "Attachée à la protection des vivants ; ses choix moraux restent à jouer"),
        ("Faction", "Les Veilleurs du Voile — dirigeante, sous validation de l'administration"),
        ("Résidence", "La Nouvelle-Orléans"),
        ("Activité", "Gardienne d'archives et médiatrice auprès des sorciers de la ville"),
    ]:
        parts.append(f'<dt style="color:#a78bfa;margin-top:.6rem;">{escape(label)}</dt><dd style="margin:.2rem 0;">{escape(value)}</dd>')
    parts.append(f'</dl></section><section style="{section}"><h2 style="color:#c4b5fd;">II. Quatre capacités de départ</h2>')
    parts.append('<p>Ses quatre capacités occupent ses emplacements de départ. Diriger le coven ne lui accorde aucun pouvoir supplémentaire. Toute nouvelle capacité ou évolution demande l’approbation du staff.</p>')
    for name, description in [
        ("Perception des présences", "Au cours d'un rituel, elle perçoit la trace d'un esprit proche d'un lieu consacré. Elle n'identifie pas automatiquement cet esprit et ne peut le contraindre à répondre."),
        ("Protection rituelle", "Elle trace une protection temporaire autour d'une personne ou d'un petit espace. Une magie plus puissante peut la rompre."),
        ("Localisation", "À partir d'un objet lié à la cible, elle recherche une direction ou un lieu approximatif. Les protections magiques et les déplacements brouillent le résultat."),
        ("Apaisement", "Par un sort bref, elle atténue une agitation surnaturelle ou les effets d'un enchantement mineur. Elle ne supprime ni la volonté ni les émotions d'autrui."),
    ]:
        parts.append(f'<div data-base-power="1"><h3 style="color:#f5d76e;font-size:1rem;">{escape(name)}</h3><p>{escape(description)}</p></div>')
    parts.append('<p>Ses rituels exigent du temps, de la concentration et une source de magie adaptée. Les esprits ne sont ni des serviteurs ni une source de réponses infaillible.</p></section>')
    parts.append(f'<section style="{section}"><h2 style="color:#c4b5fd;">III. Histoire</h2>')
    for paragraph in [
        "Sélène a grandi à La Nouvelle-Orléans au milieu des rites, des archives familiales et des querelles entre covens. Très tôt, elle a appris à écouter les récits des ancêtres, mais aussi à distinguer un conseil d'un ordre. Une décision imposée au nom des morts a autrefois coûté cher à une personne qu'elle voulait protéger ; depuis, elle refuse que la tradition dispense les vivants de répondre de leurs actes.",
        "Elle a réuni les Veilleurs du Voile autour d'une promesse : préserver les rites ancestraux, garder la mémoire des disparus et permettre aux sorciers de discuter ce qu'ils entendent. Sa place de dirigeante repose sur la confiance du coven, non sur une autorité absolue. Certains membres apprécient sa prudence ; d'autres estiment qu'elle hésite trop face aux avertissements des ancêtres.",
        "En 2033, la Convergence trouble des lieux de recueillement et fait surgir des échos difficiles à interpréter. Sélène enquête avec les siens, entre La Nouvelle-Orléans et les autres villes touchées. Elle ignore l'origine de la puissance à l'œuvre et refuse d'annoncer une prophétie qu'elle ne comprend pas. Ses alliances avec Vincent, Davina ou Freya restent à construire avec leurs joueurs.",
    ]:
        parts.append(f'<p style="line-height:1.8;">{escape(paragraph)}</p>')
    parts.append(f'</section><section style="{section}"><h2 style="color:#c4b5fd;">IV. Liens</h2><ul>')
    for name, slug, description in LINKS:
        parts.append(f'<li><a href="/topics/{slug}" style="color:#f5d76e;">{escape(name)}</a> — {escape(description)}</li>')
    parts.append(f'</ul></section><section style="{section}"><h2 style="color:#c4b5fd;">V. Pistes de jeu</h2><ul>')
    for hook in [
        "Faire face à un désaccord au sein des Veilleurs sur la place à donner aux ancêtres.",
        "Enquêter sur un lieu de mémoire perturbé par la Convergence, sans présumer de la cause du phénomène.",
        "Négocier avec les autres covens de La Nouvelle-Orléans pour protéger les habitants et les rites de chacun.",
    ]:
        parts.append(f'<li>{escape(hook)}</li>')
    parts.append('</ul><p>Les relations, les détails du passé et les évolutions se construisent avec les joueurs concernés et le staff.</p></section></div>')
    return ''.join(parts)


class Command(BaseCommand):
    help = "Publie Sélène Beauchamp sans écraser une fiche déjà modifiée."

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
                        {"gif": LINK_GIFS[name], "title": name, "text": description}
                        for name, _, description in LINKS
                    ],
                    "is_locked": False,
                },
            )
            if created:
                Post.objects.create(topic=topic, author=author, content=render_sheet(), is_trusted_html=True)
                self.stdout.write(self.style.SUCCESS(f"Scénario publié : {TITLE}"))
            else:
                cards = [dict(card) for card in topic.scenario_link_cards]
                for card in cards:
                    if not card.get("gif") and card.get("title") in LINK_GIFS:
                        card["gif"] = LINK_GIFS[card["title"]]
                if cards != topic.scenario_link_cards:
                    topic.scenario_link_cards = cards
                    topic.save(update_fields=["scenario_link_cards"])
                self.stdout.write(f"Scénario existant conservé : {topic.title}")
