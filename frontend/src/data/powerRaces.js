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
  phenixLegacies: 'Phénix de Legacies',
  phenixCharmed: 'Phénix de Charmed',
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
add(`Traque des êtres de lumière`, [R.tenebres])
add(`Présage de rupture
Vision d'issue
Lecture des destinées
Révélation du point de rupture`, [R.prophetesses])
add(`Soif révélatrice
Vitesse vampirique
Contrainte du regard`, [R.vampire])
add(`Transformation lupine
Instinct de meute
Pistage lupin`, [R.loup])
add(`Renaissance du phénix`, [R.phenixLegacies])
add(`Reconstitution du phénix`, [R.phenixCharmed])
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
Flux emprunté`, [R.sorcier, R.demon, R.fee, R.elfe, R.lumiere])

add(`Pyrokinésie
Combustion moléculaire
Combustion par le regard
Boules d'énergie
Immunité aux flammes
Magmakinésie`, [R.sorcier, R.demon, R.phenix, R.kitsuneFeu])
add(`Pyrokinésie
Combustion par le regard
Résistance aux flammes`, [R.hellhound])
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
Camouflage magique
Pas de brume`, [R.demon, R.feeNoire, R.elfeNoir, R.kitsuneOmbre])
add(`Arbalète d'ombre
Orbing sombre`, [R.tenebres])
add(`Brumokinésie
Fumokinésie
Cinerokinésie
Poussiérokinésie`, [R.sorcier, R.demon, R.fee, R.kitsuneAir, R.phenix])
add(`Acidokinésie
Toxikinésie`, [R.sorcier, R.demon, R.kanima])
add(`Hématokinésie
Ostéokinésie`, [R.sorcier, R.demon, R.feeNoire, R.elfeNoir, R.kitsuneSang])
add(`Sonokinésie
Vibrakinésie
Leurre acoustique
Cri perçant
Silence surnaturel
Écholocalisation`, [R.sorcier, R.demon, R.banshee, R.muse, R.kitsuneSon, R.sirenePsychique])
add(`Chant apaisant
Voix mimétique`, [R.sorcier, R.muse, R.fee, R.sirenePsychique])
add(`Chant apaisant`, [R.cupidon])
add(`Cri de Furie`, [R.furies])
add(`Hurlement de ralliement
Rugissement de garde`, [R.demon, R.valkyrie, R.loup, R.changeforme])

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
Partage sensoriel`, [R.sorcier, R.fee, R.elfe, R.sphinx, R.muse, R.kitsuneEsprit])
add(`Détection de magie
Précognition
Clairvoyance
Sens des présages
Lecture des intentions`, [R.banshee])
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
Émotionkinésie`, [R.sorcier, R.muse, R.fee, R.nymphe, R.sirenePsychique, R.kitsuneEsprit])
add(`Empathie
Empathie inversée
Perception des liens affectifs
Élan affectif
Rayonnement de joie
Chagrin partagé
Élan de courage
Accord des sens
Émotionkinésie`, [R.cupidon])
add(`Phobokinésie`, [R.sorcier, R.demon, R.sirenePsychique, R.kitsuneEsprit])
add(`Vertige de folie
Malaise surnaturel
Germe de discorde
Torture mentale`, [R.sorcier, R.demon, R.sirenePsychique, R.kitsuneEsprit])
add(`Algokinésie`, [R.sorcier, R.demon, R.sirenePsychique, R.kitsuneEsprit])
add(`Suggestion mentale
Manipulation des sentiments
Illusion mentale
Onirokinésie
Chant envoûtant`, [R.sorcier, R.demon, R.fee, R.muse, R.sirenePsychique, R.kitsuneEsprit])
add(`Illusion visuelle`, [R.sorcier, R.demon, R.fee, R.muse, R.sirenePsychique, R.kitsuneEsprit])
add(`Sommeil induit`, [R.sorcier, R.demon, R.fee, R.muse, R.sirenePsychique, R.kitsuneEsprit])
add(`Réminiscence
Mnémokinésie
Intuition des mensonges
Omnilinguisme`, [R.sorcier, R.sphinx, R.muse, R.elfe, R.sirenePsychique, R.kitsuneEsprit])
add(`Nécromancie
Projection astrale
Écho des savoirs`, [R.sorcier, R.demon, R.sphinx, R.valkyrie, R.kitsuneEsprit])
add(`Égide de l'esprit
Dissipation de magie
Bénédiction fugace`, [R.sorcier, R.lumiere, R.fee, R.elfe, R.sphinx])

