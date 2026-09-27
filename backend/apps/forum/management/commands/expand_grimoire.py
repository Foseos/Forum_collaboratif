import json
from html import escape

from django.core.management.base import BaseCommand, CommandError

from apps.forum.models import Topic
from apps.forum.power_kinesis import KINETIC_POWER_SECTIONS


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
  <p style="margin:0.5rem 0 0; color:#d8d1e5; line-height:1.7;">Les pouvoirs ci-dessous complètent le grimoire historique. Ce catalogue présente des possibilités, jamais des dons automatiquement acquis. Toute évolution majeure, combinaison inhabituelle ou capacité de niveau exceptionnel passe par le staff.</p>
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
    ("Empathie → lecture des émotions → apaisement", "Perçoit les émotions, puis peut aider à les apaiser. Aucun ressenti ne force le personnage visé à agir."),
    ("Prémonition → vision partagée → projection dans la vision", "Les visions sont fragmentaires, interprétables et ne garantissent pas l'avenir."),
    ("Télépathie → lien mental → relais de groupe", "Permet une communication mentale limitée. La cible peut résister et le consentement hors jeu reste nécessaire."),
    ("Suggestion → hypnose → altération brève d'un souvenir", "Toute perte durable de souvenir est soumise à l'accord du joueur concerné."),
    ("Clairsentience → rétrocognition → lecture d'un lieu", "Les informations reçues restent incomplètes et liées au support touché."),
    ("Rêves lucides → intrusion onirique → illusion partagée", "L'illusion peut troubler, jamais décider définitivement d'une action adverse."),
    ("Lecture d'aura → détection magique → dissimulation d'aura", "La dissimulation n'annule pas tous les moyens de détection."),
    ("Télépathie animale → communication → appel de meute", "Établit un contact limité avec un animal ; un appel de groupe demande portée et limites validées."),
]) + section("XIII", "Pouvoirs physiques, moléculaires et de soin", "rgba(96,165,250,0.30)", [
    ("Télékinésie → répulsion → onde télékinétique", "La masse, la distance et la concentration limitent l'effet."),
    ("Accélération moléculaire → combustion → pyrokinésie", "La maîtrise finale est réservée à une évolution validée."),
    ("Inhibition moléculaire → gel → cryokinésie", "Aucun gel total durable sur un personnage sans accord."),
    ("Guérison → soin profond → transfert vital", "La guérison ne ramène pas les morts."),
    ("Régénération → guérison accélérée → résistance accrue", "Les faiblesses définies dans la fiche restent effectives."),
    ("Intangibilité → invisibilité → métamorphie", "Une transformation conserve les limites physiques de la forme adoptée."),
    ("Force accrue → réflexes surnaturels → vitesse", "Ne garantit jamais une attaque ou une esquive réussie."),
]) + section("XIV", "Éléments, énergie et matière", "rgba(251,146,60,0.30)", [
    ("Boule de feu → jet de flammes → mur de feu", "La portée, la durée et la chaleur doivent être définies ; un mur de feu exige une évolution validée."),
    ("Étincelle → éclair → électrokinésie", "L'eau, les isolants et l'épuisement modifient l'efficacité."),
    ("Bulle d'eau → aquakinésie / hydrokinésie → tempête locale", "Les grandes manifestations exigent une source proche."),
    ("Brise → rafale → aérokinésie", "Une tempête complète requiert une validation du staff."),
    ("Pierre → géokinésie → fissure contrôlée", "Aucun séisme dévastateur sans accord du staff."),
    ("Lumière → flash aveuglant → photokinésie", "L'éblouissement est temporaire et ne décide pas seul de l'issue d'une scène."),
    ("Ombre → camouflage → umbrakinésie", "Le camouflage peut être percé par une perception ou une protection adaptée."),
    ("Graine → lianes → phytokinésie", "La végétation existante facilite toujours l'usage."),
]) + section("XV", "Déplacement, espace et rituels", "rgba(45,212,191,0.30)", [
    ("Projection astrale → projection tangible → ubiquité limitée", "Le corps reste vulnérable et une projection ne peut pas résoudre seule une intrigue."),
    ("Téléportation → apportation → déplacement de groupe", "La distance, les protections et la charge transportée limitent l'usage."),
    ("Orbing → localisation → télékinésie orbing", "Ces évolutions restent distinctes et doivent être validées séparément."),
    ("Clignement → clignement à distance → portail bref", "Impossible à travers un sceau ou une barrière adaptée."),
    ("Rituel de protection → cercle de scellement → bannissement", "Un rituel majeur demande composants, temps de jeu et participants."),
    ("Conjuration → création temporaire → invocation contrôlée", "Les êtres invoqués ne sont jamais sous contrôle absolu."),
    ("Perception temporelle → boucle brève → déplacement temporel", "Staff uniquement pour tout effet sur le temps ; aucune réécriture unilatérale de l'histoire."),
])

