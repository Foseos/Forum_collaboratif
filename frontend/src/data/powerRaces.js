// Possibilités de Nexus Arcana. Elles n'accordent aucun pouvoir automatiquement.
// Les sorciers TVD / The Originals / Legacies sont volontairement absents.
const R = {
  sorcier: 'Sorcières et sorciers Charmed',
  heretique: 'Hérétiques',
  demon: 'Démons',
  tenebres: 'Êtres des ténèbres',
  furies: 'Furies',
  lazare: 'Démons de Lazare',
  kazi: 'Démons Kazi',
  succubes: 'Succubes et incubes',
  prophetesses: 'Prophétesses démoniaques',
  lumiere: 'Êtres de lumière',
  fee: 'Fées',
  feeBois: 'Fées sylvestres',
  feeEau: 'Fées des eaux',
  feeLumiere: 'Fées lumineuses',
  feeNoire: 'Fées noires',
  elfe: 'Elfes',
  elfeBois: 'Elfes sylvains',
  elfeEau: 'Elfes des sources',
  elfeAstre: 'Elfes des astres',
  elfeNoir: 'Elfes noirs',
  nymphe: 'Nymphes et satyres',
  cupidon: 'Cupidons',
  valkyrie: 'Valkyries',
  muse: 'Muses',
  banshee: 'Banshees',
  sphinx: 'Sphinx',
  vampire: 'Vampires',
  phenix: 'Phénix',
  loup: 'Loups-garous',
  changeforme: 'Autres changeformes',
  kanima: 'Kanimas',
  hellhound: 'Chiens de l’enfer',
  kitsune: 'Kitsunes',
  kitsuneEau: 'Kitsunes de l’eau',
  kitsuneGlace: 'Kitsunes de la glace',
  kitsuneFeu: 'Kitsunes du feu',
  kitsuneTerre: 'Kitsunes de la terre',
  kitsuneAir: 'Kitsunes de l’air',
  kitsuneSon: 'Kitsunes soniques',
  kitsuneLumiere: 'Kitsunes de la lumière',
  kitsuneOmbre: 'Kitsunes de l’ombre',
  kitsunePlante: 'Kitsunes des plantes',
  kitsuneEsprit: 'Kitsunes de l’esprit',
  kitsuneSang: 'Kitsunes du sang',
  kitsuneTonnerre: 'Kitsunes du tonnerre',
  chimere: 'Chimères',
  sireneMarine: 'Sirènes et tritons marins',
  sirenePsychique: 'Sirènes psychiques de The Vampire Diaries',
}

const possibilities = new Map()
function add(names, races) {
  for (const name of names.trim().split('\n').map(value => value.trim()).filter(Boolean)) {
    const existing = possibilities.get(name) || new Set()
    races.forEach(race => existing.add(race))
    possibilities.set(name, existing)
  }
}

add(`Écho des fautes`, [R.furies])
add(`Mémoire des cendres`, [R.lazare])
add(`Pression crânienne`, [R.kazi])
add(`Lecture des désirs
Éveil de l'attirance`, [R.succubes])
add(`Marque de traque`, [R.tenebres])
add(`Présage de rupture`, [R.prophetesses])
add(`Soif révélatrice
Vitesse vampirique
Contrainte du regard`, [R.vampire])
add(`Transformation lupine
Instinct de meute
Pistage lupin`, [R.loup])
add(`Formule improvisée
Alchimie de terrain
Lien d'incantation`, [R.sorcier])

add(`Boules d'énergie
Télékinésie
Vague de force
Bouclier d'énergie
Voile cinétique
Gravikinésie
Énergokinésie
Flux emprunté`, [R.sorcier, R.demon, R.fee, R.elfe, R.lumiere, R.tenebres])

