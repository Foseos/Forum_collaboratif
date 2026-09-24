from django.core.management.base import BaseCommand, CommandError

from apps.forum.models import Topic


MARKER = "<!-- NEXUS-ARCANA-CROSSOVER-GRIMOIRE -->"
DIRECTORY_MARKER = "<!-- NEXUS-ARCANA-POWER-DIRECTORY -->"


def section(number, title, color, items):
    lines = "".join(
        f"<li style='margin:0 0 0.55rem;'><strong style='color:#e2d9f3;'>{name}</strong> — {text}</li>"
        for name, text in items
    )
    return f"""
<div style="margin:1.4rem 0; border:1px solid {color}; border-radius:8px; overflow:hidden;">
  <div style="padding:0.55rem 1rem; background:linear-gradient(90deg, {color}, transparent);">
    <h2 style="margin:0; color:#f5d76e; font-size:0.68rem; letter-spacing:0.2em; text-transform:uppercase;">{number}. {title}</h2>
  </div>
  <ul style="margin:0; padding:0.95rem 1.2rem 0.7rem 2.2rem; color:#c4b5d4; font-size:0.87rem; line-height:1.65;">{lines}</ul>
</div>"""


CROSSOVER_GRIMOIRE = MARKER + """
<div style="margin:1.75rem 0 1rem; padding:1rem; border:1px solid rgba(245,215,110,0.35); border-radius:8px; background:rgba(245,215,110,0.05);">
  <p style="margin:0; color:#f5d76e; font-size:0.68rem; letter-spacing:0.18em; text-transform:uppercase;">✦ Addendum crossover · Nexus Arcana ✦</p>
  <p style="margin:0.5rem 0 0; color:#d8d1e5; line-height:1.7;">Les pouvoirs ci-dessous complètent le grimoire historique. Un personnage possède les dons liés à sa race et à son histoire, jamais l'intégralité des capacités de sa lignée. Toute évolution majeure, combinaison inhabituelle ou capacité de niveau exceptionnel passe par le staff.</p>
</div>
""" + section("VIII", "Magies et disciplines du crossover", "rgba(139,92,246,0.30)", [
    ("Sorcellerie Charmed", "sorts, potions, télékinésie et pouvoirs actifs personnels. Les sortilèges collectifs demandent préparation et accord des participants."),
    ("Sorcellerie TVD / The Originals", "canalisation, rituels, protections, liens d'objets et magie ancestrale. Un rituel puissant implique un prix, une source ou un contrecoup."),
    ("Siphonnage", "absorption temporaire de magie contenue dans un sort, un objet ou une créature consentante. Il ne permet pas de voler définitivement les dons d'autrui."),
    ("Magie des esprits", "contacts, visions et rituels liés à l'au-delà. Les esprits ne sont ni omniscients ni obligés de répondre."),
    ("Druidisme et rituels de meute", "lecture des présages, protection des territoires, ancrage au Nemeton et rites communautaires."),
]) + section("IX", "Vampires, loups et héritages hybrides", "rgba(185,28,28,0.30)", [
    ("Vampires", "force, vitesse, guérison et compulsions selon l'âge et la lignée. Le soleil, la verveine, le feu et la décapitation restent des menaces sérieuses."),
    ("Loups-garous", "sens décuplés, guérison et transformation. Les contraintes de la pleine lune, de la meute et du contrôle émotionnel doivent être jouées."),
    ("WereCoyote / WereJaguar / WereLion", "capacités de changeforme propres à leur espèce : adaptabilité du coyote, agilité du jaguar, puissance et présence du lion. Une forme animale n'est jamais invulnérable."),
    ("Hybrides et Trybrides", "cumulent des héritages mais aussi leurs faiblesses. Les Trybrides sont exceptionnelles et nécessitent l'accord préalable du staff."),
    ("Hérétiques", "vampires siphonneurs : ils canalisent une magie absorbée, mais leur soif et l'épuisement limitent leur puissance."),
]) + section("X", "Créatures singulières", "rgba(20,184,166,0.28)", [
    ("Banshees", "présages, perception des morts et cri surnaturel. Les visions sont fragmentaires et ne donnent jamais une solution certaine."),
    ("Kanimas", "venin paralysant, sens aiguisés et transformation reptilienne. Le venin immobilise temporairement ; il ne décide pas de l'issue d'une scène."),
    ("Kitsunes", "feu, foudre, illusions ou ruse selon la lignée. Les illusions peuvent tromper, pas imposer une croyance durable à un autre joueur."),
    ("Chiens de l'enfer", "pistage surnaturel, chaleur infernale et passages limités entre les mondes. Chaque passage exige une raison narrative et une issue."),
    ("Chimères", "combinaison contrôlée de traits surnaturels. Deux axes de capacités cohérents maximum, avec contreparties validées."),
    ("Sphinx", "clairvoyance, énigmes et mémoire des savoirs cachés. Les prophéties indiquent des possibilités, jamais une vérité immuable."),
]) + section("XI", "Règles d'évolution et limites", "rgba(245,215,110,0.25)", [
    ("Progression", "quatre capacités maximum à la création pour tous, capacités actives et passives comprises. Tout ajout de pouvoir et toute évolution, y compris ceux de ce registre, s’achètent en Arcana Flouz avec approbation du staff avant utilisation. Aucun RP justificatif n’est demandé. Deux améliorations maximum par capacité acquise."),
    ("Contrecoup", "chaque grand usage implique fatigue, douleur, perte de contrôle, besoin d'une source ou conséquence narrative équivalente."),
    ("Consentement RP", "contrôle mental, possession, paralysie prolongée, blessure grave ou mort demandent l'accord OOC de la personne concernée."),
    ("Interdits", "pas d'omnipotence, d'immortalité sans faille, de voyage temporel libre, de résurrection sans conséquence ou de pouvoir qui annule le jeu d'autrui."),
])