POWER_DIRECTORY += """
<div style="margin:1.4rem 0; border:1px solid rgba(167,139,250,0.34); border-radius:8px; overflow:hidden;">
  <div style="padding:0.55rem 1rem; background:linear-gradient(90deg, rgba(167,139,250,0.34), transparent);">
    <h2 style="margin:0; color:#f5d76e; font-size:0.68rem; letter-spacing:0.2em; text-transform:uppercase;">XVI. Capacités complémentaires</h2>
  </div>
  <div style="overflow-x:auto;"><table><thead><tr><th>Pouvoir</th><th>Description</th><th>Évolutions possibles</th></tr></thead><tbody>
    <tr><td>Empathie inversée</td><td>Perçoit une émotion dominante et peut proposer à une cible proche un ressenti opposé pendant un court moment. Ne force ni décision ni souvenir.</td><td>Diffusion empathique ★ · Ancrage émotionnel ★</td></tr>
    <tr><td>Réplique de pouvoir</td><td>Après avoir observé une capacité, en reproduit un seul effet affaibli, une seule fois dans une scène. La réplique ne donne ni maîtrise durable ni accès aux pouvoirs exceptionnels.</td><td>Réplique affinée ★ · Réplique prolongée ★</td></tr>
    <tr><td>Toucher paralysant</td><td>Un contact direct peut engourdir brièvement un membre de la cible. Une immobilisation complète n'est pas automatique.</td><td>Entrave étendue ★ · Maintien bref ★</td></tr>
    <tr><td>Hématokinésie</td><td>Déplace ou façonne une petite quantité de sang déjà versé. Le sang présent dans le corps d'une autre personne ne peut pas être contrôlé par ce pouvoir de base.</td><td>Hémostase ★ · Façonnage sanguin ★</td></tr>
    <tr><td>Aérokinésie</td><td>Dirige des courants d'air à proximité pour créer une brise ou une rafale limitée. N'accorde ni vol libre ni contrôle général de la météo.</td><td>Mur de vent ★ · Courants multiples ★</td></tr>
    <tr><td>Sens aiguisés</td><td>Perçoit plus finement les sons, les odeurs ou les mouvements proches. Les stimuli intenses peuvent aussi gêner le personnage.</td><td>Pistage sensoriel ★ · Perception sélective ★</td></tr>
    <tr><td>Régénération</td><td>Récupère plus vite de blessures ordinaires, sans annuler les faiblesses ni les limites définies dans la fiche.</td><td>Guérison accélérée ★ · Résistance accrue ★</td></tr>
    <tr><td>Force accrue</td><td>Déploie une force supérieure à la moyenne humaine, sans garantir la réussite d'une attaque ni supprimer la résistance d'une cible.</td><td>Réflexes surnaturels ★ · Vitesse accrue ★</td></tr>
    <tr><td>Suggestion mentale</td><td>Tente d'influencer brièvement une décision simple chez une cible réceptive. Ne force pas un joueur à agir ni n'efface ses souvenirs.</td><td>Hypnose ★ · Suggestion différée ★</td></tr>
    <tr><td>Perception des liens affectifs</td><td>Ressent l'existence d'un attachement émotionnel marqué entre deux personnes proches, sans en connaître la nature exacte ni accéder à leurs pensées.</td><td>Lecture affinée des liens ★ · Écho affectif ★</td></tr>
    <tr><td>Élan affectif</td><td>Favorise une émotion positive déjà présente entre deux personnes consentantes, sans créer de l'amour ni imposer une relation.</td><td>Apaisement partagé ★ · Harmonie passagère ★</td></tr>
    <tr><td>Phobokinésie</td><td>Éveille brièvement une peur liée au contexte chez une cible proche. La cible choisit sa réaction et peut résister à l'effet.</td><td>Écho des craintes ★ · Onde d'effroi ★</td></tr>
    <tr><td>Rayonnement de joie</td><td>Diffuse une sensation de joie passagère autour du personnage, sans effacer une peine profonde ni forcer l'enthousiasme.</td><td>Joie partagée ★ · Réconfort durable ★</td></tr>
    <tr><td>Vertige de folie</td><td>Trouble brièvement les perceptions d'une cible, comme si le décor devenait incohérent. Ne provoque ni maladie mentale ni perte durable de contrôle.</td><td>Illusions sensorielles ★ · Désorientation de groupe ★</td></tr>
    <tr><td>Chagrin partagé</td><td>Fait ressentir une tristesse passagère ou permet d'en porter une part avec une personne consentante. Aucun souvenir n'est modifié.</td><td>Écho mélancolique ★ · Partage du fardeau ★</td></tr>
    <tr><td>Élan de courage</td><td>Soutient temporairement la détermination d'une personne consentante face à une peur, sans supprimer le danger ni garantir sa réussite.</td><td>Courage collectif ★ · Résistance à l'effroi ★</td></tr>
    <tr><td>Malaise surnaturel</td><td>Provoque brièvement des symptômes fictifs comme une faiblesse, des frissons ou des vertiges. Ne transmet aucune maladie réelle, ne se propage pas et ne laisse aucune séquelle.</td><td>Symptômes ciblés ★ · Onde de malaise ★</td></tr>
    <tr><td>Réminiscence</td><td>Perçoit un fragment de souvenir lié à une personne consentante ou à un objet touché. Les images restent partielles et n'offrent pas un accès libre aux secrets d'autrui.</td><td>Partage de souvenir ★ · Reconstitution mémorielle ★</td></tr>
    <tr><td>Manipulation des sentiments</td><td>Influe sur l'intensité ou la nature d'un sentiment, et peut notamment faire naître l'amour. Pour un personnage joué, l'effet et sa durée sont convenus avec son joueur ; aucun lien amoureux ni aucune relation ne sont imposés.</td><td>Éveil amoureux ★ · Sentiment durable ★</td></tr>
    <tr><td>Illusion mentale</td><td>Fait percevoir à une cible une scène, une voix ou une sensation qui n'existe que dans son esprit. Le décor réel ne change pas et la cible garde ses décisions.</td><td>Illusion multisensorielle ★ · Projection mentale multiple ★</td></tr>
  </tbody></table></div>
</div>"""


