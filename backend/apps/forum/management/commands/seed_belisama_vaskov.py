"""Publie la dirigeante de la Chambre des Murmures sans écraser sa fiche."""

from html import escape

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.forum.models import Category, Post, Topic


TITLE = "Belisama Vaskov"
SLUG = "belisama-vaskov"
ACTOR = "Sarah Paulson"
PORTRAIT = (
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/"
    "Sarah_Paulson_at_the_2024_Toronto_International_Film_Festival_2_%28cropped%29.jpg/"
    "500px-Sarah_Paulson_at_the_2024_Toronto_International_Film_Festival_2_%28cropped%29.jpg"
)
PHOTO_SOURCE = (
    "https://commons.wikimedia.org/wiki/File:"
    "Sarah_Paulson_at_the_2024_Toronto_International_Film_Festival_2_(cropped).jpg"
)
LINKS = [
    (
        "Sélène Beauchamp", "selene-beauchamp",
        "Les deux dirigeantes défendent le droit de leurs membres à choisir, mais leurs méthodes magiques suscitent des désaccords.",
        "https://media.tenor.com/KAIBDVzia8IAAAAM/caitriona-balfe-cait.gif",
    ),
    (
        "Bonnie Bennett", "bonnie-bennett",
        "Belisama respecte sa détermination et aimerait confronter avec elle les limites de l'Expression ; Bonnie reste libre de refuser.",
        "https://media.tenor.com/SgwzIqg9Z_QAAAAC/bonnie-bennett.gif",
    ),
    (
        "Davina Claire", "davina-claire",
        "Leur goût pour l'indépendance peut les rapprocher, même si Davina se méfie de toute magie présentée comme une solution universelle.",
        "https://media.tenor.com/AOLeCs-uzRwAAAAM/davina-claire-the-originals.gif",
    ),
]


