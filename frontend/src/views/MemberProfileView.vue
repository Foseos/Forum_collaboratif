<template>
  <div class="page profile-page">
    <div class="container">

      <div v-if="loading" class="loading-state">
        <span class="spinner-small"></span> Chargement du profil…
      </div>

      <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

      <template v-else-if="member">

        <!-- Si c'est son propre profil → lien vers l'édition -->
        <div v-if="isOwnProfile" class="own-banner">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14M4.93 4.93a10 10 0 0 0 0 14.14"/></svg>
          Vous consultez votre propre profil.
          <router-link to="/profile" class="btn btn-sm btn-primary own-edit-btn">✏️ Modifier mon profil</router-link>
        </div>

        <section v-if="canDeleteMember" class="card delete-character-card">
          <div class="delete-character-heading">
            <div><strong>Administration du personnage</strong><p>Supprimer définitivement ce personnage, son compte, ses sujets et ses messages.</p></div>
            <button type="button" class="btn btn-sm btn-secondary" @click="showDeleteForm = !showDeleteForm">{{ showDeleteForm ? 'Annuler' : 'Supprimer le personnage' }}</button>
          </div>
          <div v-if="showDeleteForm" class="delete-character-form">
            <p>Cette action est définitive. Les réponses d’autres membres dans ses sujets disparaîtront également.</p>
            <label for="delete-character-confirm">Saisissez « {{ member.username }} » pour confirmer :</label>
            <input id="delete-character-confirm" v-model="deleteConfirmation" class="form-input" autocomplete="off" />
            <button type="button" class="btn btn-sm delete-character-button" :disabled="deleteConfirmation !== member.username || deletingMember" @click="deleteMember">{{ deletingMember ? 'Suppression…' : 'Confirmer la suppression' }}</button>
            <p v-if="deleteError" role="alert">{{ deleteError }}</p>
          </div>
        </section>

        <section v-if="isFounder" class="card founder-name-card">
          <div class="delete-character-heading">
            <div><strong>Nom d’utilisateur</strong><p>Seule la fondatrice peut le modifier. Le nouveau nom sera utilisé pour la connexion et affiché sur le forum.</p></div>
            <button type="button" class="btn btn-secondary btn-sm" @click="showNameForm = !showNameForm">{{ showNameForm ? 'Annuler' : 'Modifier le nom' }}</button>
          </div>
          <form v-if="showNameForm" class="founder-name-form" @submit.prevent="saveUsername">
            <label for="founder-new-username">Nouveau nom d’utilisateur</label>
            <input id="founder-new-username" v-model="newUsername" class="form-input" maxlength="150" required />
            <button type="submit" class="btn btn-primary btn-sm" :disabled="savingUsername || !newUsername.trim() || newUsername.trim() === member.username">{{ savingUsername ? 'Enregistrement…' : 'Enregistrer le nouveau nom' }}</button>
            <p v-if="usernameMessage" role="status">{{ usernameMessage }}</p>
          </form>
        </section>

        <section v-if="canManageAccounts" class="card linked-accounts-card">
          <strong>🔒 Comptes liés validés par le staff</strong>
          <p class="text-secondary">Après acceptation d'une demande de double compte, choisissez ici son compte principal.</p>
          <div class="form-group">
            <label for="main-account">Compte principal de {{ member.username }}</label>
            <select id="main-account" v-model="selectedMainAccount" class="form-input">
              <option value="">Aucun compte lié</option>
              <option v-for="account in availableMainAccounts" :key="account.id" :value="account.id">{{ account.username }}</option>
            </select>
          </div>
          <button class="btn btn-secondary btn-sm" :disabled="linkSaving" @click="saveLinkedAccount">Enregistrer le lien</button>
          <p v-if="linkMessage" class="text-secondary">{{ linkMessage }}</p>
          <p v-if="linkedAccounts?.linked_accounts?.length">Autres comptes liés : <router-link v-for="(account, index) in linkedAccounts.linked_accounts" :key="account.id" :to="`/membres/${account.id}`">{{ index ? ', ' : '' }}{{ account.username }}</router-link></p>
        </section>

        <div class="id-card card">

          <!-- Colonne gauche : portrait + badges -->
          <div class="id-left">
            <div class="avatar-section">
              <div class="character-name-display">{{ member.username }}</div>

              <div class="avatar-preview" :class="{ 'avatar-editable': isOwnProfile }" @click="isOwnProfile && $router.push('/profile')" :title="isOwnProfile ? 'Cliquer pour modifier mon avatar' : ''">
                <img v-if="member.avatar" :src="member.avatar" :alt="member.username" class="avatar-img" />
                <div v-else class="avatar-placeholder">
                  <span>{{ member.username?.[0]?.toUpperCase() || '?' }}</span>
                </div>
                <div v-if="isOwnProfile" class="avatar-edit-overlay">
                  <span>✏️ Modifier</span>
                </div>
              </div>

              <div v-if="member.avatar_name" class="avatar-celeb">{{ member.avatar_name }}</div>
              <div v-if="member.profile_gif_url" class="profile-gif">
                <img :src="member.profile_gif_url" :alt="`GIF de ${member.username}`" loading="lazy" />
              </div>

              <!-- Badges faction + race -->
              <div v-if="member.groupe || member.race" class="group-badges">
                <div v-if="member.groupe" class="group-badge badge-faction">
                  <span class="badge-icon">⚜</span>
                  <div class="badge-text">
                    <span class="badge-label">Faction</span>
                    <span class="badge-value">{{ member.groupe }}</span>
                  </div>
                </div>
                <div v-for="race in raceList(member.race)" :key="race" class="group-badge badge-race">
                  <span class="badge-icon">✦</span>
                  <div class="badge-text">
                    <span class="badge-label">Espèce</span>
                    <span class="badge-value">{{ race }}</span>
                  </div>
                </div>
              </div>

              <!-- Sexe / Nature / Camp -->
              <div class="char-pills">
                <span v-if="member.sexe" class="pill">{{ capitalize(member.sexe) }}</span>
                <span v-if="member.nature" class="pill">{{ member.nature }}</span>
                <span v-if="member.camp" class="pill" :class="campClass(member.camp)">{{ member.camp }}</span>
              </div>
            </div>
          </div>

          <!-- Colonne droite : infos -->
          <div class="id-right">

            <!-- Stats : messages / inscription / Arcana Flouz -->
            <div class="id-meta">
              <div class="id-meta-item">
                <span class="meta-label">Messages</span>
                <span class="meta-value">{{ member.messages_count || 0 }}</span>
              </div>
              <div class="id-meta-item">
                <span class="meta-label">Inscription</span>
                <span class="meta-value">{{ formatDate(member.date_joined) }}</span>
              </div>
              <div class="id-meta-item">
                <span class="meta-label">Fiche</span>
                <span class="meta-value">{{ ficheStatusLabel(member.fiche_status) }}</span>
              </div>
              <div class="id-meta-item">
                <span class="meta-label">Disponibilité RP</span>
                <span class="meta-value">{{ rpAvailabilityLabel(member.rp_availability) }}</span>
              </div>
              <div class="id-meta-item">
                <span class="meta-label">Solde Arcana Flouz</span>
                <span class="meta-value text-gold">{{ member.compte_bancaire || 0 }} Arcana Flouz</span>
              </div>
              <div class="id-meta-item">
                <span class="meta-label">Dernière connexion</span>
                <span class="meta-value">{{ formatDateTime(member.last_login) }}</span>
              </div>
            </div>

            <div class="divider"></div>

            <div class="profile-sheet-links">
              <router-link v-if="auth.isAuthenticated && !isOwnProfile && member.username === 'Ava Bartholomé'" :to="`/messageries?to=${member.id}&username=${encodeURIComponent(member.username)}`" class="btn btn-primary btn-sm">✉ Envoyer un message privé à Ava</router-link>
              <router-link v-if="isOwnProfile && member.username === 'Ava Bartholomé'" to="/messageries" class="btn btn-primary btn-sm">✉ Voir mes messages privés</router-link>
              <router-link v-if="isOwnProfile && member.username === 'Ava Bartholomé'" to="/administration/signalements" class="btn btn-secondary btn-sm">⚑ Voir les signalements</router-link>
              <router-link v-if="member.presentation_topic_slug" :to="`/topics/${member.presentation_topic_slug}`" class="btn btn-secondary btn-sm">✦ Présentation validée</router-link>
              <span v-else class="text-secondary text-sm">Présentation validée : aucune fiche archivée.</span>
              <router-link v-if="member.recap_topic_slug" :to="`/topics/${member.recap_topic_slug}`" class="btn btn-secondary btn-sm">✦ Carnet du personnage</router-link>
              <span v-else class="text-secondary text-sm">Carnet du personnage : pas encore publié.</span>
            </div>

            <!-- Infos RP -->
            <div class="info-grid">
              <div v-if="member.pseudo" class="info-row full">
                <span class="info-label">Pseudo RP du joueur</span>
                <span class="info-value highlight">{{ member.pseudo }}</span>
              </div>
              <div v-if="member.age_personnage" class="info-row">
                <span class="info-label">Âge</span>
                <span class="info-value">{{ member.age_personnage }}</span>
              </div>
              <div v-if="member.metier" class="info-row">
                <span class="info-label">Métier</span>
                <span class="info-value">{{ member.metier }}</span>
              </div>
              <div v-if="member.lieu_residence" class="info-row full">
                <span class="info-label">Résidence</span>
                <span class="info-value">{{ member.lieu_residence }}</span>
              </div>
              <div v-if="member.quartier_residentiel" class="info-row full">
                <span class="info-label">Quartier résidentiel</span>
                <span class="info-value">{{ member.quartier_residentiel }}</span>
              </div>
              <div v-if="member.situation" class="info-row full">
                <span class="info-label">Situation</span>
                <span class="info-value">{{ member.situation }}</span>
              </div>
              <div v-if="member.pouvoirs" class="info-row full">
                <span class="info-label">Pouvoirs</span>
                <span class="info-value">{{ member.pouvoirs }}</span>
              </div>
              <div v-if="member.bio" class="info-row full">
                <span class="info-label">Biographie</span>
                <p class="info-bio">{{ member.bio }}</p>
              </div>
              <div v-if="member.double_compte" class="info-row full">
                <span class="info-label">Double compte</span>
                <span class="info-value text-muted">{{ member.double_compte }}</span>
              </div>
              <div v-if="member.credits" class="info-row full">
                <span class="info-label">Crédits</span>
                <span class="info-value text-muted">{{ member.credits }}</span>
              </div>
            </div>

          </div>
        </div>

        <section v-if="member.signature" class="member-signature card">
          <p class="member-signature-label">Signature</p>
          <img
            v-if="signatureImageUrl"
            :src="signatureImageUrl"
            :alt="`Signature de ${member.username}`"
            class="member-signature-image"
          />
          <p v-else class="member-signature-text">{{ member.signature }}</p>
        </section>

        <!-- ── Sujets créés ── -->
        <div class="topics-panel card" style="margin-top: 1.5rem;">
          <div class="topics-panel-header" @click="toggleCreatedTopics">
            <span class="topics-panel-title">📜 Sujets créés</span>
            <span class="topics-panel-toggle">{{ showCreatedTopics ? '▲' : '▼' }}</span>
          </div>
          <div v-if="showCreatedTopics" class="topics-panel-body">
            <div v-if="loadingCreated" class="topics-loading">Chargement…</div>
            <ul v-else-if="createdTopics.length" class="topics-list-ul">
              <li v-for="t in createdTopics" :key="t.slug" class="topics-list-item">
                <router-link :to="`/topics/${t.slug}`" class="topics-list-link">{{ t.title }}</router-link>
                <span class="topics-list-meta">{{ formatDate(t.created_at) }}</span>
              </li>
            </ul>
            <p v-else class="topics-empty">Aucun sujet créé pour l'instant.</p>
          </div>
        </div>

        <!-- ── Sujets avec participation ── -->
        <div class="topics-panel card" style="margin-top: 1rem;">
          <div class="topics-panel-header" @click="toggleParticipatedTopics">
            <span class="topics-panel-title">💬 Sujets avec participation</span>
            <span class="topics-panel-toggle">{{ showParticipatedTopics ? '▲' : '▼' }}</span>
          </div>
          <div v-if="showParticipatedTopics" class="topics-panel-body">
            <div v-if="loadingParticipated" class="topics-loading">Chargement…</div>
            <ul v-else-if="participatedTopics.length" class="topics-list-ul">
              <li v-for="t in participatedTopics" :key="t.slug" class="topics-list-item">
                <router-link :to="`/topics/${t.slug}`" class="topics-list-link">{{ t.title }}</router-link>
                <span class="topics-list-meta">{{ formatDate(t.created_at) }}</span>
              </li>
            </ul>
            <p v-else class="topics-empty">Aucune participation pour l'instant.</p>
          </div>
        </div>

        <!-- Bouton retour -->
        <div class="back-row">
          <router-link to="/membres" class="btn btn-ghost btn-sm">
            ← Retour aux membres
          </router-link>
        </div>

      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../composables/useApi'