def power_table(number, title, color, powers):
    rows = []
    for power in powers:
        name, description, evolutions = power[:3]
        explanations = power[3] if len(power) > 3 else ()
        if explanations and len(explanations) != len(evolutions):
            raise ValueError(f"Évolutions incomplètes pour {name}")
        notes_attribute = (
            f' data-evolution-explanations="{escape(json.dumps(explanations, ensure_ascii=False), quote=True)}"'
            if explanations else ""
        )
        rows.append(
            "<tr{}><td>{}</td><td>{}</td><td>{}</td></tr>".format(
                notes_attribute, escape(name), escape(description),
                " · ".join(escape(evolution) for evolution in evolutions),
            )
        )
    return f"""
<div style="margin:1.4rem 0; border:1px solid {color}; border-radius:8px; overflow:hidden;">
  <div style="padding:0.55rem 1rem; background:linear-gradient(90deg, {color}, transparent);">
    <h2 style="margin:0; color:#f5d76e; font-size:0.68rem; letter-spacing:0.2em; text-transform:uppercase;">{number}. {escape(title)}</h2>
  </div>
  <div style="overflow-x:auto;"><table data-power-paths="true"><thead><tr><th>Pouvoir</th><th>Description</th><th>Évolutions possibles</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
</div>"""


POWER_DIRECTORY += power_table("XVII", "Cris, voix et vibrations", "rgba(244,114,182,0.32)", [
    ("Cri de Furie", "Libère par la voix une onde liée à une émotion intense qui peut repousser ou déséquilibrer à courte portée. Ne blesse pas automatiquement une cible.", ("Onde furieuse ★", "Déflagration vocale ★")),
    ("Cri perçant", "Émet une fréquence aiguë capable de troubler brièvement l'ouïe et la concentration d'une cible proche. Ne rend pas sourd durablement.", ("Fréquence ciblée", "Cri de groupe ★")),
    ("Chant apaisant", "Apaise brièvement une tension chez les personnes qui entendent la voix et acceptent l'effet. Ne modifie ni souvenirs ni décisions.", ("Accord protecteur", "Chœur apaisant ★")),
    ("Voix mimétique", "Reproduit le timbre et la manière de parler d'une voix déjà entendue, sans acquérir les connaissances de son propriétaire.", ("Timbre parfait", "Écho différé")),
    ("Silence surnaturel", "Atténue les sons dans une petite zone pendant un court moment. Les vibrations et les autres moyens de communication restent possibles.", ("Bulle silencieuse", "Silence dirigé")),
    ("Écholocalisation", "Perçoit les contours proches grâce au retour d'un son émis. Le bruit, les protections et les matières absorbantes peuvent brouiller la lecture.", ("Cartographie sonore", "Filtrage des échos")),
])

