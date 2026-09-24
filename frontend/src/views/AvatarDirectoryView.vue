<template>
  <main class="avatar-directory container">
    <header class="directory-head">
      <span class="directory-kicker">📸 Les visages du Nexus</span>
      <h1>Bottin des avatars</h1>
      <p>Retrouvez les célébrités utilisées par les personnages et celles proposées pour les scénarios.</p>
    </header>

    <section class="directory-guide" aria-label="Comment lire le bottin">
      <p><strong>Pris</strong> : avatar d’un personnage validé ou scénario joué. <strong>En attente</strong> : avatar indiqué sur un profil dont la fiche n’est pas encore validée. <strong>Scénario</strong> : personnage libre ou réservé ; une mention signale quand son avatar est négociable.</p>
      <p>Le bottin suit les profils et les fiches scénarios. Seule l’administration peut modifier les célébrités enregistrées. Pour demander un avatar, indiquez la célébrité souhaitée dans votre fiche ou votre demande de double compte ; l’administration confirmera sa disponibilité.</p>
      <div class="directory-actions">
        <router-link to="/categories/scenarios-a-prendre">Voir les scénarios</router-link>
        <button v-if="isAdmin" type="button" @click="showCreate = !showCreate">{{ showCreate ? 'Fermer' : 'Ajouter un personnage' }}</button>
      </div>
    </section>

    <form v-if="isAdmin && showCreate" class="avatar-create" @submit.prevent="createEntry">
      <h2>Ajouter un personnage au bottin</h2>
      <label>Nom du personnage <input v-model.trim="newEntry.character" maxlength="150" required /></label>
      <label>Célébrité <input v-model.trim="newEntry.avatar" maxlength="100" required /></label>
      <label>Statut <select v-model="newEntry.status"><option value="taken">Pris</option><option value="pending">En attente</option><option value="scenario">Scénario</option></select></label>
      <label>Lien vers sa fiche (facultatif) <input v-model.trim="newEntry.url" maxlength="250" placeholder="/topics/nom-de-la-fiche" /></label>
      <label v-if="newEntry.status === 'scenario'" class="avatar-checkbox"><input v-model="newEntry.negotiable" type="checkbox" /> Avatar négociable</label>
      <p v-if="createError" class="avatar-edit-error">{{ createError }}</p>
      <button type="submit" :disabled="creating">{{ creating ? 'Enregistrement…' : 'Enregistrer le personnage' }}</button>
    </form>

    <div class="directory-controls">
      <label for="avatar-search">Rechercher une célébrité ou un personnage</label>
      <input id="avatar-search" v-model="search" type="search" placeholder="Ex. Alyssa Milano, Piper Halliwell…" />
      <div class="directory-filters" role="group" aria-label="Filtrer les avatars">
        <button v-for="filter in filters" :key="filter.value" type="button" :class="{ active: status === filter.value }" @click="status = filter.value">{{ filter.label }}</button>
      </div>
    </div>

    <p v-if="loading" class="directory-state">Chargement du bottin…</p>
    <p v-else-if="error" class="directory-state">Le bottin est momentanément indisponible. <button type="button" @click="loadDirectory">Réessayer</button></p>
    <template v-else>
      <p class="directory-count">{{ filteredEntries.length }} entrée{{ filteredEntries.length > 1 ? 's' : '' }}</p>
      <nav v-if="availableLetters.length" class="directory-letters" aria-label="Index alphabétique">
        <a v-for="letter in availableLetters" :key="letter" :href="`#avatars-${letter}`">{{ letter }}</a>
      </nav>
      <p v-if="!filteredEntries.length" class="directory-state">Aucun avatar ne correspond à cette recherche.</p>
      <section v-for="section in groupedEntries" :id="`avatars-${section.letter}`" :key="section.letter" class="directory-letter-section">
        <h2>{{ section.letter }}</h2>
        <div class="avatar-grid">
          <article v-for="entry in section.entries" :key="`${entry.kind}-${entry.url}-${entry.id || entry.member_id || ''}`" class="avatar-card">
            <div class="avatar-card-top">
              <h3>{{ entry.avatar }}</h3>
              <span class="avatar-status" :class="`avatar-status--${entry.status}`">{{ statusLabel(entry.status) }}</span>
            </div>
            <p>{{ entry.character }}</p>
            <small v-if="entry.kind === 'scenario'">{{ scenarioStatusLabel(entry.scenario_status) }}</small>
            <small v-if="entry.negotiable">Avatar négociable avec le staff</small>
            <router-link v-if="entry.url" :to="entry.url">{{ entry.kind === 'scenario' ? 'Voir le scénario' : 'Voir la fiche' }} →</router-link>
            <div v-if="isAdmin && entry.kind === 'member'" class="avatar-admin">
              <button v-if="editingId !== entry.member_id" type="button" @click="startEditing(entry)">Modifier la célébrité</button>
              <template v-else>
                <label :for="`avatar-edit-${entry.member_id}`">Nom de la célébrité</label>
                <input :id="`avatar-edit-${entry.member_id}`" v-model="editName" maxlength="100" />
                <p v-if="editError" class="avatar-edit-error">{{ editError }}</p>
                <div class="avatar-edit-actions"><button type="button" :disabled="saving" @click="saveAvatar(entry)">Enregistrer</button><button type="button" @click="editingId = null">Annuler</button></div>
              </template>
            </div>
            <div v-if="isAdmin && entry.kind === 'scenario'" class="avatar-admin">
              <button v-if="editingScenarioSlug !== entry.scenario_slug" type="button" @click="startScenarioEditing(entry)">Modifier le scénario</button>
              <template v-else>
                <label :for="`scenario-avatar-${entry.scenario_slug}`">Célébrité (recast)</label>
                <input :id="`scenario-avatar-${entry.scenario_slug}`" v-model="scenarioEditName" maxlength="100" />
                <label :for="`scenario-status-${entry.scenario_slug}`">Statut du scénario</label>
                <select :id="`scenario-status-${entry.scenario_slug}`" v-model="scenarioEditStatus">
                  <option value="free">Libre</option><option value="reserved">Réservé</option><option value="played">Joué</option>
                </select>
                <p v-if="scenarioEditError" class="avatar-edit-error">{{ scenarioEditError }}</p>
                <div class="avatar-edit-actions"><button type="button" :disabled="savingScenario" @click="saveScenario(entry)">Enregistrer</button><button type="button" @click="editingScenarioSlug = null">Annuler</button></div>
              </template>
            </div>
            <div v-if="isAdmin && entry.kind === 'manual'" class="avatar-admin">
              <button type="button" @click="removeEntry(entry)">Retirer du bottin</button>
            </div>
          </article>
        </div>
      </section>
      <section v-if="missingScenarios.length" class="missing-scenarios">
        <h2>Scénarios dont l’avatar reste à préciser</h2>
        <div><router-link v-for="item in missingScenarios" :key="item.url" :to="item.url">{{ item.character }}</router-link></div>
      </section>
    </template>
  </main>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import api from '../composables/useApi'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const isAdmin = computed(() => ['admin', 'fondatrice'].includes(auth.user?.role))
