<template>
  <section class="power-guide" aria-label="Grimoire des pouvoirs">
    <header class="guide-heading">
      <p class="guide-eyebrow">Nexus Arcana · Guide des joueurs</p>
      <h2>Registre des pouvoirs et de leurs évolutions</h2>
      <p>Explorez les types de pouvoirs et leurs évolutions possibles, puis filtrez les pistes selon la race de votre personnage. Ce registre n'est pas exhaustif : vous pouvez proposer un pouvoir ou une évolution au staff et en discuter avec l'équipe. <strong>Tout ajout de pouvoir et toute évolution, même présents dans ce registre, exigent l'approbation du staff avant utilisation en RP.</strong></p>
    </header>

    <details class="guide-help" open>
      <summary>Comment lire ce grimoire ?</summary>
      <ol>
        <li><strong>4 capacités maximum à la création, toutes natures confondues.</strong> Hybrides, tribrides et Originels partagent le même plafond, capacités actives et passives comprises. Les capacités manquantes se débloquent en jeu avec des Arcana Flouz, après validation du staff. Une capacité déjà acquise peut être améliorée deux fois par des achats distincts.</li>
        <li><strong>Vérifiez votre race et votre fiche.</strong> Ce catalogue propose des possibilités ; il ne donne pas tous ces pouvoirs à votre personnage.</li>
        <li><strong>Choisissez une piste d’évolution.</strong> Les flèches indiquent des branches possibles, pas des niveaux débloqués automatiquement. Certaines branches sont des dons distincts.</li>
        <li><strong>Faites valider chaque ajout.</strong> Présentez le pouvoir actuel, le changement souhaité et ses limites. Tous les nouveaux pouvoirs et toutes les évolutions demandent l'approbation du staff avant usage. Aucun RP justificatif n'est demandé. ★ signale un encadrement particulier, pas une exception à cette règle.</li>
        <li><strong>Proposez vos idées.</strong> Cette liste ne recense pas tous les pouvoirs ni toutes leurs évolutions. Vous pouvez proposer un pouvoir ou une évolution au staff et en discuter avec l’équipe avant de l’intégrer à votre fiche ou de l’utiliser en RP.</li>
      </ol>
      <p>« Maîtrise » signifie un usage plus précis ou plus étendu, jamais une puissance sans limite. Contrôle mental, blessure grave, possession et mort nécessitent l’accord du joueur concerné. Le maître du jeu est la personne qui encadre l’événement.</p>
      <p>Chaque déblocage ou amélioration passe par la boutique : 300 Arcana Flouz pour le premier achat, puis 300 de plus par achat. Décrivez la capacité souhaitée et ses limites ; le staff approuve chaque ajout ou évolution. La capacité devient utilisable après validation, débit et mise à jour de la fiche.</p>
    </details>

    <div class="guide-controls">
      <label for="power-race">Race du personnage</label>
      <select id="power-race" v-model="race" class="form-input">
        <option value="">Toutes les races · registre complet</option>
        <option v-for="choice in raceChoices" :key="choice.id" :value="choice.id">{{ choice.label }}</option>
      </select>
      <p v-if="race" class="guide-race-hint">{{ raceCodex[race]?.dons }} <strong>Ces pistes ne sont pas des pouvoirs acquis.</strong> La spécialité, la fiche validée et les règles de progression déterminent ce qui est utilisable.</p>
      <label for="power-search">Rechercher un pouvoir, une évolution ou une race</label>
      <div class="guide-search-row">
        <input id="power-search" v-model="query" type="search" placeholder="Ex. télékinésie, soin, orbing, vampire…" class="form-input" />
        <button v-if="query || family || race" class="btn btn-secondary btn-sm" @click="reset">Effacer les filtres</button>
      </div>
      <div class="guide-tabs" aria-label="Type de contenu">
        <button v-for="tab in tabs" :key="tab.id" class="btn btn-sm" :class="mode === tab.id ? 'btn-primary' : 'btn-secondary'" :aria-pressed="mode === tab.id" @click="selectMode(tab.id)">{{ tab.label }}</button>
      </div>
      <label for="power-family">Famille ou rubrique</label>
      <select id="power-family" v-model="family" class="form-input">
        <option value="">Toutes les rubriques</option>
        <option v-for="name in families" :key="name" :value="name">{{ name }}</option>
      </select>
      <p role="status" class="guide-result-count">{{ filtered.length }} fiche{{ filtered.length > 1 ? 's' : '' }} trouvée{{ filtered.length > 1 ? 's' : '' }}{{ race ? ' pour cette race' : ' dans le registre' }}</p>
    </div>

    <p v-if="!filtered.length" class="guide-empty">Aucun résultat. Essayez un autre mot ou effacez les filtres.</p>
    <details v-for="entry in filtered" :key="mode + entry.id" class="power-card">
      <summary>
        <span class="power-card-title">{{ entry.title }}<small>{{ entry.family }}</small></span>
        <span class="guide-badge">Validation du staff requise</span>
        <span v-if="entry.requiresStaff || entry.hasStar" class="guide-badge">Encadrement particulier ★</span>
      </summary>
      <div class="power-card-body">
        <p v-if="mode !== 'rules'" class="guide-races"><strong>Races possibles :</strong> {{ raceLabels(entry) || 'À préciser avec le staff selon la fiche.' }}</p>
        <template v-if="mode === 'powers'">
          <h3>Ce que fait ce pouvoir</h3>
          <p>{{ entry.notes?.[0] || entry.description }}</p>
          <p class="guide-source"><strong>Règle du grimoire :</strong> {{ entry.description }}</p>
          <template v-if="entry.notes">
            <h3>Exemple en RP</h3><p>{{ entry.notes[1] }}</p>
            <h3>Limites à jouer</h3><p>{{ entry.notes[2] }}</p>
          </template>
          <h3>Évolutions possibles : ce qui change</h3>
          <ul class="guide-evolutions">
            <li v-for="step in entry.steps" :key="step.label"><strong>{{ step.label }}</strong><p>{{ step.explanation }}</p></li>
          </ul>
        </template>
        <template v-else-if="mode === 'paths'">
          <p class="guide-source"><strong>Lignées et conditions du grimoire :</strong> {{ entry.description }}</p>
          <ol class="guide-steps">
            <li v-for="(step, index) in entry.steps" :key="step.label"><span class="guide-step-number">{{ index + 1 }}</span><div><h3>{{ step.label }}</h3><p>{{ step.explanation }}</p></div></li>
          </ol>
          <p class="guide-caution">Chaque étape est une possibilité à faire valider selon votre lignée. Elle n’accorde pas automatiquement les autres branches du même pouvoir.</p>
        </template>
        <template v-else><p>{{ entry.description }}</p></template>
      </div>
    </details>

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
import { raceCodex } from '../data/raceCodex'
import { compatibleRaces, raceChoices } from '../data/powerCompatibility'