POWER_DIRECTORY += power_table("XVIII", "Perception et conscience", "rgba(167,139,250,0.34)", [
    ("Partage sensoriel", "Transmet brièvement ce que le personnage voit ou entend à une personne consentante. Ne transmet ni pensées ni souvenirs.", ("Connexion prolongée", "Relais sensoriel ★")),
    ("Lecture des intentions", "Ressent une intention immédiate et marquée, comme attaquer ou protéger. N'offre pas la lecture des pensées ni la certitude sur les actes futurs.", ("Anticipation brève", "Veille collective ★")),
    ("Voile de présence", "Rend le personnage moins remarquable pour l'attention ordinaire sans le rendre invisible ni effacer ses traces.", ("Discrétion accrue", "Voile de groupe ★")),
    ("Sens des présages", "Ressent qu'un danger proche se prépare sans connaître sa cause exacte. Le signal peut être ambigu ou contrarié.", ("Alerte ciblée", "Pressentiment partagé ★")),
])

POWER_DIRECTORY += power_table("XIX", "Matière et forces", "rgba(96,165,250,0.30)", [
    ("Cristallokinésie", "Déplace ou façonne une petite quantité de cristal déjà présente. Ne crée pas de gemmes et ne traverse pas automatiquement les protections.", ("Barrière cristalline", "Résonance des gemmes")),
    ("Magnétokinésie", "Attire ou repousse de petits objets ferromagnétiques proches. Tous les métaux ne réagissent pas et une arme tenue peut être résistée.", ("Attraction multiple", "Bouclier magnétique ★")),
    ("Gravikinésie", "Allège ou alourdit légèrement un objet ou son propre corps pendant un court instant. Ne permet ni vol libre ni écrasement d'une personne.", ("Zone allégée ★", "Ancrage gravitationnel ★")),
    ("Brumokinésie", "Déplace et modèle une brume ou une vapeur déjà présente. L'effet dépend de la source et n'asphyxie pas automatiquement.", ("Voile de brume", "Brume dense ★")),
])

POWER_DIRECTORY += power_table("XX", "Corps et adaptation", "rgba(45,212,191,0.30)", [
    ("Métabolisme accéléré", "Accorde un bref surcroît d'énergie physique au prix d'une fatigue ensuite. Ne remplace ni la guérison ni la vitesse surnaturelle.", ("Récupération brève", "Élan prolongé")),
    ("Camouflage organique", "Modifie les couleurs ou motifs du corps pour mieux se fondre dans un environnement. Le mouvement et les autres sens peuvent révéler le personnage.", ("Mimétisme complet", "Camouflage en mouvement")),
    ("Adaptation respiratoire", "Permet de supporter brièvement un air difficile ou de retenir son souffle plus longtemps. Ne protège pas de toutes les substances dangereuses.", ("Respiration prolongée", "Filtration de l'air ★")),
    ("Algokinésie", "Module temporairement une sensation douloureuse chez soi ou une personne consentante. La blessure reste présente et peut s'aggraver si elle est ignorée.", ("Apaisement ciblé", "Apaisement partagé ★")),
])

