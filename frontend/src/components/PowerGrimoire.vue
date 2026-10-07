<template>
  <section class="power-guide" aria-label="Grimoire des pouvoirs">
    <header class="guide-heading">
      <p class="guide-eyebrow">Nexus Arcana · Guide des joueurs</p>
      <h2>Registre des pouvoirs et de leurs évolutions</h2>
      <p>Explorez les types de pouvoirs, les espèces possibles et leurs évolutions. Ce registre n'est pas exhaustif : vous pouvez proposer un pouvoir ou une évolution au staff et en discuter avec l'équipe. <strong>Tout ajout de pouvoir et toute évolution, même présents dans ce registre, exigent l'approbation du staff avant utilisation en RP.</strong></p>
    </header>

    <details class="guide-help" open>
      <summary>Comment lire ce grimoire ?</summary>
      <ol>
        <li><strong>4 pouvoirs de base maximum à la création ; un 5e peut être acheté ensuite.</strong> Le plafond est de 5 pouvoirs de base au total, capacités actives et passives comprises, pour toutes les espèces, y compris les hybrides, tribrides et Originels. Chaque pouvoir de base peut recevoir au maximum 2 évolutions, achetées et validées séparément. Les évolutions ne créent pas de nouvel emplacement de pouvoir de base.</li>
        <li><strong>Vérifiez votre fiche validée.</strong> Ce catalogue propose des possibilités ; il ne donne pas tous ces pouvoirs à votre personnage.</li>
        <li><strong>Choisissez une spécialisation.</strong> Les options proposées pour un pouvoir de base ne forment pas une chaîne obligatoire. Chaque option achetée améliore ce pouvoir et doit être validée séparément.</li>
        <li><strong>Faites valider chaque ajout.</strong> Présentez le pouvoir actuel, le changement souhaité et ses limites. Tous les nouveaux pouvoirs et toutes les évolutions demandent l'approbation du staff avant usage. Aucun RP justificatif n'est demandé. ★ indique que sa portée, sa durée ou ses conséquences doivent être précisées avec le staff.</li>
        <li><strong>Proposez vos idées.</strong> Cette liste ne recense pas tous les pouvoirs ni toutes leurs évolutions. Vous pouvez proposer un pouvoir ou une évolution au staff et en discuter avec l’équipe avant de l’intégrer à votre fiche ou de l’utiliser en RP.</li>
      </ol>
      <p>« Maîtrise » signifie un usage plus précis ou plus étendu, jamais une puissance sans limite. Contrôle mental, blessure grave, possession et mort nécessitent l’accord du joueur concerné. Le maître du jeu est la personne qui encadre l’événement.</p>
      <p>Les espèces indiquées sont des possibilités, jamais des pouvoirs acquis automatiquement. Les hybrides dépendent de leurs héritages validés ; la nature de trybride est réservée à Hope Mikaelson. Les sorciers TVD et les hérétiques disposent de fiches propres dans le registre ; les autres pouvoirs restent à discuter selon leur fiche validée.</p>
      <p><strong>Siphonneurs et hérétiques TVD :</strong> ils peuvent choisir les mêmes pistes de sorts et d’évolutions que les autres sorciers TVD. Pour utiliser un sort, ils doivent d’abord siphonner de la magie depuis une source accessible ; les hérétiques peuvent notamment puiser dans leur propre nature vampirique. Sans magie siphonnée disponible, le sort ne fonctionne pas. Chaque pouvoir et évolution reste soumis à la fiche validée et à l’accord du staff.</p>
      <p><strong>Chimères :</strong> les quatre pistes affichées sont des exemples, pas des dons communs à toutes. Leurs capacités dépendent des origines et des deux axes retenus dans la fiche validée ; d'autres pouvoirs du registre peuvent être proposés au staff si la combinaison les justifie.</p>
      <p><strong>Démons, phénix et branches :</strong> le filtre « Démons » conserve son large éventail de pistes ; le type démoniaque, la forme choisie et la fiche validée déterminent celles qui conviennent au personnage. Les phénix de Legacies et ceux de Charmed ont des possibilités distinctes. Pour les autres espèces à branches, les pouvoirs généraux et ceux de l'affinité choisie restent soumis à la fiche validée. Une fiche sans espèce indiquée peut être proposée au staff si le personnage la justifie.</p>
      <p>Le 5e pouvoir de base coûte 600 Arcana Flouz ; chaque évolution coûte 300 Arcana Flouz, quel que soit le nombre d’achats précédents. Aucun 6e pouvoir de base ni 3e évolution d’un même pouvoir ne peut être acheté. Décrivez la capacité souhaitée et ses limites ; le staff approuve chaque ajout ou évolution. La capacité devient utilisable après validation, débit et mise à jour de la fiche.</p>
    </details>

    <div class="guide-controls">
      <label for="power-search">Rechercher un pouvoir ou une évolution</label>
      <div class="guide-search-row">
        <input id="power-search" v-model="query" type="search" placeholder="Ex. télékinésie, soin, orbing…" class="form-input" />
        <button v-if="query || family || race" class="btn btn-secondary btn-sm" @click="reset">Effacer les filtres</button>
      </div>
      <div class="guide-tabs" aria-label="Type de contenu">
        <button v-for="tab in tabs" :key="tab.id" class="btn btn-sm" :class="mode === tab.id ? 'btn-primary' : 'btn-secondary'" :aria-pressed="mode === tab.id" @click="selectMode(tab.id)">{{ tab.label }}</button>
      </div>
      <label for="power-family">Catégorie</label>
      <select id="power-family" v-model="family" class="form-input">
        <option value="">Toutes les catégories</option>
        <option v-for="name in families" :key="name" :value="name">{{ name }}</option>
      </select>
      <template v-if="mode !== 'rules'">
        <label for="power-race">Espèce possible</label>
        <select id="power-race" v-model="race" class="form-input">
          <option value="">Toutes les espèces</option>
          <option v-for="name in races" :key="name" :value="name">{{ name }}</option>
        </select>
      </template>
      <p role="status" class="guide-result-count">{{ filtered.length }} fiche{{ filtered.length > 1 ? 's' : '' }} trouvée{{ filtered.length > 1 ? 's' : '' }} dans le registre</p>
    </div>

    <p v-if="!filtered.length" class="guide-empty">Aucun résultat. Essayez un autre mot ou effacez les filtres.</p>
    <section v-for="group in grouped" :key="mode + group.name" class="guide-group" :aria-label="group.name">
      <header class="guide-group-heading">
        <h3>{{ group.name }}</h3>
        <span>{{ group.entries.length }} fiche{{ group.entries.length > 1 ? 's' : '' }}</span>
      </header>
    <details v-for="entry in group.entries" :key="mode + entry.id" class="power-card">
      <summary>
        <span class="power-card-title">{{ entry.title }}</span>
        <span class="guide-badge">Validation du staff requise</span>
        <span v-if="entry.requiresStaff || entry.hasStar" class="guide-badge">Limites à préciser ★</span>
      </summary>
      <div class="power-card-body">
        <p v-if="entry.races?.length" class="guide-races"><strong>Espèces possibles :</strong> {{ entry.races.join(' · ') }}</p>
        <template v-if="mode === 'powers'">
          <h3>Ce que fait ce pouvoir</h3>
          <p>{{ entry.notes?.[0] || entry.description }}</p>
          <p v-if="entry.notes" class="guide-source"><strong>Règle du grimoire :</strong> {{ entry.description }}</p>
          <template v-if="entry.notes">
            <h3>Exemple en RP</h3><p>{{ entry.notes[1] }}</p>
            <h3>Limites à jouer</h3><p>{{ entry.notes[2] }}</p>
          </template>
          <h3>Évolutions possibles : ce qui change</h3>
          <ul class="guide-evolutions">
            <li v-for="step in entry.steps" :key="step.label"><strong>{{ step.label }}</strong><p>{{ step.explanation }}</p></li>
          </ul>
        </template>
        <template v-else-if="mode === 'paths' || mode === 'tvd' || mode === 'heretics'">
          <p class="guide-source"><strong>Conditions du grimoire :</strong> {{ entry.description }}</p>
          <ol class="guide-steps">
            <li v-for="(step, index) in entry.steps" :key="step.label"><span class="guide-step-number">{{ index === 0 ? 'B' : index }}</span><div><h3>{{ index === 0 ? 'Pouvoir de base' : `Option ${index}` }} : {{ step.label }}</h3><p>{{ step.explanation }}</p></div></li>
          </ol>
      <p class="guide-caution">Chaque option est à acheter et à faire valider selon votre personnage. Elle n’accorde pas automatiquement les autres spécialisations du même pouvoir.</p>
        </template>
        <template v-else><p>{{ entry.description }}</p></template>
      </div>
    </details>
    </section>

    <details class="guide-reference">
      <summary>Consulter le texte complet du grimoire</summary>
      <p>Le texte officiel et ses conditions sont conservés ici. En cas de doute entre deux branches, demandez à l’équipe avant de les utiliser.</p>
      <div class="guide-original" v-html="content"></div>
    </details>
  </section>
