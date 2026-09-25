<template>
  <div class="card post-card">
    <div class="post-layout">

      <!-- ══════════════════════════════════
           Colonne gauche — Profil auteur
      ══════════════════════════════════ -->
      <aside class="post-author-col">

        <!-- Portrait -->
        <div class="author-portrait" :class="{ 'portrait-editable': canEditAvatar }">
          <img
            v-if="post.author?.avatar"
            :src="avatarPreview || post.author.avatar"
            :alt="post.author.username"
            class="portrait-img"
          />
          <span v-else class="portrait-initials">
            {{ post.author?.username?.[0]?.toUpperCase() || '?' }}
          </span>
          <div v-if="canEditAvatar" class="portrait-edit-overlay" @click="avatarInput?.click()">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>
            <span>{{ uploadingAvatar ? 'Envoi…' : 'Modifier' }}</span>
          </div>
          <input
            ref="avatarInput"
            type="file"
            accept="image/*"
            style="display:none"
            @change="handleAvatarChange"
          />
        </div>

        <div class="author-sidebar-body">

          <!-- Nom du compte en titre -->
          <div class="author-pseudo-title">
            « {{ post.author?.username }} »
          </div>

          <div v-if="post.author?.profile_gif_url" class="author-profile-gif">
            <img :src="post.author.profile_gif_url" :alt="`GIF de ${post.author?.username}`" loading="lazy" />
          </div>

          <!-- Ligne décorative -->
          <div class="sidebar-divider"></div>

          <!-- Stats RPG -->
          <ul class="author-stats">
            <li v-if="post.author?.situation" class="stat-row">
              <span class="stat-label">Statut Social</span>
              <span class="stat-value">{{ post.author.situation }}</span>
            </li>
            <li v-if="post.author?.sexe" class="stat-row">
              <span class="stat-label">Sexe</span>
              <span class="stat-value">{{ formatSexe(post.author.sexe) }}</span>
            </li>
            <li v-if="post.author?.nature" class="stat-row">
              <span class="stat-label">Nature</span>
              <span class="stat-value">{{ post.author.nature }}</span>
            </li>
            <li v-if="post.author?.race" class="stat-row">
              <span class="stat-label">Race</span>
              <span class="stat-value">{{ post.author.race }}</span>
            </li>
            <li v-if="post.author?.age_personnage" class="stat-row">
              <span class="stat-label">Âge</span>
              <span class="stat-value">{{ post.author.age_personnage }}</span>
            </li>
            <li v-if="post.author?.camp" class="stat-row">
              <span class="stat-label">Alignement</span>
              <span class="stat-value">{{ post.author.camp }}</span>
            </li>
            <li v-if="pouvoirs.length" class="stat-row stat-row--block">
              <span class="stat-label">Pouvoirs</span>
              <span class="stat-value">
                <span v-for="(p, i) in pouvoirs" :key="i" class="pouvoir-item">
                  — {{ p }}
                </span>
              </span>
            </li>
            <li v-if="post.author?.metier" class="stat-row">
              <span class="stat-label">Métier</span>
              <span class="stat-value">{{ post.author.metier }}</span>
            </li>
            <li v-if="post.author?.lieu_residence" class="stat-row">
              <span class="stat-label">Résidence</span>
              <span class="stat-value">{{ post.author.lieu_residence }}</span>
            </li>
          </ul>

          <!-- Ligne décorative -->
          <div class="sidebar-divider"></div>

          <!-- Compteurs -->
          <ul class="author-stats author-stats--counts">
            <li class="stat-row">
              <span class="stat-label">Nombre de sorts</span>
              <span class="stat-value stat-value--highlight">{{ post.author?.messages_count ?? 0 }}</span>
            </li>
            <li v-if="post.author?.compte_bancaire != null" class="stat-row">
              <span class="stat-label">Arcana Flouz</span>
              <span class="stat-value stat-value--gold">{{ post.author.compte_bancaire }} Arcana Flouz</span>
            </li>
            <li v-if="post.author?.avatar_name" class="stat-row">
              <span class="stat-label">Avatar</span>
              <span class="stat-value">{{ post.author.avatar_name }}</span>
            </li>
            <li v-if="post.author?.double_compte" class="stat-row">
              <span class="stat-label">Autres comptes</span>
              <span class="stat-value">{{ post.author.double_compte }}</span>
            </li>
          </ul>

          <!-- Badges faction / race -->
          <div v-if="post.author?.groupe || post.author?.race" class="author-badges">
            <div v-if="post.author?.groupe" class="group-badge badge-faction">
              <span class="badge-icon">⚜</span>
              <div class="badge-text">
                <span class="badge-label">Faction</span>
                <span class="badge-value">{{ post.author.groupe }}</span>
              </div>
            </div>
            <div v-if="post.author?.race" class="group-badge badge-race">
              <span class="badge-icon">✦</span>
              <div class="badge-text">
                <span class="badge-label">Espèce</span>
                <span class="badge-value">{{ post.author.race }}</span>
              </div>
            </div>
          </div>

          <!-- Badge rôle admin/modo -->
          <div class="role-badge-row">
            <span v-if="post.author?.role === 'admin' || post.author?.role === 'fondatrice'" class="role-badge role-badge--admin">⚜ Administration</span>
            <span v-else-if="post.author?.role === 'moderator'" class="role-badge role-badge--mod">🛡 Modérateur</span>
          </div>

        </div>
      </aside>

      <!-- ══════════════════════════════════
           Colonne droite — Contenu du post
      ══════════════════════════════════ -->
      <div class="post-body-col">

        <!-- En-tête : date + boutons -->
        <div class="post-meta-row">
          <span class="post-date">
            {{ formatDate(post.created_at) }}
            <span v-if="post.is_edited" class="edited-badge">(modifié)</span>
          </span>
          <div v-if="canEdit" class="post-actions">
            <button class="btn-icon btn-sm" title="Modifier" @click="$emit('edit', post)">✏️</button>
            <button class="btn-icon btn-sm" title="Supprimer" @click="$emit('delete', post.id)">🗑️</button>
          </div>
        </div>

        <div class="post-body-divider"></div>

        <div v-if="post.dice_result != null" class="dice-result" role="status">
          🎲 Dé du destin : <strong>{{ post.dice_result }} / 6</strong>
          <span>— {{ post.dice_result <= 2 ? 'Complication' : post.dice_result <= 4 ? 'Réussite partielle' : 'Réussite' }}</span>
        </div>

        <!-- Contenu HTML -->
        <PowerGrimoire v-if="showGrimoire" :content="post.content" />
        <div
          v-else
          class="post-content"
          :class="{ 'post-content--collapsed': isLong && !expanded && !isRaceDirectory }"
          v-html="post.content"
          ref="contentRef"
        ></div>
        <div v-if="isLong && !showGrimoire && !isRaceDirectory" class="post-expand-row">
          <button class="post-expand-btn" @click="expanded = !expanded">
            {{ expanded ? '▲ Réduire' : '▼ Voir la suite' }}
          </button>
        </div>

        <!-- Signature RPG de l'auteur : texte ou image/GIF -->
        <div v-if="post.author?.signature" class="post-signature">
          <img
            v-if="signatureImageUrl"
            :src="signatureImageUrl"
            :alt="`Signature de ${post.author?.username}`"
            class="post-signature-image"
          />
          <p v-else class="post-signature-text">{{ post.author.signature }}</p>
        </div>

        <!-- Réactions -->
        <ReactionBar
          :counts="post.reactions_count || {}"
          :user-reactions="post.user_reactions || []"
          @react="(type) => $emit('react', post.id, type)"
        />
      </div>

    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, nextTick } from 'vue'
