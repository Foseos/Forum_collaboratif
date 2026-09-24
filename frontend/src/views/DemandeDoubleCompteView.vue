<template>
  <div class="page ddc-page">
    <div class="container">

      <!-- ── En-tête ────────────────────────────────────────────────────── -->
      <div class="ddc-header animate-fade-in-up">
        <router-link to="/categories/demande-double-compte" class="ddc-back">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <polyline points="15 18 9 12 15 6"/>
          </svg>
          Retour aux demandes
        </router-link>
        <div>
          <h1 class="page-title ddc-title">
            <span class="ddc-title-icon">👥</span>
            Demande de double compte
          </h1>
          <p class="page-subtitle">Remplissez le formulaire ci-dessous — l'équipe de Nexus Arcana étudiera votre demande</p>
        </div>
      </div>

      <!-- ── Alerte ─────────────────────────────────────────────────────── -->
      <div v-if="error" class="alert alert-danger mb-2">{{ error }}</div>

      <!-- ── Formulaire ─────────────────────────────────────────────────── -->
      <div class="card ddc-form animate-fade-in-up" style="animation-delay: 0.08s">

        <!-- Nom du personnage -->
        <div class="form-group">
          <label class="ddc-label">
            Nom du personnage
            <span class="ddc-required">*</span>
          </label>
          <input
            v-model="form.nom"
            class="form-input"
            placeholder="Ex : Elena Blackwood"
            maxlength="100"
          />
        </div>

        <!-- Nature -->
        <div class="form-group">
          <label class="ddc-label">
            Nature
            <span class="ddc-required">*</span>
          </label>
          <input
            v-model="form.nature"
            class="form-input"
            placeholder="Ex : Sorcière, Démon, Fantôme…"
            maxlength="100"
          />
          <p class="ddc-hint">Race / type de créature de votre second personnage</p>
        </div>

        <!-- Avatar -->
        <div class="form-group">
          <label class="ddc-label">
            Avatar
            <span class="ddc-required">*</span>
          </label>
          <input
            v-model="form.avatar"
            class="form-input"
            placeholder="Ex : Alyssa Milano"
            maxlength="100"
          />
          <p class="ddc-hint">Célébrité souhaitée comme avatar : <router-link to="/categories/bottin-des-avatars">vérifier le bottin des avatars</router-link>.</p>
        </div>

        <!-- Petit récit / ébauche d'idées -->
        <div class="form-group">
          <label class="ddc-label">
            Petit récit / ébauche d'idées
            <span class="ddc-required">*</span>
          </label>
          <textarea
            v-model="form.recit"
            class="form-input ddc-textarea"
            rows="8"
            placeholder="Présentez brièvement votre second personnage : son histoire, ses motivations, ses liens potentiels avec l'univers du forum…"
          ></textarea>
        </div>

        <!-- Actions -->
        <div class="ddc-actions">
          <router-link to="/categories/demande-double-compte" class="btn btn-secondary">
            Annuler
          </router-link>
          <button
            class="btn btn-primary ddc-submit"
            :disabled="!canSubmit || loading"
            @click="submit"
          >
            <span v-if="loading" class="spinner-small"></span>
            <svg v-else width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <line x1="22" y1="2" x2="11" y2="13"/>
              <polygon points="22 2 15 22 11 13 2 9 22 2"/>
            </svg>
            {{ loading ? 'Envoi en cours…' : 'Envoyer ma demande' }}
          </button>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useForumStore } from '../stores/forum'

const router = useRouter()
const forum = useForumStore()

const form = reactive({ nom: '', nature: '', avatar: '', recit: '' })
const loading = ref(false)
const error = ref('')

const canSubmit = computed(() =>
  form.nom.trim() && form.nature.trim() && form.avatar.trim() && form.recit.trim()
)

async function submit() {
  error.value = ''
  loading.value = true
  try {
    const content = `
<p><strong>Nom du personnage :</strong> ${form.nom}</p>
<p><strong>Nature :</strong> ${form.nature}</p>
<p><strong>Avatar :</strong> ${form.avatar}</p>
<hr/>
<p><strong>Petit récit / ébauche d'idées :</strong></p>
<p>${form.recit.replace(/\n/g, '<br/>')}</p>
`.trim()

    const data = await forum.createTopic('demande-double-compte', {
      title: `Demande de double compte — ${form.nom}`,
      first_post_content: content,
    })
    router.push(`/topics/${data.slug}`)
  } catch (e) {
    error.value = e.response?.data?.detail || 'Une erreur est survenue. Veuillez réessayer.'
    window.scrollTo({ top: 0, behavior: 'smooth' })
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.ddc-page {
  padding: 3rem 0;
}

/* ── En-tête ──────────────────────────────────────────────────────────────── */
.ddc-header {
  margin-bottom: 2rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.ddc-back {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.8rem;
  color: var(--text-secondary);
  text-decoration: none;
  transition: color var(--transition);
  width: fit-content;
}

.ddc-back:hover {
  color: var(--accent);
}

.ddc-title {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin-bottom: 0.25rem;
}

.ddc-title-icon {
  font-size: 1.4rem;
  line-height: 1;
}

/* ── Formulaire ───────────────────────────────────────────────────────────── */
.ddc-form {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.ddc-label {
  display: block;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 0.5rem;
}

.ddc-required {
  color: var(--accent);
  margin-left: 0.2rem;
}

.ddc-hint {
  margin: 0.4rem 0 0;
  font-size: 0.75rem;
  color: var(--text-muted);
  font-style: italic;
}

.ddc-textarea {
  resize: vertical;
  min-height: 160px;
  font-size: 0.9rem;
  line-height: 1.6;
}

/* ── Actions ──────────────────────────────────────────────────────────────── */
.ddc-actions {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 0.75rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border);
  margin-top: 0.5rem;
}

.ddc-submit {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* ── Alert ────────────────────────────────────────────────────────────────── */
.alert {
  padding: 0.875rem 1.25rem;
  border-radius: var(--radius);
  font-weight: 500;
}

.alert-danger {
  background: rgba(239, 68, 68, 0.12);
  color: #f87171;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.mb-2 {
  margin-bottom: 1rem;
}

/* ── Spinner ──────────────────────────────────────────────────────────────── */
.spinner-small {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  display: inline-block;
  flex-shrink: 0;
}

@media (max-width: 600px) {
  .ddc-form {
    padding: 1.25rem;
  }

  .ddc-actions {
    flex-direction: column-reverse;
    align-items: stretch;
  }

  .ddc-actions .btn {
    text-align: center;
    justify-content: center;
  }
}
</style>
