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
  <p style="margin:0.5rem auto 0; max-width:680px; color:#c4b5d4; line-height:1.7; font-size:0.87rem;">Chaque kinésie peut produire une manifestation limitée de son élément ou de son effet sans source déjà présente. Une source existante peut faciliter un usage plus vaste ; elle n'est pas obligatoire pour le pouvoir de base. Pour les kinésies du corps ou de l'esprit, cela ne crée ni personne, ni organe complet, ni passé réel.</p>
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
    ("Intangibilité → ancrage tangible → phase sélective", "Le retour à l'état solide et le passage partiel à travers la matière sont deux maîtrises de l'intangibilité ; ils ne donnent ni invisibilité ni métamorphie."),
    ("Force accrue → réflexes surnaturels → vitesse", "Ne garantit jamais une attaque ou une esquive réussie."),
]) + section("XIV", "Éléments, énergie et matière", "rgba(251,146,60,0.30)", [
    ("Boule de feu → jet de flammes → mur de feu", "La portée, la durée et la chaleur doivent être définies ; un mur de feu exige une évolution validée."),
    ("Étincelle → éclair → électrokinésie", "L'eau, les isolants et l'épuisement modifient l'efficacité."),
    ("Bulle d'eau → aquakinésie / hydrokinésie → tempête locale", "Le pouvoir crée de l'eau dès sa base ; les grandes manifestations exigent une évolution et une ampleur validées."),
    ("Brise → rafale → aérokinésie", "Une tempête complète requiert une validation du staff."),
    ("Pierre → géokinésie → fissure contrôlée", "Aucun séisme dévastateur sans accord du staff."),
    ("Lumière → flash aveuglant → photokinésie", "L'éblouissement est temporaire et ne décide pas seul de l'issue d'une scène."),
    ("Ombre → camouflage → umbrakinésie", "Le camouflage peut être percé par une perception ou une protection adaptée."),
    ("Graine → lianes → phytokinésie", "Le pouvoir peut créer une petite pousse ; la végétation existante facilite les manifestations plus vastes."),
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
    <tr><td>Hématokinésie</td><td>Crée une petite quantité de sang ou façonne celui qui a été versé. Une évolution validée peut aussi échauffer temporairement le sang d'une autre personne, avec l'accord du joueur concerné, sans lésion durable ni issue imposée.</td><td>Hémostase ★ · Façonnage sanguin ★ · Ébullition sanguine ★</td></tr>
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
    (
        "Leurre acoustique",
        "Projette un son trompeur dans un point proche, comme une voix ou des pas. Le son ne crée aucune image et peut être démasqué.",
        ("Écho différé ★", "Scène sonore ★"),
        (
            "Rejoue brièvement le même son après un court délai défini.",
            "Compose plusieurs sons cohérents dans une petite zone, sans imposer ce que les auditeurs croient ou font.",
        ),
    ),
    ("Cri perçant", "Émet une fréquence aiguë capable de troubler brièvement l'ouïe et la concentration d'une cible proche. Ne rend pas sourd durablement.", ("Fréquence ciblée", "Cri de groupe ★")),
    ("Chant apaisant", "Apaise brièvement une tension chez les personnes qui entendent la voix et acceptent l'effet. Ne modifie ni souvenirs ni décisions.", ("Accord protecteur", "Chœur apaisant ★")),
    ("Voix mimétique", "Reproduit le timbre et la manière de parler d'une voix déjà entendue, sans acquérir les connaissances de son propriétaire.", ("Timbre parfait", "Écho différé")),
    ("Silence surnaturel", "Atténue les sons dans une petite zone pendant un court moment. Les vibrations et les autres moyens de communication restent possibles.", ("Bulle silencieuse", "Silence dirigé")),
    ("Écholocalisation", "Perçoit les contours proches grâce au retour d'un son émis. Le bruit, les protections et les matières absorbantes peuvent brouiller la lecture.", ("Cartographie sonore", "Filtrage des échos")),
])

