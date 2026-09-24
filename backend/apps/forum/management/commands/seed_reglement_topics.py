"""
Crée les sujets « fiches de règlement » épinglés et verrouillés
dans chaque sous-catégorie de Règlement magique.
Usage : python manage.py seed_reglement_topics
        python manage.py seed_reglement_topics --reset
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.forum.models import Category, Post, Topic
from faction_role_powers import render_faction_roles

User = get_user_model()

# ── Helpers HTML réutilisables ─────────────────────────────────────────────

HEADER_STYLE = (
    "font-family: Georgia, 'Times New Roman', serif; "
    "background: #0d0a1a; color: #e2d9f3; "
    "padding: 2rem; border-radius: 10px; "
    "border: 1px solid rgba(124,58,237,0.3); "
    "max-width: 760px; margin: 0 auto;"
)

def box_purple(roman, title, body_html):
    return f"""
<div style="margin-bottom: 1.2rem; border: 1px solid rgba(124,58,237,0.28); border-radius: 7px; overflow: hidden;">
  <div style="background: linear-gradient(90deg, rgba(109,40,217,0.3), rgba(109,40,217,0.08)); padding: 0.45rem 1rem; border-bottom: 1px solid rgba(124,58,237,0.25);">
    <h2 style="margin: 0; font-size: 0.6rem; letter-spacing: 0.3em; text-transform: uppercase; color: #a78bfa; font-weight: normal;">◈ {roman}. {title}</h2>
  </div>
  <div style="padding: 0.85rem 1rem 0.75rem;">
    {body_html}
  </div>
</div>"""

def box_gold(roman, title, body_html):
    return f"""
<div style="margin-bottom: 1.2rem; border: 1px solid rgba(245,215,110,0.22); border-radius: 7px; overflow: hidden;">
  <div style="background: linear-gradient(90deg, rgba(245,215,110,0.12), rgba(245,215,110,0.03)); padding: 0.45rem 1rem; border-bottom: 1px solid rgba(245,215,110,0.2);">
    <h2 style="margin: 0; font-size: 0.6rem; letter-spacing: 0.3em; text-transform: uppercase; color: #f5d76e; font-weight: normal;">◈ {roman}. {title}</h2>
  </div>
  <div style="padding: 0.85rem 1rem 0.75rem;">
    {body_html}
  </div>
</div>"""

def box_red(roman, title, body_html):
    return f"""
<div style="margin-bottom: 1.2rem; border: 1px solid rgba(239,68,68,0.25); border-radius: 7px; overflow: hidden;">
  <div style="background: linear-gradient(90deg, rgba(239,68,68,0.18), rgba(239,68,68,0.04)); padding: 0.45rem 1rem; border-bottom: 1px solid rgba(239,68,68,0.2);">
    <h2 style="margin: 0; font-size: 0.6rem; letter-spacing: 0.3em; text-transform: uppercase; color: #f87171; font-weight: normal;">◈ {roman}. {title}</h2>
  </div>
  <div style="padding: 0.85rem 1rem 0.75rem;">
    {body_html}
  </div>
</div>"""

def rule_list(items):
    lis = "".join(
        f'<li style="margin-bottom:0.45rem;">{item}</li>'
        for item in items
    )
    return (
        f'<ul style="margin: 0; padding-left: 1.3rem; '
        f'line-height: 1.85; font-size: 0.87rem; color: #c4b5d4;">{lis}</ul>'
    )

def info_table(rows):
    trs = ""
    for i, (label, value) in enumerate(rows):
        border = "border-bottom: 1px solid rgba(124,58,237,0.08);" if i < len(rows) - 1 else ""
        trs += (
            f'<tr>'
            f'<td style="padding:0.28rem 1rem 0.28rem 0;font-size:0.74rem;color:#6d5fa0;width:42%;{border}">{label}</td>'
            f'<td style="padding:0.28rem 0;font-size:0.85rem;color:#e2d9f3;{border}">{value}</td>'
            f'</tr>'
        )
    return f'<table style="width:100%;border-collapse:collapse;">{trs}</table>'

def page_header(icon, title, subtitle):
    return f"""
<div style="margin-bottom: 1.75rem; padding-bottom: 1.5rem; border-bottom: 1px solid rgba(124,58,237,0.2); display: flex; align-items: center; gap: 1.25rem;">
  <div style="font-size: 3rem; line-height: 1; flex-shrink: 0;">{icon}</div>
  <div>
    <p style="margin: 0 0 0.3rem; font-size: 0.58rem; letter-spacing: 0.38em; text-transform: uppercase; color: #6d28d9;">✦ Nexus Arcana · Archives du Crossover ✦</p>
    <h1 style="margin: 0 0 0.35rem; font-size: 1.7rem; font-weight: normal; font-style: italic; color: #f5d76e; letter-spacing: 0.03em; line-height: 1.2;">{title}</h1>
    <p style="margin: 0; font-size: 0.8rem; color: #a78bfa; font-style: italic;">{subtitle}</p>
  </div>
