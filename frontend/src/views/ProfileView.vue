<template>
  <div class="page profile-page">
    <div class="container">
      <div class="page-header">
        <h1 class="page-title">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          Carte d'Identité Magique
        </h1>
        <p class="page-subtitle">Gérez les informations de votre personnage</p>
      </div>

      <div v-if="success" class="alert alert-success mt-2 mb-3">
        Profil mis à jour avec succès !
      </div>
      <div v-if="error" class="alert alert-danger mt-2 mb-3">
        {{ error }}
      </div>

      <form @submit.prevent="handleUpdate" class="id-card-form">
        <div class="card id-card">
          <!-- Left Column: Avatar & Character Info -->
          <div class="id-left">
            <div class="avatar-section">
              <div class="character-name-display">
                {{ auth.user?.username || 'Inconnu' }}
              </div>
              <div class="avatar-preview" @click="triggerAvatarUpload" style="cursor: pointer;" title="Cliquer pour changer la photo de profil">
                <img v-if="previewImage || auth.user?.avatar" :src="previewImage || auth.user?.avatar" alt="Avatar" class="avatar-img" />
                <div v-else class="avatar-placeholder">
                  <span>{{ auth.user?.username?.[0]?.toUpperCase() || '?' }}</span>
                </div>
                <div class="avatar-upload-btn">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
                  <span v-if="previewImage">Prête à sauvegarder</span>
                </div>
              </div>
              <input ref="fileInputRef" id="avatar-upload" type="file" accept="image/*" @change="handleImageChange" class="hidden-input" />
              <div class="form-group mb-1">
                <input v-if="isAvatarAdmin" type="text" v-model="form.avatar_name" class="form-input text-center text-sm" placeholder="Nom de la célébrité" />
                <p v-else class="text-sm text-center">{{ form.avatar_name || 'Célébrité à confirmer par l’administration' }}</p>
              </div>
              <div v-if="form.profile_gif_url" class="profile-gif-preview">
                <img :src="form.profile_gif_url" alt="Aperçu du GIF de profil" />
              </div>
              <div class="form-group profile-gif-field">
                <label for="profile-gif-url">Petit GIF de profil</label>
                <input id="profile-gif-url" v-model.trim="form.profile_gif_url" class="form-input" type="url" maxlength="500" placeholder="https://…/animation.gif" />
                <p class="form-hint">Collez un lien direct vers un GIF. Il apparaîtra sous votre avatar ; laissez vide pour le retirer.</p>
              </div>

              <div v-if="auth.user?.groupe || auth.user?.race" class="group-badges">
                <div v-if="auth.user?.groupe" class="group-badge badge-faction">
                  <span class="badge-icon">⚜</span>
                  <div class="badge-text">
                    <span class="badge-label">Faction</span>
                    <span class="badge-value">{{ auth.user.groupe }}</span>
                  </div>
                </div>
                <div v-if="auth.user?.race" class="group-badge badge-race">
                  <span class="badge-icon">✦</span>
                  <div class="badge-text">
                    <span class="badge-label">Espèce</span>
                    <span class="badge-value">{{ auth.user.race }}</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="character-stats">
              <!-- Sexe (Radio buttons custom) -->
              <div class="form-group">
                <label>Sexe</label>
                <div class="radio-group">
                  <label class="radio-label">
                    <input type="radio" v-model="form.sexe" value="feminin" name="sexe" />
                    <span class="radio-btn">Féminin</span>
                  </label>
                  <label class="radio-label">
                    <input type="radio" v-model="form.sexe" value="masculin" name="sexe" />
                    <span class="radio-btn">Masculin</span>
                  </label>
                  <label class="radio-label">
                    <input type="radio" v-model="form.sexe" value="indetermine" name="sexe" />
                    <span class="radio-btn">Indéterminé</span>
                  </label>
                </div>
              </div>

              <div class="form-group">
                <label>Nature</label>
                <input type="text" :value="auth.user?.nature || 'Non définie'" class="form-input" readonly />
                <p class="form-hint">La fondatrice attribue l’espèce et sa spécialité après validation.</p>
              </div>

              <div class="form-group">
                <label>Camp</label>
                <input type="text" v-model="form.camp" class="form-input" placeholder="Ex: Bien, Mal, Neutre..." />
              </div>

            </div>
          </div>

          <!-- Right Column: Details -->
          <div class="id-right">
            <!-- Header Meta -->
            <div class="id-meta">
              <div class="id-meta-item">
                <span class="meta-label">Messages</span>
                <span class="meta-value">{{ auth.user?.messages_count || 0 }}</span>
              </div>
              <div class="id-meta-item">
                <span class="meta-label">Inscription</span>
                <span class="meta-value">{{ formatDate(auth.user?.date_joined) }}</span>
              </div>
              <div class="id-meta-item">
                <span class="meta-label">Fiche</span>
                <span class="meta-value">{{ ficheStatusLabel(auth.user?.fiche_status) }}</span>
              </div>
              <div class="id-meta-item">
                <span class="meta-label">Disponibilité RP</span>
                <span class="meta-value">{{ rpAvailabilityLabel(form.rp_availability) }}</span>
              </div>
              <div class="id-meta-item">
                <span class="meta-label">Solde Arcana Flouz</span>
                <span class="meta-value text-gold">{{ auth.user?.compte_bancaire || 0 }} Arcana Flouz</span>
              </div>
            </div>

            <div class="divider"></div>

            <div class="profile-sheet-links">
              <div class="profile-sheet-item">
                <span class="meta-label">Présentation validée</span>
                <router-link v-if="auth.user?.presentation_topic_slug" :to="`/topics/${auth.user.presentation_topic_slug}`" class="btn btn-secondary btn-sm">Voir ma présentation</router-link>
                <span v-else class="form-hint">Aucune présentation archivée pour ce compte.</span>
              </div>
              <div class="profile-sheet-item">
                <span class="meta-label">Carnet du personnage</span>
                <router-link v-if="auth.user?.recap_topic_slug" :to="`/topics/${auth.user.recap_topic_slug}`" class="btn btn-secondary btn-sm">Voir mon carnet</router-link>
                <router-link v-else-if="auth.user?.fiche_status === 'validated'" to="/categories/fiche-personnage" class="btn btn-secondary btn-sm">Créer mon carnet</router-link>
                <span v-else class="form-hint">Disponible après validation de la présentation.</span>
              </div>
            </div>

            <div class="form-grid">
              <div class="form-group grid-col-2">
                <label>Nom d'utilisateur</label>
                <input type="text" v-model="form.username" class="form-input" autocomplete="username" readonly />
                <p class="form-hint">Nom de votre compte, choisi lors de l'inscription.</p>
              </div>

              <div class="form-group grid-col-2">
                <label>Pseudo RP</label>
                <input type="text" v-model="form.pseudo" class="form-input" placeholder="Votre surnom de joueur (facultatif)" />
                <p class="form-hint">Le pseudo que vous utilisez dans les jeux. Il peut être différent du nom d'utilisateur.</p>
              </div>

              <div class="form-group grid-col-2">
                <label>Disponibilité pour les RP</label>
                <select v-model="form.rp_availability" class="form-input">
                  <option value="open">Ouvert aux RP</option>
                  <option value="discuss">À discuter</option>
                  <option value="unavailable">Indisponible</option>
                </select>
                <p class="form-hint">Cette indication apparaît sur votre profil public et peut être changée à tout moment.</p>
              </div>

              <div class="form-group">
                <label>Âge du personnage</label>
                <input type="text" v-model="form.age_personnage" class="form-input" placeholder="Ex: 24 ans" />
              </div>

              <div class="form-group">
                <label>Double compte (DC)</label>
                <input type="text" v-model="form.double_compte" class="form-input" placeholder="Pseudo du compte principal si DC" />
              </div>

              <div class="form-group grid-col-2">
                <label>Lieu de résidence</label>
                <input type="text" v-model="form.lieu_residence" class="form-input" placeholder="Ex: Manoir Halliwell, Underworld..." />
              </div>

              <div class="form-group grid-col-2">
                <label>Quartier résidentiel</label>
                <input type="text" v-model="form.quartier_residentiel" class="form-input" placeholder="Ex: Russian Hill, French Quarter, Beacon Hills North..." />
              </div>

              <div class="form-group grid-col-2">
                <label>Situation sociale & familiale</label>
                <input type="text" v-model="form.situation" class="form-input" placeholder="Ex: Célibataire, employé au P3..." />
              </div>

              <div class="form-group grid-col-2">
                <label>Métier</label>
                <input type="text" v-model="form.metier" class="form-input" placeholder="Ex: Propriétaire du P3, Chasseur de primes..." />
              </div>

              <div class="form-group grid-col-2">
                <label>Pouvoirs magiques</label>
                <textarea v-model="form.pouvoirs" class="form-input" rows="3" placeholder="Glace, télékinésie, etc."></textarea>
              </div>

              <div class="form-group grid-col-2">
                <label>Biographie</label>
                <textarea v-model="form.bio" class="form-input" rows="4" placeholder="Histoire courte de votre personnage..."></textarea>
              </div>

              <div class="form-group grid-col-2">
                <label>Signature</label>
                <textarea
                  v-model="form.signature"
                  class="form-input"
                  rows="3"
                  placeholder="Votre texte de signature ou le lien direct d'un GIF/image (https://...gif)"
                ></textarea>
                <p class="form-hint">La signature s'affichera sous vos messages. Collez une URL directe d'image ou de GIF pour l'animer.</p>
              </div>

              <div class="form-group grid-col-2">
                <label>Crédits</label>
                <textarea v-model="form.credits" class="form-input" rows="2" placeholder="Crédits des images, GIFs ou ressources utilisées sur votre profil"></textarea>
              </div>
            </div>

            <div class="form-actions">
              <button type="submit" class="btn btn-primary" :disabled="loading">
                <svg v-if="!loading" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
                <span v-else class="spinner-small"></span>
                {{ loading ? 'Sauvegarde mystique...' : 'Mettre à jour le grimoire' }}
              </button>
            </div>
          </div>
        </div>
      </form>

      <section class="card" style="margin-top:1.5rem;padding:1.5rem">
        <h2 style="margin-top:0">Adresse e-mail du compte</h2>
        <p class="text-secondary">Adresse actuelle : {{ auth.user?.email || 'Non renseignée' }}</p>
        <p class="form-hint">Pour la modifier, confirmez votre mot de passe. Un lien sera envoyé à la nouvelle adresse et votre adresse actuelle sera avertie.</p>
        <form @submit.prevent="requestEmailChange" class="form-grid">
          <div class="form-group">
            <label for="new-email">Nouvelle adresse e-mail</label>
            <input id="new-email" v-model.trim="newEmail" class="form-input" type="email" autocomplete="email" required />
          </div>
          <div class="form-group">
            <label for="email-password">Mot de passe actuel</label>
            <input id="email-password" v-model="emailPassword" class="form-input" type="password" autocomplete="current-password" required />
          </div>
          <p v-if="emailChangeError" class="form-error grid-col-2">{{ emailChangeError }}</p>
          <p v-if="emailChangeSuccess" class="alert alert-success grid-col-2">{{ emailChangeSuccess }}</p>
          <button class="btn btn-secondary" type="submit" :disabled="emailChangeLoading">{{ emailChangeLoading ? 'Envoi…' : 'Confirmer le changement' }}</button>
        </form>
      </section>

      <section class="card" style="margin-top:1rem;padding:1.5rem">
        <h2 style="margin-top:0">Mot de passe du compte</h2>
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
          <button class="btn btn-secondary" type="submit" :disabled="passwordChangeLoading">{{ passwordChangeLoading ? 'Modification…' : 'Changer mon mot de passe' }}</button>
        </form>
      </section>

      <section class="card" style="margin-top:1rem;padding:1.5rem">
        <h2 style="margin-top:0">Alertes par e-mail</h2>
        <label><input type="checkbox" :checked="auth.user?.email_topic_replies !== false" @change="saveReplyEmailPreference($event.target.checked)" /> Recevoir un e-mail lorsqu’un sujet auquel j’ai participé reçoit une réponse</label>
        <p v-if="replyEmailFeedback" role="status" class="form-hint">{{ replyEmailFeedback }}</p>
      </section>

      <section v-if="auth.user?.fiche_status === 'validated'" class="card" style="margin-top:1rem;padding:1.5rem">
        <h2 style="margin-top:0">Mes premiers pas sur Nexus Arcana</h2>
        <p class="text-secondary">Quelques pistes pour lancer votre personnage à votre rythme.</p>
        <ul v-if="nextSteps" class="next-steps-list">
          <li><span>{{ nextSteps?.recap ? '✓' : '○' }}</span> <router-link to="/categories/fiche-personnage">Publier ma fiche personnage récapitulative</router-link></li>
          <li><span>{{ nextSteps?.housing ? '✓' : '○' }}</span> <router-link to="/topics/agence-immobiliere-demande-de-logement">Trouver un logement</router-link></li>
          <li><span>{{ nextSteps?.rp_search ? '✓' : '○' }}</span> <router-link to="/topics/demande-de-partenaire-de-rp">Chercher un partenaire de RP</router-link></li>
        </ul>
        <p v-else class="text-secondary">Chargement des étapes…</p>
      </section>

      <section class="card" style="margin-top:1rem;padding:1.5rem">
        <h2 style="margin-top:0">Historique des Arcana Flouz</h2>
        <p class="text-secondary">Solde actuel : {{ auth.user?.compte_bancaire || 0 }} Arcana Flouz</p>
        <p v-if="arcanaHistoryError" role="alert">{{ arcanaHistoryError }}</p>
        <ul v-else-if="arcanaHistory.length" class="arcana-history-list">
          <li v-for="(entry, index) in arcanaHistory" :key="index">
            <span>{{ entry.reason }} <small>· {{ formatDate(entry.created_at) }}</small></span>
            <strong>{{ entry.amount > 0 ? '+' : '' }}{{ entry.amount }}</strong>
          </li>
        </ul>
        <p v-else class="text-secondary">Aucun mouvement enregistré pour le moment.</p>
      </section>

      <!-- ── Sujets créés ── -->
      <div class="topics-panel card" style="margin-top: 2rem;">
        <div class="topics-panel-header" @click="toggleCreatedTopics">
          <span class="topics-panel-title">📜 Sujets créés</span>
          <span class="topics-panel-toggle">{{ showCreatedTopics ? '▲' : '▼' }}</span>
        </div>
        <div v-if="showCreatedTopics" class="topics-panel-body">
          <div v-if="loadingCreated" class="topics-loading">Chargement…</div>
          <ul v-else-if="createdTopics.length" class="topics-list-ul">
            <li v-for="t in createdTopics" :key="t.slug" class="topics-list-item">
              <router-link :to="`/topics/${t.slug}`" class="topics-list-link">
                {{ t.title }}
              </router-link>
              <span class="topics-list-meta">{{ formatDate(t.created_at) }}</span>
            </li>
          </ul>
          <p v-else class="topics-empty">Aucun sujet créé pour l'instant.</p>
        </div>
      </div>

      <!-- ── Sujets avec réponse ── -->
      <div class="topics-panel card" style="margin-top: 1rem;">
        <div class="topics-panel-header" @click="toggleParticipatedTopics">
          <span class="topics-panel-title">💬 Sujets avec participation</span>
          <span class="topics-panel-toggle">{{ showParticipatedTopics ? '▲' : '▼' }}</span>
        </div>
        <div v-if="showParticipatedTopics" class="topics-panel-body">
          <div v-if="loadingParticipated" class="topics-loading">Chargement…</div>
          <ul v-else-if="participatedTopics.length" class="topics-list-ul">
            <li v-for="t in participatedTopics" :key="t.slug" class="topics-list-item">
              <router-link :to="`/topics/${t.slug}`" class="topics-list-link">
                {{ t.title }}
              </router-link>
              <span class="topics-list-meta">{{ formatDate(t.created_at) }}</span>
            </li>
          </ul>
          <p v-else class="topics-empty">Aucune participation pour l'instant.</p>
        </div>
      </div>

      <!-- ── Panneau Admin : Gestion Arcana Flouz ── -->
      <div v-if="auth.user?.role === 'admin' || auth.user?.role === 'fondatrice'" class="admin-icoin-panel card" style="margin-top: 1rem;">
      <div class="admin-icoin-header" @click="showAdminIcoin = !showAdminIcoin">
        <span class="admin-icoin-title">⚙️ Admin — Validation des fiches & Arcana Flouz</span>
        <span class="admin-icoin-toggle">{{ showAdminIcoin ? '▲' : '▼' }}</span>
      </div>

      <div v-if="showAdminIcoin" class="admin-icoin-body">
        <!-- Recherche utilisateur -->
        <div class="form-group">
          <label>Rechercher un membre</label>
          <input
            type="text"
            v-model="adminSearch"
            class="form-input"
            placeholder="Nom d'utilisateur..."
            @input="filterAdminUsers"
          />
          <ul v-if="adminFiltered.length && !adminSelectedUser" class="admin-user-dropdown">
            <li
              v-for="u in adminFiltered"
              :key="u.id"
              class="admin-user-item"
              @click="selectAdminUser(u)"
            >
              <span class="admin-user-name">{{ u.username }}</span>
              <span class="admin-user-balance">{{ u.compte_bancaire }} Arcana Flouz</span>
            </li>
          </ul>
        </div>

        <!-- Utilisateur sélectionné -->
        <div v-if="adminSelectedUser" class="admin-selected-user">
          <div class="admin-selected-info">
            <strong class="admin-selected-name">{{ adminSelectedUser.username }}</strong>
            <span class="admin-selected-current">Solde actuel : <strong class="text-gold">{{ adminSelectedUser.compte_bancaire }} Arcana Flouz</strong></span>
            <span class="admin-selected-current">Fiche : <strong>{{ ficheStatusLabel(adminSelectedUser.fiche_status) }}</strong></span>
            <button class="btn-link" @click="adminSelectedUser = null; adminSearch = ''">✕ Changer</button>
          </div>
          <div class="admin-icoin-edit">
            <label>Nouveau solde Arcana Flouz</label>
            <div class="admin-icoin-input-row">
              <input
                type="number"
                v-model.number="adminNewBalance"
                class="form-input"
                min="0"
                placeholder="Montant..."
              />
              <button
                class="btn btn-primary"
                :disabled="adminSaving || adminNewBalance === null"
                @click="saveAdminIcoin"
              >
                {{ adminSaving ? 'Enregistrement…' : '💾 Enregistrer' }}
              </button>
            </div>
            <p v-if="adminIcoinSuccess" class="admin-icoin-success">✓ Solde mis à jour avec succès !</p>
            <p v-if="adminIcoinError" class="admin-icoin-error">{{ adminIcoinError }}</p>
          </div>
          <div class="admin-icoin-edit" style="margin-top: .8rem;">
            <label>Statut de la fiche personnage</label>
            <div class="admin-icoin-input-row">
              <select v-model="adminSelectedUser.fiche_status" class="form-input">
                <option value="pending">En attente</option>
                <option value="validated">Validée</option>
                <option value="rejected">À corriger</option>
              </select>
              <button class="btn btn-primary" :disabled="adminSaving" @click="saveFicheStatus">
                {{ adminSaving ? 'Enregistrement…' : 'Valider le statut' }}
              </button>
            </div>
          </div>
        </div>
      </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { useAuthStore } from '../stores/auth'