const props = defineProps({ id: { type: String, required: true } })
const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const member = ref(null)
const loading = ref(true)
const error = ref('')
const canManageAccounts = computed(() => ['admin', 'fondatrice'].includes(auth.user?.role))
const isFounder = computed(() => auth.user?.role === 'fondatrice')
const showNameForm = ref(false)
const newUsername = ref('')
const savingUsername = ref(false)
const usernameMessage = ref('')

async function saveUsername() {
  if (!isFounder.value || !newUsername.value.trim()) return
  savingUsername.value = true
  usernameMessage.value = ''
  try {
    const { data } = await api.patch(`/users/${member.value.id}/`, { username: newUsername.value.trim() })
    member.value.username = data.username
    newUsername.value = data.username
    if (auth.user?.id === member.value.id) await auth.fetchProfile()
    usernameMessage.value = 'Nom d’utilisateur modifié.'
    showNameForm.value = false
  } catch (e) {
    usernameMessage.value = e.response?.data?.username?.[0] || e.response?.data?.detail || 'Modification impossible.'
  } finally {
    savingUsername.value = false
  }
}
const canDeleteMember = computed(() => canManageAccounts.value && member.value?.role === 'user' && !isOwnProfile.value)
const showDeleteForm = ref(false)
const deleteConfirmation = ref('')
const deletingMember = ref(false)
const deleteError = ref('')