</div>"""

def footer(text):
    return f'<p style="text-align:center;margin:1.25rem 0 0;font-size:0.58rem;color:#2d1f4a;font-style:italic;letter-spacing:0.18em;">✦ {text} ✦</p>'

def wrap(inner):
    return f'<div style="{HEADER_STYLE}">{inner}\n</div>'

def gif_banner(gif_url):
    """Bannière GIF/image pleine largeur en haut de la fiche (vide = ignorée)."""
    if not gif_url:
        return ''
    return (
        f'<div style="margin:-2rem -2rem 1.5rem -2rem;overflow:hidden;'
        f'border-radius:10px 10px 0 0;border-bottom:1px solid rgba(124,58,237,0.25);">'
        f'<img src="{gif_url}" alt="" style="width:100%;height:220px;object-fit:cover;display:block;" />'
        f'</div>'
    )


# ── URLs des GIFs de bannière — renseignez l'URL puis relancez --reset ────────
GIF_URLS = {
    "reglement-du-forum":             "",
    "creatures-et-races":             "",
    "factions":                       "",
    "bottin-des-avatars":             "",
    "bottin-des-formes-demoniaques":  "",
    "contextes-et-animations":        "",
}


# ══════════════════════════════════════════════════════════════════════════════
# CONTENU — 1. Règlement du forum
# ══════════════════════════════════════════════════════════════════════════════

_reglement_body = (
    gif_banner(GIF_URLS["reglement-du-forum"])
    + page_header("⚖️", "Règlement du Forum", "Les lois fondamentales de Nexus Arcana")
    + box_purple("I", "Principes généraux", rule_list([
        "<strong style='color:#e2d9f3;'>Respect absolu</strong> — Tout membre doit se comporter avec courtoisie envers les autres joueurs, que ce soit en jeu ou hors jeu. Les attaques personnelles, insultes et discriminations de toute nature sont interdites.",
        "<strong style='color:#e2d9f3;'>Distinction IC / OOC</strong> — Les conflits entre personnages (IC) ne doivent jamais déborder sur les relations entre joueurs (OOC). Un personnage ennemi peut avoir un joueur ami.",
        "<strong style='color:#e2d9f3;'>Confidentialité</strong> — Les informations privées partagées dans les espaces OOC (Discord, MP) ne doivent pas être utilisées ou divulguées sans accord.",
        "<strong style='color:#e2d9f3;'>Majorité</strong> — Le forum est ouvert à partir de 16 ans. Les contenus explicites sont interdits.",
        "<strong style='color:#e2d9f3;'>Bonne foi</strong> — En cas de doute, contactez le staff. La mauvaise foi répétée pourra conduire à une exclusion.",
    ]))
    + box_purple("II", "Création de personnage", rule_list([
        "Chaque joueur commence avec <strong style='color:#e2d9f3;'>un seul personnage actif</strong>. Un second compte peut être accordé après 2 mois d'activité sur demande.",
        "Toute fiche doit suivre le <strong style='color:#e2d9f3;'>modèle officiel</strong> disponible dans la catégorie dédiée.",
        "Les personnages doivent être <strong style='color:#e2d9f3;'>cohérents avec l'univers crossover</strong> : Charmed, The Vampire Diaries, The Originals, Legacies et Teen Wolf se rencontrent à Nexus Arcana. Pas de personnage omnipuissant.",
        "La fiche doit être <strong style='color:#e2d9f3;'>validée par le staff</strong> avant tout jeu en dehors des zones d'introduction.",
        "Un avatar (célébrité) doit être <strong style='color:#e2d9f3;'>réservé dans le bottin</strong> avant de soumettre la fiche.",
    ]))
    + box_purple("III", "Activité &amp; présence", rule_list([
        "<strong style='color:#e2d9f3;'>Absence</strong> — Toute absence prévue de plus de 15 jours doit être signalée dans la section dédiée. Sans nouvelles après 30 jours, le personnage peut être archivé.",
        "<strong style='color:#e2d9f3;'>Délai de réponse</strong> — En RP actif, un délai de 15 jours maximum est attendu. Passé ce délai, votre partenaire peut relancer ou clore la scène.",
        "<strong style='color:#e2d9f3;'>Qualité</strong> — Un minimum de 8 à 10 lignes par réponse est attendu. Le copier-coller est interdit.",
    ]))
    + box_red("IV", "Infractions &amp; sanctions", rule_list([
        "<strong style='color:#f87171;'>Avertissement</strong> — Premier manquement mineur aux règles.",
        "<strong style='color:#f87171;'>Suspension temporaire</strong> — Récidive ou infraction grave (harcèlement, plagiat, god-moding).",
        "<strong style='color:#f87171;'>Bannissement définitif</strong> — Infraction très grave ou absence d'amélioration après multiples avertissements.",
        "Le staff statue en collégialité. Toute décision peut faire l'objet d'un <strong style='color:#f87171;'>recours écrit</strong> adressé à la fondatrice.",
    ]))
    + footer("Règlement officiel de Nexus Arcana — Version 2026")
)

CONTENT_REGLEMENT = wrap(_reglement_body)


# ══════════════════════════════════════════════════════════════════════════════
# CONTENU — 2. Créatures et races
# ══════════════════════════════════════════════════════════════════════════════

_creatures_body = (
    gif_banner(GIF_URLS["creatures-et-races"])
    + page_header("🐉", "Créatures &amp; Races", "Encyclopédie crossover de Nexus Arcana")
    + box_purple("I", "Règles générales", rule_list([
        "Chaque race possède des <strong style='color:#e2d9f3;'>capacités définies</strong> dans sa fiche encyclopédique. Le joueur ne peut revendiquer que les pouvoirs propres à sa race, sauf accord du staff.",
        "Les <strong style='color:#e2d9f3;'>hybrides</strong> (mélange de deux races) sont possibles mais doivent être justifiés dans la fiche et validés par le staff.",
        "Aucune race n'est supérieure aux autres en termes de puissance globale. L'<strong style='color:#e2d9f3;'>équilibre narratif</strong> doit être respecté.",
        "Tout nouveau pouvoir ou capacité inhabituelle doit être <strong style='color:#e2d9f3;'>soumis à validation</strong> avant utilisation en RP.",
    ]))
    + box_purple("II", "Races magiques et de lumière", rule_list([
        "<strong style='color:#e2d9f3;'>Sorciers Charmed</strong> — Pouvoirs actifs uniques, sorts, potions et magie de lignée issus de l'univers Charmed.",
        "<strong style='color:#e2d9f3;'>Sorciers</strong> — Sorciers et sorcières de The Vampire Diaries, The Originals et Legacies : covens, canalisation, rituels et magie ancestrale.",
        "<strong style='color:#e2d9f3;'>Êtres de Lumière</strong> — Orbing, guérison, connexion aux Anciens. Protecteurs attitrés de sorcières. Ne peuvent tuer.",
        "<strong style='color:#e2d9f3;'>Fées</strong> — Magie de nature, invisibilité, liens aux sorcières. Taille normale possible.",
        "<strong style='color:#e2d9f3;'>Elfes</strong> — Magie primordiale, prescience, garde de l'équilibre. Discrets par nature.",
        "<strong style='color:#e2d9f3;'>Cupidons</strong> — Manipulation des liens affectifs, connexion émotionnelle. Ne combattent pas directement.",
        "<strong style='color:#e2d9f3;'>Valkyries</strong> — Guerrières liées aux âmes des combattants tombés, à la force et à l'endurance surhumaines.",
        "<strong style='color:#e2d9f3;'>Muses</strong> — Inspiratrices immortelles capables de transmettre ou retenir leur énergie créatrice.",
        "<strong style='color:#e2d9f3;'>Banshees</strong> — Sensibles aux présages de mort et aux passages entre les mondes. Leur cri peut protéger ou dévaster.",
    ]))
    + box_purple("III", "Créatures nocturnes et changeformes", rule_list([
        "<strong style='color:#e2d9f3;'>Démons</strong> — Boules de feu, fumée noire, téléportation démoniaque. Peuvent évoluer en niveau (inférieur → supérieur).",
        "<strong style='color:#e2d9f3;'>Vampires</strong> — Force et vitesse surnaturelles, manipulation mentale. Sensibles à la lumière du soleil et à l'ail concentré.",
        "<strong style='color:#e2d9f3;'>Loups-garous</strong> — Transformation au clair de lune, force brute, odorat. Sensibles à l'argent.",
        "<strong style='color:#e2d9f3;'>WereCoyotes, WereJaguars et WereLions</strong> — Changeformes aux instincts, capacités et territoires propres à leur lignée.",
        "<strong style='color:#e2d9f3;'>Kanimas</strong> — Créatures reptiliennes à la transformation altérée, dont le venin peut paralyser.",
        "<strong style='color:#e2d9f3;'>Kitsunes</strong> — Esprits-renards maniant, selon leur lignée, le feu, les illusions ou l'électricité.",
        "<strong style='color:#e2d9f3;'>Chiens de l'enfer</strong> — Traqueurs infernaux liés aux passages entre les mondes et aux âmes perdues.",
        "<strong style='color:#e2d9f3;'>Chimères</strong> — Êtres aux origines multiples portant les traits et les capacités de plusieurs créatures.",
        "<strong style='color:#e2d9f3;'>Phénix</strong> — Résurrection (limitée), maîtrise du feu, traque de démons. Indépendants, souvent mercenaires.",
    ]))
    + box_purple("IV", "Races neutres, ancestrales et hybrides", rule_list([
        "<strong style='color:#e2d9f3;'>Humains</strong> — Sans pouvoir intrinsèque, mais peuvent être médiums, chasseurs de démons entraînés ou alliés de sorcières. Leur force est leur adaptabilité.",
        "<strong style='color:#e2d9f3;'>Sirènes / Tritons Charmed</strong> — Magie aquatique, chant envoûtant, respiration sous l'eau et forme marine.",
        "<strong style='color:#e2d9f3;'>Sirènes</strong> — Créatures immortelles de The Vampire Diaries liées à l'appel psychique, à l'esprit et à l'au-delà.",
        "<strong style='color:#e2d9f3;'>Nymphes / Satyres</strong> — Esprits liés aux forêts, sources et forces vivantes de la nature.",
        "<strong style='color:#e2d9f3;'>Sphinx</strong> — Gardiens énigmatiques des savoirs interdits, associés aux énigmes et à la clairvoyance.",
        "<strong style='color:#e2d9f3;'>Hybrides</strong> — Héritage double, pouvoirs mélangés, souvent instables. Requièrent une justification narrative solide.",
        "<strong style='color:#e2d9f3;'>Trybrides</strong> — Réunissent les héritages de sorcière, vampire et loup-garou ; leur équilibre demande une validation renforcée.",
        "<strong style='color:#e2d9f3;'>Hérétiques</strong> — Vampires siphonneurs capables d'absorber et de canaliser l'énergie magique.",
    ]))
    + box_gold("V", "Soumission d'une nouvelle fiche de race", rule_list([
        "Contactez le staff via MP ou Discord pour proposer une nouvelle race non listée.",
        "Fournissez : nom, origine, pouvoirs principaux, faiblesses, camp de base, nombre de personnages max simultanés.",
        "La validation prend entre 3 et 7 jours ouvrés.",
    ]))
    + footer("Encyclopédie des races — Nexus Arcana 2026")
)

CONTENT_CREATURES = wrap(_creatures_body)


# ══════════════════════════════════════════════════════════════════════════════
# CONTENU — 3. Factions
# ══════════════════════════════════════════════════════════════════════════════

_factions_body = (
    gif_banner(GIF_URLS["factions"])
    + page_header("⚜️", "Factions &amp; Alliances", "Les forces organisées qui façonnent l'univers de Nexus Arcana")
    + box_purple("I", "Comment fonctionnent les factions", rule_list([
        "La faction est une <strong style='color:#e2d9f3;'>organisation ou alliance</strong>, distincte de la race, du camp et des pouvoirs du personnage. Une meute peut accueillir des humains ; un coven peut compter des alliés qui ne sont pas sorciers.",
        "La faction principale figure dans la fiche personnage et dans le champ Groupe du profil après validation. Un personnage peut entretenir d'autres alliances et des liens individuels sans devenir membre de plusieurs factions.",
        "Les sièges particuliers, comme ceux de la Triade ou des Cavaliers, sont limités. Pour les autres groupes, la disponibilité se vérifie avec le staff et les joueurs concernés ; les nombres affichés sur la page Groupes indiquent les membres présents.",
        "Une faction n'accorde pas de pouvoirs supplémentaires du seul fait de l'adhésion. Pour les Cavaliers de l'Apocalypse et les Gardiens des Sceaux Primordiaux, le siège choisi impose quatre facultés liées à ce rôle, qui occupent les quatre emplacements de base du personnage. Les quatre facultés de chaque Gardien et de chaque Cavalier sont définies ci-dessous. Un personnage n'emprunte pas les facultés d'un autre siège. Rejoindre ou quitter une faction se joue avec les personnes concernées.",
    ]))
    + box_purple("II", "Factions du Bien", rule_list([
        "<strong style='color:#e2d9f3;'>Le Pouvoir des Quatre</strong> — Les sœurs Halliwell et leur allié(e). Faction fermée : personnages scénarisés uniquement.",
        "<strong style='color:#e2d9f3;'>Les Fondateurs</strong> — Haut conseil des Êtres de Lumière. Accès restreint : ancienneté et validation staff requises.",
        "<strong style='color:#e2d9f3;'>Les Veilleurs de l'Aube</strong> — Protecteurs des innocents, actifs sur le terrain. Ouverts aux candidatures.",
        "<strong style='color:#e2d9f3;'>Les Gardiens des Sceaux Primordiaux</strong> — Ordre magique chargé de surveiller les forces apocalyptiques. Quatre sièges : Vie/Terre, Esprit/Eau, Temps/Vent et Volonté/Feu. Les candidatures et missions se définissent avec le staff.",
    ]))
    + box_purple("III", "Factions des Ténèbres", rule_list([
        "<strong style='color:#e2d9f3;'>La Triade</strong> — Cercle de trois démons de niveau supérieur ; les sièges et les éventuels pouvoirs liés à la fonction se définissent avec le staff.",
        "<strong style='color:#e2d9f3;'>Le Conclave de l'Abîme</strong> — Bras droits de la Source. Accès restreint : démons de niveau supérieur uniquement.",
        "<strong style='color:#e2d9f3;'>Les Cavaliers de l'Apocalypse</strong> — Quatre rôles distincts : Guerre, Mort, Famine et Pestilence. Accès exceptionnel soumis à validation ; aucun effet apocalyptique libre sur les autres joueurs.",
    ]))
    + box_purple("IV", "Pouvoirs de fonction : Gardiens des Sceaux", render_faction_roles("Les gardiens des sceaux primordiaux"))
    + box_purple("V", "Pouvoirs de fonction : Cavaliers de l'Apocalypse", render_faction_roles("Les cavaliers de l'apocalypse"))
    + box_gold("VI", "Application des facultés de rôle", "<p style='line-height:1.8;margin:.4rem 0;'>Chaque siège impose quatre facultés de départ, à inscrire dans la fiche du personnage. Les Gardiens et les Cavaliers disposent chacun de leurs quatre facultés définies. Ces facultés occupent les quatre emplacements de base et ne s’y ajoutent pas. Leur portée et leurs limites sont fixées avec le staff. Aucun pouvoir de Cavalier ne provoque automatiquement la mort ; le Sursis funèbre retarde brièvement une issue fatale sans guérir ni ressusciter. Les effets sur un autre personnage, notamment une altération mentale, un drain vital ou une suspension du temps, demandent une résolution commune avec les joueurs concernés. Un personnage ne cumule pas les facultés de plusieurs sièges.</p>")
    + box_purple("VII", "Alliances de Teen Wolf et de TVD", rule_list([
        "<strong style='color:#e2d9f3;'>La Meute de Beacon Hills</strong> — Autour de Scott et de ses alliés, loups, coyotes-garous, humains et autres proches protègent les leurs et le Nemeton. Le rang d'Alpha ne commande pas les personnages d'autrui.",
        "<strong style='color:#e2d9f3;'>Les Gardiens de Mystic Falls</strong> — Coalition d'enquête et de défense réunissant sorciers, vampires, loups et humains. Les rivalités anciennes ne sont pas effacées par une adhésion.",
        "Ces alliances peuvent nouer des pactes avec les groupes de Charmed et les covens ci-dessous. Les accords sont des intrigues ouvertes, sans fusion obligatoire ni camp commun imposé.",
    ]))
    + box_purple("VIII", "Covens et traditions magiques", rule_list([
        "<strong style='color:#e2d9f3;'>La Maison de la Seconde Soif</strong> — Coven d'Hérétiques, vampires siphonneurs. Leur nature leur permet de puiser dans une source magique, notamment leur propre vampirisme ; le coven organise leurs liens sans créer cette nature.",
        "<strong style='color:#e2d9f3;'>La Chambre des Murmures</strong> — Coven qui pratique l'Expression en priorité. L'étude de cette magie n'accorde pas d'emblée la maîtrise de tous ses effets ; les rituels et leurs conséquences se définissent dans les fiches.",
        "<strong style='color:#e2d9f3;'>Les Héritiers du Vide</strong> — Coven de siphonneurs non vampiriques, distinct des Hérétiques. Les sources utilisées et le consentement des personnes concernées sont précisés en jeu.",
        "<strong style='color:#e2d9f3;'>Les Veilleurs du Voile</strong> — Coven attaché aux rites ancestraux de La Nouvelle-Orléans. Écouter les ancêtres n'oblige pas ses membres à partager toutes leurs décisions.",
        "<strong style='color:#e2d9f3;'>Le Cercle des Terres Perdues</strong> — Coven de Voyageurs itinérants, tourné vers les rituels collectifs et les lieux affectés par la Convergence.",
        "Chaque coven est une faction principale distincte sur la page Groupes. Ses membres peuvent nouer des alliances avec les autres sans recevoir automatiquement leurs pratiques ou leurs pouvoirs.",
    ]))
    + box_gold("IX", "Rejoindre une faction", info_table([
        ("Étape 1", "Choisir un groupe compatible avec l'histoire du personnage et vérifier sa disponibilité."),
        ("Étape 2", "Présenter la faction principale et les liens envisagés dans la fiche personnage."),
        ("Étape 3", "Définir l'intégration avec les joueurs concernés ; une scène RP peut l'accompagner."),
        ("Étape 4", "Après validation du staff, renseigner le groupe sur le profil. Les autres alliances restent des liens à jouer."),
    ]))
    + footer("Guide des Factions — Nexus Arcana")
)

CONTENT_FACTIONS = wrap(_factions_body)


# ══════════════════════════════════════════════════════════════════════════════
# CONTENU — 4. Bottin des avatars
# ══════════════════════════════════════════════════════════════════════════════

_avatars_body = (
    gif_banner(GIF_URLS["bottin-des-avatars"])
    + page_header("📸", "Bottin des Avatars", "Registre des célébrités jouées et proposées pour les scénarios")
    + box_purple("I", "Consulter le bottin", rule_list([
        "Le bottin consultable dans la catégorie Bottin des avatars se met à jour à partir des noms de célébrités renseignés sur les profils et dans les fiches scénarios.",
        "Le statut Pris correspond à un personnage validé ; En attente indique une fiche non encore validée ; Scénario indique une célébrité proposée pour un personnage à prendre.",
        "Certains avatars de scénarios sont négociables : cette possibilité est indiquée sur leur fiche et dans le bottin.",
    ]))
    + box_purple("II", "Demander un avatar", rule_list([
        "Vérifiez le nom de la célébrité dans le bottin avant de compléter votre fiche ou votre demande de double compte.",
        "Indiquez la célébrité souhaitée dans votre fiche ou votre demande. Seule l’administration peut modifier le bottin et confirmer la disponibilité de l’avatar.",
        "Si un avatar de scénario est signalé comme négociable, échangez avec l’administration avant de retenir une autre célébrité.",
    ]))
    + footer("Bottin des Avatars — Nexus Arcana 2026")
)

CONTENT_AVATARS = wrap(_avatars_body)


# ══════════════════════════════════════════════════════════════════════════════
# CONTENU — 5. Bottin des formes démoniaques
# ══════════════════════════════════════════════════════════════════════════════

_formes_body = (
    gif_banner(GIF_URLS["bottin-des-formes-demoniaques"])
    + page_header("👹", "Bottin des Formes Démoniaques", "Répertoire officiel des apparences démoniaques")
    + box_purple("I", "Présentation", """
