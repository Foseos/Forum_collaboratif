import re
from html import escape, unescape

from django.utils.html import strip_tags


# Ambiance, utilisation, limites : les effets et prix du catalogue restent la référence.
ITEM_DETAILS = {
    "Potion d'invisibilité": (
        "Une fiole opalescente dont le liquide semble disparaître lorsqu’on la regarde de côté.",
        "Consommable · une fiole, une personne, trois tours de RP. À boire avant une infiltration ou une filature ; les vêtements portés au moment de la prise sont dissimulés avec le personnage.",
        "Les bruits, les odeurs, les traces et le contact restent perceptibles. Ne garantit pas de tromper un sens surnaturel ou une protection magique. Les partenaires déterminent ensemble si leur personnage remarque une présence.",
    ),
    'Potion de guérison': (
        "Un élixir ambré qui diffuse une chaleur douce au contact de la peau.",
        "Consommable · une fiole pour une personne. La guérison des blessures mineures à modérées se joue sur un tour de RP.",
        "Ne ressuscite pas, ne soigne pas une blessure mortelle et ne retire ni poison ni malédiction. La fatigue et les conséquences émotionnelles persistent. Faire préciser les soins nécessaires par le maître du jeu lors d’un événement.",
    ),
    'Élixir de vérité': (
        "Son éclat argenté rappelle une surface d’eau parfaitement immobile.",
        "Consommable · une dose, une personne, deux tours de RP. Pour une scène d’interrogatoire ou d’aveu, convenir à l’avance de l’effet avec le joueur concerné ; en événement, demander l’accord du maître du jeu.",
        "Ne révèle que ce que la cible croit vrai : un souvenir erroné reste erroné. Ne donne accès ni aux pensées ni à des connaissances ignorées. La résistance des êtres puissants et les secrets révélés sont décidés avec leur joueur.",
    ),
    'Potion de téléportation': (
        "Des filaments bleutés tournent dans la fiole comme s’ils cherchaient déjà une sortie.",
        "Consommable · un trajet pour le buveur et ses effets portés. Décrire le lieu connu visé au moment de l’utilisation.",
        "Ne transporte pas un groupe, ne traverse pas une zone protégée et n’ouvre pas de passage entre les plans. Une destination inaccessible ou une fuite pendant un événement doit être arbitrée par le maître du jeu.",
    ),
    "Potion d'immunité magique": (
        "Un dépôt nacré tapisse le verre ; une fois agitée, la potion devient lumineuse.",
        "Consommable · une personne, trois tours de RP. Préciser la prise et sa durée avant la confrontation.",
        "La protection concerne les sorts offensifs, pas les armes, les chutes ou les conséquences matérielles d’un sort. N’annule aucun effet déjà actif. Face à un artefact ancestral ou une puissance exceptionnelle, le maître du jeu détermine sa portée.",
    ),
    'Potion de sommeil profond': (
        "Une préparation discrète conservée dans un flacon de verre sombre.",
        "Consommable · une dose pour un sommeil de deux tours de RP. Son emploi sur le personnage d’un autre membre nécessite l’accord de ce joueur ; les cibles d’événement relèvent du maître du jeu.",
        "Ne permet pas de déclarer seul une capture ou une neutralisation. Résistances, interruption du sommeil et conséquences sont convenues avant la scène. Il s’agit d’un objet fictif, sans recette de préparation.",
    ),
    'Cristal de quartz pur': (
        "Ses arêtes translucides vibrent doucement lorsqu’un cercle rituel se referme.",
        "Durable · support de rituel à placer au centre du cercle ou près de son officiant. Nettoyage rituel après une séance particulièrement intense.",
        "N’accorde aucun pouvoir nouveau. L’amplification dépend du rituel et de la maîtrise de ses participants ; empiler plusieurs quartz ne multiplie pas automatiquement leur puissance.",
    ),
    'Améthyste de protection': (
        "Une pierre violette parcourue de fines veines claires, montée pour être portée contre soi.",
        "Durable · protection personnelle contre les entités maléfiques faibles à moyennes. Sa présence et son port doivent être mentionnés dans la scène.",
        "Ne protège pas tout un lieu ni les compagnons du porteur. N’empêche pas les attaques ordinaires et ne rend pas invulnérable. La résistance du bouclier face à une attaque précise se joue avec le partenaire ou le maître du jeu.",
    ),
    'Obsidienne noire': (
        "Un éclat de verre volcanique dont la surface se ternit lorsqu’il absorbe une influence néfaste.",
        "Durable avec entretien · une absorption d’énergie négative ou de malédiction légère avant purification. Jouer le nettoyage rituel avant de la réutiliser.",
        "Une pierre saturée reste inactive. Ne retire pas une possession, une malédiction ancestrale ni un pacte. L’identification d’une malédiction légère revient au maître du jeu lorsque l’intrigue en dépend.",
    ),
    'Pierre de lune sacrée': (
        "Une lueur laiteuse court sous sa surface et s’intensifie à la pleine lune.",
        "Durable · support de divination ou de vision pour un personnage disposant déjà de ces aptitudes. Décrire une séance de concentration.",
        "Ne transforme pas un personnage sans don en voyant. Les visions restent fragmentaires et interprétables ; demander au maître du jeu les indices liés à son événement. Ne dévoile pas les secrets d’un autre personnage sans accord.",
    ),
    'Rubis de feu': (
        "Le cœur du rubis semble abriter une braise qui ne s’éteint jamais.",
        "Durable · catalyseur destiné à un personnage maîtrisant déjà la magie du feu. Peut accompagner un entraînement ou un sort préparé.",
        "N’accorde pas la pyrokinésie. Une mauvaise maîtrise expose à une perte de contrôle jouée dans la scène. Ne permet pas d’imposer une brûlure ou une destruction au personnage d’un partenaire.",
    ),
    'Saphir des eaux profondes': (
        "Bleu presque noir au repos, il s’éclaircit lorsqu’une magie aquatique approche.",
        "Durable · à porter sur soi pour bénéficier de sa résistance aux sorts aquatiques. Peut servir de point de concentration dans une scène éprouvante.",
        "Résistance ne signifie pas immunité. Ne permet ni de respirer sous l’eau ni de manipuler l’eau et ne protège pas de la noyade. La clarté d’esprit n’annule pas une emprise mentale puissante.",
    ),
    'Miroir de vérité': (
        "Un petit miroir au cadre ancien dont le reflet accuse parfois un léger retard.",
        "Durable · présenter le miroir à une personne qui s’y regarde. Prévoir l’accord du joueur avant de révéler la nature de son personnage ; le maître du jeu décide pour ses personnages d’événement.",
        "Montre une nature surnaturelle, pas les intentions, les souvenirs ou les pouvoirs exacts. Une protection ou une dissimulation exceptionnelle peut brouiller le reflet selon l’arbitrage convenu.",
    ),
    'Amulette de protection': (
        "Un pendentif gravé d’un cercle fermé, tiède lorsqu’une présence hostile s’approche.",
        "Durable · à porter pour repousser les entités de bas niveau et atténuer les sorts de domination. Protection limitée à son porteur.",
        "Ne bloque pas toute attaque magique et ne lève pas une possession. L’atténuation laisse au joueur la possibilité de décrire une résistance, sans imposer l’échec automatique du pouvoir adverse.",
    ),
    "Talisman d'équilibre": (
        "Ses deux faces portent des motifs opposés qui semblent s’aligner lorsque son porteur se calme.",
        "Durable · accompagne l’apprentissage de pouvoirs instables. Utiliser le talisman comme point d’ancrage pendant une scène d’entraînement ou de crise.",
        "Ne remplace pas l’apprentissage et n’augmente pas la puissance. Une émotion extrême peut dépasser son aide. Il ne supprime pas les faiblesses liées à la nature du personnage.",
    ),
    'Grimoire vierge enchanté': (
        "Un carnet aux pages épaisses dont l’encre semble pénétrer les fibres aussitôt déposée.",
        "Durable · définir à l’achat le propriétaire et les personnes autorisées à le lire. Les pages accueillent les sorts, recherches et notes réellement appris en RP.",
        "Les pages vierges ne contiennent aucun sort offert. La résistance au feu et à l’eau n’empêche ni le vol ni toutes les destructions magiques. Une tentative de déchiffrement se joue avec l’accord du propriétaire.",
    ),
    'Baguette de saule pleureur': (
        "Souple et légère, cette baguette conserve les nervures argentées de son bois.",
        "Durable · focaliseur pour les sorts de divination et de localisation déjà maîtrisés. Associer un pendule, une carte ou un lien avec la cible lorsque le sort l’exige.",
        "Ne localise personne seule et ne contourne pas automatiquement une protection. La précision dépend des informations disponibles ; aucun emplacement secret d’un personnage n’est révélé sans accord.",
    ),
    'Calice de cristal': (
        "Les voix du cercle se répercutent dans sa coupe comme un chant lointain.",
        "Durable mais fragile · support d’un rituel collectif. Définir le sort, les participants et leurs contributions ; l’amplification peut aller jusqu’à trois fois avec validation du maître du jeu.",
        "Le maximum n’est pas un bonus automatique à chaque sort. Ne fournit ni énergie infinie ni connaissances manquantes. Une surcharge ou une mauvaise utilisation peut briser le calice ; préciser ce risque avant le rituel.",
    ),
    'Pochette de sortilèges': (
        "Trois compartiments cousus de fil runique gardent leurs contenus soigneusement séparés.",
        "Durable · capacité de trois sorts actifs préparés par un personnage capable de les lancer. Noter le contenu et retirer chaque sort de la liste lorsqu’il est libéré.",
        "Ne crée pas de sorts, ne les copie pas et n’en augmente pas la puissance. Le déclenchement suit les conditions du sort stocké. Les rituels majeurs et les pouvoirs innés non transférables n’y entrent pas sans accord du maître du jeu.",
    ),
    'Sauge blanche': (
        "Un petit fagot lié de fil clair, réservé aux cérémonies de purification du monde du forum.",
        "Consommable · un lot pour une purification d’objet ou d’une pièce. Décrire le rituel et la dissipation des résidus légers.",
        "Ne bannit pas une entité puissante et ne remplace pas un exorcisme. Un lieu frappé d’une malédiction majeure nécessite une intrigue et un rituel adaptés.",
    ),
    'Lavande enchantée': (
        "Quelques brins violets conservent leur parfum bien après la récolte.",
        "Consommable · un sachet pour accompagner une scène d’apaisement. À employer avec l’accord du personnage concerné.",
        "N’efface pas les émotions, les souvenirs ou les conséquences d’un traumatisme. Peut aider à résister à une influence légère, sans annuler automatiquement une domination.",
    ),
    'Belladone distillée': (
        "Une préparation d’alchimie fictive scellée et étiquetée par l’échoppe.",
        "Consommable · une dose pour une préparation de potion de sommeil ou d’illusion. Réservée aux sorcières expérimentées, avec une recette magique validée dans le cadre du jeu.",
        "L’ingrédient seul n’équivaut pas à une potion achevée. Aucun dosage ni procédé réel n’est fourni. Les effets sur un personnage restent soumis à l’accord de son joueur.",
    ),
    'Herbes du solstice': (
        "Un bouquet séché dont les feuilles gardent des reflets cuivrés de leur récolte annuelle.",
        "Consommable · un lot pour un rituel lors d’un solstice ou d’un équinoxe en RP. Prévoir le rituel avec le maître du jeu avant de bénéficier de son amplification exceptionnelle.",
        "L’amplification annoncée concerne ce rituel, pas tous les pouvoirs du personnage. Hors de ces dates, le bonus exceptionnel ne s’applique pas. Ne se cumule pas librement avec d’autres multiplicateurs.",
    ),
    'Encens de purification': (
        "Une boîte compartimentée abrite douze bâtons marqués du sceau de la boutique.",
        "Consommable · douze utilisations, à raison d’un bâton pour une petite pièce ou un objet. Décompter les bâtons au fil des scènes.",
        "Agit sur les présences faibles et les résidus de sorts. N’annule pas un rituel actif, une possession ou une protection majeure. Un lieu étendu demande un dispositif défini avec le maître du jeu.",
    ),
    'Orbe du Destin': (
        "Sous le verre, des chemins lumineux apparaissent puis se referment avant d’être entièrement lisibles.",
        "Artefact ancestral · acquisition validée par la fondatrice, non revendable. Une activation par intrigue ; la vision concerne un événement à venir de cette intrigue, défini avec le maître du jeu.",
        "Le maître du jeu propose le fragment aperçu et valide la légère modification possible. Ne réécrit ni une prophétie fixée, ni les choix d’un autre joueur, ni le résultat complet d’un événement.",
    ),
    'Sceptre des Ancêtres': (
        "Dix sillons parcourent son manche et s’illuminent lorsque le cercle unit ses voix.",
        "Artefact ancestral durable · acquisition validée par la fondatrice, non revendable. Un groupe d’au moins cinq personnes prépare ensemble un sort unique et son coût narratif avec le maître du jeu.",
        "La puissance annoncée est canalisée pour ce sort, jamais acquise définitivement. Ne remplace pas les connaissances nécessaires et ne garantit pas le succès contre un adversaire ou une protection majeure.",
    ),
    'Boussole des Failles': (
        "Son aiguille d'argent tremble près d'une brèche et s'oriente vers son écho magique.",
        "Artefact ancestral durable · acquisition validée par la fondatrice, non revendable. Une activation par intrigue révèle pendant trois tours de RP la direction d'une faille active dans la scène et si elle s'élargit ou se referme.",
        "Ne crée, n'ouvre ni ne ferme aucune faille. N'indique pas ce qui se trouve de l'autre côté et ne repère pas une brèche dissimulée par une protection majeure. Les indices liés à une intrigue sont donnés par le maître du jeu.",
    ),
    "Cristal d'Omniscience": (
        "Ses facettes reflètent des scènes différentes, dont certaines appartiennent à celui qui le tient.",
        "Artefact ancestral durable · acquisition validée par la fondatrice, non revendable. Poser une question précise sur le passé ou le présent ; la réponse est fournie par le maître du jeu.",
        "Ne donne pas carte blanche pour inventer la vérité du forum ou consulter les secrets d’un autre joueur. La révélation concernant le détenteur et les informations accessibles sont convenues avec les personnes concernées.",
    ),
    'Dague des Anciens': (
        "Une lame sombre dont le tranchant semble absorber les reflets plutôt que les renvoyer.",
        "Artefact ancestral durable · acquisition validée par la fondatrice, non revendable. Usage réservé à la légitime défense ; annoncer son emploi au maître du jeu avant la résolution de l’affrontement.",
        "La blessure exceptionnelle n’est appliquée qu’après un coup effectivement porté et validé. La dague ne garantit ni de toucher ni de tuer. Ses conséquences durables sur un personnage exigent l’accord de son joueur et de la fondatrice.",
    ),
    'Anneau des Éléments': (
        "Quatre incrustations changent d’éclat au rythme du feu, de l’eau, de la terre et de l’air.",
        "Artefact ancestral durable · acquisition validée par la fondatrice, non revendable. Une activation donne trois tours de RP de maîtrise temporaire ; définir les manifestations autorisées avant la scène.",
        "Les pouvoirs innés ne peuvent pas être employés simultanément. Ne donne aucune maîtrise permanente, ne dispense pas de prudence et ne permet pas de manipuler le corps d’autrui. La fréquence des activations est fixée lors de la validation.",
    ),
}