import api from '../composables/useApi'
import { useRouter } from 'vue-router'

const router = useRouter()

const auth = useAuthStore()
const isAvatarAdmin = computed(() => ['admin', 'fondatrice'].includes(auth.user?.role))

const form = reactive({
  username: '',
  email: '',
  bio: '',
  signature: '',
  profile_gif_url: '',
  sexe: '',
  nature: '',
  camp: '',
  pseudo: '',
  rp_availability: 'discuss',
  situation: '',
  metier: '',
  age_personnage: '',
  pouvoirs: '',
  lieu_residence: '',
  quartier_residentiel: '',
  credits: '',
  avatar_name: '',
  double_compte: ''
})

const fileInputRef = ref(null)
const selectedFile = ref(null)
const previewImage = ref(null)
const uploadingAvatar = ref(false)
const error = ref('')
const success = ref(false)
const loading = ref(false)
const newEmail = ref('')
const emailPassword = ref('')
const emailChangeLoading = ref(false)
const emailChangeError = ref('')
const emailChangeSuccess = ref('')
const currentPassword = ref('')
const newPassword = ref('')
const newPasswordConfirm = ref('')
const passwordChangeLoading = ref(false)
const passwordChangeError = ref('')
const replyEmailFeedback = ref('')
const arcanaHistory = ref([])
const arcanaHistoryError = ref('')
const nextSteps = ref(null)