<p style="margin: 0; line-height: 1.9; color: #c4b5d4; font-size: 0.87rem;">
Dans l'esprit de Charmed, chaque <strong style="color:#e2d9f3;">personnage démon</strong> choisit et décrit une forme démoniaque dans sa fiche de présentation. Ce bottin recense ces apparences afin d'éviter les
doublons et de garantir la cohérence de l'univers. La forme doit aussi être déclarée ici avant
utilisation en RP. Les autres natures admises peuvent proposer une forme alternative si leur fiche le justifie.
</p>""")
    + box_purple("II", "Règles de réservation", rule_list([
        "Pour un personnage <strong style='color:#e2d9f3;'>Démon</strong>, le choix et la description d'une forme démoniaque font partie de la fiche. Cette apparence n'ajoute aucun pouvoir à ceux validés.",
        "Seuls les personnages de race <strong style='color:#e2d9f3;'>Démon, Hybride, Loup-garou, Vampire ou Phénix</strong> peuvent revendiquer une forme démoniaque.",
        "Une forme est liée à <strong style='color:#e2d9f3;'>un seul personnage</strong>. Elle ne peut pas être identique à celle d'un autre joueur.",
        "La description de la forme doit être <strong style='color:#e2d9f3;'>cohérente avec la race</strong> du personnage (ex : un démon de feu aura une forme ignée).",
        "Les formes empruntant directement l'apparence de <strong style='color:#e2d9f3;'>créatures canoniques</strong> des univers du crossover nécessitent une validation staff préalable.",
        "Une image de référence (facultative mais recommandée) peut être jointe à la réservation.",
    ]))
    + box_purple("III", "Format de réservation", """