def enrich_catalogue(content):
    found = []

    def enrich_row(match):
        row = match.group(0)
        cells = list(re.finditer(r'<td\b[^>]*>(.*?)</td>', row, re.S | re.I))
        if len(cells) != 3:
            return row
        name = unescape(strip_tags(cells[0].group(1))).strip()
        if name not in ITEM_DETAILS:
            return row
        found.append(name)
        if 'data-shop-details' in row:
            return row
        atmosphere, usage, limits = ITEM_DETAILS[name]
        extra = (
            '<details data-shop-details="1" style="margin-top:.7rem;">'
            '<summary style="cursor:pointer;color:#c4b5fd;font-weight:600;">Description &amp; utilisation en RP</summary>'
            '<div style="margin-top:.6rem;line-height:1.7;">'
            f'<p style="margin:0 0 .6rem;font-style:italic;">{escape(atmosphere)}</p>'
            f'<p style="margin:0 0 .6rem;"><strong>Utilisation :</strong> {escape(usage)}</p>'
            f'<p style="margin:0;"><strong>Limites :</strong> {escape(limits)}</p>'
            '</div></details>'
        )
        cell = cells[1]
        return row[:cell.end(1)] + extra + row[cell.end(1):]

    result = re.sub(r'<tr\b[^>]*>.*?</tr>', enrich_row, content, flags=re.S | re.I)
    return result, found
