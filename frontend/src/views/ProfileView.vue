<template>
  <div class="page">
    <div class="auth-page">
      <div class="auth-card card" style="max-width: 500px">
        <h1>Mon profil</h1>

        <div v-if="success" class="badge badge-primary mb-2" style="display: block; text-align: center">
          Profil mis à jour !
        </div>
        <div v-if="error" class="form-error mb-2">{{ error }}</div>

        <div class="profile-header">
          <div class="profile-avatar">
            {{ auth.user?.username?.[0]?.toUpperCase() || '?' }}
          </div>
          <div>
            <div class="profile-username">{{ auth.user?.username }}</div>
            <div class="text-sm text-secondary">
              {{ roleLabel }} &middot; Membre depuis {{ formatDate(auth.user?.date_joined) }}
            </div>
          </div>
        </div>

        <form @submit.prevent="handleUpdate">
          <div class="form-group">
            <label for="email">Email</label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label for="bio">Bio</label>
            <textarea
              id="bio"
              v-model="form.bio"
              class="form-input"
              rows="3"
              maxlength="500"
              placeholder="Parlez de vous..."
            ></textarea>
            <div class="text-sm text-secondary mt-1">
              {{ form.bio?.length || 0 }} / 500
            </div>
          </div>

          <button type="submit" class="btn btn-primary" style="width: 100%" :disabled="loading">
            {{ loading ? 'Enregistrement...' : 'Enregistrer' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()

const form = reactive({ email: '', bio: '' })
const error = ref('')
const success = ref(false)
const loading = ref(false)

const roleLabel = computed(() => {
  const roles = { admin: 'Administrateur', moderator: 'Modérateur', user: 'Utilisateur' }
  return roles[auth.user?.role] || 'Utilisateur'
})

onMounted(() => {
  form.email = auth.user?.email || ''
  form.bio = auth.user?.bio || ''
})

function formatDate(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('fr-FR', {
    month: 'long',
    year: 'numeric',
  })
}

async function handleUpdate() {
  error.value = ''
  success.value = false
  loading.value = true
  try {
    await auth.updateProfile(form)
    success.value = true
    setTimeout(() => (success.value = false), 3000)
  } catch (e) {
    error.value = "Erreur lors de la mise à jour."
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.profile-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border);
}

.profile-avatar {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: var(--primary);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 700;
  flex-shrink: 0;
}

.profile-username {
  font-size: 1.25rem;
  font-weight: 700;
}
</style>