async function saveReplyEmailPreference(enabled) {
  try {
    await auth.updateProfile({ email_topic_replies: enabled })
    replyEmailFeedback.value = 'Préférence enregistrée.'
  } catch {
    replyEmailFeedback.value = 'Impossible d’enregistrer cette préférence.'
    await auth.fetchProfile()
  }
}

async function loadProfileExtras() {
  try {
    const { data } = await api.get('/arcana/history/')
    arcanaHistory.value = data
  } catch {
    arcanaHistoryError.value = 'Impossible de charger l’historique.'
  }
  if (auth.user?.fiche_status === 'validated') {
    try {
      const { data } = await api.get('/next-steps/')
      nextSteps.value = data
    } catch { nextSteps.value = null }
  }
}

onMounted(loadProfileExtras)
watch(() => auth.user?.fiche_status, (status) => {
  if (status === 'validated' && !nextSteps.value) loadProfileExtras()
})

async function requestEmailChange() {
  emailChangeError.value = ''
  emailChangeSuccess.value = ''
  emailChangeLoading.value = true
  try {
    const { data } = await api.post('/auth/request-email-change/', {
      email: newEmail.value, password: emailPassword.value,
    })
    emailChangeSuccess.value = data.detail
    emailPassword.value = ''
  } catch (e) {
    emailChangeError.value = Object.values(e.response?.data || {}).flat().join(' ') || "Le changement d'adresse a échoué."
  } finally {
    emailChangeLoading.value = false
  }
}

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

