"""Propositions de kinésies pour le bottin, sans attribution à une espèce."""

KINETIC_POWER_SECTIONS = (
    (
        "XXIV", "Ciel et phénomènes", "rgba(125,211,252,0.32)", (
            (
                "Pluviokinésie",
                "Crée une faible pluie locale ou guide une averse existante. Ne déclenche pas un orage complet.",
                ("Rideau de pluie", "Averse dirigée ★"),
                (
                    "Épaissit la pluie sur un passage étroit pour gêner la vue sans piéger une cible.",
                    "Concentre une averse brève sur une petite zone, même sans pluie préalable.",
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
                "Amplifie, atténue ou dévie des sons et peut émettre des ondes sonores à une fréquence choisie. Elle se distingue d'un cri surnaturel émis par la voix.",
                ("Écho dirigé", "Silence sélectif ★", "Onde de fréquence ★"),
                (
                    "Redirige un son identifiable vers un point proche sans inventer sa source.",
                    "Atténue une source sonore choisie, sans supprimer toutes les vibrations.",
                    "Projette une onde vibratoire dont la fréquence peut dévier de petits objets ou repousser brièvement une personne proche. Sa portée et son intensité sont validées par le staff ; la réaction d'un personnage se joue avec son accord.",
                ),
            ),
            (
                "Vibrakinésie",
                "Crée de faibles vibrations et peut les transmettre à un objet solide proche, sans le détruire automatiquement.",
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
                "Crée une petite quantité de sable ou modèle celui qui est présent. Une évolution permet de soulever une tempête locale ; les grains ne deviennent ni verre ni pierre sans autre pouvoir.",
                ("Voile de sable", "Forme sableuse ★", "Tempête de sable ★"),
                (
                    "Soulève un rideau de sable qui gêne la vue mais peut être dispersé.",
                    "Donne au sable une forme temporaire de petite taille, sans solidité parfaite.",
                    "Crée ou rassemble assez de sable pour soulever une tempête dans une zone limitée. Sa durée et son intensité sont validées par le staff ; elle peut gêner la vue et les déplacements sans piéger ni blesser automatiquement une cible.",
                ),
            ),
            (
                "Cinerokinésie",
                "Crée une petite quantité de cendres ou dirige celles qui sont présentes, sans créer de feu ni brûler une cible.",
                ("Nuage de cendres", "Traces cendrées"),
                (
                    "Soulève une petite quantité de cendres pour masquer brièvement un passage.",
                    "Rassemble les cendres en marques lisibles ou en piste visible.",
                ),
            ),
            (
                "Magmakinésie",
                "Crée une faible quantité de magma ou influe sur une coulée existante. Sa chaleur et ses dégâts restent encadrés.",
                ("Croûte refroidie ★", "Courant magmatique ★"),
                (
                    "Accélère le refroidissement d'une faible quantité de lave pour créer une croûte fragile.",
                    "Guide un court écoulement créé ou existant sans provoquer d'éruption.",
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
                "Courant de limon",
                "Crée une petite quantité de boue ou déplace celle qui est présente. Elle ne peut engloutir ni immobiliser automatiquement un personnage.",
                ("Bourbier local ★", "Rempart de limon ★"),
                (
                    "Étend une zone boueuse qui ralentit les déplacements sans piéger une cible contre son gré.",
                    "Dresse une masse de boue compacte pour amortir un choc, avec une résistance limitée.",
                ),
            ),
            (
                "Fumokinésie",
                "Crée un peu de fumée ou déplace celle qui est présente. Elle ne produit pas de combustion et ne devient pas un poison.",
                ("Écran de fumée", "Courant de fumée ★"),
                (
                    "Forme ou épaissit un voile de fumée pour réduire la visibilité.",
                    "Guide la fumée hors d'une zone ou vers une ouverture sur une courte distance.",
                ),
            ),
            (
                "Acidokinésie",
                "Crée une petite quantité d'acide fictif ou guide celui qui est présent. Sa corrosion et sa durée restent limitées ; il n'impose aucune blessure à un personnage.",
                ("Gouttes corrosives", "Jet acide ★", "Neutralisation acide ★"),
                (
                    "Dépose quelques gouttes pour attaquer lentement une petite surface non protégée.",
                    "Projette un bref jet sur une cible proche ; tout dégât sur un personnage ou un objet lui appartenant se joue avec son accord.",
                    "Dissipe ou neutralise une faible quantité d'acide créé ou déjà présent, sans annuler toutes les substances dangereuses.",
                ),
            ),
        ),
    ),
    (
        "XXVI", "Lumière, ombres et énergie", "rgba(196,181,253,0.34)", (
            (
                "Photokinésie",
                "Crée une lumière limitée ou module celle qui existe pour l'intensifier, l'adoucir ou la diriger, sans télékinésie sur la matière.",
                ("Halo dirigé", "Éblouissement contrôlé ★", "Lumière recueillie ★"),
                (
                    "Crée ou concentre un halo lumineux mobile de petite taille.",
                    "Produit un éclat bref dont la cible peut détourner les yeux ou se protéger.",
                    "Absorbe brièvement une partie de la lumière d'une petite zone pour la restituer ensuite, sans plonger automatiquement tout un lieu dans le noir.",
                ),
            ),
            (
                "Umbrakinésie",
                "Crée une zone d'ombre ou façonne les ombres présentes. L'ombre ne devient pas automatiquement un objet solide.",
                ("Voile d'ombre", "Forme ombreuse ★"),
                (
                    "Étend une zone d'ombre pour faciliter une dissimulation imparfaite.",
                    "Donne à une ombre une forme visible et passagère, sans prise physique garantie.",
                ),
            ),
            (
                "Énergokinésie",
                "Génère et canalise une petite quantité d'énergie magique. Ne copie, ne vole ni n'annule les dons d'autrui.",
                ("Flux stabilisé ★", "Impulsion énergétique ★"),
                (
                    "Stabilise brièvement un flux d'énergie créé ou déjà maîtrisé dans la fiche.",
                    "Libère une faible poussée d'énergie dont l'impact se joue avec la cible.",
                ),
            ),
        ),
    ),
    (
        "XXVII", "Matières et matériaux", "rgba(148,163,184,0.34)", (
            (
                "Métallokinésie",
                "Crée une petite quantité de métal ou façonne un objet métallique, même non magnétique. Se distingue de la magnétokinésie.",
                ("Fil métallique", "Armure souple ★"),
                (
                    "Crée ou étire du métal en fil court sans le rendre incassable.",
                    "Façonne du métal créé ou présent en protection limitée dont le poids reste à porter.",
                ),
            ),
            (
                "Vitrokinésie",
                "Crée une petite quantité de verre ou modèle celui qui est présent. Les éclats restent dangereux et aucune blessure n'est imposée.",
                ("Mosaïque mobile", "Écran de verre ★"),
                (
                    "Crée ou assemble de petits fragments en motif mobile sans les transformer en cristal.",
                    "Place un panneau de verre fragile comme obstacle temporaire.",
                ),
            ),
            (
                "Lignokinésie",
                "Crée une petite quantité de bois ou façonne du bois mort ou travaillé, sans commander les plantes vivantes de la phytokinésie.",
                ("Raccommodage du bois", "Barrière ligneuse ★"),
                (
                    "Réassemble brièvement des fragments de bois compatibles.",
                    "Dresse un obstacle avec du bois créé ou présent, avec une résistance limitée.",
                ),
            ),
            (
                "Encrekinésie",
                "Crée un peu d'encre ou déplace celle d'un support visible. Ne lit pas automatiquement les textes cachés.",
                ("Message mouvant", "Encre dissimulée ★"),
                (
                    "Fait se déplacer des mots déjà écrits sur une page proche.",
                    "Cache temporairement un message encré sans le rendre indéchiffrable à toute magie.",
                ),
            ),
            (
                "Halokinésie",
                "Crée une petite quantité de sel ou façonne celui qui est présent, y compris dissous dans l'eau.",
                ("Extraction saline", "Brume de sel ★", "Rempart cristallin ★"),
                (
                    "Sépare une petite quantité de sel de l'eau et la rassemble sous forme de grains, sans dépendre de cette source pour en créer.",
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
                "Fait apparaître quelques champignons ou spores, et guide ceux qui sont présents. Leur effet, portée et durée sont définis dans la fiche ; aucune maladie réelle n'est transmise.",
                ("Réseau fongique", "Voile de spores ★", "Spores à effet ciblé ★"),
                (
                    "Crée et étend un réseau de filaments sur une surface compatible pour transmettre un signal.",
                    "Produit et diffuse un nuage de spores dans une petite zone, avec une durée définie.",
                    "Donne aux spores un effet temporaire validé, comme une irritation, une somnolence ou un marquage visible, sans imposer la réaction d'une cible.",
                ),
            ),
            (
                "Ostéokinésie",
                "Crée une petite quantité de matière osseuse, façonne des os détachés ou agit sur son propre squelette selon sa fiche. Aucun os d'autrui n'est altéré sans accord.",
                ("Armature osseuse ★", "Façonnage d'ossements ★"),
                (
                    "Renforce brièvement un appui osseux personnel sans annuler les blessures.",
                    "Crée ou assemble de petits ossements en une structure fragile.",
                ),
            ),
            (
                "Biokinésie",
                "Génère une petite quantité de tissu vivant ou influe modestement sur celui du personnage ou d'une cible consentante. Ne crée pas d'être vivant et ne remplace ni la guérison ni une transformation totale.",
                ("Réparation ciblée ★", "Adaptation organique ★"),
                (
                    "Soutient la réparation d'une petite atteinte avec fatigue et limites validées.",
                    "Adapte brièvement une fonction corporelle précise sans mutation permanente.",
                ),
            ),
            (
                "Myokinésie",
                "Génère une brève impulsion musculaire et module l'effort de ses propres muscles. Ne crée pas de nouveaux muscles et ne contrôle pas les mouvements d'autrui.",
                ("Précision musculaire", "Effort renforcé ★"),
                (
                    "Affermit un geste fin ou un équilibre au prix d'une concentration accrue.",
                    "Soutient un effort bref plus important, suivi d'une fatigue à jouer.",
                ),
            ),
            (
                "Neurokinésie",
                "Crée ou module légèrement une sensation nerveuse chez soi ou une cible consentante. Ne commande ni les pensées ni les actes.",
                ("Signal apaisé ★", "Perception affinée ★"),
                (
                    "Atténue temporairement un signal sensoriel défini sans soigner sa cause.",
                    "Renforce brièvement un sens choisi avec un risque de surcharge sensorielle.",
                ),
            ),
            (
                "Toxikinésie",
                "Crée une faible quantité de toxine fictive ou déplace et neutralise celle qui est présente. N'invente ni maladie réelle ni effet mortel automatique.",
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
                "Crée un écho mnésique ou agit sur l'accès temporaire à un souvenir défini avec le joueur concerné. Ne crée pas de faux passé et n'efface rien durablement.",
                ("Rappel partagé ★", "Voile mnésique ★"),
                (
                    "Aide une personne consentante à faire remonter un fragment de souvenir choisi.",
                    "Rend un souvenir précis plus difficile à rappeler pendant une scène convenue.",
                ),
            ),
            (
                "Onirokinésie",
                "Crée et modèle un rêve chez soi ou chez une personne endormie et consentante. Ne force pas l'endormissement.",
                ("Rêve partagé ★", "Décor onirique ★"),
                (
                    "Relie deux rêveurs volontaires dans un même rêve temporaire.",
                    "Façonne un lieu de rêve sans imposer les actes de ses visiteurs.",
                ),
            ),
            (
                "Émotionkinésie",
                "Fait naître, amplifie ou atténue brièvement une émotion simple. La naissance de sentiments amoureux relève du pouvoir distinct de manipulation des sentiments.",
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
                "Génère une impulsion de commande ou influence une fonction simple d'un appareil proche. Ne crée pas d'appareil et ne donne pas accès à tous les systèmes ni à leurs données privées.",
                ("Interface intuitive", "Réseau local ★", "Silence des circuits ★"),
                (
                    "Comprend et déclenche une commande simple d'un appareil compatible à portée.",
                    "Coordonne brièvement plusieurs appareils accessibles dans un même lieu.",
                    "Émet une impulsion qui interrompt temporairement de petits appareils proches. N'efface aucune donnée et ne neutralise pas toutes les protections.",
                ),
            ),
            (
                "Poussiérokinésie",
                "Crée une petite quantité de poussière ordinaire ou déplace celle qui est présente. Elle reste distincte de la poussière de fée enchantée.",
                ("Nuage de poussière", "Traces révélées"),
                (
                    "Soulève un léger nuage qui gêne la vue sans étouffer une cible.",
                    "Fait suivre à la poussière une empreinte récente sur une surface proche.",
                ),
            ),
        ),
    ),
)
