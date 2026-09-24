import { raceCodex } from './raceCodex'

export const raceChoices = Object.keys(raceCodex).map(id => ({ id, label: {
  'sorcier-charmed': 'Sorcier Charmed', 'sorcier-tvd': 'Sorcier TVD',
  'etre-de-lumiere': 'Être de lumière', 'sirene-tvd': 'Sirène TVD',
  'sirene-triton-charmed': 'Sirène / Triton Charmed', demon: 'Démon',
  Phoenix: 'Phénix', 'Hérétique': 'Hérétique', 'Loup-garou': 'Loup-garou',
  'Chien de l\'enfer': 'Chien de l’enfer',
}[id] || id })).sort((a, b) => a.label.localeCompare(b.label, 'fr'))

const S = ['sorcier-charmed', 'sorcier-tvd']
const D = ['demon']
const N = ['Fée', 'Elfe', 'Nymphe/Satyre']
const E = ['etre-de-lumiere']
const V = ['Vampire', 'Hérétique', 'Trybride']
const W = ['Loup-garou', 'WereCoyote', 'WereJaguar', 'WereLion']

// Compatibilité indicative pour les pouvoirs du tableau historique.
// Les branches précises restent définies par la race, la spécialité et la fiche validée.
export const powerRaces = {
  "Boules d'énergie": [...S, ...D, ...E],
  'Télékinésie': [...S, ...D, ...E, 'Cupidon'],
  'Pyrokinésie': [...S, ...D, 'Kitsune', 'Phoenix', "Chien de l'enfer"],
  'Cryokinésie': [...S, ...D, 'Kitsune', 'Fée', 'Elfe'],
  'Combustion moléculaire': [...S, ...D],
  'Décélération moléculaire': [...S, ...D],
  'Foudre / Électrokinésie': [...S, ...D, 'Kitsune'],
  'Vague de force': [...S, ...D, ...E],
  'Cyclogenèse': [...S, ...D, 'Kitsune', 'Fée', 'Elfe'],
  'Combustion par le regard': [...D, ...S],
  "Bouclier d'énergie": [...S, ...D, ...E, 'Fée'],
  'Invulnérabilité partielle': [...D, ...V, ...W, 'Kanima', 'Chimère', 'Phoenix', "Chien de l'enfer"],
  'Absorption de magie': [...S, ...D, 'Hérétique', 'Trybride'],
  'Camouflage magique': [...S, ...D, ...N, 'Kitsune'],
  'Immunité aux flammes': [...D, 'Phoenix', "Chien de l'enfer"],
  'Guérison': [...S, ...E, 'Fée', 'Elfe', 'Phoenix'],
  'Empathie': [...S, ...E, 'Cupidon', 'Muse', 'Fée', 'sirene-tvd'],
  'Localisation': [...S, ...E, ...D, 'Sphinx'],
  'Transmission de pouvoirs': [...S, ...E, 'Cupidon'],
  'Lien vital': [...S, ...E, 'Fée'],
  'Orbing': [...E, 'Hybride'],
  'Téléportation / Flash': [...S, ...D, 'Cupidon', ...E],
  'Shimmer': [...D],
  'Lévitation': [...S, ...D, ...E, 'Fée', 'Cupidon'],
  'Portail temporel': [...S, ...D],
  'Précognition': [...S, 'Banshee', 'Sphinx', 'Kitsune'],
  'Clairvoyance': [...S, 'Sphinx', 'Banshee', ...E],
  'Télépathie': [...S, ...D, 'sirene-tvd', 'Sphinx'],
  'Nécromancie': [...S, ...D, 'Banshee', 'Kitsune'],
  'Détection de magie': [...S, ...D, ...E, ...N, 'Kitsune'],
  'Métamorphose': [...S, ...D, 'Kitsune', 'Fée', 'Elfe'],
  'Illusion': [...S, ...D, 'Kitsune', 'Fée', 'Elfe', 'sirene-tvd'],
  'Invisibilité': [...S, ...D, 'Fée', 'Elfe', 'Kitsune'],
  'Projection astrale': [...S, ...D, ...E, 'Sphinx'],
  'Contrôle végétal': [...S, ...N, 'Kitsune'],
  "Contrôle de l'eau": [...S, 'sirene-triton-charmed', 'Fée', 'Elfe', 'Kitsune'],
  'Communication animale': [...S, ...N, 'Kitsune', ...W],
  'Géokinésie': [...S, ...N, 'Kitsune', 'Chimère'],
}

const aliases = {
  'sorcier-charmed': /sorci[eè]r|magie charmed/i,
  'sorcier-tvd': /sorci[eè]r|coven|magie ancestrale/i,
  demon: /d[eé]mon/i,
  'etre-de-lumiere': /[eê]tre[s]? de lumi[eè]re|orbing/i,
  Cupidon: /cupidon/i,
  Vampire: /vampire/i,
  'Loup-garou': /loup|loups|meute/i,
  Banshee: /banshee/i,
  Kanima: /kanima/i,
  Kitsune: /kitsun/i,
  Fée: /f[eé]e|f[eé]eri/i,
  Elfe: /elfe/i,
  Sphinx: /sphinx/i,
  Chimère: /chim[eè]re/i,
  Phoenix: /ph[eé]nix/i,
  'sirene-tvd': /sir[eè]ne[s]? TVD|sir[eè]ne[s]? psychique/i,
  'sirene-triton-charmed': /sir[eè]ne[s]?\/triton|sir[eè]ne[s]? charmed/i,
  'Nymphe/Satyre': /nymphe|satyre/i,
  'Chien de l\'enfer': /chien[s]? de l.enfer/i,
  Muse: /muse/i,
  'Hérétique': /h[eé]r[eé]tique|siphonn/i,
  Trybride: /trybride|tribride/i,
  WereCoyote: /werecoyote|changeforme/i,
  WereJaguar: /werejaguar|changeforme/i,
  WereLion: /werelion|changeforme/i,
}

export function compatibleRaces(entry, mode) {
  let races = []
  if (mode === 'powers') races = powerRaces[entry.title] || []
  else if (mode === 'paths') races = raceChoices.filter(race => aliases[race.id]?.test(entry.description)).map(race => race.id)
  else races = raceChoices.filter(race => aliases[race.id]?.test(entry.title)).map(race => race.id)
  if (races.some(id => ['sorcier-tvd', 'Vampire', 'Loup-garou'].includes(id))) races = [...races, 'Trybride']
  if (races.some(id => ['sorcier-tvd', 'Vampire'].includes(id))) races = [...races, 'Hérétique']
  if (races.length && mode !== 'rules') races = [...races, 'Hybride']
  return [...new Set(races)]
}