function triggerAvatarUpload() {
  fileInputRef.value?.click()
}

// ── Topics panels ─────────────────────────────────────────────────
const showCreatedTopics = ref(false)
const showParticipatedTopics = ref(false)
const createdTopics = ref([])
const participatedTopics = ref([])
const loadingCreated = ref(false)
const loadingParticipated = ref(false)

async function toggleCreatedTopics() {
  showCreatedTopics.value = !showCreatedTopics.value
  if (showCreatedTopics.value && !createdTopics.value.length) {
    loadingCreated.value = true
    try {
      const { data } = await api.get(`/topics/?author=${auth.user.id}&ordering=-created_at`)
      createdTopics.value = data.results || data
    } catch { /* silent */ } finally {
      loadingCreated.value = false
    }
  }
}

async function toggleParticipatedTopics() {
  showParticipatedTopics.value = !showParticipatedTopics.value
  if (showParticipatedTopics.value && !participatedTopics.value.length) {
    loadingParticipated.value = true
    try {
      const { data } = await api.get('/topics/participated/')
      participatedTopics.value = data.results || data
    } catch { /* silent */ } finally {
      loadingParticipated.value = false
    }
  }
}

// ── Admin Arcana Flouz panel ──────────────────────────────────────────────
const showAdminIcoin = ref(false)
const adminSearch = ref('')
const adminAllUsers = ref([])
const adminFiltered = ref([])
const adminSelectedUser = ref(null)
const adminNewBalance = ref(null)
const adminSaving = ref(false)
const adminIcoinSuccess = ref(false)
const adminIcoinError = ref('')

