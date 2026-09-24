<template>
  <div class="page">
    <div class="container activity-alerts">
      <div class="page-header">
        <h1 class="page-title">⚑ Alertes d’activité</h1>
        <p class="page-subtitle">Suivi réservé à l’administration des membres sans message de plus de 150 mots depuis plus de 30 jours.</p>
      </div>

      <div v-if="loading" class="card activity-card">Chargement des alertes…</div>
      <div v-else-if="error" class="alert alert-danger">{{ error }}</div>
      <template v-else>
        <p class="activity-count">{{ members.length }} membre{{ members.length > 1 ? 's' : '' }} à suivre</p>
        <div v-if="!members.length" class="card activity-card">Aucune alerte pour le moment.</div>
        <div v-for="member in members" :key="member.id" class="card activity-card">
          <div>
            <router-link :to="`/membres/${member.id}`" class="member-name">{{ member.username }}</router-link>
            <p>{{ member.last_qualifying_post ? `Dernier message de plus de 150 mots : ${formatDate(member.last_qualifying_post)}` : 'Aucun message de plus de 150 mots' }}</p>
          </div>
          <span class="delay">{{ member.days_without_qualifying_post }} jours</span>
          <router-link :to="`/membres/${member.id}?supprimer=1`" class="btn btn-secondary btn-sm">Supprimer</router-link>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../composables/useApi'

const members = ref([])
const loading = ref(true)
const error = ref('')

function formatDate(value) {
  return new Intl.DateTimeFormat('fr-FR', { dateStyle: 'long' }).format(new Date(value))
}

onMounted(async () => {
  try {
    const { data } = await api.get('/users/activity-alerts/')
    members.value = data.members
  } catch {
    error.value = 'Impossible de charger les alertes d’activité.'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.activity-alerts { max-width: 900px; }
.activity-count { color: var(--gold); font-weight: 700; margin: 1.5rem 0 1rem; }
.activity-card { padding: 1.25rem; margin-bottom: .8rem; display: flex; justify-content: space-between; align-items: center; gap: 1rem; }
.activity-card p { margin: .4rem 0 0; color: var(--text-secondary); }
.member-name { color: var(--gold); font-weight: 700; }
.delay { white-space: nowrap; color: var(--gold); font-weight: 700; }
@media (max-width: 560px) { .activity-card { align-items: flex-start; flex-direction: column; } }
</style>