const entries = ref([])
const missingScenarios = ref([])
const loading = ref(true)
const error = ref(false)
const search = ref('')
const status = ref('all')
const editingId = ref(null)
const editName = ref('')
const editError = ref('')
const saving = ref(false)
const editingScenarioSlug = ref(null)
const scenarioEditName = ref('')
const scenarioEditStatus = ref('free')
const scenarioEditError = ref('')
const savingScenario = ref(false)
const showCreate = ref(false)
const creating = ref(false)
const createError = ref('')
const newEntry = ref({ character: '', avatar: '', status: 'taken', url: '', negotiable: false })
const filters = [
  { value: 'all', label: 'Tous' },
  { value: 'taken', label: 'Pris' },
  { value: 'pending', label: 'En attente' },
  { value: 'scenario', label: 'Scénarios' },
]

function normalize(value) {
  return (value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase()
}

const filteredEntries = computed(() => entries.value.filter(entry => {
  const matchesStatus = status.value === 'all' || entry.status === status.value
  const query = normalize(search.value.trim())
  return matchesStatus && (!query || normalize(`${entry.avatar} ${entry.character}`).includes(query))
}))

const groupedEntries = computed(() => {
  const groups = new Map()
  for (const entry of filteredEntries.value) {
    const letter = normalize(entry.avatar)[0]?.toUpperCase() || '#'
    if (!groups.has(letter)) groups.set(letter, [])
    groups.get(letter).push(entry)
  }
  return [...groups].map(([letter, items]) => ({ letter, entries: items }))
})
const availableLetters = computed(() => groupedEntries.value.map(group => group.letter))

function statusLabel(value) {
  return { taken: 'Pris', pending: 'En attente', scenario: 'Scénario' }[value] || value
}

function scenarioStatusLabel(value) {
  return { free: 'Scénario libre', reserved: 'Scénario réservé', played: 'Scénario joué' }[value] || 'Scénario'
}

function startScenarioEditing(entry) {
  editingScenarioSlug.value = entry.scenario_slug
  scenarioEditName.value = entry.avatar
  scenarioEditStatus.value = entry.scenario_status
  scenarioEditError.value = ''
}

async function saveScenario(entry) {
  const avatar = scenarioEditName.value.trim()
  if (!avatar) {
    scenarioEditError.value = 'Indiquez une célébrité.'
    return
  }
  savingScenario.value = true
  scenarioEditError.value = ''
  try {
    await api.patch(`/topics/${entry.scenario_slug}/`, {
      scenario_avatar_name: avatar,
      scenario_status: scenarioEditStatus.value,
    })
    editingScenarioSlug.value = null
    await loadDirectory()
  } catch (e) {
    const data = e.response?.data
    scenarioEditError.value = data?.scenario_avatar_name?.[0] || data?.scenario_status?.[0] || data?.detail || 'Modification impossible.'
  } finally {
    savingScenario.value = false
  }
}

function startEditing(entry) {
  editingId.value = entry.member_id
  editName.value = entry.avatar
  editError.value = ''
}

async function saveAvatar(entry) {
  const name = editName.value.trim()
  if (!name) {
    editError.value = 'Indiquez une célébrité.'
    return
  }
  saving.value = true
  editError.value = ''
  try {
    await api.patch(`/users/${entry.member_id}/`, { avatar_name: name })
    editingId.value = null
    await loadDirectory()
  } catch (e) {
    editError.value = e.response?.data?.avatar_name?.[0] || e.response?.data?.detail || 'Modification impossible.'
  } finally {
    saving.value = false
  }
}

async function createEntry() {
  creating.value = true
  createError.value = ''
  try {
    await api.post('/avatars/', newEntry.value)
    newEntry.value = { character: '', avatar: '', status: 'taken', url: '', negotiable: false }
    showCreate.value = false
    await loadDirectory()
  } catch (e) {
    const data = e.response?.data
    createError.value = data?.avatar?.[0] || data?.url?.[0] || data?.detail || 'Enregistrement impossible.'
  } finally {
    creating.value = false
  }
}

async function removeEntry(entry) {
  if (!window.confirm(`Retirer ${entry.character} du bottin ?`)) return
  try {
    await api.delete(`/avatars/${entry.id}/`)
    await loadDirectory()
  } catch {
    window.alert('Suppression impossible.')
  }
}

async function loadDirectory() {
  loading.value = true
  error.value = false
  try {
    const { data } = await api.get('/avatars/')
    entries.value = data.entries || []
    missingScenarios.value = data.missing_scenarios || []
  } catch {
    error.value = true
  } finally {
    loading.value = false
  }
}

onMounted(loadDirectory)
</script>

<style scoped>
.avatar-directory { padding-top: 2.5rem; padding-bottom: 4rem; max-width: 1100px; }
.directory-head { padding: 2rem; border: 1px solid rgba(245,215,110,.28); border-radius: 16px; background: linear-gradient(135deg,#241634,#100b1e); }
.directory-kicker { color: #f5d76e; font-size: .78rem; letter-spacing: .15em; text-transform: uppercase; }
.directory-head h1 { margin: .5rem 0; color: #f7e8ad; font-family: Georgia,serif; font-size: clamp(2rem,5vw,3.2rem); }
.directory-head p,.directory-guide p { color: #d5c9e6; line-height: 1.7; }
.directory-guide { margin: 1.2rem 0; padding: 1rem 1.4rem; border: 1px solid rgba(139,92,246,.3); border-radius: 12px; background: rgba(55,32,79,.35); }
.directory-guide p { margin: .4rem 0; }
.directory-guide strong { color: #f5d76e; }
.directory-actions { display: flex; flex-wrap: wrap; gap: .6rem; margin-top: .9rem; }
.directory-actions a,.directory-actions button { padding: .55rem .8rem; border: 1px solid #8f72b6; border-radius: 7px; color: #eee0ff; background: #2c1c3e; text-decoration: none; font: inherit; cursor: pointer; }
.avatar-create { display: grid; gap: .8rem; margin: 1.2rem 0; padding: 1.3rem; border: 1px solid #8f72b6; border-radius: 12px; background: #1c1329; }
.avatar-create h2 { margin: 0; color: #f5d76e; font-family: Georgia,serif; }
.avatar-create label { display: grid; gap: .35rem; color: #e9dcf4; }
.avatar-create input,.avatar-create select { padding: .65rem; border: 1px solid #73578f; border-radius: 6px; background: #150f21; color: #fff; font: inherit; }
.avatar-create .avatar-checkbox { display: flex; align-items: center; }
.avatar-create .avatar-checkbox input { width: auto; }
.avatar-create button { justify-self: start; padding: .6rem .9rem; border: 1px solid #f5d76e; border-radius: 6px; background: #3b2946; color: #f5d76e; cursor: pointer; }
.directory-controls { display: grid; gap: .65rem; margin: 1.5rem 0; }
.directory-controls label { color: #e9dcf4; font-weight: 600; }
.directory-controls input { width: 100%; padding: .8rem 1rem; border: 1px solid #73578f; border-radius: 8px; background: #191125; color: #fff; font: inherit; }
.directory-filters { display: flex; flex-wrap: wrap; gap: .45rem; }
.directory-filters button { padding: .45rem .75rem; border: 1px solid #67517e; border-radius: 7px; background: #20152f; color: #d8cae8; cursor: pointer; }
.directory-filters button.active { border-color: #f5d76e; color: #f5d76e; }
.directory-count { color: #cfc1db; font-size: .88rem; }
.directory-letters { display: flex; flex-wrap: wrap; gap: .4rem; margin: 1rem 0 1.6rem; }
.directory-letters a { min-width: 2rem; padding: .3rem; border: 1px solid #66517d; border-radius: 5px; text-align: center; color: #f5d76e; text-decoration: none; }
.directory-letter-section { margin: 1.6rem 0; scroll-margin-top: 5rem; }
.directory-letter-section h2 { color: #f5d76e; border-bottom: 1px solid #67517e; padding-bottom: .35rem; font-family: Georgia,serif; }
.avatar-grid { display: grid; grid-template-columns: repeat(auto-fill,minmax(230px,1fr)); gap: .8rem; }
.avatar-card { padding: 1rem; border: 1px solid #5c476e; border-radius: 10px; background: #1c1329; }
.avatar-card-top { display: flex; flex-wrap: wrap; align-items: start; justify-content: space-between; gap: .4rem; }
.avatar-card h3 { margin: 0; color: #f2e4fb; font-size: 1rem; }
.avatar-card p { margin: .55rem 0; color: #cdbfda; }
.avatar-card small { display: block; color: #e3cf9a; margin-bottom: .55rem; }
.avatar-card a,.missing-scenarios a { color: #d7b8ff; text-decoration: underline; }
.avatar-admin { margin-top: .7rem; border-top: 1px solid #5c476e; padding-top: .6rem; }
.avatar-admin button { padding: .35rem .55rem; border: 1px solid #8f72b6; border-radius: 5px; background: #2c1c3e; color: #eee0ff; cursor: pointer; }
.avatar-admin label { display: block; margin-bottom: .3rem; color: #e8d7f8; font-size: .8rem; }
.avatar-admin input,.avatar-admin select { width: 100%; margin-bottom: .4rem; padding: .5rem; border: 1px solid #73578f; border-radius: 5px; background: #150f21; color: #fff; }
.avatar-edit-actions { display: flex; gap: .4rem; }
.avatar-edit-error { color: #ffc0c0 !important; font-size: .8rem; }
.avatar-status { padding: .18rem .4rem; border-radius: 5px; font-size: .69rem; white-space: nowrap; }
.avatar-status--taken { background: #56303d; color: #ffd3d9; }
.avatar-status--pending { background: #50422a; color: #ffe6a3; }
.avatar-status--scenario { background: #293b54; color: #c6dcff; }
.directory-state { padding: 2rem; color: #d5c9e6; }
.directory-state button { color: #f5d76e; background: none; border: 0; text-decoration: underline; cursor: pointer; }
.missing-scenarios { margin-top: 2.5rem; padding: 1rem; border: 1px solid #66517d; border-radius: 10px; }
.missing-scenarios h2 { color: #f5d76e; font-size: 1.1rem; }
.missing-scenarios div { display: flex; flex-wrap: wrap; gap: 1rem; }
</style>