add(`Guérison`, [R.sorcier, R.lumiere, R.feeLumiere, R.elfeEau, R.nymphe])
add(`Lien vital
Rayonnement réparateur
Rosée réparatrice
Biokinésie`, [R.sorcier, R.lumiere, R.feeLumiere, R.elfeEau, R.nymphe])
add(`Détection des protégés
Localisation`, [R.lumiere, R.cupidon, R.sorcier, R.valkyrie])
add(`Orbing`, [R.lumiere])
add(`Téléportation / Flash
Shimmer
Lévitation`, [R.sorcier, R.demon, R.fee, R.lumiere, R.muse, R.phenix])
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
Adaptation respiratoire`, [R.demon, R.heretique, R.loup, R.changeforme, R.kanima, R.phenix, R.valkyrie])
add(`Force accrue
Sens aiguisés
Régénération
Résistance vampirique`, [R.vampire])
add(`Force accrue
Sens aiguisés
Régénération
Invulnérabilité partielle`, [R.hellhound])
add(`Force accrue
Sens aiguisés`, [R.tenebres])
add(`Vision thermique
Nyctalopie
Camouflage organique
Piste brouillée
Bond silencieux`, [R.loup, R.changeforme, R.kanima, R.elfe, R.kitsune])
add(`Nyctalopie
Bond silencieux`, [R.vampire])
add(`Vision thermique
Nyctalopie`, [R.hellhound])
add(`Métamorphose
Peau des bêtes
Variation de taille
Variation de densité
Clonage`, [R.sorcier, R.demon, R.fee, R.changeforme, R.kitsune])
add(`Invisibilité`, [R.sorcier, R.demon, R.fee, R.kitsune])
add(`Communication animale
Parole des bêtes
Ascendant animal`, [R.sorcier, R.feeBois, R.elfeBois, R.nymphe, R.loup, R.changeforme])
add(`Toucher paralysant`, [R.sorcier, R.demon, R.kanima, R.sirenePsychique])
add(`Sillage des effluves`, [R.cupidon, R.fee, R.nymphe, R.sirenePsychique, R.demon])
add(`Pétrification progressive`, [R.sorcier, R.demon, R.sphinx])
add(`Myokinésie
Neurokinésie`, [R.sorcier, R.demon, R.loup, R.changeforme])
add(`Aile spectrale`, [R.sorcier, R.phenix, R.valkyrie, R.sphinx])

add(`Absorption de magie`, [R.sorcier, R.heretique, R.demon])
add(`Réplique de pouvoir`, [R.sorcier, R.demon])
add(`Technokinésie`, [R.sorcier, R.demon, R.phenix])
add(`Tychokinésie`, [R.sorcier, R.fee, R.sphinx])

// Noms de départ des parcours historiques qui n'ont pas de fiche autonome.
add(`Prémonition
Clairsentience
Lecture d'aura
Perception temporelle`, [R.sorcier, R.sphinx, R.elfeAstre, R.kitsuneEsprit])
add(`Prémonition
Clairsentience
Lecture d'aura`, [R.banshee])
add(`Suggestion
Rêves lucides`, [R.sorcier, R.demon, R.muse, R.sirenePsychique, R.kitsuneEsprit])
add(`Télépathie animale`, [R.sorcier, R.feeBois, R.elfeBois, R.nymphe, R.loup, R.changeforme])
add(`Accélération moléculaire
Inhibition moléculaire
Étincelle
Boule de feu`, [R.sorcier, R.demon, R.phenix, R.kitsuneFeu])
add(`Intangibilité
Téléportation
Clignement`, [R.sorcier, R.demon, R.fee, R.lumiere])
add(`Brise
Lumière
Ombre`, [R.sorcier, R.fee, R.elfe, R.kitsuneAir, R.kitsuneLumiere, R.kitsuneOmbre])
add(`Bulle d'eau`, [R.sorcier, R.feeEau, R.elfeEau, R.nymphe, R.kitsuneEau, R.sireneMarine])
add(`Pierre`, [R.sorcier, R.kitsuneTerre, R.elfeBois, R.nymphe])
add(`Graine`, [R.sorcier, R.feeBois, R.elfeBois, R.nymphe, R.kitsunePlante])
add(`Rituel de protection
Conjuration`, [R.sorcier, R.demon, R.fee, R.elfe, R.sphinx])