POWER_DIRECTORY += power_table("XVIII", "Perception et conscience", "rgba(167,139,250,0.34)", [
    (
        "Regards croisés",
        "Perçoit brièvement deux points de vue à la fois : le sien et celui d'une personne consentante liée au pouvoir. Chaque vue reste limitée par les obstacles et la distance.",
        ("Focalisation double ★", "Relais de regards ★"),
        (
            "Distingue un détail dans chaque vue au prix d'une forte concentration, sans agir plus vite.",
            "Passe temporairement d'un point de vue volontaire à un autre, sans voir partout en même temps.",
        ),
    ),
    (
        "Vision thermique",
        "Perçoit les différences de chaleur à courte portée, même dans une faible lumière. Les murs épais, les isolants et les sources chaudes peuvent brouiller la lecture.",
        ("Lecture des traces chaudes ★", "Contraste affiné ★"),
        (
            "Repère pendant un court moment la chaleur laissée récemment sur une surface accessible.",
            "Distingue mieux deux sources proches sans identifier automatiquement une personne ni voir à travers tous les obstacles.",
        ),
    ),
    (
        "Nyctalopie",
        "Voit mieux dans la pénombre et l'obscurité partielle. Une absence totale de lumière, un éblouissement ou une illusion adaptée peuvent gêner la vision.",
        ("Pénombre profonde ★", "Adaptation rapide ★"),
        (
            "Distingue davantage de formes dans une obscurité presque complète, sans voir dans le noir absolu.",
            "S'adapte plus vite aux changements entre lumière et obscurité, sans immunité à l'éblouissement.",
        ),
    ),
    (
        "Écho des savoirs",
        "Capte un fragment de connaissance précis au contact d'une personne ou d'un objet lié à ce savoir, avec l'accord du joueur concerné. Ne donne ni maîtrise complète ni accès libre aux secrets.",
        ("Lecture approfondie ★", "Transmission d'un écho ★"),
        (
            "Obtient un détail supplémentaire sur le même sujet, avec des informations convenues avec les joueurs concernés.",
            "Partage brièvement le fragment reçu avec une personne consentante, sans lui transmettre une compétence durable.",
        ),
    ),
    (
        "Augure des marées",
        "Perçoit dans l'eau un présage fragmentaire lié à une personne, un lieu ou un événement proche. La vision ne garantit pas l'avenir.",
        ("Reflet du passé ★", "Vision des courants ★"),
        (
            "Entrevoit une trace passée liée à l'eau consultée, sans reconstituer toute la scène.",
            "Affûte un présage lié à un lieu traversé par l'eau, avec des limites validées par le staff.",
        ),
    ),
    (
        "Augure des nuées",
        "Lit dans les nuages des signes incertains sur un danger ou un changement possible. Un ciel dégagé n'empêche pas le don, mais rend le présage plus diffus.",
        ("Signe lointain ★", "Présage partagé ★"),
        (
            "Distingue un indice concernant un événement plus éloigné, sans en connaître la date certaine.",
            "Montre à une personne consentante une partie de la vision, sans imposer une interprétation unique.",
        ),
    ),
    (
        "Augure des racines",
        "Ressent dans une plante un écho du passé ou une possibilité à venir liée à son environnement. Les impressions restent fragmentaires.",
        ("Mémoire végétale ★", "Avertissement des racines ★"),
        (
            "Perçoit une trace plus ancienne conservée par une plante ou par le sol qui la nourrit.",
            "Reçoit un signal de danger proche à travers les végétaux, sans connaître automatiquement sa cause.",
        ),
    ),
    (
        "Détection des protégés",
        "Ressent la présence et l'état général des personnes avec lesquelles un lien de protection a été établi. Ne révèle ni leurs pensées ni leur position exacte.",
        ("Alerte du protégé ★", "Repérage du protégé ★"),
        (
            "Perçoit un appel ou un danger marqué touchant un protégé lié, sans en connaître automatiquement la cause.",
            "Obtient une direction approximative vers un protégé lié. La distance, les protections et l'accord du joueur concerné limitent la précision.",
        ),
    ),
    ("Partage sensoriel", "Transmet brièvement ce que le personnage voit ou entend à une personne consentante. Ne transmet ni pensées ni souvenirs.", ("Connexion prolongée", "Relais sensoriel ★")),
    ("Lecture des intentions", "Ressent une intention immédiate et marquée, comme attaquer ou protéger. N'offre pas la lecture des pensées ni la certitude sur les actes futurs.", ("Anticipation brève", "Veille collective ★")),
    ("Voile de présence", "Rend le personnage moins remarquable pour l'attention ordinaire sans le rendre invisible ni effacer ses traces.", ("Discrétion accrue", "Voile de groupe ★")),
    ("Sens des présages", "Ressent qu'un danger proche se prépare sans connaître sa cause exacte. Le signal peut être ambigu ou contrarié.", ("Alerte ciblée", "Pressentiment partagé ★")),
])