POWER_DIRECTORY = DIRECTORY_MARKER + """
<div style="margin:2rem 0 1rem; text-align:center;">
  <p style="margin:0; color:#f5d76e; font-size:0.68rem; letter-spacing:0.22em; text-transform:uppercase;">✦ Répertoire détaillé des pouvoirs ✦</p>
  <p style="margin:0.5rem auto 0; max-width:680px; color:#c4b5d4; line-height:1.7; font-size:0.87rem;">Chaque ligne suit le modèle <strong style="color:#e2d9f3;">pouvoir de base → évolution → maîtrise</strong>. Les branches sont des pistes : un personnage n'a pas à toutes les posséder. Les mentions « staff » demandent une validation avant la fiche ou une évolution jouée.</p>
</div>
""" + section("XII", "Pouvoirs psychiques, médiumniques et émotionnels", "rgba(167,139,250,0.34)", [
    ("Empathie → lecture des émotions → apaisement", "Sorciers Charmed, Sorciers, Cupidons, Muses et créatures sensibles. Aucun ressenti ne force le personnage visé à agir."),
    ("Prémonition → vision partagée → projection dans la vision", "Sorciers, Banshees et Sphinx. Les visions sont fragmentaires, interprétables et ne garantissent pas l'avenir."),
    ("Télépathie → lien mental → relais de groupe", "Sorciers et démons psychiques. La cible peut résister et le consentement OOC reste nécessaire."),
    ("Suggestion → hypnose → altération brève d'un souvenir", "Démons, vampires et sorciers spécialisés. Toute perte durable de souvenir est soumise à l'accord du joueur."),
    ("Clairsentience → rétrocognition → lecture d'un lieu", "Sorciers, médiums et Sphinx. Les informations reçues restent incomplètes et liées au support touché."),
    ("Rêves lucides → intrusion onirique → illusion partagée", "Sorciers, démons et Kitsunes. L'illusion peut troubler, jamais décider définitivement d'une action adverse."),
    ("Lecture d'aura → détection magique → dissimulation d'aura", "Sorciers, Êtres de Lumière et démons. La dissimulation n'annule pas tous les moyens de détection."),
    ("Télépathie animale → communication → appel de meute", "Sorciers liés au vivant, changeformes et Kitsunes."),
]) + section("XIII", "Pouvoirs physiques, moléculaires et de soin", "rgba(96,165,250,0.30)", [
    ("Télékinésie → répulsion → onde télékinétique", "Sorciers et démons. La masse, la distance et la concentration limitent l'effet."),
    ("Accélération moléculaire → combustion → pyrokinésie", "Sorciers et démons liés au feu. La maîtrise finale est réservée à une évolution validée."),
    ("Inhibition moléculaire → gel → cryokinésie", "Sorciers et démons liés au froid. Aucun gel total durable sur un personnage sans accord."),
    ("Guérison → soin profond → transfert vital", "Êtres de Lumière, sorciers et créatures guérisseuses. La guérison ne ramène pas les morts."),
    ("Régénération → guérison accélérée → résistance accrue", "Vampires, loups, Phénix et certains démons. Feu, décapitation ou faiblesse de l'espèce restent effectifs."),
    ("Intangibilité → invisibilité → métamorphie", "Démons, sorciers et créatures féeriques. Une transformation conserve les limites physiques de la forme adoptée."),
    ("Force accrue → réflexes surnaturels → vitesse", "Vampires, loups, changeformes et démons. Ne garantit jamais une attaque ou une esquive réussie."),
]) + section("XIV", "Éléments, énergie et matière", "rgba(251,146,60,0.30)", [
    ("Boule de feu → jet de flammes → mur de feu", "Démons, sorciers du feu, Phénix et Chiens de l'enfer."),
    ("Étincelle → éclair → électrokinésie", "Sorciers et Kitsunes électriques. L'eau, les isolants et l'épuisement modifient l'efficacité."),
    ("Bulle d'eau → hydrokinésie → tempête locale", "Sirènes/Tritons Charmed et sorciers de l'eau. Les grandes manifestations exigent une source proche."),
    ("Brise → rafale → aérokinésie", "Sorciers, Banshees et êtres ailés. Une tempête complète requiert une validation staff."),
    ("Pierre → géokinésie → fissure contrôlée", "Sorciers terrestres et Chimères adaptées. Aucun séisme dévastateur sans accord staff."),
    ("Lumière → flash aveuglant → photokinésie", "Sorciers, Êtres de Lumière et créatures célestes."),
    ("Ombre → camouflage → umbrakinésie", "Démons, Êtres des Ténèbres et certaines lignées de Kitsunes."),
    ("Graine → lianes → phytokinésie", "Sorciers, Fées, Nymphes et Satyres. La végétation existante facilite toujours l'usage."),
]) + section("XV", "Déplacement, espace et rituels", "rgba(45,212,191,0.30)", [
    ("Projection astrale → projection tangible → ubiquité limitée", "Sorciers. Le corps reste vulnérable et une projection ne peut pas résoudre seule une intrigue."),
    ("Téléportation → apportation → déplacement de groupe", "Sorciers et démons. La distance, les protections et la charge transportée limitent l'usage."),
    ("Orbing → localisation → télékinésie orbing", "Êtres de Lumière. Lié à leurs règles de protection et à leur connexion magique."),
    ("Clignement → clignement à distance → portail bref", "Démons et certaines lignées surnaturelles. Impossible à travers un sceau ou une barrière adaptée."),
    ("Rituel de protection → cercle de scellement → bannissement", "Sorciers et covens. Un rituel majeur demande composants, temps de jeu et participants."),
    ("Conjuration → création temporaire → invocation contrôlée", "Démons et sorciers. Les êtres invoqués ne sont jamais sous contrôle absolu."),
    ("Perception temporelle → boucle brève → déplacement temporel", "Staff uniquement pour tout effet sur le temps ; aucune réécriture unilatérale de l'histoire."),
]) + section("XVI", "Affinités et limites selon les races", "rgba(244,114,182,0.28)", [
    ("Sorciers Charmed", "quatre pouvoirs de base à la création, choisis dans les familles cohérentes avec leur lignée ; chacun peut évoluer deux fois après achat et validation. Les sorts et potions complètent leur magie."),
    ("Sorciers", "magie de coven, canalisation, magie ancestrale et rituels issus de The Vampire Diaries, The Originals et Legacies."),
    ("Démons", "langues démoniaques, résistance propre à leur rang et une manifestation personnelle. Les pouvoirs destructeurs majeurs évoluent uniquement en jeu."),
    ("Vampires", "force, vitesse, sens, guérison et compulsions selon leur lignée. Soleil, verveine et faim restent des contraintes narratives."),
    ("Sirènes/Tritons Charmed et Sirènes", "forme aquatique, chant et pouvoirs liés à l'eau pour les premiers ; appel psychique et connexion à l'au-delà pour les Sirènes TVD."),
    ("Loups et changeformes", "sens, guérison et forme animale. Chaque lignée — WereCoyote, WereJaguar, WereLion — garde son identité et ses faiblesses."),
    ("Banshees / Kanimas / Kitsunes", "présages et cri ; paralysie venimeuse ; feu, foudre ou illusions selon la lignée. Leurs effets majeurs restent temporaires et joués à deux."),
    ("Chimères / Chiens de l'enfer / Sphinx", "traits combinés validés ; pistage infernal et chaleur ; énigmes et clairvoyance. Aucun ne donne d'information ou de victoire automatique."),
    ("Trybrides et Hérétiques", "quatre capacités maximum à la création, réparties entre tous leurs héritages ; aucun don actif ou passif gratuit en supplément. Les capacités manquantes se débloquent en jeu par achat en Arcana Flouz et validation du staff."),
])