import { useAuthStore } from '../stores/auth'
import api from '../composables/useApi'
import ReactionBar from './ReactionBar.vue'
import PowerGrimoire from './PowerGrimoire.vue'

const props = defineProps({
  post: { type: Object, required: true },
  grimoire: { type: Boolean, default: false },
  locked: { type: Boolean, default: false },
  scenarioFirstPost: { type: Boolean, default: false },
})
const showGrimoire = computed(() => props.grimoire && props.post.content.includes('NEXUS-ARCANA-POWER-DIRECTORY'))
const isRaceDirectory = computed(() => props.post.content.includes('data-nexus-race-directory="1"'))

const emit = defineEmits(['edit', 'delete', 'react', 'avatarUpdated'])

const auth = useAuthStore()

// Collapse long posts
const COLLAPSE_HEIGHT = 500
const contentRef = ref(null)
const isLong = ref(false)
const expanded = ref(false)
onMounted(async () => {
  await nextTick()
  if (contentRef.value && contentRef.value.scrollHeight > COLLAPSE_HEIGHT) {
    isLong.value = true
  }
  initAccordion()
})

function initAccordion() {
  if (!contentRef.value || isRaceDirectory.value) return
  contentRef.value.querySelectorAll('h2').forEach(h2 => {
    const headerDiv = h2.parentElement
    const contentDiv = headerDiv?.nextElementSibling
    if (!headerDiv || !contentDiv) return

    headerDiv.style.cursor = 'pointer'
    headerDiv.style.userSelect = 'none'

    const indicator = document.createElement('span')
    indicator.textContent = '▼'
    indicator.style.cssText = 'font-size:0.55rem;opacity:0.6;transition:transform 0.25s;margin-left:auto;padding-left:0.5rem;flex-shrink:0;'
    h2.style.display = 'flex'
    h2.style.alignItems = 'center'
    h2.appendChild(indicator)

    headerDiv.addEventListener('click', () => {
      const collapsed = contentDiv.style.display === 'none'
      contentDiv.style.display = collapsed ? '' : 'none'
      indicator.style.transform = collapsed ? '' : 'rotate(-90deg)'
    })
  })
}