POWER_DIRECTORY += power_table("XIX", "Matière et forces", "rgba(96,165,250,0.30)", [
    (
        "Arbalète d'ombre",
        "Matérialise brièvement une arbalète d'énergie obscure et quelques traits surnaturels. Leur portée et leurs effets sont définis dans la fiche ; un tir n'atteint pas automatiquement sa cible.",
        ("Orbes d'emprise ★", "Rempart d'orbes obscures ★", "Transit d'orbes sombres ★"),
        (
            "Projette des orbes sombres pour attirer, repousser ou déplacer un petit objet visible. Une cible peut résister ; ce don ne déplace pas librement les personnes.",
            "Assemble plusieurs orbes en bouclier temporaire capable d'amortir une attaque, avec une taille et une résistance validées par le staff.",
            "Se téléporte en orbes sombres vers un point connu et accessible à courte distance. Les protections magiques peuvent bloquer le trajet ; transporter une autre personne demande une évolution distincte.",
        ),
    ),
    (
        "Voile cinétique",
        "Dresse devant soi une barrière physique brève qui amortit un choc ou dévie un petit projectile. Sa résistance est limitée et elle ne protège pas l'esprit.",
        ("Rempart partagé ★", "Déviation contrôlée ★"),
        (
            "Élargit la barrière pour protéger quelques personnes proches pendant un court instant.",
            "Oriente une partie de l'impact vers une zone libre, sans retourner automatiquement une attaque contre son auteur.",
        ),
    ),
    (
        "Flux emprunté",
        "Absorbe une faible quantité d'énergie ambiante ou offerte par une personne consentante. Ne retire pas les pouvoirs d'autrui et ne constitue pas une réserve illimitée.",
        ("Don de flux ★", "Décharge de flux ★"),
        (
            "Transmet une partie de l'énergie recueillie à une personne consentante, au prix d'une fatigue à jouer.",
            "Libère l'énergie accumulée en une impulsion courte dont l'effet sur une cible se joue avec elle.",
        ),
    ),
    (
        "Cristallokinésie",
        "Crée une petite quantité de cristaux, puis peut les déplacer et les façonner. Leur taille et leur résistance restent limitées.",
        ("Barrière cristalline ★", "Résonance des gemmes ★"),
        (
            "Assemble les cristaux créés en une protection temporaire dont la taille et la solidité sont validées.",
            "Fait vibrer les cristaux proches pour produire un signal ou repérer une résonance, sans traverser toutes les protections.",
        ),
    ),
    ("Magnétokinésie", "Crée un champ magnétique local pour attirer ou repousser de petits objets ferromagnétiques proches. Tous les métaux ne réagissent pas et une arme tenue peut être résistée.", ("Attraction multiple", "Bouclier magnétique ★")),
    ("Gravikinésie", "Crée une variation locale de gravité qui allège ou alourdit légèrement un objet ou son propre corps pendant un court instant. Ne permet ni vol libre ni écrasement d'une personne.", ("Zone allégée ★", "Ancrage gravitationnel ★")),
    ("Brumokinésie", "Crée une faible brume ou vapeur, ou modèle celle qui est présente. Elle n'asphyxie pas automatiquement.", ("Voile de brume", "Brume dense ★")),
])

