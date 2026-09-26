<template>
  <div class="page admin-requests-page"><div class="container">
    <h1>Demandes et signalements</h1>
    <p v-if="loading">Chargement…</p>
    <p v-else-if="error" role="alert">{{ error }}</p>
    <p v-else-if="!requests.length">Aucune demande reçue.</p>
    <div v-else class="request-list">
      <article v-for="item in requests" :key="item.id" class="card request-card">
        <div class="request-top"><strong>{{ labels[item.kind] }}</strong><span>{{ new Date(item.created_at).toLocaleString('fr-FR') }}</span></div>
        <p><strong>Contact :</strong> {{ item.email }}<span v-if="item.author"> · {{ item.author }}</span></p>
        <p v-if="item.post_id"><router-link :to="`/topics/${item.topic_slug}`">Voir le sujet du message n° {{ item.post_id }}</router-link></p>
        <p class="request-message">{{ item.message }}</p>
        <button class="btn btn-secondary btn-sm" @click="toggleResolved(item)">{{ item.is_resolved ? 'Marquer à traiter' : 'Marquer comme traité' }}</button>
      </article>
    </div>
  </div></div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import api from '../composables/useApi'

const labels = { privacy: 'Données personnelles', report: 'Signalement', general: 'Autre demande' }
const requests = ref([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try { requests.value = (await api.get('/administration/contact/')).data }
  catch { error.value = 'Impossible de charger les demandes.' }
  finally { loading.value = false }
})

async function toggleResolved(item) {
  try {
    const { data } = await api.patch('/administration/contact/', { id: item.id, is_resolved: !item.is_resolved })
    item.is_resolved = data.is_resolved
  } catch { error.value = 'Impossible de mettre à jour cette demande.' }
}
</script>

<style scoped>
.admin-requests-page { padding: 2.5rem 0; }
.admin-requests-page h1 { color: var(--accent); }
.request-list { display: grid; gap: 1rem; }
.request-card { padding: 1.25rem; }
.request-top { display: flex; justify-content: space-between; gap: 1rem; flex-wrap: wrap; }
.request-top span { color: var(--text-secondary); }
.request-message { white-space: pre-wrap; line-height: 1.6; }
</style>