async function deleteMember() {
  if (!canDeleteMember.value || deleteConfirmation.value !== member.value?.username) return
  deletingMember.value = true
  deleteError.value = ''
  try {
    await api.delete(`/users/${member.value.id}/`, { data: { confirm_username: deleteConfirmation.value } })
    await router.push('/membres')
  } catch (e) {
    deleteError.value = e.response?.data?.detail || 'Suppression impossible.'
  } finally {
    deletingMember.value = false
  }
}
const linkedAccounts = ref(null)
const selectedMainAccount = ref('')
const accountOptions = ref([])
const linkSaving = ref(false)
const linkMessage = ref('')
const availableMainAccounts = computed(() => accountOptions.value.filter(account => account.id !== member.value?.id))

async function loadLinkedAccounts() {
  if (!canManageAccounts.value) return
  try {
    const [links, users] = await Promise.all([
      api.get(`/users/${props.id}/linked-accounts/`), api.get('/users/'),
    ])
    linkedAccounts.value = links.data
    selectedMainAccount.value = links.data.main_account || ''
    accountOptions.value = users.data.results || users.data
  } catch {
    linkMessage.value = 'Impossible de charger les comptes liés.'
  }
}

async function saveLinkedAccount() {
  linkSaving.value = true
  linkMessage.value = ''
  try {
    const { data } = await api.patch(`/users/${props.id}/linked-accounts/`, {
      main_account: selectedMainAccount.value || null,
    })
    linkedAccounts.value = data
    linkMessage.value = 'Lien entre comptes enregistré.'
  } catch (e) {
    linkMessage.value = e.response?.data?.detail || 'Enregistrement impossible.'
  } finally {
    linkSaving.value = false
  }
}

