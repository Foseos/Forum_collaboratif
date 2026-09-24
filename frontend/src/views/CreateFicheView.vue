<template>
  <div class="page create-fiche-page">
    <div class="container">

      <!-- ── En-tête ────────────────────────────────────────────────────── -->
      <div class="cf-header animate-fade-in-up">
        <router-link to="/categories/fiches-de-presentation-terminees" class="cf-back">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <polyline points="15 18 9 12 15 6"/>
          </svg>
          Retour aux fiches
        </router-link>
        <div>
          <h1 class="page-title cf-title">
            <span class="cf-title-icon">✨</span>
            Créer ma fiche de présentation
          </h1>
          <p class="page-subtitle">Soumettez votre personnage à la validation de l'équipe de Nexus Arcana</p>
        </div>
      </div>

      <!-- ── Alerte ─────────────────────────────────────────────────────── -->
      <div v-if="error" class="alert alert-danger mb-2">{{ error }}</div>

      <!-- ── Formulaire ─────────────────────────────────────────────────── -->
      <div class="card cf-form animate-fade-in-up" style="animation-delay: 0.08s">

        <p class="cf-demon-note">Si votre personnage est un <strong>démon</strong>, indiquez le nom et la description de sa forme démoniaque dans la fiche. Vous pouvez aussi ajouter une image ou un GIF. Déclarez cette forme dans le <router-link to="/topics/reglement-et-reservations-formes-demoniaques">bottin des formes démoniaques</router-link> avant de la jouer. Cette apparence n'ajoute pas de pouvoir.</p>

        <!-- Titre -->
        <div class="form-group">
          <label class="cf-label">
            Titre du sujet
            <span class="cf-required">*</span>
          </label>
          <input
            v-model="form.title"
            class="form-input cf-title-input"
            placeholder="Ex : Fiche de Présentation — Léa Moreau"
            maxlength="200"
          />
          <p class="cf-hint">Format recommandé : <em>Fiche de Présentation — Prénom Nom</em></p>
        </div>

        <!-- Contenu avec onglets -->
        <div class="form-group" style="margin-bottom: 0">
          <label class="cf-label">
            Contenu de la fiche
            <span class="cf-required">*</span>
          </label>

          <!-- Onglets Écrire / Prévisualiser -->
          <div class="editor-tabs">
            <button
              class="editor-tab"
              :class="{ active: !showPreview }"
              @click="showPreview = false"
            >
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
              </svg>
              Écrire
            </button>
            <button
              class="editor-tab"
              :class="{ active: showPreview }"
              :disabled="!form.content.trim()"
              @click="showPreview = true"
            >
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                <circle cx="12" cy="12" r="3"/>
              </svg>
              Prévisualiser
            </button>
          </div>

          <!-- Zone de rédaction -->
          <RichTextField v-if="!showPreview" v-model="form.content" label="Contenu de la fiche de présentation" placeholder="Rédigez votre fiche ou collez le modèle ici…" />

          <!-- Panneau de prévisualisation -->
          <div v-else class="preview-panel">
            <div class="preview-bar">
              <span class="preview-label">Aperçu</span>
              <span class="preview-hint">Rendu tel qu'il apparaîtra sur le forum</span>
            </div>
            <div class="preview-body" v-html="form.content"></div>
          </div>
        </div>

        <!-- Actions -->
        <div class="cf-actions">
          <router-link
            to="/categories/fiches-de-presentation-terminees"
            class="btn btn-secondary"
          >
            Annuler
          </router-link>
          <button
            class="btn btn-primary cf-submit"
            :disabled="!canSubmit || loading"
            @click="submit"
          >
            <span v-if="loading" class="spinner-small"></span>
            <svg v-else width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <line x1="22" y1="2" x2="11" y2="13"/>
              <polygon points="22 2 15 22 11 13 2 9 22 2"/>
            </svg>
            {{ loading ? 'Envoi en cours…' : 'Envoyer ma fiche' }}
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
import RichTextField from '../components/RichTextField.vue'