POWER_DIRECTORY += power_table("XXI", "Facultés mentales et pouvoirs insolites", "rgba(196,181,253,0.34)", [
    ("Torture mentale", "Inflige à une cible une sensation de souffrance psychique temporaire, sans blessure physique ni séquelle imposée. Les réactions, révélations et limites de la scène sont convenues avec son joueur.", ("Étau psychique ★", "Pression partagée ★")),
    ("Omnilinguisme", "Permet de comprendre et de parler les langues ordinaires entendues, sans donner accès aux pensées, aux codes secrets ou aux savoirs de leurs locuteurs.", ("Écritures anciennes", "Langues occultes ★")),
    ("Intuition des mensonges", "Perçoit une discordance lorsqu'une personne ment délibérément, sans connaître la vérité ni détecter une erreur sincère.", ("Dissonance des récits", "Lecture des omissions ★")),
    ("Tychokinésie", "Infléchit légèrement la chance d'un événement banal et incertain. Ne garantit aucun résultat et ne décide pas seule de l'issue d'une scène.", ("Chance favorable ★", "Malchance localisée ★")),
    ("Transmutation mineure", "Modifie temporairement la matière d'un petit objet inerte. Ne touche ni les êtres vivants ni les objets protégés sans accord.", ("Matière durable ★", "Transformation multiple ★")),
    ("Animation d'objets", "Anime brièvement un petit objet inerte pour une action simple. L'objet n'acquiert ni pensée ni pouvoir propre.", ("Mouvement coordonné", "Assistant animé ★")),
    ("Sommeil induit", "Favorise une somnolence progressive chez une cible réceptive. Ne provoque pas d'inconscience instantanée et la cible peut résister.", ("Sommeil profond ★", "Rêve dirigé ★")),
    ("Dissipation de magie", "Affaiblit ou dénoue un effet magique temporaire de portée limitée après concentration. N'efface pas les pouvoirs d'une personne.", ("Dissipation ciblée ★", "Cercle de dissipation ★")),
])

POWER_DIRECTORY += power_table("XXII", "Eaux, lumière et enchantements", "rgba(103,232,249,0.34)", [
    ("Bouclier aquatique", "Dresse une barrière d'eau issue d'une source proche pour amortir une attaque. La protection a une résistance et une durée limitées.", ("Dôme aqueux ★", "Bouclier mobile ★")),
    ("Fouet d'eau", "Projette un jet d'eau souple pour repousser ou tenter de saisir un objet proche. N'immobilise pas automatiquement une personne.", ("Double fouet", "Entrave aqueuse ★")),
    ("Respiration aquatique", "Permet de respirer sous l'eau pendant quelques tours de RP, sans protéger du froid, de la pression ou des courants.", ("Souffle prolongé", "Partage du souffle ★")),
    ("Chant envoûtant", "Éveille une fascination passagère chez les personnes qui entendent la mélodie. Une cible garde ses choix et peut rompre l'écoute.", ("Mélodie collective ★", "Écho persistant ★")),
    ("Voix des eaux", "Transmet quelques mots au travers d'une étendue d'eau reliée au personnage. N'entend pas toutes les conversations proches de l'eau.", ("Écoute des courants", "Message des marées ★")),
    ("Glamour scintillant", "Modifie l'apparence perçue du personnage par un éclat magique discret. Son corps réel ne change pas et le leurre peut être décelé.", ("Glamour prolongé", "Glamour partagé ★")),
    ("Poussière lumineuse", "Fait apparaître des particules de lumière capables d'éclairer ou de révéler brièvement une trace. Elles ne blessent pas et ne neutralisent pas une cible.", ("Traînée révélatrice", "Nuée scintillante")),
    ("Ailes d'énergie", "Forme des ailes magiques pour planer sur une courte distance. Le vol soutenu et le transport d'autrui sont des évolutions distinctes.", ("Vol soutenu ★", "Portage léger ★")),
    ("Bénédiction fugace", "Accorde à une personne consentante un soutien modeste et temporaire face à une épreuve précise, sans garantir sa réussite ni lui transmettre un pouvoir.", ("Bénédiction ciblée", "Bénédiction partagée ★")),
    ("Rosée réparatrice", "Rassemble de l'humidité pour apaiser une blessure superficielle ou une irritation. Ne remplace pas la guérison des atteintes graves.", ("Soin apaisant", "Rosée collective ★")),
])

