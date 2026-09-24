<template>
  <div class="page auth-page">
    <div class="auth-card card">
      <h1>Confirmation de l'adresse e-mail</h1>
      <p v-if="loading">Vérification du lien…</p>
      <p v-else-if="error" class="form-error">{{ error }}</p>
      <p v-else class="alert alert-success">{{ message }}</p>
      <router-link to="/login" class="btn btn-primary">Se connecter</router-link>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import api from '../composables/useApi'

const route = useRoute()
const loading = ref(true)
const error = ref('')
const message = ref('')

onMounted(async () => {
  try {
    const { data } = await api.post('/auth/confirm-email/', {
      type: route.query.type,
      jeton: route.query.jeton,
    })
    message.value = data.detail
  } catch (e) {
    error.value = e.response?.data?.detail || 'La confirmation a échoué.'
  } finally {
    loading.value = false
  }
})
</script>
