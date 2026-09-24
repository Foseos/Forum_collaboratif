<template>
  <div class="page auth-page"><div class="auth-card card">
    <h1>Mot de passe oublié</h1>
    <p>Indiquez le nom d'utilisateur de votre compte. Un lien sera envoyé à l'adresse e-mail associée.</p>
    <form @submit.prevent="submit">
      <div class="form-group"><label for="reset-username">Nom d'utilisateur</label>
        <input id="reset-username" v-model.trim="username" class="form-input" autocomplete="username" required /></div>
      <button class="btn btn-primary" type="submit" :disabled="loading">{{ loading ? 'Envoi…' : 'Recevoir un lien' }}</button>
    </form>
    <p v-if="message" class="alert alert-success">{{ message }}</p>
    <p v-if="error" class="form-error">{{ error }}</p>
    <div class="auth-footer"><router-link to="/login">Retour à la connexion</router-link></div>
  </div></div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../composables/useApi'
const username = ref('')
const loading = ref(false)
const message = ref('')
const error = ref('')
async function submit() {
  loading.value = true; error.value = ''; message.value = ''
  try {
    const { data } = await api.post('/auth/password-reset/', { username: username.value })
    message.value = data.detail
  } catch (e) { error.value = e.response?.data?.detail || "La demande n'a pas pu être envoyée." }
  finally { loading.value = false }
}
</script>