const router = useRouter()
const forum = useForumStore()

const form = reactive({ title: '', content: '' })
const showPreview = ref(false)
const loading = ref(false)
const error = ref('')

const canSubmit = computed(() => form.title.trim() && form.content.trim())

async function submit() {
  error.value = ''
  loading.value = true
  try {
    const data = await forum.createTopic('fiches-de-presentation-terminees', {
      title: form.title,
      first_post_content: form.content,
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
.cf-demon-note {
  margin: 0;
  padding: .85rem 1rem;
  border: 1px solid rgba(139, 92, 246, .3);
  border-radius: 8px;
  background: rgba(139, 92, 246, .08);
  color: var(--text-secondary);
  line-height: 1.6;
  font-size: .86rem;
}
.cf-demon-note a { color: var(--primary); }
.create-fiche-page {
  padding: 3rem 0;
}

/* ── En-tête ──────────────────────────────────────────────────────────────── */
.cf-header {
  margin-bottom: 2rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.cf-back {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.8rem;
  color: var(--text-secondary);
  text-decoration: none;
  transition: color var(--transition);
  width: fit-content;
}

.cf-back:hover {
  color: var(--accent);
}

.cf-title {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin-bottom: 0.25rem;
}

.cf-title-icon {
  font-size: 1.4rem;
  line-height: 1;
}

/* ── Formulaire ───────────────────────────────────────────────────────────── */
.cf-form {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.cf-label {
  display: block;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 0.5rem;
}

.cf-required {
  color: var(--accent);
  margin-left: 0.2rem;
}

.cf-title-input {
  font-size: 1rem;
}

.cf-hint {
  margin: 0.4rem 0 0;
  font-size: 0.75rem;
  color: var(--text-muted);
  font-style: italic;
}

/* ── Onglets éditeur ──────────────────────────────────────────────────────── */
.editor-tabs {
  display: flex;
  border-bottom: 1px solid var(--border);
  margin-bottom: 0;
}

.editor-tab {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.5rem 1rem;
  font-size: 0.8rem;
  font-weight: 500;
  color: var(--text-secondary);
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  margin-bottom: -1px;
  cursor: pointer;
  transition: color var(--transition), border-color var(--transition);
}

.editor-tab:hover:not(:disabled) {
  color: var(--text);
}

.editor-tab.active {
  color: var(--accent);
  border-bottom-color: var(--accent);
}

.editor-tab:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}

.editor-textarea {
  border-top-left-radius: 0;
  border-top-right-radius: 0;
  border-top: none;
  resize: vertical;
  min-height: 320px;
  font-family: 'Courier New', Courier, monospace;
  font-size: 0.85rem;
  line-height: 1.6;
}

/* ── Prévisualisation ─────────────────────────────────────────────────────── */
.preview-panel {
  border: 1px solid var(--border);
  border-top: none;
  border-radius: 0 0 var(--radius) var(--radius);
  min-height: 320px;
  overflow: hidden;
}

.preview-bar {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.4rem 0.875rem;
  background: rgba(139, 92, 246, 0.05);
  border-bottom: 1px solid var(--border);
}

.preview-label {
  font-size: 0.68rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--accent);
}

.preview-hint {
  font-size: 0.7rem;
  color: var(--text-muted);
  font-style: italic;
}

.preview-body {
  padding: 1.5rem;
  color: var(--text);
  font-size: 0.9rem;
  line-height: 1.75;
  word-break: break-word;
  overflow-x: auto;
}

/* ── Actions ──────────────────────────────────────────────────────────────── */
.cf-actions {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 0.75rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border);
  margin-top: 0.5rem;
}

.cf-submit {
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
  .cf-form {
    padding: 1.25rem;
  }

  .cf-actions {
    flex-direction: column-reverse;
    align-items: stretch;
  }

  .cf-actions .btn {
    text-align: center;
    justify-content: center;
  }
}
</style>
