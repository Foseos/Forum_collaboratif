"""Propositions de kinésies pour le bottin, sans attribution à une espèce."""

KINETIC_POWER_SECTIONS = (
    (
        "XXIV", "Ciel et phénomènes", "rgba(125,211,252,0.32)", (
            (
                "Pluviokinésie",
                "Guide une pluie déjà présente ou condense une faible averse locale. Ne déclenche pas un orage complet.",
                ("Rideau de pluie", "Averse dirigée ★"),
                (
                    "Épaissit la pluie sur un passage étroit pour gêner la vue sans piéger une cible.",
                    "Concentre une averse brève sur une petite zone avec humidité disponible.",
                ),
            ),
            (
                "Barokinésie",
                "Modifie la pression de l'air dans un espace limité. Une évolution peut priver brièvement une cible d'oxygène.",
                ("Poussée barométrique", "Zone de pression ★", "Privation d'oxygène ★"),
                (
                    "Produit une poussée d'air par différence de pression, avec une portée courte.",
                    "Stabilise une variation modérée de pression dans une zone définie.",
                    "Réduit l'oxygène autour d'une cible pendant un instant. L'effet et sa durée sont validés par le staff et joués avec l'accord de la cible, sans perte de connaissance ni séquelle imposée.",
                ),
            ),
            (
                "Thermokinésie",
                "Réchauffe ou refroidit modérément une surface ou l'air proche, sans créer flammes ni glace.",
                ("Gradient thermique", "Zone tempérée ★"),
                (
                    "Crée une différence de température entre deux petites surfaces.",
                    "Maintient une température modérée dans un périmètre restreint.",
                ),
            ),
            (
                "Sonokinésie",
                "Amplifie, atténue ou dévie des sons existants. Elle se distingue d'un cri surnaturel émis par la voix.",
                ("Écho dirigé", "Silence sélectif ★"),
                (
                    "Redirige un son identifiable vers un point proche sans inventer sa source.",
                    "Atténue une source sonore choisie, sans supprimer toutes les vibrations.",
                ),
            ),
            (
                "Vibrakinésie",
                "Anime légèrement les vibrations d'un objet solide touché ou proche, sans le détruire automatiquement.",
                ("Résonance ciblée", "Onde vibratoire ★"),
                (
                    "Fait vibrer un matériau précis pour émettre un signal ou en tester la structure.",
                    "Étend une vibration faible à plusieurs objets proches, sans rupture imposée.",
                ),
            ),
        ),
    ),
    (
        "XXV", "Terre, feu et résidus", "rgba(251,146,60,0.32)", (
            (
                "Arénokinésie",
                "Déplace et modèle du sable déjà présent. Les grains ne deviennent ni verre ni pierre sans autre pouvoir.",
                ("Voile de sable", "Forme sableuse ★"),
                (
                    "Soulève un rideau de sable qui gêne la vue mais peut être dispersé.",
                    "Donne au sable une forme temporaire de petite taille, sans solidité parfaite.",
                ),
            ),
            (
                "Cinerokinésie",
                "Dirige des cendres déjà produites, sans créer de feu ni brûler une cible.",
                ("Nuage de cendres", "Traces cendrées"),
                (
                    "Soulève une petite quantité de cendres pour masquer brièvement un passage.",
                    "Rassemble les cendres en marques lisibles ou en piste visible.",
                ),
            ),
            (
                "Magmakinésie",
                "Influe sur une petite quantité de roche en fusion déjà disponible dans une scène adaptée. Chaleur et dégâts restent encadrés.",
                ("Croûte refroidie ★", "Courant magmatique ★"),
                (
                    "Accélère le refroidissement d'une faible quantité de lave pour créer une croûte fragile.",
                    "Guide un court écoulement existant sans provoquer d'éruption.",
                ),
            ),
            (
                "Sismokinésie",
                "Émet de faibles secousses locales dans un sol continu. Aucun séisme majeur ni effondrement automatique.",
                ("Onde tellurique ★", "Fissure superficielle ★"),
                (
                    "Propage une vibration courte dans le sol pour déséquilibrer sans blessure garantie.",
                    "Ouvre une fissure peu profonde dans un terrain compatible, avec accord pour les dégâts.",
                ),
            ),
            (
                "Fumokinésie",
                "Déplace une fumée déjà présente. Elle ne produit pas de combustion et ne transforme pas la fumée en poison.",
                ("Écran de fumée", "Courant de fumée ★"),
                (
                    "Épaissit un voile de fumée disponible pour réduire la visibilité.",
                    "Guide la fumée hors d'une zone ou vers une ouverture sur une courte distance.",
                ),
            ),
        ),
    ),
    (
        "XXVI", "Lumière, ombres et énergie", "rgba(196,181,253,0.34)", (
            (
                "Photokinésie",
                "Module une lumière existante pour l'intensifier, l'adoucir ou la diriger, sans télékinésie sur la matière.",
                ("Halo dirigé", "Éblouissement contrôlé ★"),
                (
                    "Concentre une source lumineuse en halo mobile de petite taille.",
                    "Produit un éclat bref dont la cible peut détourner les yeux ou se protéger.",
                ),
            ),
            (
                "Umbrakinésie",
                "Épaissit et façonne les ombres présentes. L'ombre ne devient pas automatiquement un objet solide.",
                ("Voile d'ombre", "Forme ombreuse ★"),
                (
                    "Étend une zone d'ombre pour faciliter une dissimulation imparfaite.",
                    "Donne à une ombre une forme visible et passagère, sans prise physique garantie.",
                ),
            ),
            (
                "Énergokinésie",
                "Canalise une petite quantité d'énergie magique disponible. Ne copie, ne vole ni n'annule les dons d'autrui.",
                ("Flux stabilisé ★", "Impulsion énergétique ★"),
                (
                    "Stabilise brièvement un flux d'énergie déjà maîtrisé dans la fiche.",
                    "Libère une faible poussée d'énergie dont l'impact se joue avec la cible.",
                ),
            ),
        ),
    ),
    (
        "XXVII", "Matières et matériaux", "rgba(148,163,184,0.34)", (
            (
                "Métallokinésie",
                "Façonne un petit objet métallique disponible, même non magnétique. Ne crée pas de métal et se distingue de la magnétokinésie.",
                ("Fil métallique", "Armure souple ★"),
                (
                    "Étire le métal disponible en fil court sans le rendre incassable.",
                    "Dispose du métal présent en protection limitée dont le poids reste à porter.",
                ),
            ),
            (
                "Vitrokinésie",
                "Déplace ou modèle du verre déjà présent. Les éclats restent dangereux et aucune blessure n'est imposée.",
                ("Mosaïque mobile", "Écran de verre ★"),
                (
                    "Assemble de petits fragments en motif mobile sans les transformer en cristal.",
                    "Place un panneau de verre fragile comme obstacle temporaire.",
                ),
            ),
            (
                "Lignokinésie",
                "Façonne du bois mort ou travaillé déjà présent, sans commander les plantes vivantes de la phytokinésie.",
                ("Raccommodage du bois", "Barrière ligneuse ★"),
                (
                    "Réassemble brièvement des fragments de bois compatibles.",
                    "Dresse un obstacle à partir de bois disponible, avec une résistance limitée.",
                ),
            ),
            (
                "Encrekinésie",
                "Déplace de l'encre liquide ou sèche sur un support visible. Ne lit pas automatiquement les textes cachés.",
                ("Message mouvant", "Encre dissimulée ★"),
                (
                    "Fait se déplacer des mots déjà écrits sur une page proche.",
                    "Cache temporairement un message encré sans le rendre indéchiffrable à toute magie.",
                ),
            ),
            (
                "Halokinésie",
                "Déplace et façonne du sel déjà présent, y compris dissous dans l'eau, en quantité limitée.",
                ("Extraction saline", "Brume de sel ★", "Rempart cristallin ★"),
                (
                    "Sépare une petite quantité de sel de l'eau et la rassemble sous forme de grains.",
                    "Disperse le sel en fine brume qui gêne brièvement la vue ou irrite légèrement, sans blessure durable.",
                    "Assemble les grains en une paroi de cristaux fragile qui ralentit un passage ou amortit un choc.",
                ),
            ),
            (
                "Fibrokinésie",
                "Crée une quantité limitée de fibres, fils ou tissu, puis peut les animer et les façonner. La matière créée reste fragile et ne contrôle pas le corps d'une personne vêtue.",
                ("Tissage mobile", "Filet de fibres ★", "Étoffe persistante ★"),
                (
                    "Tisse et déplace les fibres créées pour former un motif ou réparer une petite déchirure.",
                    "Crée puis tend un filet léger dont une cible peut se dégager.",
                    "Maintient une étoffe créée pendant une durée plus longue, avec une taille validée.",
                ),
            ),
        ),
    ),
    (
        "XXVIII", "Nature et corps", "rgba(74,222,128,0.30)", (
            (
                "Mycokinésie",
                "Guide des champignons déjà présents et peut produire une petite quantité de spores. Leur effet, portée et durée sont définis dans la fiche ; aucune maladie réelle n'est transmise.",
                ("Réseau fongique", "Voile de spores ★", "Spores à effet ciblé ★"),
                (
                    "Étend un réseau de filaments sur une surface compatible pour transmettre un signal.",
                    "Produit et diffuse un nuage de spores dans une petite zone, avec une durée définie.",
                    "Donne aux spores un effet temporaire validé, comme une irritation, une somnolence ou un marquage visible, sans imposer la réaction d'une cible.",
                ),
            ),
            (
                "Ostéokinésie",
                "Façonne des os déjà détachés ou agit sur son propre squelette selon sa fiche. Aucun os d'autrui n'est altéré sans accord.",
                ("Armature osseuse ★", "Façonnage d'ossements ★"),
                (
                    "Renforce brièvement un appui osseux personnel sans annuler les blessures.",
                    "Assemble de petits ossements disponibles en structure fragile.",
                ),
            ),
            (
                "Biokinésie",
                "Influe modestement sur un tissu vivant du personnage ou d'une cible consentante. Ne remplace ni la guérison ni une transformation totale.",
                ("Réparation ciblée ★", "Adaptation organique ★"),
                (
                    "Soutient la réparation d'une petite atteinte avec fatigue et limites validées.",
                    "Adapte brièvement une fonction corporelle précise sans mutation permanente.",
                ),
            ),
            (
                "Myokinésie",
                "Module l'effort de ses propres muscles pendant un court moment. N'accorde pas le contrôle des mouvements d'autrui.",
                ("Précision musculaire", "Effort renforcé ★"),
                (
                    "Affermit un geste fin ou un équilibre au prix d'une concentration accrue.",
                    "Soutient un effort bref plus important, suivi d'une fatigue à jouer.",
                ),
            ),
            (
                "Neurokinésie",
                "Influence légèrement une sensation nerveuse chez soi ou une cible consentante. Ne commande ni les pensées ni les actes.",
                ("Signal apaisé ★", "Perception affinée ★"),
                (
                    "Atténue temporairement un signal sensoriel défini sans soigner sa cause.",
                    "Renforce brièvement un sens choisi avec un risque de surcharge sensorielle.",
                ),
            ),
            (
                "Toxikinésie",
                "Déplace ou neutralise une faible quantité de toxine fictive déjà présente. N'invente ni maladie réelle ni effet mortel automatique.",
                ("Extraction ciblée ★", "Confinement toxique ★"),
                (
                    "Retire une petite quantité d'une substance identifiée avec accord des joueurs concernés.",
                    "Contient provisoirement une toxine fictive dans un récipient adapté.",
                ),
            ),
        ),
    ),
    (
        "XXIX", "Esprit et sensations", "rgba(244,114,182,0.30)", (
            (
                "Mnémokinésie",
                "Agit sur l'accès temporaire à un souvenir défini avec le joueur concerné. Ne réécrit ni n'efface durablement le passé.",
                ("Rappel partagé ★", "Voile mnésique ★"),
                (
                    "Aide une personne consentante à faire remonter un fragment de souvenir choisi.",
                    "Rend un souvenir précis plus difficile à rappeler pendant une scène convenue.",
                ),
            ),
            (
                "Onirokinésie",
                "Modèle son propre rêve ou celui d'une personne endormie et consentante. Ne force pas l'endormissement.",
                ("Rêve partagé ★", "Décor onirique ★"),
                (
                    "Relie deux rêveurs volontaires dans un même rêve temporaire.",
                    "Façonne un lieu de rêve sans imposer les actes de ses visiteurs.",
                ),
            ),
            (
                "Émotionkinésie",
                "Amplifie ou atténue brièvement une émotion déjà présente. La naissance de sentiments amoureux relève du pouvoir distinct de manipulation des sentiments.",
                ("Émotion partagée ★", "Équilibre affectif ★"),
                (
                    "Fait ressentir une émotion présente à un allié consentant sans en transmettre la cause.",
                    "Aide une personne réceptive à tempérer plusieurs émotions mêlées pour un court moment.",
                ),
            ),
        ),
    ),
    (
        "XXX", "Machines et poussière", "rgba(250,204,21,0.28)", (
            (
                "Technokinésie",
                "Influence une fonction simple d'un appareil proche. Ne donne pas accès à tous les systèmes ni à leurs données privées.",
                ("Interface intuitive", "Réseau local ★"),
                (
                    "Comprend et déclenche une commande simple d'un appareil compatible à portée.",
                    "Coordonne brièvement plusieurs appareils accessibles dans un même lieu.",
                ),
            ),
            (
                "Poussiérokinésie",
                "Rassemble et déplace la poussière ordinaire existante. Elle reste distincte de la poussière de fée enchantée.",
                ("Nuage de poussière", "Traces révélées"),
                (
                    "Soulève un léger nuage qui gêne la vue sans étouffer une cible.",
                    "Fait suivre à la poussière une empreinte récente sur une surface proche.",
                ),
            ),
        ),
    ),
)
