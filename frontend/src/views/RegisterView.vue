<template>
  <div class="page auth-page">
    <div class="auth-card card">
      <h1>Inscription</h1>

      <div v-if="error" class="form-error mb-2">{{ error }}</div>

      <form @submit.prevent="handleRegister">
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
          <label for="email">Email</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            class="form-input"
            required
            autocomplete="email"
          />
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
import { useNotificationStore } from '../stores/notifications'

const auth = useAuthStore()
const notifications = useNotificationStore()
const router = useRouter()

const form = reactive({
  username: '',
  email: '',
  password: '',
  password_confirm: '',
})
const error = ref('')
const loading = ref(false)

async function handleRegister() {
  error.value = ''
  loading.value = true
  try {
    await auth.register(form)
    notifications.startPolling()
    router.push('/')
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
</script>