watch(showAdminIcoin, async (val) => {
  if (val && !adminAllUsers.value.length) {
    try {
      const { data } = await api.get('/users/')
      adminAllUsers.value = data.results || data
    } catch { /* silent */ }
  }
})

function filterAdminUsers() {
  adminSelectedUser.value = null
  const q = adminSearch.value.trim().toLowerCase()
  if (!q) { adminFiltered.value = []; return }
  adminFiltered.value = adminAllUsers.value
    .filter(u => u.username.toLowerCase().includes(q))
    .slice(0, 8)
}

function selectAdminUser(u) {
  adminSelectedUser.value = { ...u }
  adminNewBalance.value = u.compte_bancaire
  adminSearch.value = u.username
  adminFiltered.value = []
}

async function saveAdminIcoin() {
  adminIcoinSuccess.value = false
  adminIcoinError.value = ''
  adminSaving.value = true
  try {
    const { data } = await api.patch(`/users/${adminSelectedUser.value.id}/`, {
      compte_bancaire: adminNewBalance.value
    })
    adminSelectedUser.value.compte_bancaire = data.compte_bancaire
    adminIcoinSuccess.value = true
    setTimeout(() => (adminIcoinSuccess.value = false), 4000)
  } catch (e) {
    adminIcoinError.value = e.response?.data?.detail || 'Erreur lors de la mise à jour.'
  } finally {
    adminSaving.value = false
  }
}