POWER_DIRECTORY += power_table("XX", "Corps et adaptation", "rgba(45,212,191,0.30)", [
    (
        "Accord des sens",
        "Associe temporairement deux perceptions du personnage, par exemple voir un son comme une couleur. L'effet enrichit la perception sans révéler des informations cachées.",
        ("Accord empathique ★", "Spectre élargi ★"),
        (
            "Perçoit une émotion forte comme une nuance sensorielle, sans lire les pensées ni connaître sa cause certaine.",
            "Associe brièvement plusieurs sens avec une précision accrue, au risque d'une surcharge sensorielle.",
        ),
    ),
    (
        "Éclat moléculaire",
        "Accélère brièvement les molécules de l'air pour produire un flash lumineux local. Il peut gêner la vue sans brûlure ni aveuglement durable imposés.",
        ("Flash dirigé ★", "Éclats successifs ★"),
        (
            "Concentre l'éclat dans une direction définie, avec la réaction des personnes exposées jouée librement.",
            "Produit deux flashes brefs à quelques instants d'intervalle, au prix d'une fatigue accrue.",
        ),
    ),
    (
        "Souffle d'expansion",
        "Dilate temporairement une petite quantité de matière inerte pour déplacer ou écarter un objet léger. Ne provoque ni explosion ni dommage corporel automatique.",
        ("Expansion dirigée ★", "Retour stable ★"),
        (
            "Oriente la dilatation pour exercer une poussée courte sur un objet compatible.",
            "Ramène plus vite la matière modifiée à sa forme initiale, sans réparer les dégâts antérieurs.",
        ),
    ),
    (
        "Rémanence moléculaire",
        "Rétablit progressivement une petite matière inerte récemment altérée par un effet moléculaire identifiable. N'annule pas une blessure, une mort ou toute magie adverse.",
        ("Stabilisation ciblée ★", "Réversion étendue ★"),
        (
            "Interrompt la progression d'une altération moléculaire limitée avant de rétablir la matière.",
            "Rétablit une zone inerte un peu plus grande avec l'accord des joueurs concernés et une ampleur validée par le staff.",
        ),
    ),
    (
        "Peau des bêtes",
        "Adopte temporairement une forme animale définie dans la fiche. La transformation ne donne ni les souvenirs ni tous les instincts de l'animal.",
        ("Forme affinée ★", "Répertoire animal ★"),
        (
            "Maîtrise mieux une forme choisie et ses mouvements, sans supprimer ses faiblesses.",
            "Ajoute une seconde forme animale validée, avec ses propres limites et une durée définie.",
        ),
    ),
    (
        "Rayonnement réparateur",
        "Diffuse un soin léger à deux personnes consentantes proches. La fatigue augmente avec le nombre de cibles et les blessures graves restent hors de portée.",
        ("Cercle de soin ★", "Soutien prolongé ★"),
        (
            "Étend le soin léger à quelques personnes supplémentaires dans une zone limitée.",
            "Maintient le soin sur deux personnes pendant quelques tours de RP, avec un coût physique accru.",
        ),
    ),
    (
        "Pétrification progressive",
        "Durcit temporairement une petite partie de son corps ou une surface touchée. Une atteinte sur un autre personnage demande son accord et ne l'immobilise pas automatiquement.",
        ("Pétrification étendue ★", "Réversion de la pierre ★"),
        (
            "Étend l'effet à une zone plus grande pendant une durée validée, avec l'accord de toute personne ciblée.",
            "Met fin plus rapidement à une pétrification causée par ce pouvoir, sans annuler toutes les malédictions de pierre.",
        ),
    ),
    (
        "Variation de taille",
        "Agrandit ou réduit légèrement sa propre taille pendant quelques tours de RP. La masse, la force et l'accès aux lieux ne changent pas sans limites convenues.",
        ("Changement marqué ★", "Taille d'autrui ★"),
        (
            "Accentue la variation de taille avec une durée et des effets physiques validés par le staff.",
            "Applique une variation modérée à une personne consentante proche, sans lui imposer d'action.",
        ),
    ),
    (
        "Variation de densité",
        "Allège ou densifie temporairement son propre corps dans une mesure limitée. Cela ne rend ni intangible ni invulnérable et ne permet pas le vol libre.",
        ("Ancrage dense ★", "Légèreté accrue ★"),
        (
            "Résiste mieux à une poussée ou à un choc, sans annuler les dégâts ni empêcher toute chute.",
            "Réduit davantage le poids ressenti pour franchir un obstacle court, sans flotter indéfiniment.",
        ),
    ),
    (
        "Sillage des effluves",
        "Crée ou module une faible émission de phéromones surnaturelles qui peut attirer l'attention ou modifier une impression passagère. Ne fait naître ni amour ni obéissance.",
        ("Empreinte apaisante ★", "Sillage diffus ★"),
        (
            "Propose une sensation de calme à une cible réceptive, qui garde ses choix et sa réaction.",
            "Étend l'effluve à quelques personnes proches pendant une courte durée, avec leurs réactions jouées librement.",
        ),
    ),
    (
        "Clonage",
        "Crée un double physique temporaire du personnage, capable d'agir à proximité pendant quelques tours de RP. Il partage ses limites et ne multiplie ni ses pouvoirs ni sa réserve d'énergie.",
        ("Double prolongé ★", "Clones multiples ★"),
        (
            "Maintient un double pendant davantage de tours de RP, avec une durée validée par le staff.",
            "Crée jusqu'à deux doubles temporaires à la fois. Leurs actions demandent l'attention du personnage et ne garantissent aucune réussite contre une cible.",
        ),
    ),
    ("Métabolisme accéléré", "Accorde un bref surcroît d'énergie physique au prix d'une fatigue ensuite. Ne remplace ni la guérison ni la vitesse surnaturelle.", ("Récupération brève", "Élan prolongé")),
    ("Camouflage organique", "Modifie les couleurs ou motifs du corps pour mieux se fondre dans un environnement. Le mouvement et les autres sens peuvent révéler le personnage.", ("Mimétisme complet", "Camouflage en mouvement")),
    ("Adaptation respiratoire", "Permet de supporter brièvement un air difficile ou de retenir son souffle plus longtemps. Ne protège pas de toutes les substances dangereuses.", ("Respiration prolongée", "Filtration de l'air ★")),
    ("Algokinésie", "Crée ou module temporairement une sensation douloureuse chez soi ou une personne consentante, sans créer de blessure. Une blessure existante reste présente même si la douleur est apaisée.", ("Apaisement ciblé", "Apaisement partagé ★")),
])

