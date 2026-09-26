<template>
  <div class="page contact-page">
    <div class="container contact-wrap">
      <h1>Contacter l’administration</h1>
      <p>Utilisez ce formulaire pour une question sur vos données, signaler un contenu ou demander de l’aide. Votre demande est visible uniquement par l’administration.</p>
      <form class="card contact-form" @submit.prevent="submit">
        <label for="contact-kind">Motif</label>
        <select id="contact-kind" v-model="form.kind" class="form-input">
          <option value="privacy">Mes données personnelles ou la suppression de mon compte</option>
          <option value="report">Signaler un message ou une image</option>
          <option value="general">Autre question</option>
        </select>
        <template v-if="form.kind === 'report'">
          <label for="contact-post">Numéro du message concerné</label>
          <input id="contact-post" v-model.number="form.post" type="number" min="1" class="form-input" required />
          <p class="contact-hint">Depuis un message, le bouton « Signaler » remplit ce numéro automatiquement.</p>
        </template>
        <template v-if="!auth.isAuthenticated">
          <label for="contact-email">Votre adresse e-mail pour recevoir une réponse</label>
          <input id="contact-email" v-model.trim="form.email" type="email" class="form-input" required autocomplete="email" />
        </template>
        <label for="contact-message">Votre demande</label>
        <textarea id="contact-message" v-model.trim="form.message" class="form-input" rows="7" minlength="10" maxlength="3000" required></textarea>
        <button class="btn btn-primary" :disabled="sending">{{ sending ? 'Envoi…' : 'Envoyer à l’administration' }}</button>
        <p v-if="error" class="form-error" role="alert">{{ error }}</p>
        <p v-if="success" class="alert alert-success" role="status">{{ success }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import api from '../composables/useApi'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const auth = useAuthStore()
const form = reactive({ kind: route.query.post ? 'report' : 'privacy', post: Number(route.query.post) || '', email: '', message: '' })
const sending = ref(false)
const error = ref('')
const success = ref('')

watch(() => route.query.post, value => {
  if (value) { form.kind = 'report'; form.post = Number(value) || '' }
})

async function submit() {
  sending.value = true
  error.value = ''
  success.value = ''
  try {
    const payload = { kind: form.kind, message: form.message }
    if (form.kind === 'report') payload.post = form.post
    if (!auth.isAuthenticated) payload.email = form.email
    const { data } = await api.post('/contact/', payload)
    success.value = data.detail
    form.message = ''
  } catch (failure) {
    const data = failure.response?.data
    error.value = data?.detail || Object.values(data || {}).flat().join(' ') || 'Envoi impossible pour le moment.'
  } finally {
    sending.value = false
  }
}
</script>

<style scoped>
.contact-page { padding: 2.5rem 0; }
.contact-wrap { max-width: 760px; }
.contact-wrap h1 { color: var(--accent); margin-bottom: .5rem; }
.contact-wrap > p { color: var(--text-secondary); line-height: 1.6; }
.contact-form { display: grid; gap: .75rem; padding: 1.5rem; margin-top: 1.25rem; }
.contact-form label { font-weight: 600; }
.contact-form button { justify-self: start; margin-top: .5rem; }
.contact-hint { color: var(--text-secondary); font-size: .85rem; margin: 0; }
</style>