def render_sheet():
    frame = "font-family:Georgia,serif;background:#0d0a1a;color:#e2d9f3;padding:clamp(1rem,4vw,2rem);border-radius:10px;max-width:800px;margin:auto;"
    section = "margin:1rem 0;padding:1rem;border:1px solid #574477;border-radius:8px;"
    parts = [
        f'<div data-belisama-scenario="1" style="{frame}">',
        '<p style="color:#a78bfa;letter-spacing:.1em;">✦ NEXUS ARCANA · SCÉNARIO À PRENDRE ✦</p>',
        '<div style="display:flex;flex-wrap:wrap;gap:1.5rem;align-items:center;">',
        '<div style="flex:1;min-width:180px;">',
        f'<h1 style="color:#f5d76e;">{TITLE}</h1>',
        '<p>Sorcière TVD · Dirigeante de la Chambre des Murmures · Mystic Falls</p>',
        '<p style="font-style:italic;">« Une voix qui murmure n’a pas toujours raison. Encore faut-il oser l’écouter. »</p>',
        '</div><figure style="margin:0;max-width:100%;">',
        f'<img src="{PORTRAIT}" alt="{TITLE}, incarnée par {ACTOR}" style="width:200px;max-width:100%;height:320px;object-fit:cover;border-radius:8px;">',
        f'<figcaption style="max-width:200px;font-size:.75rem;">{TITLE} — Ft {ACTOR}. '
        f'<a href="{PHOTO_SOURCE}" target="_blank" rel="noopener noreferrer" style="color:#c4b5fd;">Photo : John Sears / WikiPortraits, CC BY-SA 4.0</a>.</figcaption>',
        '</figure></div>',
        f'<section style="{section}"><h2 style="color:#c4b5fd;">I. Identité</h2><dl>',
    ]
    for label, value in [
        ("Âge", "48 ans en 2033"),
        ("Date de naissance", "16 janvier 1985"),
        ("Orientation sexuelle", "Au choix de la joueuse"),
        ("Origines", "Famille de sorciers ; parcours et liens familiaux à préciser avec la joueuse"),
        ("Nature", "Sorcière TVD"),
        ("Camp", "Au choix de la joueuse ; ses décisions ont des conséquences à assumer"),
        ("Faction", "La Chambre des Murmures — dirigeante, sous validation de l'administration"),
        ("Résidence", "Mystic Falls"),
        ("Activité", "Chercheuse en traditions magiques et responsable des archives du coven"),
    ]:
        parts.append(f'<dt style="color:#a78bfa;margin-top:.6rem;">{escape(label)}</dt><dd style="margin:.2rem 0;">{escape(value)}</dd>')
    parts.append(f'</dl></section><section style="{section}"><h2 style="color:#c4b5fd;">II. Quatre capacités de départ</h2>')
    parts.append('<p>Belisama privilégie l’Expression, sans en maîtriser tous les effets. Ses quatre capacités occupent ses emplacements de départ ; le coven et sa fonction ne lui en donnent aucune autre. Toute nouvelle capacité ou évolution demande l’approbation du staff.</p>')
    for name, description in [
        ("Expression focalisée", "Elle canalise une émotion dans un sort bref et précis, sans rituel long. L'effet reste limité ; la fatigue ou une émotion contradictoire peut rompre sa concentration."),
        ("Perception des traces magiques", "Elle ressent qu'un sort récent a marqué un objet ou un lieu proche. Elle n'en connaît pas automatiquement l'auteur, la nature exacte ni l'intention."),
        ("Voile de silence", "Elle étouffe les sons dans un petit espace pendant quelques instants. Le sort exige sa concentration et ne rend personne invisible."),
        ("Dissipation mineure", "Elle défait un enchantement simple après en avoir compris le point d'ancrage. Les protections complexes ou entretenues par un autre sorcier lui résistent."),
    ]:
        parts.append(f'<div data-base-power="1"><h3 style="color:#f5d76e;font-size:1rem;">{escape(name)}</h3><p>{escape(description)}</p></div>')
    parts.append('<p>L’Expression ne contourne ni les limites du personnage ni l’accord des autres joueurs pour les effets qui touchent leurs personnages.</p></section>')
    parts.append(f'<section style="{section}"><h2 style="color:#c4b5fd;">III. Histoire</h2>')
    for paragraph in [
        "Belisama a appris la magie au sein d'une famille attachée aux rituels et aux règles transmises de génération en génération. En découvrant l'Expression, elle a d'abord cherché ce qu'elle permettait là où les sorts connus échouaient. Une expérience menée trop vite a blessé une personne proche d'elle ; Belisama n'en tire ni une interdiction absolue ni une excuse. Elle a choisi d'étudier cette pratique avec plus de méthode.",
        "Elle a fondé la Chambre des Murmures pour rassembler des sorcières et des sorciers prêts à discuter leurs essais, leurs échecs et leurs limites. Le coven utilise l'Expression en priorité, mais ses membres ne sont pas tenus de penser comme elle. Certains souhaitent aller plus loin ; d'autres jugent que Belisama ouvre une porte qu'elle ne pourra pas refermer. Sa direction tient à la confiance de ces membres, pas à un pouvoir sur eux.",
        "En 2033, les perturbations de la Convergence touchent Mystic Falls. Belisama cherche à savoir si elles modifient les sorts d'Expression, sans prétendre connaître l'origine du phénomène. Elle veut comparer ses observations avec d'autres covens ; ses rapports avec Sélène, Bonnie et Davina seront décidés avec leurs joueuses.",
    ]:
        parts.append(f'<p style="line-height:1.8;">{escape(paragraph)}</p>')
    parts.append(f'</section><section style="{section}"><h2 style="color:#c4b5fd;">IV. Liens</h2><ul>')
    for name, slug, description, _ in LINKS:
        parts.append(f'<li><a href="/topics/{slug}" style="color:#f5d76e;">{escape(name)}</a> — {escape(description)}</li>')
    parts.append(f'</ul></section><section style="{section}"><h2 style="color:#c4b5fd;">V. Pistes de jeu</h2><ul>')
    for hook in [
        "Arbitrer un désaccord entre membres de la Chambre sur un rituel d'Expression.",
        "Étudier une anomalie de la Convergence sans promettre de solution immédiate.",
        "Négocier un échange de connaissances avec un autre coven tout en protégeant la liberté du sien.",
    ]:
        parts.append(f'<li>{escape(hook)}</li>')
    parts.append('</ul><p>Les relations, les détails du passé et les évolutions se construisent avec les joueurs concernés et le staff.</p></section></div>')
    return ''.join(parts)


class Command(BaseCommand):
    help = "Publie Belisama Vaskov sans écraser une fiche déjà modifiée."

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