POWER_DIRECTORY += power_table("XXI", "Facultés mentales et pouvoirs insolites", "rgba(196,181,253,0.34)", [
    (
        "Sillage fulgurant",
        "Se déplace sur une très courte distance sous la forme d'un éclair magique. Le trajet doit rester accessible et les protections adaptées peuvent l'arrêter.",
        ("Relais conducteur ★", "Passage accompagné ★"),
        (
            "Prolonge légèrement le trajet en suivant un conducteur visible, sans traverser librement les lieux protégés.",
            "Emmène une personne consentante sur un trajet bref, avec un effort et une portée validés par le staff.",
        ),
    ),
    (
        "Germe de discorde",
        "Accentue brièvement une tension déjà perceptible entre des personnes proches. Ne crée pas de haine durable et ne force ni dispute ni violence.",
        ("Dissonance partagée ★", "Tension dissipée ★"),
        (
            "Étend la tension à quelques personnes réceptives, chacune gardant ses choix.",
            "Apaise plus vite une discorde provoquée par ce pouvoir, sans effacer les désaccords réels.",
        ),
    ),
    (
        "Pas de brume",
        "Se dissout brièvement en brume pour rejoindre un point visible à courte distance. Les protections magiques et les obstacles hermétiques peuvent interrompre le trajet.",
        ("Trajet voilé ★", "Passage accompagné ★"),
        (
            "Parcourt une distance un peu plus longue dans les limites du lieu, sans devenir invisible ni intouchable durant toute la scène.",
            "Emmène une personne consentante sur un court trajet, avec une charge et un effort validés par le staff.",
        ),
    ),
    (
        "Égide de l'esprit",
        "Dresse une protection mentale temporaire contre une intrusion ou une influence psychique. Elle peut céder face à une force supérieure et ne bloque pas les attaques physiques.",
        ("Égide partagée ★", "Ancrage mental ★"),
        (
            "Étend brièvement la protection à une personne consentante proche.",
            "Renforce la résistance à une influence précise déjà identifiée, sans immunité absolue.",
        ),
    ),
    ("Torture mentale", "Inflige à une cible une sensation de souffrance psychique temporaire, sans blessure physique ni séquelle imposée. Les réactions, révélations et limites de la scène sont convenues avec son joueur.", ("Étau psychique ★", "Pression partagée ★")),
    ("Omnilinguisme", "Permet de comprendre et de parler les langues ordinaires entendues, sans donner accès aux pensées, aux codes secrets ou aux savoirs de leurs locuteurs.", ("Écritures anciennes", "Langues occultes ★")),
    ("Intuition des mensonges", "Perçoit une discordance lorsqu'une personne ment délibérément, sans connaître la vérité ni détecter une erreur sincère.", ("Dissonance des récits", "Lecture des omissions ★")),
    ("Tychokinésie", "Crée une légère inflexion de chance autour d'un événement banal et incertain. Ne garantit aucun résultat et ne décide pas seule de l'issue d'une scène.", ("Chance favorable ★", "Malchance localisée ★")),
    ("Transmutation mineure", "Modifie temporairement la matière d'un petit objet inerte. Ne touche ni les êtres vivants ni les objets protégés sans accord.", ("Matière durable ★", "Transformation multiple ★")),
    ("Animation d'objets", "Anime brièvement un petit objet inerte pour une action simple. L'objet n'acquiert ni pensée ni pouvoir propre.", ("Mouvement coordonné", "Assistant animé ★")),
    ("Sommeil induit", "Favorise une somnolence progressive chez une cible réceptive. Ne provoque pas d'inconscience instantanée et la cible peut résister.", ("Sommeil profond ★", "Rêve dirigé ★")),
    ("Dissipation de magie", "Affaiblit ou dénoue un effet magique temporaire de portée limitée après concentration. N'efface pas les pouvoirs d'une personne.", ("Dissipation ciblée ★", "Cercle de dissipation ★")),
])