const canEdit = computed(() => {
  if (props.post.dice_result != null) return false
  if (!auth.isAuthenticated) return false
  if (props.scenarioFirstPost && !['admin', 'fondatrice'].includes(auth.user?.role)) return false
  if (props.locked && !['admin', 'fondatrice'].includes(auth.user?.role)) return false
  return auth.user?.id === props.post.author?.id || auth.isModerator
})

const canEditAvatar = computed(() =>
  auth.isAuthenticated && auth.user?.id === props.post.author?.id
)

const avatarInput = ref(null)
const avatarPreview = ref(null)
const uploadingAvatar = ref(false)

async function handleAvatarChange(e) {
  const file = e.target.files[0]
  if (!file) return
  avatarPreview.value = URL.createObjectURL(file)
  uploadingAvatar.value = true
  try {
    const form = new FormData()
    form.append('avatar', file)
    await api.patch('/users/me/', form)
    await auth.fetchProfile()
    emit('avatarUpdated')
  } catch (err) {
    console.error('Avatar update failed:', err)
  } finally {
    avatarPreview.value = null
    uploadingAvatar.value = false
  }
}

const pouvoirs = computed(() => {
  const raw = props.post.author?.pouvoirs
  if (!raw) return []
  return raw.split(/[\n,]/).map(p => p.trim()).filter(Boolean)
})