<p style="margin: 0 0 0.6rem; font-size: 0.85rem; color: #c4b5d4;">Répondez à ce sujet avec le modèle suivant :</p>""" + info_table([
        ("Pseudonyme", "Votre pseudo sur le forum"),
        ("Personnage concerné", "Prénom Nom du personnage"),
        ("Race du personnage", "Démon / Hybride / Vampire / Loup-garou / Phénix"),
        ("Nom de la forme", "Nom donné à la forme démoniaque"),
        ("Description visuelle", "Apparence, couleurs, traits distinctifs (5 lignes min.)"),
        ("Image de référence", "URL (facultatif)"),
    ]))
    + box_red("IV", "Formes interdites", rule_list([
        "Toute forme imitant un <strong style='color:#f87171;'>personnage canonique</strong> de la série (La Source, Barbas, etc.) sans accord du staff.",
        "Toute forme jugée <strong style='color:#f87171;'>pornographique, gore ou irrespectueuse</strong>.",
        "Toute forme revendiquant une <strong style='color:#f87171;'>toute-puissance narrative</strong> (invincibilité absolue, contrôle total…).",
    ]))
    + footer("Bottin des Formes Démoniaques — Nexus Arcana 2026")
)

CONTENT_FORMES = wrap(_formes_body)


# ══════════════════════════════════════════════════════════════════════════════
# CONTENU — 6. Contextes et animations
# ══════════════════════════════════════════════════════════════════════════════

_contextes_body = (
    gif_banner(GIF_URLS["contextes-et-animations"])
    + page_header("🎭", "Contextes &amp; Animations", "Événements et fils narratifs actifs sur le Cercle")
    + box_purple("I", "Qu'est-ce qu'un contexte ?", """