class Command(BaseCommand):
    help = "Complète le Grimoire des pouvoirs avec les capacités du crossover Nexus Arcana."

    def add_arguments(self, parser):
        parser.add_argument(
            "--refresh-directory",
            action="store_true",
            help="Actualise le répertoire détaillé sans toucher au reste du Grimoire.",
        )

    def handle(self, *args, **options):
        try:
            topic = Topic.objects.get(slug="liste-des-pouvoirs-magiques")
        except Topic.DoesNotExist as exc:
            raise CommandError("Le sujet du Grimoire des pouvoirs est introuvable.") from exc

        post = topic.posts.order_by("created_at").first()
        if not post:
            raise CommandError("Le Grimoire ne possède aucun contenu à mettre à jour.")

        content = post.content.replace("Charmed Arcana", "Nexus Arcana")
        if MARKER not in content:
            before_footer, closing_tag, after_footer = content.rpartition("</div>")
            content = before_footer + CROSSOVER_GRIMOIRE + closing_tag + after_footer
        if options["refresh_directory"] and DIRECTORY_MARKER in content:
            before_directory, _, _ = content.partition(DIRECTORY_MARKER)
            content = before_directory + POWER_DIRECTORY + "</div>"
        elif DIRECTORY_MARKER not in content:
            before_footer, closing_tag, after_footer = content.rpartition("</div>")
            content = before_footer + POWER_DIRECTORY + closing_tag + after_footer

        post.content = content
        post.save(update_fields=["content", "updated_at"])
        self.stdout.write(self.style.SUCCESS("Grimoire des pouvoirs complété et renommé pour Nexus Arcana."))