POWER_DIRECTORY += power_table("XXIII", "Nuages, poussières et lumière", "rgba(186,230,253,0.34)", [
    ("Néphokinésie", "Déplace ou modèle des nuages déjà présents à proximité, ou condense une petite vapeur disponible. Ne contrôle pas librement le climat.", ("Courants nuageux", "Couverture céleste ★")),
    ("Nuage protecteur", "Maintient un nuage dense entre une attaque et ses cibles pour gêner la visée ou amortir un impact léger. Ne remplace pas un bouclier invulnérable.", ("Écran suspendu", "Dôme de nuages ★")),
    ("Marche des nuages", "Condense brièvement un appui sous les pieds pour franchir un vide limité. L'appui se dissipe rapidement et n'accorde pas le vol libre.", ("Pas successifs ★", "Plateforme partagée ★")),
    ("Poussière de fée", "Crée une fine poussière enchantée qui allège momentanément un petit objet ou une personne consentante. Ne donne ni vol permanent ni pouvoirs supplémentaires.", ("Lévitation légère ★", "Nuée féerique ★")),
    ("Télékinésie lumineuse", "Emploie des filaments de lumière condensée pour attirer ou déplacer un petit objet visible. Une source lumineuse et la concentration sont nécessaires.", ("Prise photique", "Manipulation multiple ★")),
    ("Prisme de lumière", "Réfracte une lumière présente pour produire des reflets trompeurs ou dévier un éclat. Ne crée ni matière ni illusion mentale.", ("Déviation lumineuse", "Miroirs prismatiques ★")),
])

for section_number, section_title, section_color, powers in KINETIC_POWER_SECTIONS:
    POWER_DIRECTORY += power_table(section_number, section_title, section_color, powers)

POWER_DIRECTORY += power_table("XXXI", "Instinct, traque et ralliement", "rgba(251,191,36,0.32)", [
    (
        "Hurlement de ralliement",
        "Transmet une alerte ou une direction simple aux alliés qui entendent le cri. Ne commande pas leurs actes et ne traverse pas toute distance.",
        ("Appel lointain", "Ralliement coordonné ★"),
        (
            "Porte l'alerte un peu plus loin dans un environnement où le son circule.",
            "Permet à plusieurs alliés volontaires de reconnaître un même signal convenu.",
        ),
    ),
    (
        "Piste brouillée",
        "Atténue temporairement sa propre trace olfactive ou ses empreintes récentes. Ne supprime pas toutes les preuves de son passage.",
        ("Fausse piste", "Effacement de groupe ★"),
        (
            "Oriente un poursuivant vers une trace trompeuse, sans garantir qu'il la suivra.",
            "Aide quelques alliés proches à brouiller leurs traces pendant une courte traversée.",
        ),
    ),
    (
        "Bond silencieux",
        "Effectue un saut court en réduisant le bruit de l'atterrissage. Ne permet ni vol ni franchissement illimité.",
        ("Atterrissage feutré", "Bond enchaîné ★"),
        (
            "Amortit davantage le bruit et l'impact d'une réception sur un sol compatible.",
            "Enchaîne deux sauts courts au prix d'un effort accru et avec des appuis disponibles.",
        ),
    ),
    (
        "Rugissement de garde",
        "Soutient brièvement la détermination d'alliés proches qui entendent le rugissement. Ne crée pas de bouclier physique ni d'obéissance.",
        ("Courage partagé", "Cri dissuasif ★"),
        (
            "Étend le soutien moral à plusieurs alliés réceptifs pendant une action précise.",
            "Intimide momentanément une cible réceptive, qui conserve sa réaction et peut résister.",
        ),
    ),
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
