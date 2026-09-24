<template>
  <div class="page auth-page">
    <div class="auth-card card">
      <h1>Inscription</h1>

      <div v-if="error" class="form-error mb-2">{{ error }}</div>
      <div v-if="registered" class="alert alert-success mb-2">Un lien de confirmation a été envoyé à {{ form.email }}. Ouvrez-le pour activer votre compte avant de vous connecter.</div>

      <form v-if="!registered" @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="username">Nom d'utilisateur</label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            class="form-input"
            required
            autocomplete="username"
          />
        </div>

        <div class="form-group">
          <label for="email">Adresse e-mail personnelle</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            class="form-input"
            required
            autocomplete="email"
          />
          <p class="text-secondary" style="font-size:.78rem;line-height:1.55;margin:.4rem 0 0">Chaque compte doit avoir une adresse différente, même s'il s'agit d'un double compte.</p>
        </div>

        <div class="form-group">
          <label for="password">Mot de passe</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            class="form-input"
            required
            autocomplete="new-password"
          />
        </div>

        <div class="form-group">
          <label for="password_confirm">Confirmer le mot de passe</label>
          <input
            id="password_confirm"
            v-model="form.password_confirm"
            type="password"
            class="form-input"
            required
            autocomplete="new-password"
          />
        </div>

        <button type="submit" class="btn btn-primary" style="width: 100%" :disabled="loading">
          {{ loading ? 'Inscription...' : "S'inscrire" }}
        </button>
      </form>

      <div v-if="registered" class="form-group">
        <button type="button" class="btn btn-secondary" :disabled="loading" @click="resendConfirmation">Renvoyer le lien de confirmation</button>
        <p v-if="resendMessage" class="text-secondary">{{ resendMessage }}</p>
      </div>

      <div class="auth-footer">
        Déjà un compte ?
        <router-link to="/login">Se connecter</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../composables/useApi'

const auth = useAuthStore()
const router = useRouter()

const form = reactive({
  username: '',
  email: '',
  password: '',
  password_confirm: '',
})
const error = ref('')
const loading = ref(false)
const registered = ref(false)
const resendMessage = ref('')

async function handleRegister() {
  error.value = ''
  loading.value = true
  try {
    await auth.register(form)
    registered.value = true
  } catch (e) {
    const data = e.response?.data
    if (data) {
      const messages = Object.values(data).flat()
      error.value = messages.join(' ')
    } else {
      error.value = "Erreur lors de l'inscription."
    }
  } finally {
    loading.value = false
  }
}

async function resendConfirmation() {
  loading.value = true
  try {
    const { data } = await api.post('/auth/resend-confirmation/', {
      username: form.username, password: form.password,
    })
    resendMessage.value = data.detail
  } catch (e) {
    resendMessage.value = e.response?.data?.detail || "Le renvoi a échoué. Réessayez dans quelques instants."
  } finally {
    loading.value = false
  }
}
</script>