// ── Topics panels ──────────────────────────────────────────────────
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
      const { data } = await api.get(`/topics/?author=${member.value.id}&ordering=-created_at`)
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
      const { data } = await api.get(`/topics/participated/?user_id=${member.value.id}`)
      participatedTopics.value = data.results || data
    } catch { /* silent */ } finally {
      loadingParticipated.value = false
    }
  }
}

const isOwnProfile = computed(() => auth.user?.id === member.value?.id)

const signatureImageUrl = computed(() => {
  const signature = member.value?.signature?.trim()
  if (!signature) return null

  const bbcodeMatch = signature.match(/^\[img\](https?:\/\/[^\s\]]+)\[\/img\]$/i)
  const imageUrl = bbcodeMatch?.[1] || signature
  return /^https?:\/\/\S+\.(?:gif|png|jpe?g|webp)(?:[?#]\S*)?$/i.test(imageUrl)
    ? imageUrl
    : null
})

function formatDate(d) {
  if (!d) return '—'
  return new Date(d).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' })
}

function formatDateTime(d) {
  if (!d) return 'Jamais'
  return new Date(d).toLocaleString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

function ficheStatusLabel(status) {
  return { pending: 'En attente', validated: 'Validée', rejected: 'À corriger' }[status] || 'En attente'
}

function rpAvailabilityLabel(status) {
  return { open: 'Ouvert aux RP', discuss: 'À discuter', unavailable: 'Indisponible' }[status] || 'À discuter'
}

function capitalize(str) {
  return str ? str.charAt(0).toUpperCase() + str.slice(1) : ''
}

function raceList(race) {
  if (!race) return []
  return race.split(',').map(r => r.trim()).filter(Boolean)
}

function campClass(camp) {
  const c = camp?.toLowerCase() || ''
  if (c.includes('bien')) return 'camp-bien'
  if (c.includes('mal')) return 'camp-mal'
  return 'camp-neutre'
}

async function fetchMember() {
  try {
    const { data } = await api.get(`/users/${props.id}/`)
    member.value = data
    newUsername.value = data.username
    if (canDeleteMember.value && route.query.supprimer === '1') showDeleteForm.value = true
    await loadLinkedAccounts()
  } catch {
    error.value = 'Membre introuvable ou profil inaccessible.'
  } finally {
    loading.value = false
  }
}

onMounted(fetchMember)
watch(() => props.id, () => {
  member.value = null
  loading.value = true
  showDeleteForm.value = false
  deleteConfirmation.value = ''
  showNameForm.value = false
  usernameMessage.value = ''
  fetchMember()
})
</script>

<style scoped>
.profile-page { padding: 2.5rem 0; }
.linked-accounts-card { margin: 0 0 1.5rem; padding: 1.25rem; border-color: rgba(167,139,250,.45); }
.delete-character-card { margin: 0 0 1.5rem; padding: 1.25rem; border-color: rgba(239, 68, 68, .4); }
.delete-character-heading { display: flex; justify-content: space-between; align-items: center; gap: 1rem; flex-wrap: wrap; }
.delete-character-heading p, .delete-character-form p { color: var(--text-secondary); margin: .4rem 0; }
.delete-character-form { display: grid; gap: .75rem; margin-top: 1rem; max-width: 600px; }
.delete-character-button { background: #a42b37; color: white; justify-self: start; }
.delete-character-button:disabled { opacity: .5; cursor: not-allowed; }
.founder-name-card { margin: 0 0 1.5rem; padding: 1.25rem; border-color: rgba(245, 215, 110, .4); }
.founder-name-form { display: grid; gap: .75rem; margin-top: 1rem; max-width: 600px; }
.founder-name-form .btn { justify-self: start; }
.founder-name-form p { margin: 0; color: var(--text-secondary); }

/* Banner propre compte */
.own-banner {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: rgba(139,92,246,0.1);
  border: 1px solid rgba(139,92,246,0.3);
  border-radius: var(--radius);
  padding: 0.75rem 1.25rem;
  font-size: 0.875rem;
  color: var(--accent);
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}
.own-edit-btn { margin-left: auto; }

.member-signature {
  margin-top: 1.5rem;
  padding: 1.25rem 1.5rem;
}

.member-signature-label {
  color: var(--accent);
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  margin: 0 0 0.85rem;
  text-transform: uppercase;
}

.member-signature-image {
  display: block;
  height: auto;
  max-height: 260px;
  max-width: 100%;
  object-fit: contain;
}

.member-signature-text {
  color: var(--text-secondary);
  font-size: 0.88rem;
  font-style: italic;
  line-height: 1.65;
  margin: 0;
  white-space: pre-line;
}

/* Card layout */
.id-card {
  display: flex;
  padding: 0;
  overflow: hidden;
}

.id-left {
  width: 240px;
  flex-shrink: 0;
  background: var(--glass-bg);
  border-right: 1px solid var(--border);
  padding: 2rem 1.25rem;
  border-radius: var(--radius-lg) 0 0 var(--radius-lg);
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.id-right {
  flex: 1;
  padding: 2rem 1.75rem;
  display: flex;
  flex-direction: column;
  min-width: 0;
}
.profile-sheet-links { display: flex; flex-wrap: wrap; gap: .65rem; margin: .2rem 0 1rem; }

/* Avatar */
.avatar-section { display: flex; flex-direction: column; gap: 0.875rem; }
.profile-gif { width: 180px; height: 104px; margin: 0 auto; border: 1px solid var(--border-strong); border-radius: var(--radius); overflow: hidden; background: var(--bg-elevated); }
.profile-gif img { display: block; width: 100%; height: 100%; object-fit: cover; }

.character-name-display {
  text-align: center;
  font-family: var(--font-display);
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--gold);
  text-shadow: 0 0 10px rgba(240,198,116,0.4);
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.avatar-preview {
  width: 180px;
  height: 270px;
  margin: 0 auto;
  border-radius: var(--radius);
  border: 2px solid var(--border-strong);
  overflow: hidden;
  box-shadow: var(--shadow-lg), var(--shadow-glow);
  background: linear-gradient(135deg, var(--bg-elevated), var(--bg));
  position: relative;
}

.avatar-editable {
  cursor: pointer;
}

.avatar-edit-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  background: rgba(10, 10, 20, 0.8);
  backdrop-filter: blur(6px);
  color: #fff;
  padding: 0.5rem 0;
  font-size: 0.8rem;
  font-weight: 600;
  text-align: center;
  opacity: 0;
  transform: translateY(100%);
  transition: all var(--transition);
}

.avatar-editable:hover .avatar-edit-overlay {
  opacity: 1;
  transform: translateY(0);
}

.avatar-img { width: 100%; height: 100%; object-fit: cover; object-position: top center; }

.avatar-placeholder {
  width: 100%; height: 100%;
  display: flex; align-items: center; justify-content: center;
  font-family: var(--font-display); font-size: 4.5rem; font-weight: 700;
  color: var(--primary-light);
  background: linear-gradient(135deg, var(--bg-deep), var(--bg-secondary));
}

.avatar-celeb {
  text-align: center;
  font-size: 0.7rem;
  color: var(--text-secondary);
  font-style: italic;
}

/* Pills */
.char-pills { display: flex; flex-wrap: wrap; gap: 0.3rem; justify-content: center; }
.pill {
  font-size: 0.65rem;
  padding: 0.2rem 0.6rem;
  border-radius: 99px;
  background: rgba(255,255,255,0.06);
  border: 1px solid var(--border);
  color: var(--text-secondary);
}
.camp-bien  { background: rgba(52,211,153,0.1);  border-color: rgba(52,211,153,0.3);  color: #34d399; }
.camp-mal   { background: rgba(239,68,68,0.1);   border-color: rgba(239,68,68,0.3);   color: #f87171; }
.camp-neutre{ background: rgba(148,163,184,0.1); border-color: rgba(148,163,184,0.2); color: #94a3b8; }

/* Badges */
.group-badges { display: flex; flex-direction: column; gap: 0.4rem; }
.group-badge {
  display: flex; align-items: center; gap: 0.5rem;
  padding: 0.4rem 0.75rem;
  border-radius: var(--radius);
  border: 1px solid transparent;
}
.badge-faction {
  background: linear-gradient(135deg, rgba(139,92,246,0.15), rgba(109,40,217,0.08));
  border-color: rgba(139,92,246,0.35);
}
.badge-race {
  background: linear-gradient(135deg, rgba(240,198,116,0.12), rgba(200,150,40,0.06));
  border-color: rgba(240,198,116,0.3);
}
.badge-icon { font-size: 0.8rem; flex-shrink: 0; }
.badge-faction .badge-icon { color: var(--accent); }
.badge-race    .badge-icon { color: var(--gold); }
.badge-text { display: flex; flex-direction: column; gap: 0.05rem; min-width: 0; }
.badge-label { font-size: 0.6rem; text-transform: uppercase; letter-spacing: 0.07em; font-weight: 700; color: var(--text-secondary); }
.badge-value { font-size: 0.78rem; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.badge-faction .badge-value { color: var(--accent); }
.badge-race    .badge-value { color: var(--gold); }

/* Meta stats */
.id-meta {
  display: flex;
  justify-content: space-between;
  gap: 0.75rem;
  background: var(--bg-deep);
  padding: 0.875rem 1.25rem;
  border-radius: var(--radius);
  border: 1px solid var(--border);
  flex-wrap: wrap;
}
.id-meta-item { display: flex; flex-direction: column; gap: 0.2rem; }
.meta-label { font-size: 0.68rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; }
.meta-value { font-family: var(--font-display); font-size: 1rem; font-weight: 700; color: var(--text); }
.text-gold { color: var(--gold); text-shadow: 0 0 8px rgba(240,198,116,0.3); }

.divider { margin: 1.5rem 0; border-top: 1px solid var(--border); }

/* Info grid */
.info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.875rem 1.25rem; }
.info-row { display: flex; flex-direction: column; gap: 0.2rem; }
.info-row.full { grid-column: 1 / -1; }
.info-label { font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.06em; font-weight: 700; color: var(--text-secondary); }
.info-value { font-size: 0.875rem; color: var(--text); }
.info-value.highlight { font-size: 0.95rem; font-weight: 600; color: var(--gold); }
.info-bio { margin: 0; font-size: 0.875rem; color: var(--text-secondary); line-height: 1.7; }
.text-muted { color: var(--text-secondary) !important; }

/* Bouton retour */
.back-row { margin-top: 1.25rem; }

/* === Topics panels === */
.topics-panel { padding: 0; overflow: visible; }

.topics-panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  cursor: pointer;
  border-radius: var(--radius-lg);
  transition: background var(--transition);
}
.topics-panel-header:hover { background: rgba(109,40,217,0.08); }

.topics-panel-title { font-size: 0.9rem; font-weight: 600; color: var(--text-secondary); letter-spacing: 0.02em; }
.topics-panel-toggle { font-size: 0.75rem; color: var(--text-muted, #6d5fa0); }

.topics-panel-body { padding: 0 1.5rem 1.25rem; border-top: 1px solid var(--border); }

.topics-loading { padding: 0.75rem 0; color: var(--text-secondary); font-size: 0.85rem; }

.topics-list-ul { list-style: none; margin: 0; padding: 0.5rem 0 0; display: flex; flex-direction: column; gap: 0.5rem; }

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
.topics-list-item:hover { background: rgba(109,40,217,0.08); border-color: var(--border-strong); }

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
.topics-list-link:hover { text-decoration: underline; color: var(--primary-light); }

.topics-list-meta { font-size: 0.75rem; color: var(--text-secondary); white-space: nowrap; flex-shrink: 0; }

.topics-empty { padding: 0.75rem 0; color: var(--text-secondary); font-size: 0.85rem; margin: 0; }

/* States */
.loading-state {
  text-align: center; padding: 4rem;
  color: var(--text-secondary);
  display: flex; align-items: center; justify-content: center; gap: 0.75rem;
}
.alert { padding: 1rem 1.5rem; border-radius: var(--radius); text-align: center; }
.alert-danger { background: rgba(239,68,68,0.1); color: #ef4444; border: 1px solid rgba(239,68,68,0.3); }

.spinner-small {
  width: 16px; height: 16px;
  border: 2px solid rgba(255,255,255,0.2);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  display: inline-block; flex-shrink: 0;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Responsive */
@media (max-width: 860px) {
  .id-card { flex-direction: column; }
  .id-left { width: 100%; border-right: none; border-bottom: 1px solid var(--border); border-radius: var(--radius-lg) var(--radius-lg) 0 0; }
}
@media (max-width: 560px) {
  .info-grid { grid-template-columns: 1fr; }
  .id-meta { flex-direction: column; }
}
</style>