<p style="margin: 0; line-height: 1.9; color: #c4b5d4; font-size: 0.87rem;">
Un <strong style="color:#e2d9f3;">contexte</strong> est un fil narratif ou un événement lancé par le staff qui
affecte l'ensemble du forum (ou une partie). Il peut s'agir d'une menace démoniaque, d'un tournant
politique dans l'Inframonde, d'une fête, d'une enquête collective, etc. Les contextes définissent
<em>le cadre actuel des villes du crossover</em> et enrichissent le jeu libre.
</p>""")
    + box_purple("II", "Participer à un contexte", rule_list([
        "Tout personnage <strong style='color:#e2d9f3;'>validé</strong> peut participer à un contexte ouvert, sauf mention contraire dans la description.",
        "Chaque contexte précise son <strong style='color:#e2d9f3;'>niveau de priorité</strong> (optionnel, recommandé, obligatoire pour certaines factions).",
        "Les actions RP dans un contexte peuvent avoir des <strong style='color:#e2d9f3;'>conséquences permanentes</strong> sur le personnage : blessures, alliances, révélations.",
        "En cas d'implication forte, prévenir le staff pour coordonner l'issue narrative.",
    ]))
    + box_purple("III", "Proposer une animation", rule_list([
        "Tout membre peut proposer une animation en contactant le staff par MP ou Discord.",
        "La proposition doit inclure : <strong style='color:#e2d9f3;'>titre, résumé, factions concernées, durée estimée, récompenses ou conséquences éventuelles</strong>.",
        "Le staff évalue la cohérence avec la continuité narrative avant validation.",
        "Les animations approuvées sont publiées dans cette section avec le tag <strong style='color:#e2d9f3;'>[ANIMATION]</strong>.",
    ]))
    + box_gold("IV", "Niveaux d'implication", info_table([
        ("🟢 Optionnel", "Le contexte enrichit le jeu mais aucune participation n'est requise."),
        ("🟡 Recommandé", "Le contexte est central à la période en cours. Participation encouragée."),
        ("🔴 Obligatoire", "Les factions concernées doivent réagir en RP sous 15 jours."),
        ("⚫ Clôturé", "Le contexte est terminé. Les posts restent accessibles mais le fil est verrouillé."),
    ]))
    + box_red("V", "Règles de conduite dans les animations", rule_list([
        "<strong style='color:#f87171;'>God-moding interdit</strong> — Il est interdit de décider des actions ou réactions d'un autre personnage sans accord OOC.",
        "<strong style='color:#f87171;'>Mort de personnage</strong> — La mort définitive d'un personnage dans un contexte requiert l'accord écrit du joueur concerné.",
        "Respecter le <strong style='color:#f87171;'>canon narratif</strong> établi par le staff pour l'événement.",
    ]))
    + footer("Guide des Contextes &amp; Animations — Nexus Arcana 2026")
)

CONTENT_CONTEXTES = wrap(_contextes_body)


# ══════════════════════════════════════════════════════════════════════════════
# Définition des sujets à créer
# ══════════════════════════════════════════════════════════════════════════════

TOPICS = [
    {
        "category_slug": "reglement-du-forum",
        "topic_slug": "reglement-officiel-du-forum",
        "title": "⚖️ Règlement officiel du forum",
        "content": CONTENT_REGLEMENT,
    },
    {
        "category_slug": "creatures-et-races",
        "topic_slug": "encyclopedie-des-creatures-et-races",
        "title": "🐉 Encyclopédie des Créatures & Races",
        "content": CONTENT_CREATURES,
    },
    {
        "category_slug": "factions",
        "topic_slug": "guide-des-factions-et-alliances",
        "title": "⚜️ Guide des Factions & Alliances",
        "content": CONTENT_FACTIONS,
    },
    {
        "category_slug": "bottin-des-avatars",
        "topic_slug": "reglement-et-reservations-avatars",
        "title": "📸 Règlement & Réservations — Avatars",
        "content": CONTENT_AVATARS,
    },
    {
        "category_slug": "bottin-des-formes-demoniaques",
        "topic_slug": "reglement-et-reservations-formes-demoniaques",
        "title": "👹 Règlement & Réservations — Formes Démoniaques",
        "content": CONTENT_FORMES,
    },
    {
        "category_slug": "contextes-et-animations",
        "topic_slug": "guide-des-contextes-et-animations",
        "title": "🎭 Guide des Contextes & Animations",
        "content": CONTENT_CONTEXTES,
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# Commande Django
# ══════════════════════════════════════════════════════════════════════════════

class Command(BaseCommand):
    help = "Crée les fiches de règlement épinglées et verrouillées dans chaque sous-catégorie du Règlement magique."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Supprime et recrée les sujets existants.",
        )
        parser.add_argument(
            "--update",
            action="store_true",
            help="Met à jour le contenu des fiches de règlement existantes.",
        )

    def handle(self, *args, **options):
        author = (
            User.objects.filter(role__in=["fondatrice", "admin"]).first()
            or User.objects.filter(is_superuser=True).first()
        )
        if not author:
            self.stdout.write(self.style.ERROR(
                "Aucun utilisateur admin/fondatrice trouvé. "
                "Lancez d'abord : python manage.py create_staff"
            ))
            return

        created_count = 0
        skipped_count = 0
        updated_count = 0

        for entry in TOPICS:
            try:
                category = Category.objects.get(slug=entry["category_slug"])
            except Category.DoesNotExist:
                self.stdout.write(self.style.WARNING(
                    f"  [SKIP] Catégorie introuvable : {entry['category_slug']}"
                ))
                skipped_count += 1
                continue

            if options["reset"]:
                deleted, _ = Topic.objects.filter(
                    category=category,
                    slug=entry["topic_slug"],
                ).delete()
                if deleted:
                    self.stdout.write(self.style.WARNING(
                        f"  [DEL]  Sujet supprimé : « {entry['title']} »"
                    ))

            topic, created = Topic.objects.get_or_create(
                category=category,
                slug=entry["topic_slug"],
                defaults={
                    "title": entry["title"],
                    "author": author,
                    "is_pinned": True,
                    "is_locked": True,
                },
            )

            if created:
                Post.objects.create(
                    topic=topic,
                    author=author,
                    content=entry["content"],
                )
                self.stdout.write(self.style.SUCCESS(
                    f"  [OK]   « {entry['title']} » → {entry['category_slug']}"
                ))
                created_count += 1
            elif options["update"]:
                topic.title = entry["title"]
                topic.save(update_fields=["title"])
                first_post = topic.posts.order_by("created_at").first()
                if first_post:
                    first_post.content = entry["content"]
                    first_post.save(update_fields=["content", "updated_at"])
                else:
                    Post.objects.create(
                        topic=topic,
                        author=author,
                        content=entry["content"],
                    )
                self.stdout.write(self.style.SUCCESS(
                    f"  [UPD]  « {entry['title']} »"
                ))
                updated_count += 1
            else:
                self.stdout.write(
                    f"  [—]   Déjà existant : « {entry['title']} »"
                )
                skipped_count += 1

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(
            f"[DONE] {created_count} sujet(s) créé(s), {updated_count} mis à jour, {skipped_count} ignoré(s)."
        ))
        self.stdout.write(f"[AUTH] Auteur : {author.username} ({author.role})")