add(`Pyrokinésie
Combustion moléculaire
Combustion par le regard
Boules d'énergie
Immunité aux flammes
Magmakinésie`, [R.sorcier, R.demon, R.phenix, R.hellhound, R.kitsuneFeu])
add(`Foudre / Électrokinésie
Sillage fulgurant
Magnétokinésie`, [R.sorcier, R.demon, R.kitsuneTonnerre, R.phenix])
add(`Cryokinésie
Thermokinésie`, [R.sorcier, R.feeEau, R.elfeEau, R.kitsuneGlace])
add(`Cyclogenèse
Aérokinésie
Barokinésie
Pluviokinésie
Néphokinésie`, [R.sorcier, R.feeEau, R.elfeAstre, R.kitsuneAir, R.kitsuneEau, R.nymphe])
add(`Aquakinésie (contrôle de l'eau)
Bouclier aquatique
Fouet d'eau
Respiration aquatique
Voix des eaux
Corps de marée
Augure des marées`, [R.sorcier, R.feeEau, R.elfeEau, R.nymphe, R.kitsuneEau, R.sireneMarine])
add(`Géokinésie
Cristallokinésie
Arénokinésie
Sismokinésie
Courant de limon
Métallokinésie
Vitrokinésie
Halokinésie`, [R.sorcier, R.demon, R.kitsuneTerre, R.elfeBois, R.nymphe])
add(`Phytokinésie (contrôle végétal)
Lignokinésie
Mycokinésie
Augure des racines`, [R.sorcier, R.feeBois, R.elfeBois, R.nymphe, R.kitsunePlante])
add(`Photokinésie
Poussière lumineuse
Télékinésie lumineuse
Prisme de lumière
Glamour scintillant`, [R.sorcier, R.feeLumiere, R.elfeAstre, R.lumiere, R.kitsuneLumiere])
add(`Umbrakinésie
Arbalète d'ombre
Camouflage magique
Pas de brume`, [R.demon, R.tenebres, R.feeNoire, R.elfeNoir, R.kitsuneOmbre])
add(`Brumokinésie
Fumokinésie
Cinerokinésie
Poussiérokinésie`, [R.sorcier, R.demon, R.fee, R.kitsuneAir, R.phenix])
add(`Acidokinésie
Toxikinésie`, [R.sorcier, R.demon, R.kanima, R.chimere, R.hellhound])
add(`Hématokinésie
Ostéokinésie`, [R.sorcier, R.demon, R.feeNoire, R.elfeNoir, R.kitsuneSang])
add(`Sonokinésie
Vibrakinésie
Leurre acoustique
Cri perçant
Silence surnaturel
Écholocalisation`, [R.sorcier, R.demon, R.banshee, R.muse, R.kitsuneSon, R.sirenePsychique])
add(`Chant apaisant
Voix mimétique`, [R.sorcier, R.muse, R.fee, R.cupidon, R.sirenePsychique])
add(`Cri de Furie`, [R.furies])
add(`Hurlement de ralliement
Rugissement de garde`, [R.demon, R.banshee, R.valkyrie, R.loup, R.changeforme, R.hellhound])

add(`Décélération moléculaire
Éclat moléculaire
Souffle d'expansion
Rémanence moléculaire
Transmutation mineure
Animation d'objets
Fibrokinésie
Encrekinésie`, [R.sorcier, R.demon, R.fee, R.elfe, R.muse])
add(`Détection de magie
Précognition
Clairvoyance
Sens des présages
Lecture des intentions
Regards croisés
Écho des savoirs
Augure des nuées
Partage sensoriel`, [R.sorcier, R.fee, R.elfe, R.sphinx, R.muse, R.banshee, R.kitsuneEsprit])
add(`Voile de présence`, [R.sorcier, R.fee, R.elfe, R.vampire, R.kitsuneOmbre])
add(`Télépathie
Empathie
Empathie inversée
Perception des liens affectifs
Élan affectif
Rayonnement de joie
Chagrin partagé
Élan de courage
Accord des sens
Émotionkinésie`, [R.sorcier, R.cupidon, R.muse, R.fee, R.nymphe, R.sirenePsychique, R.kitsuneEsprit])
add(`Phobokinésie`, [R.sorcier, R.demon, R.sirenePsychique, R.kitsuneEsprit])
add(`Vertige de folie
Malaise surnaturel
Germe de discorde
Torture mentale`, [R.sorcier, R.demon, R.tenebres, R.sirenePsychique, R.kitsuneEsprit])
add(`Algokinésie`, [R.sorcier, R.demon, R.sirenePsychique, R.kitsuneEsprit])
add(`Suggestion mentale
Manipulation des sentiments
Illusion mentale
Onirokinésie
Chant envoûtant`, [R.sorcier, R.demon, R.fee, R.cupidon, R.muse, R.sirenePsychique, R.kitsuneEsprit])
add(`Illusion visuelle`, [R.sorcier, R.demon, R.fee, R.muse, R.sirenePsychique, R.kitsuneEsprit])
add(`Sommeil induit`, [R.sorcier, R.demon, R.fee, R.muse, R.sirenePsychique, R.kitsuneEsprit])
add(`Réminiscence
Mnémokinésie
Intuition des mensonges
Omnilinguisme`, [R.sorcier, R.sphinx, R.muse, R.elfe, R.sirenePsychique, R.kitsuneEsprit])
add(`Nécromancie
Projection astrale
Écho des savoirs`, [R.sorcier, R.demon, R.tenebres, R.sphinx, R.valkyrie, R.kitsuneEsprit])
add(`Égide de l'esprit
Dissipation de magie
Bénédiction fugace`, [R.sorcier, R.lumiere, R.fee, R.elfe, R.sphinx])