// Le registre rassemble des pistes très larges. Chaque filtre d'espèce ne garde
// que les pouvoirs cohérents avec sa nature ou sa branche dans le codex.
function limit(race, names) {
  const allowed = new Set(names.trim().split('\n').map(name => name.trim()).filter(Boolean))
  for (const name of allowed) {
    if (!possibilities.has(name)) throw new Error(`Pouvoir introuvable dans le registre : ${name}`)
  }
  for (const [name, races] of possibilities) {
    if (races.has(race) && !allowed.has(name)) races.delete(race)
  }
}

limit(R.elfe, `Détection de magie
Précognition
Sens des présages
Écho des savoirs
Voile de présence
Nyctalopie
Bond silencieux`)
limit(R.elfeAstre, `Photokinésie
Poussière lumineuse
Télékinésie lumineuse
Prisme de lumière
Glamour scintillant
Prémonition
Clairsentience
Lecture d'aura`)
limit(R.elfeEau, `Aquakinésie (contrôle de l'eau)
Bouclier aquatique
Fouet d'eau
Respiration aquatique
Voix des eaux
Corps de marée
Augure des marées
Guérison
Rosée réparatrice
Bulle d'eau`)
limit(R.elfeBois, `Phytokinésie (contrôle végétal)
Lignokinésie
Mycokinésie
Augure des racines
Communication animale
Télépathie animale
Graine`)
limit(R.lumiere, `Bouclier d'énergie
Télékinésie lumineuse
Égide de l'esprit
Guérison
Lien vital
Rayonnement réparateur
Détection des protégés
Localisation
Orbing`)
limit(R.fee, `Télékinésie
Bouclier d'énergie
Chant apaisant
Voile de présence
Empathie
Illusion visuelle
Lévitation
Ailes d'énergie
Poussière de fée
Variation de taille
Invisibilité
Lumière`)
limit(R.feeEau, `Cryokinésie
Pluviokinésie
Aquakinésie (contrôle de l'eau)
Bouclier aquatique
Fouet d'eau
Respiration aquatique
Voix des eaux
Corps de marée
Augure des marées
Nuage protecteur
Bulle d'eau`)
limit(R.feeLumiere, `Photokinésie
Poussière lumineuse
Télékinésie lumineuse
Prisme de lumière
Glamour scintillant
Guérison
Rayonnement réparateur`)
limit(R.kanima, `Toxikinésie
Force accrue
Sens aiguisés
Régénération
Nyctalopie
Camouflage organique
Toucher paralysant`)
limit(R.kitsune, `Nyctalopie
Bond silencieux
Métamorphose
Peau des bêtes`)
limit(R.kitsuneAir, `Cyclogenèse
Aérokinésie
Barokinésie
Néphokinésie
Brumokinésie
Marche des nuages
Nuage protecteur
Brise`)
limit(R.kitsuneEau, `Pluviokinésie
Aquakinésie (contrôle de l'eau)
Bouclier aquatique
Fouet d'eau
Respiration aquatique
Voix des eaux
Corps de marée
Augure des marées
Bulle d'eau`)
limit(R.kitsuneEsprit, `Détection de magie
Précognition
Clairvoyance
Sens des présages
Lecture des intentions
Écho des savoirs
Télépathie
Empathie
Illusion mentale
Onirokinésie
Illusion visuelle
Réminiscence
Mnémokinésie
Projection astrale
Prémonition
Clairsentience
Lecture d'aura
Rêves lucides`)
limit(R.kitsuneOmbre, `Umbrakinésie
Camouflage magique
Pas de brume
Voile de présence
Ombre`)
limit(R.kitsuneLumiere, `Photokinésie
Poussière lumineuse
Télékinésie lumineuse
Prisme de lumière
Glamour scintillant
Lumière`)
limit(R.kitsuneTerre, `Géokinésie
Cristallokinésie
Arénokinésie
Sismokinésie
Courant de limon
Pierre`)
limit(R.kitsuneFeu, `Pyrokinésie
Combustion par le regard
Magmakinésie
Étincelle
Boule de feu`)
limit(R.kitsuneSang, `Hématokinésie`)
limit(R.kitsuneTonnerre, `Foudre / Électrokinésie
Sillage fulgurant`)
limit(R.loup, `Transformation lupine
Instinct de meute
Pistage lupin
Hurlement de ralliement
Force accrue
Sens aiguisés
Régénération
Nyctalopie
Bond silencieux`)
limit(R.changeforme, `Rugissement de garde
Force accrue
Sens aiguisés
Régénération
Nyctalopie
Piste brouillée
Bond silencieux
Métamorphose
Peau des bêtes`)
limit(R.muse, `Leurre acoustique
Chant apaisant
Voix mimétique
Animation d'objets
Écho des savoirs
Télépathie
Empathie
Accord des sens
Émotionkinésie
Illusion visuelle
Réminiscence`)
limit(R.nymphe, `Aquakinésie (contrôle de l'eau)
Bouclier aquatique
Géokinésie
Phytokinésie (contrôle végétal)
Lignokinésie
Augure des racines
Empathie
Guérison
Rosée réparatrice
Communication animale
Télépathie animale
Bulle d'eau
Pierre
Graine`)
limit(R.sireneMarine, `Aquakinésie (contrôle de l'eau)
Bouclier aquatique
Fouet d'eau
Respiration aquatique
Voix des eaux
Corps de marée
Bulle d'eau`)
limit(R.sirenePsychique, `Chant apaisant
Voix mimétique
Télépathie
Empathie
Émotionkinésie
Suggestion mentale
Illusion mentale
Onirokinésie
Chant envoûtant
Réminiscence
Mnémokinésie
Suggestion`)
limit(R.sphinx, `Détection de magie
Précognition
Clairvoyance
Sens des présages
Lecture des intentions
Écho des savoirs
Réminiscence
Intuition des mensonges
Omnilinguisme
Prémonition
Clairsentience
Lecture d'aura`)
limit(R.valkyrie, `Écho des savoirs
Localisation
Force accrue
Sens aiguisés
Régénération
Aile spectrale`)
limit(R.heretique, `Force accrue
Sens aiguisés
Régénération
Absorption de magie`)
limit(R.banshee, `Sonokinésie
Vibrakinésie
Cri perçant
Sens des présages
Prémonition
Clairsentience`)
limit(R.cupidon, `Chant apaisant
Empathie
Empathie inversée
Perception des liens affectifs
Élan affectif
Rayonnement de joie
Chagrin partagé
Élan de courage
Émotionkinésie
Détection des protégés
Localisation`)
limit(R.phenix, ``)
possibilities.get('Shimmer')?.delete(R.sorcier)
possibilities.get('Détection des protégés')?.delete(R.sorcier)

// Quatre pistes au minimum pour chaque choix du filtre. Pour les chimères,
// ces exemples restent conditionnés aux deux origines validées.
add(`Fumokinésie
Shimmer`, [R.furies])
add(`Régénération
Force accrue
Shimmer`, [R.lazare])
add(`Force accrue
Sens aiguisés
Bouclier d'énergie`, [R.kazi])
add(`Empathie
Sillage des effluves`, [R.succubes])
add(`Lévitation
Aile spectrale
Régénération`, [R.phenixLegacies])
add(`Boules d'énergie
Formule improvisée
Alchimie de terrain`, [R.phenixCharmed])
add(`Brume glacée
Bouclier de givre`, [R.kitsuneGlace])
add(`Écho du sang
Fil sanguin
Garde de sang`, [R.kitsuneSang])
add(`Étincelle
Magnétokinésie`, [R.kitsuneTonnerre])
add(`Métamorphose
Force accrue
Sens aiguisés
Régénération`, [R.chimere])

export const powerRaces = Object.fromEntries(
  [...possibilities].map(([name, races]) => [name, [...races].sort((left, right) => left.localeCompare(right, 'fr'))]),
)