const props = defineProps({ content: { type: String, required: true } })
const query = ref('')
const family = ref('')
const race = ref('')
const mode = ref('powers')
const tabs = [{ id: 'powers', label: 'Tous les pouvoirs' }, { id: 'paths', label: 'Évolutions possibles' }, { id: 'rules', label: 'Races & règles' }]
const raceLabels = entry => compatibleRaces(entry, mode.value)
  .filter(id => !['Hybride', 'Trybride'].includes(id))
  .map(id => raceChoices.find(choice => choice.id === id)?.label || id).join(' · ')
function heading(element) {
  let parent = element.parentElement
  while (parent) {
    const title = parent.querySelector('h2')
    if (title) return title.textContent.trim().replace(/^[^\p{L}]*[IVX]+\.\s*/u, '')
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
    powers.push({ id: powers.length, title, description, evolution, family,
      notes: powerNotes[title], hasStar: evolution.includes('★'),
      requiresStaff: title === 'Portail temporel',
      steps: evolution.split('·').map(label => ({ label: label.trim(), explanation: explainStep(label) })),
    })
  }
  const paths = [], rules = []
  for (const item of doc.querySelectorAll('li')) {
    if (item.closest('table')) continue
    const strong = item.querySelector('strong')
    if (!strong) continue
    const title = strong.textContent.trim()
    const description = item.textContent.trim().slice(title.length).replace(/^\s*[—–-]\s*/, '')
    const family = heading(item)
    if (title.includes('→')) {
      const names = title.split('→').map(name => name.trim())
      const explanations = pathwayNotes[names[0]]
      paths.push({ id: paths.length, title, description, family, requiresStaff: names[0] === 'Perception temporelle',
        steps: names.map((label, index) => ({ label, explanation: explanations?.[index] || explainStep(label) })),
      })
    } else {
      rules.push({ id: rules.length, title, description, family })
    }
  }
  return { powers, paths, rules }
})
const families = computed(() => [...new Set(entries.value[mode.value].map(entry => entry.family))])
const filtered = computed(() => {
  const terms = normalize(query.value).split(/\s+/).filter(Boolean)
  return entries.value[mode.value].filter(entry => {
    if (family.value && entry.family !== family.value) return false
    if (race.value && !compatibleRaces(entry, mode.value).includes(race.value)) return false
    const text = normalize([entry.title, entry.description, entry.evolution || '', entry.family, ...(entry.notes || []), ...(entry.steps || []).flatMap(step => [step.label, step.explanation])].join(' '))
    return terms.every(term => text.includes(term))
  })
})
function reset() { query.value = ''; family.value = ''; race.value = '' }
function selectMode(value) { mode.value = value; family.value = '' }
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
.guide-race-hint, .guide-races { padding: .8rem 1rem; border-left: 3px solid var(--accent); background: rgba(124,58,237,.07); border-radius: 4px; line-height: 1.65; }
.guide-race-hint { font-size: .85rem; margin: .7rem 0 1rem; }
.guide-races { font-size: .8rem; }
.guide-controls label { display: block; font-weight: 600; font-size: .85rem; margin: .65rem 0 .4rem; }
.guide-search-row { display: flex; gap: .5rem; flex-wrap: wrap; }
.guide-search-row input { flex: 1 1 220px; min-width: 0; }
.guide-tabs { display: flex; flex-wrap: wrap; gap: .5rem; margin: .8rem 0; }
.guide-result-count { color: var(--text-secondary); font-size: .8rem; margin: .8rem 0; }
.power-card { border: 1px solid var(--border); border-radius: 10px; margin: .65rem 0; overflow: hidden; }
.power-card > summary { padding: 1rem; background: var(--bg-secondary); }
.power-card-title { overflow-wrap: anywhere; }
.power-card-title small { display: block; color: var(--text-secondary); font-size: .72rem; font-weight: 400; margin: .2rem 0 0 1rem; }
.guide-badge { display: inline-block; margin: .5rem 0 0 1rem; color: var(--accent); font-size: .72rem; }
.power-card-body { padding: .3rem 1rem 1rem; }
.power-card-body h3 { font-size: .9rem; margin: 1rem 0 .35rem; }
.power-card-body p { font-size: .9rem; line-height: 1.75; margin: .3rem 0 .8rem; overflow-wrap: anywhere; }
.guide-source { padding: .8rem; background: rgba(124,58,237,.06); border-radius: 6px; }
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
