<template>
  <div class="page questions-page"><div class="container">
    <h1>Questions du forum en attente</h1>
    <p class="text-secondary">Sujets des rubriques « Questions invités » et « Questions membres » sans réponse de l’équipe du staff. Le compteur se retire automatiquement après une réponse du staff.</p>
    <p v-if="loading">Chargement…</p>
    <p v-else-if="error" role="alert">{{ error }}</p>
    <p v-else-if="!questions.length">Aucune question en attente.</p>
    <div v-else class="questions-list">
      <router-link v-for="question in questions" :key="`${question.category}-${question.slug}`" :to="`/topics/${question.slug}`" class="card question-card">
        <strong>{{ question.title }}</strong>
        <span>{{ question.category }} · {{ question.author }} · {{ new Date(question.created_at).toLocaleString('fr-FR') }}</span>
      </router-link>
    </div>
  </div></div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import api from '../composables/useApi'

const questions = ref([])
const loading = ref(true)
const error = ref('')
onMounted(async () => {
  try { questions.value = (await api.get('/administration/contact/', { params: { kind: 'forum_questions' } })).data }
  catch { error.value = 'Impossible de charger les questions.' }
  finally { loading.value = false }
})
</script>

<style scoped>
.questions-page { padding: 2.5rem 0; }
.questions-page h1 { color: var(--accent); }
.questions-list { display: grid; gap: .8rem; margin-top: 1.5rem; }
.question-card { display: grid; gap: .35rem; padding: 1rem 1.25rem; text-decoration: none; }
.question-card span { color: var(--text-secondary); font-size: .85rem; }
</style>
