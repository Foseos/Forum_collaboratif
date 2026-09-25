"""Complète Valérie et publie les scénarios de Mary Louise et Nora."""

from html import escape

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.forum.models import Category, Post, Topic


LINK_GIFS = {
    "Valérie Tulle": "https://media.tenor.com/-SrvDzmkULAAAAAC/valerie-tulle-the-vampire-diaries.gif",
    "Mary Louise": "https://media.tenor.com/b2MsZTkCAYoAAAAC/mary-louise-the-vampire-diaries.gif",
    "Nora Hildegard": "https://media.tenor.com/7SxQpQtLPkQAAAAC/nora-hildegard-nora.gif",
    "Stefan Salvatore": "https://media.tenor.com/wD9Tb8gIE1EAAAAM/stefan-salvatore.gif",
    "Bonnie Bennett": "https://media.tenor.com/SgwzIqg9Z_QAAAAC/bonnie-bennett.gif",
}


SCENARIOS = [
    {
        "title": "Valérie Tulle",
        "slug": "valerie-tulle",
        "actor": "Elizabeth Blackmore",
        "image": "https://i.pinimg.com/originals/6a/0e/d6/6a0ed60d2bf039c858af53255595aead.jpg",
        "previous_image": "https://light.sunphoto.ro/photos/normal/112549028_ENPDSIJ3.jpg",
        "birth": "14 septembre 1845 · repère adapté pour Nexus Arcana",
        "age": "188 ans en 2033 · apparence d'environ 18 ans",
        "orientation": "Au choix de la joueuse ; son histoire passée avec Stefan reste établie",
        "origin": "Coven Gemini, puis famille des Hérétiques de Lily Salvatore",
        "camp": "Au choix du joueur, selon son parcours actuel",
        "quote": "Survivre n'est pas la même chose que recommencer.",
        "history": [
            "Née siphonneuse au XIXe siècle, Valérie a grandi dans un monde qui traitait sa magie comme une anomalie. Sa rencontre avec Stefan Salvatore et la perte de leur enfant ont marqué sa vie bien avant qu'elle ne devienne la première Hérétique de la famille de Lily.",
            "L'emprisonnement dans le monde de 1903, puis les fractures de la famille hérétique, lui ont appris à se méfier des promesses de protection. En 2033, elle vient à Mystic Falls puis à San Francisco pour retrouver des traces de magie siphonnée près du Nexus.",
            "Elle connaît Stefan, mais ne revendique aucune place dans sa vie actuelle. Son histoire avec lui appartient au passé ; toute évolution se construit avec les joueurs concernés. Sa relation avec Mary Louise et Nora porte autant les souvenirs d'une famille que ses anciennes blessures.",
        ],
        "powers": [
            ("Siphonnage", "Absorbe une quantité limitée de magie au contact d'une source, y compris de son propre vampirisme ; la réserve s'épuise et ne permet pas d'annuler tout sort."),
            ("Vitesse vampirique", "Se déplace rapidement sur une courte distance ; surprise, obstacles et adversaires entraînés restent pertinents."),
            ("Guérison vampirique", "Récupère de blessures ordinaires avec du temps et du sang ; ne répare pas instantanément les atteintes surnaturelles graves."),
            ("Sort de protection", "Utilise la magie siphonnée pour renforcer brièvement une protection simple sur une personne ou un objet."),
        ],
        "links": [
            ("Stefan Salvatore", "stefan-salvatore", "Un premier amour et une perte commune. Leurs vies de 2033 ont suivi des routes différentes."),
            ("Mary Louise", "mary-louise", "Une ancienne sœur de cœur ; la confiance doit être reconstruite, sans effacer les désaccords."),
            ("Nora Hildegard", "nora-hildegard", "Une mémoire partagée du monde-prison et un regard parfois différent sur la liberté."),
        ],
        "hooks": [
            "Enquêter sur une source de magie que plusieurs covens souhaitent contrôler.",
            "Décider si elle rejoint la Maison de la Seconde Soif ou préfère rester indépendante.",
            "Retrouver les deux Hérétiques sans rejouer les conflits de leur ancienne famille.",
        ],
    },
    {
        "title": "Mary Louise",
        "slug": "mary-louise",
        "actor": "Teressa Liane",
        "image": "https://i.pinimg.com/736x/9e/c6/ed/9ec6ede8402146df0e0381900d5f0503.jpg",
        "previous_image": "https://www.hypnoweb.net/photo/153/3624/ok/1-Luinel.jpg",
        "birth": "22 mai 1851 · repère adapté pour Nexus Arcana",
        "age": "182 ans en 2033 · apparence d'environ 25 ans",
        "orientation": "Lesbienne · fiancée à Nora Hildegard",
        "origin": "Coven Gemini, puis famille des Hérétiques de Lily Salvatore",
        "camp": "Au choix du joueur ; sa loyauté envers Nora reste un lien établi",
        "quote": "Il m'a fallu un siècle pour apprendre à dire qui j'aime.",
        "history": [
            "Siphonneuse rejetée par les siens, Mary Louise a trouvé auprès de Lily et des Hérétiques la famille qui lui avait manqué. Le monde-prison de 1903 a renforcé sa fidélité aux personnes qu'elle aime, mais aussi sa peur de les perdre.",
            "Elle et Nora étaient fiancées. Dans la continuité de Nexus Arcana, la Convergence ouvre une bifurcation avant leur sacrifice : elles survivent sans comprendre la force qui a changé ce destin. Cela ne leur donne aucun pouvoir sur les mondes, la mort ou le temps.",
            "En 2033, Mary Louise hésite entre protéger Nora à tout prix et lui laisser l'espace qu'elle réclame. Elle observe avec méfiance les covens de Mystic Falls, puis découvre la Maison de la Seconde Soif. Leur couple est établi ; son évolution se décide avec la joueuse de Nora.",
        ],
        "powers": [
            ("Siphonnage", "Puise une réserve limitée de magie par contact avec une source, notamment son propre vampirisme ; ne vole pas durablement les pouvoirs d'autrui."),
            ("Sens vampiriques", "Perçoit plus nettement sons et odeurs proches ; le bruit, la distance et les protections peuvent la tromper."),
            ("Vitesse vampirique", "Accélère ses mouvements brièvement, sans garantir l'esquive ni la victoire."),
            ("Bouclier simple", "Canalise la magie disponible en une défense brève contre une attaque limitée ; sa concentration peut être rompue."),
        ],
        "links": [
            ("Nora Hildegard", "nora-hildegard", "Sa fiancée. Leur amour survit à la Convergence, mais leurs choix futurs se jouent à deux."),
            ("Valérie Tulle", "valerie-tulle", "Une ancienne alliée dont les secrets ont fissuré la confiance familiale."),
            ("Bonnie Bennett", "bonnie-bennett", "Une sorcière de Mystic Falls dont la proximité avec Nora peut devenir une occasion de dialogue ou de tension."),
        ],
        "hooks": [
            "Tenter de faire de la Maison de la Seconde Soif un refuge plutôt qu'une nouvelle prison.",
            "Explorer une alliance prudente avec les sorcières de Mystic Falls.",
            "Apprendre à protéger Nora sans décider à sa place.",
        ],
    },
    {
        "title": "Nora Hildegard",
        "slug": "nora-hildegard",
        "actor": "Scarlett Byrne",
        "image": "https://i.pinimg.com/736x/f0/95/b4/f095b4f2ab72c7879f617e696ccf087a.jpg",
        "birth": "3 novembre 1852 · repère adapté pour Nexus Arcana",
        "age": "181 ans en 2033 · apparence d'environ 23 ans",
        "orientation": "Lesbienne · fiancée à Mary Louise",
        "origin": "Coven Gemini, puis famille des Hérétiques de Lily Salvatore",
        "camp": "Au choix du joueur ; sa relation avec Mary Louise reste établie",
        "quote": "Une seconde vie mérite plus qu'une seconde cage.",
        "history": [
            "Nora a connu le rejet réservé aux siphonneurs avant de rejoindre la famille de Lily Salvatore. Sa relation avec Mary Louise lui a offert un point d'ancrage à travers les décennies et l'isolement du monde-prison.",
            "Dans la continuité de Nexus Arcana, la Convergence fait bifurquer leur histoire avant leur sacrifice. Nora et Mary Louise ont survécu, mais ignorent pourquoi. Le phénomène n'est ni un don personnel ni une protection permanente.",
            "En 2033, Nora veut connaître la vie hors des anciennes fidélités. La Maison de la Seconde Soif l'intéresse si elle y trouve une place librement choisie. Son lien avec Bonnie et ses retrouvailles avec Valérie ouvrent des conversations que la famille avait longtemps évitées.",
        ],
        "powers": [
            ("Siphonnage", "Prélève par contact une quantité limitée de magie, y compris depuis son vampirisme ; un manque de source ou l'épuisement interrompt ses sorts."),
            ("Vitesse vampirique", "Se déplace vite sur une courte distance, sans devenir insaisissable."),
            ("Guérison vampirique", "Guérit progressivement de blessures ordinaires ; les blessures graves et la faim restent des contraintes."),
            ("Illusion mineure", "À partir d'énergie siphonnée, altère brièvement une perception simple ; ne contrôle ni pensée ni volonté."),
        ],
        "links": [
            ("Mary Louise", "mary-louise", "Sa fiancée et son amour de longue date. Elles doivent redéfinir ensemble leur avenir."),
            ("Valérie Tulle", "valerie-tulle", "Une sœur de cœur dont elle connaît les forces et les silences."),
            ("Bonnie Bennett", "bonnie-bennett", "Une amitié possible née de leur curiosité mutuelle ; la suite appartient aux joueuses."),
        ],
        "hooks": [
            "Chercher ce qui a fait bifurquer son destin sans prétendre maîtriser la Convergence.",
            "Choisir une place dans un coven, ou assumer une voie indépendante.",
            "Créer de nouveaux liens sans renier ceux qui l'ont portée jusque-là.",
        ],
    },
]