function ficheStatusLabel(status) {
  return { pending: 'En attente', validated: 'Validée', rejected: 'À corriger' }[status] || 'En attente'
}

function rpAvailabilityLabel(status) {
  return { open: 'Ouvert aux RP', discuss: 'À discuter', unavailable: 'Indisponible' }[status] || 'À discuter'
}

async function saveFicheStatus() {
  if (!adminSelectedUser.value) return
  adminIcoinError.value = ''
  adminSaving.value = true
  try {
    const { data } = await api.patch(`/users/${adminSelectedUser.value.id}/`, {
      fiche_status: adminSelectedUser.value.fiche_status,
    })
    adminSelectedUser.value.fiche_status = data.fiche_status
  } catch (e) {
    adminIcoinError.value = e.response?.data?.detail || 'Impossible de modifier le statut de la fiche.'
  } finally {
    adminSaving.value = false
  }
}

watch(() => auth.user, (newUser) => {
  if (newUser) {
    Object.keys(form).forEach(key => {
      form[key] = newUser[key] !== null ? newUser[key] : ''
    })
  }
}, { immediate: true })

function formatDate(dateStr) {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  })
}

function formatError(e) {
  if (e.response?.data) {
    if (typeof e.response.data === 'string') {
      error.value = e.response.data
    } else if (e.response.data.detail) {
      error.value = e.response.data.detail
    } else if (typeof e.response.data === 'object') {
      const messages = []
      const fieldNames = {
        avatar: 'Photo de profil',
        username: "Nom d'utilisateur",
        email: 'Adresse e-mail',
        bio: 'Biographie',
        signature: 'Signature',
        profile_gif_url: 'GIF de profil',
        sexe: 'Sexe',
        nature: 'Nature',
        camp: 'Camp',
        pseudo: 'Pseudo RP',
        rp_availability: 'Disponibilité RP',
        situation: 'Situation',
        metier: 'Métier',
        age_personnage: 'Âge du personnage',
        pouvoirs: 'Pouvoirs magiques',
        lieu_residence: 'Lieu de résidence',
        quartier_residentiel: 'Quartier résidentiel',
        credits: 'Crédits',
        avatar_name: 'Nom de la célébrité',
        double_compte: 'Double compte'
      }
      for (const [key, val] of Object.entries(e.response.data)) {
        const label = fieldNames[key] || key
        const errStr = Array.isArray(val) ? val.join(', ') : val
        messages.push(`${label} : ${errStr}`)
      }
      error.value = messages.join(' | ')
    } else {
      error.value = "Une erreur est survenue lors de la mise à jour."
    }
  } else {
    error.value = e.message || "Une erreur de connexion est survenue."
  }
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function handleImageChange(event) {
  const file = event.target.files[0]
  if (!file) return

  if (!file.type.startsWith('image/')) {
    error.value = "Veuillez sélectionner un fichier image valide (JPG, PNG, GIF, WebP)."
    window.scrollTo({ top: 0, behavior: 'smooth' })
    return
  }

  selectedFile.value = file
  previewImage.value = URL.createObjectURL(file)
}

async function handleUpdate() {
  error.value = ''
  success.value = false
  loading.value = true

  try {
    const formData = new FormData()

    Object.keys(form).filter(key => key !== 'nature').forEach(key => {
      if (key === 'avatar_name' && !isAvatarAdmin.value) return
      if (form[key] !== null && form[key] !== undefined) {
        formData.append(key, form[key])
      }
    })

    if (selectedFile.value) {
      formData.append('avatar', selectedFile.value)
    }

    await auth.updateProfile(formData)
    selectedFile.value = null
    previewImage.value = null
    success.value = true
    window.scrollTo({ top: 0, behavior: 'smooth' })
    setTimeout(() => (success.value = false), 5000)
  } catch (e) {
    formatError(e)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.next-steps-list, .arcana-history-list { list-style: none; padding: 0; margin: .75rem 0 0; }
.next-steps-list li { margin: .55rem 0; }
.next-steps-list span { color: var(--accent); font-weight: bold; margin-right: .4rem; }
.arcana-history-list li { display: flex; justify-content: space-between; gap: 1rem; padding: .6rem 0; border-top: 1px solid var(--border); }
.arcana-history-list strong { color: var(--accent); white-space: nowrap; }
.arcana-history-list small { color: var(--text-muted); }
.profile-gif-preview { width: 180px; height: 104px; margin: 0 auto; border: 1px solid var(--border-strong); border-radius: var(--radius); overflow: hidden; background: var(--bg-elevated); }
.profile-gif-preview img { display: block; width: 100%; height: 100%; object-fit: cover; }
.profile-gif-field { width: 100%; }
.profile-sheet-links { display: flex; flex-wrap: wrap; gap: .8rem; margin-bottom: 1rem; }
.profile-sheet-item { display: flex; flex: 1 1 190px; flex-direction: column; align-items: flex-start; gap: .55rem; padding: .85rem 1rem; border: 1px solid var(--border); border-radius: var(--radius); background: var(--bg-elevated); }
.profile-sheet-item .form-hint { margin: 0; }
.profile-page {
  padding: 3rem 0;
}

.page-header {
  margin-bottom: 2rem;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.page-title svg {
  color: var(--accent);
}

.form-hint {
  color: var(--text-muted);
  font-size: 0.72rem;
  line-height: 1.45;
  margin: 0.35rem 0 0;
}

.alert {
  padding: 1rem 1.5rem;
  border-radius: var(--radius);
  font-weight: 500;
  text-align: center;
  animation: fade-in-up 0.3s ease-out;
}

.alert-success {
  background: rgba(52, 211, 153, 0.15);
  color: #34d399;
  border: 1px solid rgba(52, 211, 153, 0.3);
}

.alert-danger {
  background: rgba(239, 68, 68, 0.15);
  color: #f87171;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

/* === ID Card Layout === */
.id-card {
  display: flex;
  padding: 0;
  overflow: visible; /* To allow avatar upload button overflow */
}

.id-left {
  width: 260px;
  flex-shrink: 0;
  background: var(--glass-bg);
  border-right: 1px solid var(--border);
  padding: 2rem 1.5rem;
  border-radius: var(--radius-lg) 0 0 var(--radius-lg);
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.id-right {
  flex: 1;
  padding: 2.5rem 2rem;
  display: flex;
  flex-direction: column;
}

/* === Avatar Section === */
.avatar-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.character-name-display {
  text-align: center;
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--gold);
  text-shadow: 0 0 10px rgba(240, 198, 116, 0.4);
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.avatar-preview {
  width: 200px;
  height: 320px;
  margin: 0 auto;
  border-radius: var(--radius);
  background: linear-gradient(135deg, var(--bg-elevated), var(--bg));
  border: 2px solid var(--border-strong);
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow-lg), var(--shadow-glow);
}

.avatar-upload-overlay {
  position: absolute;
  inset: 0;
  z-index: 10;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  background: rgba(10, 10, 20, 0.85);
  backdrop-filter: blur(8px);
  color: var(--accent);
  font-size: 0.85rem;
  font-weight: 600;
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform var(--transition-slow);
}

.avatar-preview:hover .avatar-img {
  transform: scale(1.05);
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-display);
  font-size: 5rem;
  font-weight: 700;
  color: var(--primary-light);
  background: linear-gradient(135deg, var(--bg-deep), var(--bg-secondary));
}

.avatar-upload-btn {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  background: rgba(10, 10, 20, 0.8);
  backdrop-filter: blur(8px);
  color: #fff;
  padding: 0.75rem 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  font-size: 0.78rem;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition);
  opacity: 0;
  transform: translateY(100%);
}

.avatar-preview:hover .avatar-upload-btn {
  opacity: 1;
  transform: translateY(0);
}

.avatar-upload-btn:hover {
  background: var(--primary);
  color: #fff;
}

.hidden-input {
  display: none;
}

/* === Radio Group (Sexe) === */
.radio-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.radio-label {
  cursor: pointer;
  display: block;
}

.radio-label input {
  display: none;
}

.radio-btn {
  display: block;
  padding: 0.625rem 1rem;
  text-align: center;
  border-radius: var(--radius);
  border: 1px solid var(--border);
  background: var(--bg-secondary);
  color: var(--text-secondary);
  font-size: 0.875rem;
  font-weight: 500;
  transition: all var(--transition);
}

.radio-label input:checked + .radio-btn {
  background: var(--primary-light);
  color: var(--accent);
  border-color: var(--accent);
  box-shadow: inset 0 0 10px rgba(139, 92, 246, 0.1);
}

.radio-label:hover input:not(:checked) + .radio-btn {
  background: var(--bg-elevated);
  border-color: var(--border-strong);
}

/* === ID Meta Info === */
.id-meta {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  background: var(--bg-deep);
  padding: 1rem 1.5rem;
  border-radius: var(--radius);
  border: 1px solid var(--border);
}

.id-meta-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.meta-label {
  font-size: 0.75rem;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 600;
}

.meta-value {
  font-family: var(--font-display);
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text);
}

.text-gold {
  color: var(--gold);
  text-shadow: 0 0 10px rgba(240, 198, 116, 0.3);
}

.divider {
  margin: 2rem 0;
}

/* === Form Grid === */
.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.grid-col-2 {
  grid-column: 1 / -1;
}

.form-actions {
  margin-top: 2.5rem;
  display: flex;
  justify-content: flex-end;
}

.spinner-small {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  display: inline-block;
}

/* === Responsive === */
@media (max-width: 900px) {
  .id-card {
    flex-direction: column;
  }
  
  .id-left {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid var(--border);
    border-radius: var(--radius-lg) var(--radius-lg) 0 0;
  }
  
  .radio-group {
    flex-direction: row;
  }
  
  .radio-label {
    flex: 1;
  }
}

@media (max-width: 600px) {
  .form-grid {
    grid-template-columns: 1fr;
  }

  .id-meta {
    flex-direction: column;
  }
}

/* === Group Badges (read-only) === */
.group-badges {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.group-badge {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  padding: 0.5rem 0.875rem;
  border-radius: var(--radius);
  border: 1px solid transparent;
  pointer-events: none;
  user-select: none;
}

.badge-faction {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.15), rgba(109, 40, 217, 0.08));
  border-color: rgba(139, 92, 246, 0.35);
}

.badge-race {
  background: linear-gradient(135deg, rgba(240, 198, 116, 0.12), rgba(200, 150, 40, 0.06));
  border-color: rgba(240, 198, 116, 0.3);
}

.badge-icon {
  font-size: 0.875rem;
  flex-shrink: 0;
}

.badge-faction .badge-icon {
  color: var(--accent);
  text-shadow: 0 0 8px rgba(139, 92, 246, 0.6);
}

.badge-race .badge-icon {
  color: var(--gold);
  text-shadow: 0 0 8px rgba(240, 198, 116, 0.5);
}

.badge-text {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
  min-width: 0;
}

.badge-label {
  font-size: 0.625rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-weight: 700;
  color: var(--text-secondary);
}

.badge-value {
  font-size: 0.8rem;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.badge-faction .badge-value {
  color: var(--accent);
}

.badge-race .badge-value {
  color: var(--gold);
}

/* === Admin Arcana Flouz Panel === */
.admin-icoin-panel {
  padding: 0;
  overflow: visible;
}

.admin-icoin-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  cursor: pointer;
  border-radius: var(--radius-lg);
  transition: background var(--transition);
}

.admin-icoin-header:hover {
  background: rgba(109, 40, 217, 0.08);
}

.admin-icoin-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-secondary);
  letter-spacing: 0.02em;
}

