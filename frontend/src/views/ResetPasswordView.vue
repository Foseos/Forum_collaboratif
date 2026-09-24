<template>
  <div class="page auth-page"><div class="auth-card card">
    <h1>Nouveau mot de passe</h1>
    <form v-if="!success" @submit.prevent="submit">
      <div class="form-group"><label for="new-password">Nouveau mot de passe</label>
        <input id="new-password" v-model="password" type="password" class="form-input" autocomplete="new-password" required /></div>
      <div class="form-group"><label for="confirm-password">Confirmer le mot de passe</label>
        <input id="confirm-password" v-model="passwordConfirm" type="password" class="form-input" autocomplete="new-password" required /></div>
      <button class="btn btn-primary" type="submit" :disabled="loading">{{ loading ? 'Enregistrement…' : 'Changer le mot de passe' }}</button>
    </form>
    <p v-if="success" class="alert alert-success">{{ success }}</p>
    <p v-if="error" class="form-error">{{ error }}</p>
    <div class="auth-footer"><router-link to="/login">Se connecter</router-link></div>
  </div></div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import api from '../composables/useApi'
const route = useRoute()
const password = ref('')
const passwordConfirm = ref('')
const loading = ref(false)
const success = ref('')
const error = ref('')
async function submit() {
  error.value = ''; loading.value = true
  try {
    const { data } = await api.post('/auth/password-reset/confirm/', {
      uid: route.query.uid, jeton: route.query.jeton,
      password: password.value, password_confirm: passwordConfirm.value,
    })
    success.value = data.detail
    password.value = ''; passwordConfirm.value = ''
  } catch (e) {
    error.value = Object.values(e.response?.data || {}).flat().join(' ') || 'Ce lien est invalide ou a expiré.'
  } finally { loading.value = false }
}
</script>