</template>

<script setup>
import { computed, ref } from 'vue'
import { powerNotes, evolutionNotes, pathwayNotes, normalize } from '../data/powerGuide'
import { powerRaces } from '../data/powerRaces'

const props = defineProps({ content: { type: String, required: true } })
const query = ref('')
const family = ref('')
const race = ref('')
const mode = ref('powers')
const tabs = [{ id: 'powers', label: 'Tous les pouvoirs' }, { id: 'paths', label: 'Évolutions possibles' }, { id: 'tvd', label: 'Sorciers TVD' }, { id: 'heretics', label: 'Hérétiques TVD' }, { id: 'rules', label: 'Règles et limites' }]
const featuredPathTitles = new Set([
  'Empathie inversée', 'Réplique de pouvoir', 'Toucher paralysant',
  'Phytokinésie (contrôle végétal)', "Aquakinésie (contrôle de l'eau)",
  'Hématokinésie', 'Aérokinésie', 'Sens aiguisés', 'Régénération',
  'Force accrue', 'Suggestion mentale', 'Perception des liens affectifs',
  'Élan affectif',
  'Phobokinésie', 'Rayonnement de joie', 'Vertige de folie',
  'Chagrin partagé', 'Élan de courage',
  'Illusion visuelle', 'Illusion mentale',
  'Malaise surnaturel',
  'Réminiscence',
  'Manipulation des sentiments',
])
function heading(element) {
  let parent = element.parentElement
  while (parent) {
    const title = parent.querySelector('h2')
    if (title) return title.textContent.trim().replace(/^[^\p{L}]*[IVXLCDM]+\.\s*/u, '')
    parent = parent.parentElement
  }
  return 'Grimoire'
}
function explainStep(label) {
  const name = label.replace(/\s*[★(].*$/, '').trim()
  return evolutionNotes[name] || 'Cette branche doit être précisée avec l’équipe : définissez son effet, sa portée et ses limites avant de l’utiliser.'
}
const entries = computed(() => {
  const doc = new DOMParser().parseFromString(props.content, 'text/html')
  const powers = []
  for (const row of doc.querySelectorAll('table tbody tr')) {
    const cells = [...row.querySelectorAll('td')].map(cell => cell.textContent.trim())
    if (cells.length !== 3) continue
    const [title, description, evolution] = cells
    const family = heading(row.closest('table'))
    let evolutionExplanations = []
    try { evolutionExplanations = JSON.parse(row.dataset.evolutionExplanations || '[]') } catch { /* Keep the standard explanation. */ }
    powers.push({ id: powers.length, title, description, evolution, family,
      races: row.dataset.races ? row.dataset.races.split('|') : (powerRaces[title] || []),
      showInPaths: row.closest('table')?.dataset.powerPaths === 'true',
      notes: powerNotes[title], hasStar: evolution.includes('★'),
      requiresStaff: title === 'Réplique de pouvoir',
      steps: evolution.split('·').map((label, index) => ({ label: label.trim(), explanation: evolutionExplanations[index] || explainStep(label) })),
    })
  }
  const paths = powers.filter(power => power.showInPaths || featuredPathTitles.has(power.title)).map(power => ({
    id: `power-${power.id}`, title: power.title, description: power.description,
    races: power.races,
    family: power.family, requiresStaff: power.requiresStaff,
    steps: [
      { label: power.title, explanation: power.notes?.[0] || power.description },
      ...power.steps,
    ],
  }))
  const rules = []
  for (const item of doc.querySelectorAll('li')) {
    if (item.closest('table')) continue
    const strong = item.querySelector('strong')
    if (!strong) continue
    const title = strong.textContent.trim()
    const description = item.textContent.trim().slice(title.length).replace(/^\s*[—–-]\s*/, '')
    const family = heading(item)
    if (item.dataset.powerOptions) {
      let options = []
      try { options = JSON.parse(item.dataset.powerOptions) } catch { /* Keep the base power visible. */ }
      if (featuredPathTitles.has(title)) continue
      const explanations = pathwayNotes[title]
      paths.push({ id: paths.length, title, description, family, races: powerRaces[title] || [], requiresStaff: title === 'Perception temporelle',
        steps: [title, ...options].map((label, index) => ({ label, explanation: explanations?.[index] || explainStep(label) })),
      })
    } else {
      rules.push({ id: rules.length, title, description, family })
    }
  }
  return {
    powers, paths,
    tvd: paths.filter(path => path.family === 'Sorciers TVD'),
    heretics: paths.filter(path => path.races?.includes('Hérétiques')),
    rules,
  }
})
const frenchOrder = (left, right) => left.localeCompare(right, 'fr', { sensitivity: 'base' })
const speciesFamilies = new Set(['Vampires', 'Loups-garous', 'Sorcières et sorciers Charmed', 'Furies', 'Démons de Lazare', 'Démons Kazi', 'Succubes et incubes', 'Êtres des ténèbres', 'Prophétesses démoniaques', "Chiens de l'enfer", 'Phénix : deux continuités', 'Kitsunes de la glace', 'Kitsunes du sang'])
const highlightedRaces = ['Vampires', 'Loups-garous', 'Sorcières et sorciers Charmed', 'Furies', 'Démons de Lazare', 'Démons Kazi', 'Succubes et incubes', 'Êtres des ténèbres', 'Prophétesses démoniaques']
function categoryForFamily(name) {
  if (speciesFamilies.has(name)) return 'Pouvoirs liés aux espèces'
  if (name === 'Sorcellerie Charmed') return 'Traditions magiques'
  if (name === 'Vampires, loups et héritages hybrides') return 'Règles des espèces'
  return name
}
function optionsWithHighlights(values, highlights) {
  const available = new Set(values)
  return [
    ...highlights.filter(name => available.delete(name)),
    ...[...available].sort(frenchOrder),
  ]
}
const families = computed(() => [...new Set(entries.value[mode.value].map(entry => categoryForFamily(entry.family)))].sort(frenchOrder))
const races = computed(() => optionsWithHighlights(
  entries.value[mode.value].flatMap(entry => entry.races || []), highlightedRaces,
))
const filtered = computed(() => {
  const terms = normalize(query.value).split(/\s+/).filter(Boolean)
  return entries.value[mode.value].filter(entry => {
    if (family.value && categoryForFamily(entry.family) !== family.value) return false
    if (race.value && !entry.races?.includes(race.value)) return false
    const text = normalize([entry.title, entry.description, entry.evolution || '', entry.family, ...(entry.races || []), ...(entry.notes || []), ...(entry.steps || []).flatMap(step => [step.label, step.explanation])].join(' '))
    return terms.every(term => text.includes(term))
  })
})
const grouped = computed(() => [...new Set(filtered.value.map(entry => entry.family))].sort(frenchOrder)
  .map(name => ({
    name,
    entries: filtered.value.filter(entry => entry.family === name).sort((left, right) => frenchOrder(left.title, right.title)),
  }))
  .filter(group => group.entries.length))
function reset() { query.value = ''; family.value = ''; race.value = '' }
function selectMode(value) { mode.value = value; family.value = ''; race.value = '' }
</script>

<style scoped>
.power-guide { color: var(--text-primary); min-width: 0; }
.guide-heading { padding: 1.3rem; border: 1px solid var(--border); border-radius: 12px; background: linear-gradient(130deg,rgba(124,58,237,.15),rgba(245,215,110,.05)); }
.guide-heading h2 { margin: .4rem 0 .8rem; font-family: var(--font-heading); font-size: clamp(1.25rem,3vw,1.8rem); line-height: 1.25; }
.guide-heading p { line-height: 1.7; }
.guide-eyebrow { color: var(--accent); font-size: .75rem; letter-spacing: .08em; }
.guide-help, .guide-reference { margin: 1rem 0; padding: 1rem; border: 1px solid var(--border); border-radius: 10px; }
summary { cursor: pointer; font-weight: 600; line-height: 1.5; }
summary:focus-visible { outline: 2px solid var(--accent); outline-offset: 4px; border-radius: 4px; }
.guide-help ol { padding-left: 1.4rem; }
.guide-help li { margin: .7rem 0; line-height: 1.65; }
.guide-help p, .guide-reference p { font-size: .88rem; line-height: 1.7; }
.guide-controls { margin: 1.2rem 0; }
.guide-controls label { display: block; font-weight: 600; font-size: .85rem; margin: .65rem 0 .4rem; }
.guide-search-row { display: flex; gap: .5rem; flex-wrap: wrap; }
.guide-search-row input { flex: 1 1 220px; min-width: 0; }
.guide-tabs { display: flex; flex-wrap: wrap; gap: .5rem; margin: .8rem 0; }
.guide-result-count { color: var(--text-secondary); font-size: .8rem; margin: .8rem 0; }
.guide-group { margin: 1.45rem 0 1.8rem; }
.guide-group-heading { display: flex; align-items: baseline; justify-content: space-between; gap: 1rem; padding: .65rem .85rem; border-bottom: 1px solid var(--border); background: linear-gradient(90deg, rgba(124,58,237,.13), transparent); }
.guide-group-heading h3 { margin: 0; color: var(--accent); font-family: var(--font-heading); font-size: 1rem; line-height: 1.4; }
.guide-group-heading span { color: var(--text-secondary); font-size: .76rem; white-space: nowrap; }
.power-card { border: 1px solid var(--border); border-radius: 10px; margin: .65rem 0; overflow: hidden; }
.power-card > summary { padding: 1rem; background: var(--bg-secondary); }
.power-card-title { overflow-wrap: anywhere; }
.guide-badge { display: inline-block; margin: .5rem 0 0 1rem; color: var(--accent); font-size: .72rem; }
.power-card-body { padding: .3rem 1rem 1rem; }
.power-card-body h3 { font-size: .9rem; margin: 1rem 0 .35rem; }
.power-card-body p { font-size: .9rem; line-height: 1.75; margin: .3rem 0 .8rem; overflow-wrap: anywhere; }
.guide-source { padding: .8rem; background: rgba(124,58,237,.06); border-radius: 6px; }
.guide-races { padding: .65rem .8rem; border-left: 3px solid var(--accent); background: rgba(124,58,237,.08); }
.guide-evolutions { padding-left: 1.3rem; }
.guide-evolutions li { margin: .8rem 0; }
.guide-steps { list-style: none; padding: 0; }
.guide-steps li { display: flex; gap: .8rem; margin: 1rem 0; }
.guide-steps h3 { margin-top: 0; }
.guide-step-number { flex: 0 0 28px; height: 28px; border-radius: 50%; display: grid; place-items: center; background: rgba(124,58,237,.18); color: var(--accent); }
.guide-caution { padding: .75rem; border-left: 3px solid var(--accent); }
.guide-original { overflow-x: auto; max-width: 100%; margin-top: 1rem; }
.guide-empty { padding: 1rem; border: 1px dashed var(--border); border-radius: 8px; }
@media(max-width:600px) { .guide-heading, .guide-help { padding: .85rem; } .guide-tabs button { flex: 1 1 140px; } }
</style>