add(`Guérison`, [R.sorcier, R.lumiere, R.feeLumiere, R.elfeEau, R.nymphe])
add(`Lien vital
Rayonnement réparateur
Rosée réparatrice
Biokinésie`, [R.sorcier, R.lumiere, R.feeLumiere, R.elfeEau, R.nymphe, R.cupidon])
add(`Détection des protégés
Localisation`, [R.lumiere, R.cupidon, R.sorcier, R.valkyrie])
add(`Orbing`, [R.lumiere, R.tenebres])
add(`Téléportation / Flash
Shimmer
Lévitation`, [R.sorcier, R.demon, R.fee, R.lumiere, R.tenebres, R.muse, R.phenix])
add(`Ailes d'énergie`, [R.fee])
add(`Corps de marée
Marche des nuages
Nuage protecteur`, [R.feeEau, R.nymphe, R.sireneMarine, R.kitsuneEau, R.kitsuneAir])
add(`Poussière de fée`, [R.fee])

add(`Force accrue
Sens aiguisés
Régénération
Invulnérabilité partielle
Métabolisme accéléré
Adaptation respiratoire`, [R.demon, R.tenebres, R.vampire, R.heretique, R.loup, R.changeforme, R.kanima, R.hellhound, R.phenix, R.valkyrie])
add(`Vision thermique
Nyctalopie
Camouflage organique
Piste brouillée
Bond silencieux`, [R.loup, R.changeforme, R.kanima, R.hellhound, R.vampire, R.elfe, R.kitsune])
add(`Métamorphose
Peau des bêtes
Variation de taille
Variation de densité
Invisibilité
Clonage`, [R.sorcier, R.demon, R.fee, R.changeforme, R.kitsune, R.chimere])
add(`Communication animale
Parole des bêtes
Ascendant animal`, [R.sorcier, R.feeBois, R.elfeBois, R.nymphe, R.loup, R.changeforme, R.hellhound])
add(`Toucher paralysant`, [R.sorcier, R.demon, R.kanima, R.chimere, R.sirenePsychique])
add(`Sillage des effluves`, [R.cupidon, R.fee, R.nymphe, R.sirenePsychique, R.demon, R.vampire])
add(`Pétrification progressive`, [R.sorcier, R.demon, R.sphinx, R.chimere])
add(`Myokinésie
Neurokinésie`, [R.sorcier, R.demon, R.vampire, R.loup, R.changeforme, R.chimere])
add(`Aile spectrale`, [R.sorcier, R.phenix, R.valkyrie, R.sphinx])

add(`Absorption de magie`, [R.sorcier, R.heretique, R.demon, R.tenebres])
add(`Réplique de pouvoir`, [R.sorcier, R.demon, R.chimere])
add(`Technokinésie`, [R.sorcier, R.demon, R.phenix, R.chimere])
add(`Tychokinésie`, [R.sorcier, R.fee, R.sphinx])

// Noms de départ des parcours historiques qui n'ont pas de fiche autonome.
add(`Prémonition
Clairsentience
Lecture d'aura
Perception temporelle`, [R.sorcier, R.sphinx, R.banshee, R.elfeAstre, R.kitsuneEsprit])
add(`Suggestion
Rêves lucides`, [R.sorcier, R.demon, R.muse, R.sirenePsychique, R.kitsuneEsprit])
add(`Télépathie animale`, [R.sorcier, R.feeBois, R.elfeBois, R.nymphe, R.loup, R.changeforme])
add(`Accélération moléculaire
Inhibition moléculaire
Étincelle
Boule de feu`, [R.sorcier, R.demon, R.phenix, R.kitsuneFeu])
add(`Intangibilité
Téléportation
Clignement`, [R.sorcier, R.demon, R.fee, R.lumiere, R.tenebres])
add(`Brise
Lumière
Ombre`, [R.sorcier, R.fee, R.elfe, R.kitsuneAir, R.kitsuneLumiere, R.kitsuneOmbre])
add(`Bulle d'eau`, [R.sorcier, R.feeEau, R.elfeEau, R.nymphe, R.kitsuneEau, R.sireneMarine])
add(`Pierre`, [R.sorcier, R.kitsuneTerre, R.elfeBois, R.nymphe])
add(`Graine`, [R.sorcier, R.feeBois, R.elfeBois, R.nymphe, R.kitsunePlante])
add(`Rituel de protection
Conjuration`, [R.sorcier, R.demon, R.fee, R.elfe, R.sphinx])

export const powerRaces = Object.fromEntries(
  [...possibilities].map(([name, races]) => [name, [...races].sort((left, right) => left.localeCompare(right, 'fr'))]),
)