const signatureImageUrl = computed(() => {
  const signature = props.post.author?.signature?.trim()
  if (!signature) return null

  const bbcodeMatch = signature.match(/^\[img\](https?:\/\/[^\s\]]+)\[\/img\]$/i)
  const imageUrl = bbcodeMatch?.[1] || signature
  return /^https?:\/\/\S+\.(?:gif|png|jpe?g|webp)(?:[?#]\S*)?$/i.test(imageUrl)
    ? imageUrl
    : null
})

function formatSexe(sexe) {
  const map = { feminin: 'Féminin', masculin: 'Masculin', indetermine: 'Indéterminé' }
  return map[sexe] || sexe
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}
</script>

<style scoped>
.dice-result { padding:.75rem 1rem;margin:0 0 1rem;border:1px solid rgba(245,215,110,.45);border-radius:8px;background:rgba(245,215,110,.08);color:#f5d76e;display:flex;gap:.5rem;flex-wrap:wrap;align-items:center; }
.post-card {
  margin-bottom: 1rem;
  padding: 0;
  overflow: hidden;
}

/* ══ Layout deux colonnes ══ */
.post-layout {
  display: flex;
  align-items: stretch;
  min-height: 0;
}

/* ══════════════════════════════
   Colonne gauche
══════════════════════════════ */
.post-author-col {
  width: 200px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  border-right: 1px solid var(--border);
  background: rgba(109, 40, 217, 0.03);
}

/* Portrait 200 × 320 */
.author-portrait {
  width: 200px;
  height: 320px;
  flex-shrink: 0;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--bg-elevated, #1a1a2e), var(--bg, #0f0f1a));
  border-bottom: 1px solid var(--border);
  position: relative;
}

.portrait-editable {
  cursor: pointer;
}

.portrait-edit-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.55);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  color: #fff;
  font-size: 0.78rem;
  font-weight: 600;
  opacity: 0;
  transition: opacity 0.2s;
  cursor: pointer;
}

.portrait-editable:hover .portrait-edit-overlay {
  opacity: 1;
}

.portrait-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: top;
  display: block;
}

