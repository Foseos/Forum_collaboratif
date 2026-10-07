<template>
  <div class="page settings-page">
    <div class="container">
      <div class="page-header">
        <h1 class="page-title">Paramètres</h1>
        <p class="page-subtitle">Gérez la sécurité de votre compte.</p>
      </div>

      <section class="card settings-card">
        <h2>Changer mon mot de passe</h2>
        <p class="form-hint">Après le changement, vous devrez vous reconnecter avec votre nouveau mot de passe.</p>
        <form @submit.prevent="changePassword" class="form-grid">
          <div class="form-group">
            <label for="current-password">Mot de passe actuel</label>
            <input id="current-password" v-model="currentPassword" class="form-input" type="password" autocomplete="current-password" required />
          </div>
          <div class="form-group">
            <label for="new-password">Nouveau mot de passe</label>
            <input id="new-password" v-model="newPassword" class="form-input" type="password" autocomplete="new-password" required />
          </div>
          <div class="form-group">
            <label for="confirm-password">Confirmer le nouveau mot de passe</label>
            <input id="confirm-password" v-model="newPasswordConfirm" class="form-input" type="password" autocomplete="new-password" required />
          </div>
          <p v-if="passwordChangeError" class="form-error grid-col-2" role="alert">{{ passwordChangeError }}</p>
          <button class="btn btn-primary" type="submit" :disabled="passwordChangeLoading">
            {{ passwordChangeLoading ? 'Modification…' : 'Changer mon mot de passe' }}
          </button>
        </form>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../composables/useApi'

const router = useRouter()
const auth = useAuthStore()
const currentPassword = ref('')
const newPassword = ref('')
const newPasswordConfirm = ref('')
const passwordChangeLoading = ref(false)
const passwordChangeError = ref('')

async function changePassword() {
  passwordChangeError.value = ''
  passwordChangeLoading.value = true
  try {
    await api.post('/users/me/change-password/', {
      current_password: currentPassword.value,
      new_password: newPassword.value,
      new_password_confirm: newPasswordConfirm.value,
    })
    auth.logout()
    await router.push({ path: '/login', query: { password_changed: '1' } })
  } catch (e) {
    passwordChangeError.value = Object.values(e.response?.data || {}).flat().join(' ') || 'Le changement de mot de passe a échoué.'
  } finally {
    currentPassword.value = ''
    newPassword.value = ''
    newPasswordConfirm.value = ''
    passwordChangeLoading.value = false
  }
}
</script>

<style scoped>
.page-header { margin-bottom: 2rem; }
.form-hint { color: var(--text-muted); font-size: 0.72rem; line-height: 1.45; margin: 0.35rem 0 1.5rem; }
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
.grid-col-2 { grid-column: 1 / -1; }
.settings-card { max-width: 720px; padding: 1.5rem; }
.settings-card h2 { margin-top: 0; }
@media (max-width: 600px) {
  .form-grid { grid-template-columns: 1fr; }
}
</style>