def render_scenario(data):
    heading = "font-family:Georgia,serif;background:#0d0a1a;color:#e2d9f3;padding:clamp(1rem,4vw,2rem);border-radius:10px;max-width:800px;margin:auto;"
    section = "margin:1rem 0;padding:1rem;border:1px solid #574477;border-radius:8px;"
    parts = [
        f'<div data-heretic-scenario="1" style="{heading}">',
        '<p style="color:#a78bfa;letter-spacing:.1em;">✦ NEXUS ARCANA · SCÉNARIO À PRENDRE ✦</p>',
        '<div style="display:flex;flex-wrap:wrap;gap:1.5rem;align-items:center;">',
        '<div style="flex:1;min-width:180px;">',
        f'<h1 style="color:#f5d76e;">{escape(data["title"])}</h1>',
        '<p>Hérétique · Vampire siphonneuse · The Vampire Diaries</p>',
        f'<p style="font-style:italic;">« {escape(data["quote"])} »</p>',
        '</div><figure style="margin:0;max-width:100%;">',
        f'<img src="{escape(data["image"], quote=True)}" alt="{escape(data["title"], quote=True)}" style="width:200px;max-width:100%;height:320px;object-fit:cover;border-radius:8px;">',
        f'<figcaption style="max-width:200px;font-size:.75rem;">{escape(data["title"])} — Ft {escape(data["actor"])} (négociable avec le staff)</figcaption>',
        '</figure></div>',
        f'<section style="{section}"><h2 style="color:#c4b5fd;">I. Identité</h2><dl>',
    ]
    for label, value in [
        ("Âge", data["age"]), ("Date de naissance", data["birth"]),
        ("Orientation sexuelle", data["orientation"]),
        ("Origines", data["origin"]), ("Nature", "Hérétique · vampire siphonneuse"),
        ("Camp", data["camp"]),
        ("Faction", "Maison de la Seconde Soif possible, sous validation de l'administration"),
        ("Résidence", "Mystic Falls ou San Francisco, au choix du joueur"),
        ("Activité", "À définir par le joueur"),
    ]:
        parts.append(f'<dt style="color:#a78bfa;margin-top:.6rem;">{escape(label)}</dt><dd style="margin:.2rem 0;">{escape(value)}</dd>')
    parts.append(f'</dl></section><section style="{section}"><h2 style="color:#c4b5fd;">II. Quatre capacités de départ</h2>')
    parts.append('<p>Ces quatre capacités, actives et passives comprises, sont celles de départ. Toute nouvelle capacité ou évolution demande l’approbation du staff. Le coven ne donne aucun pouvoir supplémentaire.</p>')
    for name, description in data["powers"]:
        parts.append(f'<div data-base-power="1"><h3 style="color:#f5d76e;font-size:1rem;">{escape(name)}</h3><p>{escape(description)}</p></div>')
    parts.append('<p>La soif, les limites du siphonnage, le soleil et les autres faiblesses vampiriques restent applicables. Une bague de jour doit être obtenue selon les règles du forum.</p></section>')
    parts.append(f'<section style="{section}"><h2 style="color:#c4b5fd;">III. Histoire</h2>')
    parts.extend(f'<p style="line-height:1.8;">{escape(paragraph)}</p>' for paragraph in data["history"])
    parts.append(f'</section><section style="{section}"><h2 style="color:#c4b5fd;">IV. Liens</h2><ul>')
    for name, slug, description in data["links"]:
        parts.append(f'<li><a href="/topics/{escape(slug)}" style="color:#f5d76e;">{escape(name)}</a> — {escape(description)}</li>')
    parts.append(f'</ul></section><section style="{section}"><h2 style="color:#c4b5fd;">V. Pistes de jeu</h2><ul>')
    parts.extend(f'<li>{escape(hook)}</li>' for hook in data["hooks"])
    parts.append('</ul><p>Les détails non fixés se construisent avec les joueurs concernés et le staff, dans le respect de la chronologie de 2033.</p></section></div>')
    return ''.join(parts)