POWER_DIRECTORY += power_table("XXII", "Eaux, lumière et enchantements", "rgba(103,232,249,0.34)", [
    (
        "Corps de marée",
        "Liquéfie temporairement une petite partie de son propre corps. Cela ne rend ni insensible aux attaques ni capable de traverser toute surface.",
        ("Forme fluide ★", "Écoulement guidé ★"),
        (
            "Étend la transformation à une plus grande partie du corps pendant quelques tours de RP, avec des limites validées.",
            "Se glisse par une ouverture compatible sur une courte distance, sans contourner automatiquement les protections magiques.",
        ),
    ),
    ("Bouclier aquatique", "Crée ou rassemble de l'eau en barrière pour amortir une attaque. La protection a une résistance et une durée limitées.", ("Dôme aqueux ★", "Bouclier mobile ★")),
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
    ("Néphokinésie", "Crée un petit nuage ou déplace et modèle ceux qui sont présents à proximité. Ne contrôle pas librement le climat.", ("Courants nuageux", "Couverture céleste ★")),
    ("Nuage protecteur", "Maintient un nuage dense entre une attaque et ses cibles pour gêner la visée ou amortir un impact léger. Ne remplace pas un bouclier invulnérable.", ("Écran suspendu", "Dôme de nuages ★")),
    ("Marche des nuages", "Condense brièvement un appui sous les pieds pour franchir un vide limité. L'appui se dissipe rapidement et n'accorde pas le vol libre.", ("Pas successifs ★", "Plateforme partagée ★")),
    ("Poussière de fée", "Crée une fine poussière enchantée qui allège momentanément un petit objet ou une personne consentante. Ne donne ni vol permanent ni pouvoirs supplémentaires.", ("Lévitation légère ★", "Nuée féerique ★")),
    ("Télékinésie lumineuse", "Crée des filaments de lumière condensée pour attirer ou déplacer un petit objet visible. La concentration reste nécessaire.", ("Prise photique", "Manipulation multiple ★")),
    ("Prisme de lumière", "Réfracte une lumière présente pour produire des reflets trompeurs ou dévier un éclat. Ne crée ni matière ni illusion mentale.", ("Déviation lumineuse", "Miroirs prismatiques ★")),
])

for section_number, section_title, section_color, powers in KINETIC_POWER_SECTIONS:
    POWER_DIRECTORY += power_table(section_number, section_title, section_color, powers)

