<template>
  <main class="forms-page container">
    <header class="forms-header">
      <router-link to="/" class="back-link">← Catégories</router-link>
      <p class="eyebrow">✦ Les visages de l'Inframonde</p>
      <h1>Bottin des formes démoniaques</h1>
      <p>Chaque démon choisit une forme pour son personnage. Retrouvez ici son nom, son apparence et le personnage auquel elle appartient.</p>
      <router-link class="rules-link" to="/topics/reglement-et-reservations-formes-demoniaques">Consulter les règles des formes →</router-link>
    </header>

    <section v-if="isAdmin" class="admin-section card">
      <button type="button" class="btn btn-primary" @click="showForm = !showForm">{{ showForm ? 'Fermer' : '+ Ajouter une forme' }}</button>
      <form v-if="showForm" class="form-fields" @submit.prevent="createEntry">
        <label>Nom de la forme démoniaque <input v-model.trim="newEntry.name" maxlength="120" required></label>
        <label>Photo ou GIF (adresse de l'image) <input v-model.trim="newEntry.image_url" type="url" maxlength="500" placeholder="https://…"></label>
        <label>Nom du personnage lié <input v-model.trim="newEntry.character" maxlength="150" required></label>
        <p v-if="formError" role="alert">{{ formError }}</p>
        <button type="submit" class="btn btn-primary" :disabled="saving">{{ saving ? 'Enregistrement…' : 'Enregistrer' }}</button>
      </form>
    </section>

    <p v-if="loading" class="state">Chargement du bottin…</p>
    <p v-else-if="error" class="state">Le bottin est momentanément indisponible. <button type="button" @click="loadEntries">Réessayer</button></p>
    <p v-else-if="!entries.length" class="state">Aucune forme n'est encore inscrite dans le bottin.</p>
    <div v-else class="forms-grid">
      <article v-for="entry in entries" :key="entry.id" class="form-card card">
        <div class="form-image">
          <img v-if="entry.image_url" :src="entry.image_url" :alt="`Forme démoniaque ${entry.name}`" loading="lazy">
          <span v-else aria-hidden="true">✦</span>
        </div>
        <div class="form-body">
          <h2>{{ entry.name }}</h2>
          <p>{{ entry.character }}</p>
          <div v-if="isAdmin" class="entry-actions">
            <button type="button" @click="startEdit(entry)">Modifier</button>
            <button type="button" @click="removeEntry(entry)">Retirer</button>
          </div>
          <form v-if="editingId === entry.id" class="form-fields edit-fields" @submit.prevent="saveEdit(entry)">
            <label>Nom de la forme <input v-model.trim="editEntry.name" maxlength="120" required></label>
            <label>Photo ou GIF <input v-model.trim="editEntry.image_url" type="url" maxlength="500"></label>
            <label>Personnage lié <input v-model.trim="editEntry.character" maxlength="150" required></label>
            <p v-if="editError" role="alert">{{ editError }}</p>
            <div class="edit-actions"><button type="submit" :disabled="saving">Enregistrer</button><button type="button" @click="editingId = null">Annuler</button></div>
          </form>
        </div>
      </article>
    </div>
  </main>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import api from '../composables/useApi'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const isAdmin = computed(() => ['admin', 'fondatrice'].includes(auth.user?.role))
const entries = ref([])
const loading = ref(true)
const error = ref(false)
const showForm = ref(false)
const saving = ref(false)
const formError = ref('')
const editError = ref('')
const editingId = ref(null)
const newEntry = reactive({ name: '', image_url: '', character: '' })
const editEntry = reactive({ name: '', image_url: '', character: '' })

async function loadEntries() {
  loading.value = true
  error.value = false
  try {
    const { data } = await api.get('/demonic-forms/')
    entries.value = data
  } catch {
    error.value = true
  } finally {
    loading.value = false
  }
}

function errorMessage(error) {
  const data = error.response?.data
  return data?.name?.[0] || data?.character?.[0] || data?.image_url?.[0] || data?.detail || 'Enregistrement impossible.'
}

async function createEntry() {
  saving.value = true
  formError.value = ''
  try {
    await api.post('/demonic-forms/', newEntry)
    Object.assign(newEntry, { name: '', image_url: '', character: '' })
    showForm.value = false
    await loadEntries()
  } catch (e) {
    formError.value = errorMessage(e)
  } finally {
    saving.value = false
  }
}

function startEdit(entry) {
  editingId.value = entry.id
  editError.value = ''
  Object.assign(editEntry, { name: entry.name, image_url: entry.image_url, character: entry.character })
}

async function saveEdit(entry) {
  saving.value = true
  editError.value = ''
  try {
    await api.patch(`/demonic-forms/${entry.id}/`, editEntry)
    editingId.value = null
    await loadEntries()
  } catch (e) {
    editError.value = errorMessage(e)
  } finally {
    saving.value = false
  }
}

async function removeEntry(entry) {
  if (!window.confirm(`Retirer la forme « ${entry.name} » du bottin ?`)) return
  try {
    await api.delete(`/demonic-forms/${entry.id}/`)
    await loadEntries()
  } catch {
    window.alert('Suppression impossible.')
  }
}

onMounted(loadEntries)
</script>

<style scoped>
.forms-page { padding: 2.5rem 0 4rem; }
.forms-header { max-width: 720px; margin-bottom: 1.8rem; }
.back-link, .rules-link { color: var(--primary); text-decoration: none; }
.back-link { font-size: .8rem; }
.eyebrow { margin: 1rem 0 .2rem; color: #a78bfa; letter-spacing: .16em; font-size: .72rem; text-transform: uppercase; }
.forms-header h1 { margin: 0 0 .7rem; color: var(--text-primary); font-family: Georgia, serif; font-size: clamp(1.6rem, 3vw, 2.4rem); }
.forms-header > p:not(.eyebrow) { color: var(--text-secondary); line-height: 1.65; }
.rules-link { display: inline-block; margin-top: .25rem; font-size: .82rem; }
.admin-section { display: flex; flex-direction: column; align-items: flex-start; gap: 1rem; padding: 1rem; margin-bottom: 1.5rem; }
.form-fields { display: grid; gap: .75rem; width: min(100%, 520px); }
.form-fields label { display: grid; gap: .3rem; color: var(--text-secondary); font-size: .82rem; }
.form-fields input { width: 100%; box-sizing: border-box; padding: .6rem; border-radius: 6px; border: 1px solid var(--border); color: var(--text-primary); background: var(--bg-input, var(--bg-secondary)); font: inherit; }
.form-fields [role="alert"] { margin: 0; color: #f87171; }
.form-fields .btn { justify-self: start; }
.state { padding: 2rem; text-align: center; color: var(--text-secondary); }
.state button { color: var(--primary); background: none; border: 0; cursor: pointer; }
.forms-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 250px), 1fr)); gap: 1rem; }
.form-card { overflow: hidden; padding: 0; }
.form-image { height: 230px; display: grid; place-items: center; background: radial-gradient(circle, rgba(139,92,246,.18), #0d0a1a 70%); }
.form-image img { display: block; width: 100%; height: 100%; object-fit: cover; }
.form-image span { font-size: 3rem; color: #a78bfa; }
.form-body { padding: 1rem; }
.form-body h2 { margin: 0; color: #f5d76e; font-family: Georgia, serif; font-size: 1.15rem; }
.form-body > p { margin: .4rem 0 0; color: var(--text-secondary); font-size: .86rem; }
.entry-actions, .edit-actions { display: flex; gap: .75rem; margin-top: .85rem; }
.entry-actions button, .edit-actions button { border: 0; background: none; color: var(--primary); cursor: pointer; padding: 0; font: inherit; font-size: .8rem; }
.edit-fields { margin-top: 1rem; }
</style>