class Command(BaseCommand):
    help = "Publie les trois scénarios Hérétiques sans écraser les fiches déjà rédigées."

    def handle(self, *args, **options):
        category = Category.objects.filter(slug="scenarios-a-prendre").first()
        author = get_user_model().objects.filter(role="fondatrice").order_by("id").first()
        if not category or not author:
            raise CommandError("La catégorie Scénarios ou le compte fondatrice est introuvable.")
        with transaction.atomic():
            for data in SCENARIOS:
                topic, created = Topic.objects.get_or_create(
                    category=category, slug=data["slug"],
                    defaults={"title": data["title"], "author": author, "is_locked": False},
                )
                post = topic.posts.order_by("created_at", "id").first()
                if post:
                    cards = [dict(card) for card in topic.scenario_link_cards]
                    for card in cards:
                        if not card.get("gif") and card.get("title") in LINK_GIFS:
                            card["gif"] = LINK_GIFS[card["title"]]
                    if cards != topic.scenario_link_cards:
                        topic.scenario_link_cards = cards
                        topic.save(update_fields=["scenario_link_cards"])
                        self.stdout.write(self.style.SUCCESS(f"GIF des liens ajoutés : {data['title']}"))
                    content = post.content
                    old_image = data.get("previous_image")
                    if 'data-heretic-scenario="1"' in content:
                        if old_image and old_image in content:
                            content = content.replace(old_image, data["image"])
                        if '>Orientation sexuelle</dt>' not in content:
                            anchor = '<dt style="color:#a78bfa;margin-top:.6rem;">Origines</dt>'
                            orientation = f'<dt style="color:#a78bfa;margin-top:.6rem;">Orientation sexuelle</dt><dd style="margin:.2rem 0;">{escape(data["orientation"])}</dd>'
                            content = content.replace(anchor, orientation + anchor, 1)
                        if content != post.content:
                            Post.objects.filter(pk=post.pk).update(content=content)
                            self.stdout.write(self.style.SUCCESS(f"Fiche actualisée : {data['title']}"))
                            continue
                    self.stdout.write(f"Fiche existante conservée : {data['title']}")
                    continue
                if not topic.scenario_avatar_name:
                    topic.scenario_avatar_name = data["actor"]
                topic.is_locked = False
                topic.scenario_link_cards = [
                    {"gif": LINK_GIFS.get(name, ""), "title": name, "text": description}
                    for name, _, description in data["links"]
                ]
                topic.save(update_fields=["scenario_avatar_name", "scenario_link_cards", "is_locked"])
                Post.objects.create(
                    topic=topic, author=author,
                    content=render_scenario(data), is_trusted_html=True,
                )
                self.stdout.write(self.style.SUCCESS(
                    f"{'Créé' if created else 'Complété'} : {data['title']}"
                ))