.portrait-initials {
  font-size: 4rem;
  font-weight: 700;
  color: var(--primary, #6d28d9);
  opacity: 0.6;
}

/* Corps de la sidebar (sous le portrait) */
.author-sidebar-body {
  padding: 0.75rem 0.65rem 0.9rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  flex: 1;
}

/* Pseudo en titre */
.author-pseudo-title {
  text-align: center;
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--gold, #f0c674);
  font-style: italic;
  letter-spacing: 0.02em;
  word-break: break-word;
  text-shadow: 0 0 8px rgba(240, 198, 116, 0.3);
}

.author-profile-gif {
  width: 100%;
  height: 96px;
  border: 1px solid var(--border);
  border-radius: 6px;
  overflow: hidden;
  background: var(--bg-elevated, #1a1a2e);
}

.author-profile-gif img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Séparateur décoratif */
.sidebar-divider {
  height: 1px;
  background: linear-gradient(to right, transparent, var(--border), transparent);
  margin: 0.1rem 0;
}

/* ── Stats list ── */
.author-stats {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.22rem;
}

.stat-row {
  display: flex;
  flex-direction: column;
  gap: 0.05rem;
  padding-left: 0.5rem;
  border-left: 2px solid rgba(109, 40, 217, 0.25);
}

/* Bloc multi-ligne (pouvoirs) */
.stat-row--block {
  gap: 0.15rem;
}

.stat-label {
  font-size: 0.58rem;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  font-weight: 700;
  color: var(--text-secondary, #8b8ba7);
  line-height: 1.2;
}

.stat-label::before {
  content: '› ';
  color: var(--accent, #a78bfa);
}

.stat-value {
  font-size: 0.7rem;
  color: var(--text-primary, #e2d9f3);
  line-height: 1.4;
  word-break: break-word;
  overflow-wrap: break-word;
}

.stat-value--highlight {
  color: var(--accent, #a78bfa);
  font-weight: 600;
}

.stat-value--gold {
  color: var(--gold, #f0c674);
  font-weight: 600;
}

/* Pouvoirs en liste */
.pouvoir-item {
  display: block;
  font-size: 0.68rem;
  color: var(--text-secondary, #8b8ba7);
  line-height: 1.5;
}

/* Compteurs avec léger fond */
.author-stats--counts {
  background: rgba(0, 0, 0, 0.15);
  border-radius: 6px;
  padding: 0.45rem 0.5rem;
  gap: 0.3rem;
}

/* ── Badges faction / race ── */
.author-badges {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  margin-top: 0.15rem;
}

.group-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.35rem 0.6rem;
  border-radius: 6px;
  border: 1px solid transparent;
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
  font-size: 0.75rem;
  flex-shrink: 0;
}

.badge-faction .badge-icon { color: var(--accent, #a78bfa); }
.badge-race .badge-icon    { color: var(--gold, #f0c674); }

.badge-text {
  display: flex;
  flex-direction: column;
  gap: 0.05rem;
  min-width: 0;
}

.badge-label {
  font-size: 0.55rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-weight: 700;
  color: var(--text-secondary, #8b8ba7);
}

.badge-value {
  font-size: 0.72rem;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.badge-faction .badge-value { color: var(--accent, #a78bfa); }
.badge-race .badge-value    { color: var(--gold, #f0c674); }

/* Badge rôle */
.role-badge-row {
  margin-top: 0.15rem;
  text-align: center;
}

.role-badge {
  display: inline-block;
  font-size: 0.62rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  padding: 0.2rem 0.6rem;
  border-radius: 999px;
}

.role-badge--admin {
  background: rgba(234, 179, 8, 0.18);
  color: #eab308;
  border: 1px solid rgba(234, 179, 8, 0.4);
}

.role-badge--mod {
  background: rgba(59, 130, 246, 0.18);
  color: #60a5fa;
  border: 1px solid rgba(59, 130, 246, 0.3);
}

/* ══════════════════════════════
   Colonne droite
══════════════════════════════ */
.post-body-col {
  flex: 1;
  min-width: 0;
  padding: 0.9rem 1.1rem;
  display: flex;
  flex-direction: column;
}

.post-meta-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.post-date {
  font-size: 0.72rem;
  color: var(--text-secondary, #8b8ba7);
}

.edited-badge {
  font-style: italic;
}

.post-actions {
  display: flex;
  gap: 0.25rem;
}

.post-body-divider {
  height: 1px;
  background: var(--border);
  margin-bottom: 0.85rem;
  opacity: 0.4;
}

.post-content {
  flex: 1;
  line-height: 1.75;
  overflow-x: auto;
  margin-bottom: 0.75rem;
}

.post-content--collapsed {
  max-height: 500px;
  overflow: hidden;
  mask-image: linear-gradient(to bottom, black 70%, transparent 100%);
  -webkit-mask-image: linear-gradient(to bottom, black 70%, transparent 100%);
}

.post-expand-row {
  text-align: center;
  margin: 0.5rem 0 0.75rem;
}

.post-expand-btn {
  background: none;
  border: 1px solid rgba(124, 58, 237, 0.35);
  color: #a78bfa;
  font-size: 0.8rem;
  padding: 0.3rem 1.2rem;
  border-radius: 20px;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}

.post-expand-btn:hover {
  background: rgba(124, 58, 237, 0.15);
  color: #c4b5fd;
}

.post-signature {
  border-top: 1px solid rgba(124, 58, 237, 0.2);
  margin: 0.25rem 0 0.85rem;
  padding-top: 0.85rem;
}

.post-signature-image {
  display: block;
  height: auto;
  max-height: 220px;
  max-width: 100%;
  object-fit: contain;
}

.post-signature-text {
  color: var(--text-secondary, #aaa5bf);
  font-size: 0.8rem;
  font-style: italic;
  line-height: 1.6;
  margin: 0;
  white-space: pre-line;
}

.post-content :deep(p),
.post-content :deep(td),
.post-content :deep(li) {
  white-space: pre-wrap;
}

/* ══ Responsive mobile ══ */
@media (max-width: 700px) {
  .post-layout {
    flex-direction: column;
  }

  .post-author-col {
    width: 100%;
    flex-direction: row;
    border-right: none;
    border-bottom: 1px solid var(--border);
  }

  .author-portrait {
    width: 90px;
    height: 144px;
    flex-shrink: 0;
    border-bottom: none;
    border-right: 1px solid var(--border);
  }

  .author-sidebar-body {
    padding: 0.6rem 0.75rem;
    overflow: hidden;
  }

  .author-pseudo-title {
    text-align: left;
  }

  .author-profile-gif {
    width: 100px;
    height: 56px;
  }

  .author-stats--counts,
  .author-badges,
  .role-badge-row {
    display: none;
  }
}
</style>