POWER_DIRECTORY += power_table("XXXI", "Instinct, traque et ralliement", "rgba(251,191,36,0.32)", [
    (
        "Aile spectrale",
        "Invoque un petit oiseau spectral capable d'observer un lieu proche ou de porter un message bref. Il ne combat pas et peut être dissipé.",
        ("Messager lointain ★", "Volée spectrale ★"),
        (
            "Envoie l'oiseau plus loin avec un trajet et une durée définis, sans vision omnisciente.",
            "Invoque quelques oiseaux pour explorer des directions distinctes ; les informations reçues restent partielles.",
        ),
    ),
    (
        "Parole des bêtes",
        "Échange des impressions et des intentions simples avec un animal proche. Comprendre un animal ne garantit ni sa confiance ni son obéissance.",
        ("Langage approfondi ★", "Appel animal ★"),
        (
            "Comprend un message animal plus précis dans les limites de ce que l'animal a réellement perçu.",
            "Adresse un appel à des animaux proches, sans les forcer à venir ou à aider.",
        ),
    ),
    (
        "Ascendant animal",
        "Tente d'orienter brièvement l'action simple d'un animal présent, selon son instinct et sa disposition. Ne commande pas une créature contre sa survie ou son maître sans accord.",
        ("Lien de confiance ★", "Influence de groupe ★"),
        (
            "Renforce une coopération déjà acceptée par un animal, sans effacer sa volonté.",
            "Adresse la même suggestion simple à quelques animaux proches, sans garantir leur réaction.",
        ),
    ),
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

POWER_DIRECTORY += power_table("XXXII", "Furies", "rgba(248,113,113,0.32)", [
    ("Cri de Furie", "Libère par la voix une onde liée à une émotion intense qui peut repousser ou déséquilibrer à courte portée. Ne blesse pas automatiquement une cible.", ("Onde furieuse ★", "Déflagration vocale ★")),
    (
        "Écho des fautes",
        "Fait entendre à une cible proche un bref écho des voix de personnes qu'elle pense avoir blessées. Le pouvoir ne révèle aucun fait inconnu du lanceur et ne force ni aveu ni réaction.",
        ("Clameur des fautes ★", "Voix persistante ★"),
        (
            "Étend un écho plus faible à quelques cibles proches, chacune conservant sa réaction.",
            "Prolonge brièvement la perception chez une cible, sans l'épuiser ni lui imposer des souvenirs.",
        ),
    ),
])

POWER_DIRECTORY += power_table("XXXIII", "Démons de Lazare", "rgba(148,163,184,0.34)", [
    (
        "Mémoire des cendres",
        "Perçoit des impressions fragmentaires laissées dans les cendres issues de sa propre destruction. Ne reconstitue ni toute la scène ni les pensées d'autrui.",
        ("Lecture des vestiges ★", "Retour des fragments ★"),
        (
            "Affûte une impression liée à son corps disparu, sans obtenir un récit certain des événements.",
            "Reconstitue lentement un petit objet personnel détruit avec lui, à condition d'en retrouver les fragments ; aucun objet magique ou détenu par autrui n'est recréé librement.",
        ),
    ),
])

POWER_DIRECTORY += power_table("XXXIV", "Démons Kazi", "rgba(239,68,68,0.34)", [
    (
        "Pression crânienne",
        "Exerce une pression magique brève sur une cible à courte portée, pouvant causer douleur ou désorientation passagère. Aucune lésion ni perte de connaissance n'est automatique.",
        ("Étau focalisé ★", "Onde de pression ★"),
        (
            "Maintient la pression un peu plus longtemps sur une seule cible, avec concentration et possibilité de résistance.",
            "Répartit une pression atténuée entre quelques cibles proches ; chacune peut réagir ou s'en protéger.",
        ),
    ),
])

POWER_DIRECTORY += power_table("XXXV", "Succubes et incubes", "rgba(236,72,153,0.34)", [
    (
        "Lecture des désirs",
        "Perçoit une attirance ou un désir déjà présent chez une personne proche, sans lire ses pensées ni connaître toute son histoire intime.",
        ("Nuance du désir ★", "Miroir du désir ★"),
        (
            "Distingue plus finement une émotion déjà ressentie, sans en connaître nécessairement la cause.",
            "Suggère une brève illusion liée au désir perçu ; la cible peut la reconnaître et conserve ses sentiments et ses choix.",
        ),
    ),
])

POWER_DIRECTORY += power_table("XXXVI", "Vampires", "rgba(185,28,28,0.34)", [
    ("Soif révélatrice", "Perçoit à courte portée une odeur de sang récente ou la présence d'une blessure ouverte. Ne révèle ni identité certaine ni état de santé complet.", ("Piste sanguine ★", "Faim maîtrisée ★"), ("Suit une trace de sang récente sur une distance limitée, tant qu'elle n'est pas masquée.", "Distingue plus facilement une piste malgré la soif, sans supprimer celle-ci ni les autres faiblesses.")),
    ("Vitesse vampirique", "Accélère brièvement ses mouvements pour franchir une courte distance ou esquiver. Ne rend pas invisible et ne garantit aucun coup porté.", ("Élan prolongé ★", "Réflexe fulgurant ★"), ("Maintient la vitesse sur un trajet un peu plus long, avec fatigue et obstacles à jouer.", "Réagit plus vite à une menace perceptible, sans esquive automatique.")),
    ("Contrainte du regard", "Tente une suggestion simple par contact visuel direct. La cible peut résister et le joueur concerné décide de sa réaction ; la verveine et les protections adaptées restent efficaces.", ("Suggestion précise ★", "Souvenir voilé ★"), ("Formule une consigne simple plus claire, sans contrôler durablement une personne.", "Brouille un détail récent avec l'accord du joueur concerné, sans réécrire tout un souvenir.")),
])

POWER_DIRECTORY += power_table("XXXVII", "Loups-garous", "rgba(217,119,6,0.34)", [
    ("Transformation lupine", "Prend une forme lupine ou manifeste un trait de cette forme selon sa continuité d'origine. La transformation et son contrôle sont définis dans la fiche.", ("Mutation partielle ★", "Retour maîtrisé ★"), ("Manifeste un trait précis sans transformation complète, selon sa continuité validée.", "Revient plus sûrement à sa forme ordinaire, sans annuler les contraintes lunaires ou émotionnelles.")),
    ("Instinct de meute", "Ressent l'état émotionnel général d'un allié de meute proche avec lequel un lien a été établi. Ne lit ni pensées ni position exacte.", ("Alerte de meute ★", "Lien resserré ★"), ("Transmet une impression simple de danger aux alliés réceptifs à proximité.", "Distingue mieux l'état d'un allié lié, sans accéder à ses secrets ni imposer ses décisions.")),
    ("Pistage lupin", "Suit une odeur récente sur une distance limitée. Pluie, foule, obstacles et autres pistes peuvent brouiller la trace.", ("Tri des effluves ★", "Piste prolongée ★"), ("Isole une odeur connue parmi plusieurs traces proches, sans certitude absolue.", "Suit plus longtemps une trace exploitable, avec fatigue et perturbations possibles.")),
])

POWER_DIRECTORY += power_table("XXXVIII", "Sorcières et sorciers Charmed", "rgba(167,139,250,0.34)", [
    ("Formule improvisée", "Compose un sort simple pour un effet limité et préparé dans la scène. Son fonctionnement et ses limites sont validés ; elle ne remplace pas n'importe quel pouvoir du registre.", ("Formule affinée ★", "Incantation partagée ★"), ("Rend un effet déjà connu plus précis, sans élargir librement sa portée.", "Réalise un sort défini avec une personne consentante, selon une préparation commune.")),
    ("Alchimie de terrain", "Prépare une potion simple avec des ingrédients identifiés et du temps de jeu. L'effet doit être défini dans la fiche ou validé par le staff.", ("Préparation stable ★", "Potion adaptée ★"), ("Conserve un peu plus longtemps une préparation connue dans des conditions adaptées.", "Ajuste une recette connue à une cible précise sans inventer un nouvel effet sur place.")),
    ("Lien d'incantation", "Synchronise brièvement un sort connu avec une autre sorcière ou un autre sorcier volontaire. Chacun doit posséder et employer ses propres capacités validées.", ("Cercle restreint ★", "Harmonie rituelle ★"), ("Coordonne quelques participants consentants pour un rituel défini, sans cumul illimité de puissance.", "Réduit une perturbation mineure pendant un sort commun préparé, sans garantir sa réussite.")),
])

POWER_DIRECTORY += power_table("XXXIX", "Êtres des ténèbres", "rgba(99,102,241,0.34)", [
    (
        "Marque de traque",
        "Suit pendant quelques tours de RP la trace magique d'une personne déjà rencontrée. La distance, les protections et les déplacements peuvent brouiller la piste.",
        ("Piste d'ombre ★", "Trace persistante ★"),
        (
            "Retrouve la direction générale prise après une téléportation, sans connaître la destination exacte ni traverser les protections.",
            "Conserve un peu plus longtemps une trace identifiée, sans localisation permanente.",
        ),
    ),
])

POWER_DIRECTORY += power_table("XL", "Prophétesses démoniaques", "rgba(168,85,247,0.34)", [
    (
        "Présage de rupture",
        "Entrevoit qu'une décision proche pourrait infléchir un événement. La vision reste symbolique et ne donne ni issue certaine ni moyen d'imposer un choix.",
        ("Visions divergentes ★", "Écho du choix ★"),
        (
            "Aperçoit deux issues possibles sans savoir laquelle se réalisera ; l'intrigue détermine les informations révélées.",
            "Partage un fragment du présage avec une personne consentante, sans lui transmettre un pouvoir de divination.",
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
