<template>
  <div class="page"><div class="container rp-tracker">
    <h1 class="page-title">Mes RP</h1>
    <p class="text-secondary">Retrouvez les sujets auxquels vous participez. « À reprendre » signifie qu’un partenaire a écrit le dernier message.</p>
    <div class="rp-filters" aria-label="Filtrer mes RP">
      <button v-for="item in filters" :key="item.value" class="btn btn-sm" :class="filter === item.value ? 'btn-primary' : 'btn-secondary'" :aria-pressed="filter === item.value" @click="selectFilter(item.value)">{{ item.label }}</button>
      <button class="btn btn-secondary btn-sm" :disabled="loading" @click="load">Actualiser</button>
    </div>
    <p v-if="error" role="alert">{{ error }}</p>
    <LoadingSpinner v-if="loading" />
    <template v-else-if="!error">
      <div v-if="!topics.length" class="card rp-empty">Aucun RP dans cette sélection. Vos sujets et vos participations dans les rubriques RP apparaîtront ici.</div>
      <article v-for="topic in topics" :key="topic.id" class="card rp-item">
        <div class="rp-item-top">
          <span class="text-sm text-secondary">{{ topic.category }}</span>
          <span class="badge" :class="topic.awaiting_reply ? 'badge-warning' : ''">{{ topic.is_locked ? 'Verrouillé' : topic.awaiting_reply ? 'À reprendre' : 'En attente des partenaires' }}</span>
        </div>
        <h2><router-link :to="topicLink(topic)">{{ topic.title }}</router-link></h2>
        <p class="text-sm text-secondary">{{ topic.post_count }} message{{ topic.post_count > 1 ? 's' : '' }}<template v-if="topic.last_author"> · Dernier message de {{ topic.last_author }} · {{ formatDate(topic.last_activity) }}</template></p>
        <router-link class="btn btn-secondary btn-sm" :to="topicLink(topic)">Lire les derniers messages</router-link>
      </article>
      <PaginationBar :page="page" :count="count" @change="changePage" />
    </template>
  </div></div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../composables/useApi'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import PaginationBar from '../components/PaginationBar.vue'

const filters = [{ value: 'active', label: 'En cours' }, { value: 'waiting', label: 'À reprendre' }, { value: 'locked', label: 'Verrouillés' }, { value: 'all', label: 'Tous' }]
const filter = ref('active')
const page = ref(1)
const count = ref(0)
const topics = ref([])
const loading = ref(false)
const error = ref('')
let requestNumber = 0
async function load() {
  const request = ++requestNumber
  loading.value = true
  error.value = ''
  try {
    const { data } = await api.get('/topics/my-rp/', { params: { status: filter.value, page: page.value } })
    if (request !== requestNumber) return
    topics.value = data.results
    count.value = data.count
  } catch {
    if (request === requestNumber) error.value = 'Impossible de charger vos RP. Cliquez sur Actualiser pour réessayer.'
  } finally {
    if (request === requestNumber) loading.value = false
  }
}
function selectFilter(value) { filter.value = value; page.value = 1; load() }
function changePage(value) { page.value = value; load() }
function topicLink(topic) { return { path: `/topics/${topic.slug}`, query: { page: Math.max(1, Math.ceil(topic.post_count / 20)) } } }
function formatDate(value) { return value ? new Date(value).toLocaleString('fr-FR', { dateStyle: 'medium', timeStyle: 'short' }) : '' }
onMounted(load)
</script>

<style scoped>
.rp-tracker { max-width: 960px; }
.rp-filters { display: flex; flex-wrap: wrap; gap: .5rem; margin: 1.5rem 0; }
.rp-item, .rp-empty { padding: 1.25rem; margin-bottom: 1rem; }
.rp-item-top { display: flex; justify-content: space-between; flex-wrap: wrap; gap: .5rem; }
.rp-item h2 { margin: .75rem 0; font-size: 1.15rem; overflow-wrap: anywhere; }
.rp-item p { margin-bottom: 1rem; }
</style>