.admin-icoin-toggle {
  font-size: 0.75rem;
  color: var(--text-muted, #6d5fa0);
}

.admin-icoin-body {
  padding: 0 1.5rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  border-top: 1px solid var(--border);
}

/* Dropdown suggestions */
.admin-user-dropdown {
  list-style: none;
  margin: 0.35rem 0 0;
  padding: 0;
  border: 1px solid var(--border-strong);
  border-radius: var(--radius);
  background: var(--bg-elevated);
  max-height: 220px;
  overflow-y: auto;
}

.admin-user-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.6rem 1rem;
  cursor: pointer;
  transition: background var(--transition);
  border-bottom: 1px solid var(--border);
  font-size: 0.875rem;
}

.admin-user-item:last-child { border-bottom: none; }

.admin-user-item:hover {
  background: rgba(109, 40, 217, 0.12);
}

.admin-user-name { color: var(--text); font-weight: 500; }
.admin-user-balance { color: var(--gold); font-size: 0.78rem; }

/* Selected user block */
.admin-selected-user {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid rgba(245, 215, 110, 0.25);
  border-radius: var(--radius);
  background: rgba(245, 215, 110, 0.04);
}

.admin-selected-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.admin-selected-name {
  font-size: 1rem;
  color: var(--text);
}

.admin-selected-current {
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.btn-link {
  background: none;
  border: none;
  color: var(--text-muted, #6d5fa0);
  cursor: pointer;
  font-size: 0.78rem;
  padding: 0;
  margin-left: auto;
}

.btn-link:hover { color: var(--text); }

.admin-icoin-edit {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.admin-icoin-edit label {
  font-size: 0.78rem;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 600;
}

.admin-icoin-input-row {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.admin-icoin-input-row .form-input {
  max-width: 180px;
}

.admin-icoin-success {
  margin: 0;
  font-size: 0.82rem;
  color: #34d399;
}

.admin-icoin-error {
  margin: 0;
  font-size: 0.82rem;
  color: #f87171;
}

/* === Topics panels === */
.topics-panel {
  padding: 0;
  overflow: visible;
}

.topics-panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  cursor: pointer;
  border-radius: var(--radius-lg);
  transition: background var(--transition);
}

.topics-panel-header:hover {
  background: rgba(109, 40, 217, 0.08);
}

.topics-panel-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-secondary);
  letter-spacing: 0.02em;
}

.topics-panel-toggle {
  font-size: 0.75rem;
  color: var(--text-muted, #6d5fa0);
}

.topics-panel-body {
  padding: 0 1.5rem 1.25rem;
  border-top: 1px solid var(--border);
}

.topics-loading {
  padding: 0.75rem 0;
  color: var(--text-secondary);
  font-size: 0.85rem;
}

.topics-list-ul {
  list-style: none;
  margin: 0;
  padding: 0.5rem 0 0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.topics-list-item {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.5rem 0.75rem;
  border-radius: var(--radius);
  border: 1px solid var(--border);
  background: var(--bg-secondary);
  transition: background var(--transition);
}

.topics-list-item:hover {
  background: rgba(109, 40, 217, 0.08);
  border-color: var(--border-strong);
}

.topics-list-link {
  color: var(--accent);
  text-decoration: none;
  font-size: 0.88rem;
  font-weight: 500;
  flex: 1;
  min-width: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.topics-list-link:hover {
  text-decoration: underline;
  color: var(--primary-light);
}

.topics-list-meta {
  font-size: 0.75rem;
  color: var(--text-secondary);
  white-space: nowrap;
  flex-shrink: 0;
}

.topics-empty {
  padding: 0.75rem 0;
  color: var(--text-secondary);
  font-size: 0.85rem;
  margin: 0;
}
</style>
