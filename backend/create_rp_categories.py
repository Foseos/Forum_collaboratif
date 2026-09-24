"""
Script de création de toutes les catégories RP manquantes.
Exécuter avec : docker-compose exec backend python manage.py shell < create_rp_categories.py
"""
from apps.forum.models import Category

def create(slug, name, description, order):
    obj, created = Category.objects.get_or_create(
        slug=slug,
        defaults={'name': name, 'description': description, 'order': order}
    )
    status = 'créée' if created else 'déjà existante'
    print(f"  [{status}] {slug}")
    return obj

print("\n=== Catégories parentes SF & lieux magiques ===")
create('san-francisco',              'San Francisco',                           'La ville magique, terrain de jeu de toutes les créatures', 10)
create('rues-commercantes',          'Rues commerçantes',                       'Boutiques, bars et lieux animés du quartier commercial',    11)
create('centre-ville',               'Centre ville',                            'Le cœur battant de San Francisco',                         12)
create('civic-center',               'Civic Center',                            'Les institutions de la ville : mairie, tribunal…',         13)
create('quartier-culturel-et-enseignement', 'Quartier culturel et d\'enseignement', 'Écoles, universités et musées',                        14)
create('quartier-des-affaires',      'Quartier des affaires',                   'Presse, droit et archives de la ville',                    15)
create('fishermans-wharf',           'Fisherman\'s Wharf',                      'Le quai animé et ses secrets',                             16)
create('presidio-of-san-francisco',  'Presidio of San Francisco',               'Parc et pont emblématique, entre deux mondes',             17)
create('glen-park',                  'Glen Park',                               'Parcs, forêts et espaces verts',                           18)
create('ocean-beach',                'Ocean Beach',                             'La plage du Pacifique et ses environs',                    19)
create('cimetiere',                  'Cimetière',                               'Cryptes, mausolées et cathédrale',                         20)
create('quartiers-residentiels',     'Quartiers résidentiels',                  'Les quartiers où vivent les habitants de San Francisco',    21)
create('ecole-de-magie',             'L\'école de magie',                       'Institution magique pour les apprentis sorciers',          22)
create('les-enfers',                 'Les Enfers',                              'Repaires démoniaques et couloirs infernaux',                23)
create('dimensions-alternatives',    'Dimensions alternatives',                 'Mondes parallèles et réalités miroir',                     24)
create('les-cieux',                  'Les Cieux',                               'Domaines célestes des forces du Bien',                     25)
create('continents',                 'Continents',                              'Aventures hors des frontières de San Francisco',           26)

print("\n=== Rues commerçantes ===")
create('salle-arcade',     'Salle d\'arcade',     'Jeux et compétitions dans les salles obscures du centre',    110)
create('tattoo-shop',      'Tattoo shop',          'Encres magiques et marques indélébiles',                     111)
create('p3',               'P3',                   'Le club de Piper Halliwell, haut lieu de la nuit',           112)
create('herboristerie',    'Herboristerie',        'Plantes rares, remèdes magiques et secrets de la nature',   113)
create('pepper-place',     'Pepper Place',         'Épicerie fine et point de rencontre discret',                114)
create('discotheque',      'Discothèque',          'Piste de danse, lumières tamisées et nuits sans fin',        115)
create('bowling',          'Bowling',              'Soirées détente entre amis, humains ou non',                 116)
create('hotel',            'Hôtel',                'Résidence de passage pour voyageurs et créatures',           117)

print("\n=== Centre ville ===")
create('le-quake',          'Le Quake',         'Bar musical emblématique du centre-ville',                      120)
create('salon-de-the',      'Salon de thé',     'Un havre de paix pour les discussions inattendues',            121)
create('bars',              'Bars',             'Les différents bars animés du centre-ville',                    122)
create('centre-commercial', 'Centre commercial','Shopping et intrigues entre les boutiques',                     123)
create('salle-omnisport',   'Salle omnisport',  'Complexe sportif ouvert à tous',                               124)

print("\n=== Civic Center ===")
create('hotel-de-ville', 'Hôtel de ville', 'Le siège du pouvoir municipal',                                          130)
create('tribunal',       'Tribunal',        'Salle d\'audience pour mortels et créatures',                            131)
create('hopital',        'Hôpital',         'Urgences, soins et secrets médicaux au cœur de San Francisco',          132)

print("\n=== Quartier culturel ===")
create('creche',          'Crèche',           'Les nourrissons et leurs premiers instants magiques',  139)
create('ecole-maternelle', 'École maternelle', 'Les tout-petits, entre magie et innocence',           140)
create('ecole-primaire',   'École primaire',   'Les premiers apprentissages, humains et magiques',    141)
create('lycee',            'Lycée',            'Couloirs et secrets d\'adolescents pas ordinaires',   142)
create('universite',       'Université',       'Amphithéâtres où savoir et pouvoir se croisent',      143)
create('musee',            'Musée',            'Artefacts anciens et reliques magiques exposés',       144)

print("\n=== Quartier des affaires ===")
create('bay-mirror',      'Bay Mirror',          'Le grand quotidien de San Francisco',                 150)
create('cabinet-avocats', 'Cabinet d\'avocats',  'Droit des mortels et des créatures',                 151)
create('mediatheque',     'Médiathèque',         'Archives publiques et grimoires sous licence',        152)
create('centre-archives', 'Centre des archives', 'Registres officiels et dossiers scellés',            153)

print("\n=== Fisherman's Wharf ===")
create('agence-de-tourisme',    'Agence de tourisme',    'Excursions et circuits secrets',              160)
create('boutiques-de-souvenirs','Boutiques de souvenirs','Objets enchantés et curiosités',              161)
create('chocolaterie',          'Chocolaterie',          'Douceurs artisanales et effluves sucrés',     162)

print("\n=== Presidio ===")
create('golden-gate-bridge', 'Golden Gate Bridge', 'Le pont mythique, passage entre deux mondes',      170)
create('collines',           'Collines',           'Les hauteurs sauvages du Presidio',                 171)
create('prison-alcatraz',    'Prison d\'Alcatraz', 'L\'île-prison hantée par ses anciens détenus',     172)

print("\n=== Glen Park ===")
create('glen-canyon-park',      'Glen Canyon Park',      'Le grand parc naturel de San Francisco',      180)
create('sentiers-de-randonnee', 'Sentiers de randonnée', 'Chemins boisés entre le mortel et le magique',181)
create('serre-botanique',       'Serre botanique',       'Plantes rares et herbes magiques sous verre', 182)
create('stade',                 'Stade',                 'Compétitions où mortels et créatures se mesurent',183)

print("\n=== Ocean Beach ===")
create('zoo',                   'Zoo',                   'Animaux sauvages et créatures magiques',      190)
create('plage',                 'Plage',                 'Le sable d\'Ocean Beach et ses secrets',       191)
create('institut-de-beaute',    'Institut de beauté',    'Soins et transformations',                     192)
create('caserne-des-pompiers',  'Caserne des pompiers',  'Les héros du feu, humains ou non',            193)
create('commissariat-de-police','Commissariat de police','Enquêtes qui dépassent le cadre mortel',       194)

print("\n=== Cimetière ===")
create('mausolee',   'Mausolée',   'Sépultures gardées par des ombres anciennes',            200)
create('crypte',     'Crypte',     'Galeries souterraines où les morts parlent',              201)
create('cathedrale', 'Cathédrale', 'Lieu de culte où sacré et obscur se disputent',          202)

print("\n=== Quartiers résidentiels ===")
create('prescott-street',  'Prescott Street',  'La rue emblématique du Nexus Arcana',  210)
create('tenderloin',       'Tenderloin',        'Quartier populaire aux ruelles animées',        211)
create('bayview-hunters',  'Bayview-Hunters',   'Quartier industriel en bord de baie',          212)
create('noe-valley',       'Noe Valley',        'Quartier résidentiel aux maisons victoriennes', 213)
create('presidio-heights', 'Presidio Heights',  'Quartier huppé surplombant la baie',           214)
create('bayview',          'Bayview',           'Entre passé industriel et renouveau',          215)

print("\n=== École de magie ===")
create('garderie',           'Garderie',            'Les tout-petits initiés à la magie',               220)
create('salles-de-cours',    'Salles de cours',     'Sorts, théories et pratiques magiques',            221)
create('bibliotheque',       'Bibliothèque',        'Grimoires anciens et savoirs interdits',           222)
create('cour-exterieure',    'Cour extérieure',     'Entraînement et duels improvisés',                 223)
create('dortoir',            'Dortoir',             'Chambres des élèves résidents',                    224)
create('salle-des-professeurs','Salle des professeurs','Intrigues du corps pédagogique',                225)

print("\n=== Les Enfers ===")
create('repaire-source-du-mal',          'Repaire de la Source du Mal',         'Le cœur ténébreux de toute magie noire',         230)
create('ecole-magie-noire',              'École de magie noire',                'Institution démoniaque aux arts obscurs',         231)
create('les-souterrains',                'Les Souterrains',                     'Galeries infernales et passages secrets',         232)
create('repaire-triade',                 'Repaire de la Triade',                'QG de la Triade du Mal',                         233)
create('repaire-conclave-abime',         'Repaire du Conclave de l\'Abîme',     'Sanctuaire du Conclave démoniaque',              234)
create('repaire-cavaliers-apocalypse',   'Repaire des Cavaliers de l\'Apocalypse','Domaine des quatre Cavaliers',                 235)
create('le-tartare',                     'Le Tartare',                          'Prison éternelle des démons condamnés',          236)

print("\n=== Dimensions alternatives ===")
create('monde-des-contes', 'Monde des contes', 'Univers enchanté où les personnages de contes prennent vie', 240)
create('monde-miroir',     'Monde miroir',     'Le reflet inversé de notre réalité',                          241)

print("\n=== Les Cieux ===")
create('repaire-des-fondateurs',           'Repaire des Fondateurs',            'Sanctuaire céleste des puissances fondatrices',  250)
create('repaire-des-gardiens-des-sceaux',  'Repaire des Gardiens des Sceaux',   'Domaine des gardiens des sceaux sacrés',         251)
create('repaire-des-veilleurs-de-laube',   'Repaire des Veilleurs de l\'Aube',  'Refuge des veilleurs entre nuit et lumière',     252)

print("\n=== Continents ===")
create('europe',          'Europe',          'Vieilles cités chargées d\'histoire et de magie millénaire',  260)
create('asie',            'Asie',            'Sagesse et mystères, arts martiaux et esprits ancestraux',    261)
create('afrique',         'Afrique',         'Berceau de la magie ancestrale et rituels séculaires',       262)
create('amerique-du-sud', 'Amérique du Sud', 'Forêts amazoniennes mystiques et magie chamanique',          263)
create('oceanie',         'Océanie',         'Archipels isolés gardant les secrets d\'une magie océanique',264)
create('antarctique',     'Antarctique',     'Glaces éternelles où se cachent des puissances oubliées',    265)

print("\n=== Catégories manquantes (questions) ===")
create('questions-membres', 'Questions membres',  'Vous êtes membre ? Posez vos questions à l\'équipe', 301)
create('signaler-absence',  'Signaler une absence','Prévenez l\'équipe de votre absence ou retour',      302)

total = Category.objects.count()
print(f"\n✅ Terminé — {total} catégories au total en base de données.")
