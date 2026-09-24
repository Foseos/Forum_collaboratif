<template>
  <div class="page">
    <div class="container">

      <div class="page-header">
        <h1 class="page-title">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
            <circle cx="9" cy="7" r="4"/>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
          </svg>
          Membres de Nexus Arcana
        </h1>
        <p class="page-subtitle">Les personnages de tous les univers réunis à Nexus Arcana</p>
      </div>

      <!-- Toolbar -->
      <div class="toolbar">
        <div class="search-wrap">
          <svg class="search-icon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
          </svg>
          <input v-model="search" class="search-input" type="text" placeholder="Rechercher…" />
        </div>
        <span class="member-count">{{ filteredUsers.length }} membre{{ filteredUsers.length > 1 ? 's' : '' }}</span>
      </div>

      <div v-if="loading" class="loading-state">
        <span class="spinner-small"></span> Invocation des membres…
      </div>
      <div v-else-if="error" class="alert alert-danger">{{ error }}</div>
      <div v-else-if="filteredUsers.length === 0" class="empty-state">Aucun membre trouvé.</div>

      <div v-else class="members-grid">
        <div v-for="user in filteredUsers" :key="user.id" class="member-card">

          <!-- Zone cliquable → profil -->
          <router-link :to="`/membres/${user.id}`" class="card-link">
            <!-- Portrait -->
            <div class="portrait-wrap">
              <img v-if="user.avatar" :src="user.avatar" :alt="user.username" class="portrait-img" />
              <div v-else class="portrait-placeholder">{{ user.username?.[0]?.toUpperCase() || '?' }}</div>
              <span class="role-pip" :class="`role-${user.role}`" :title="getRoleLabel(user.role)"></span>
            </div>

            <!-- Infos -->
            <div class="card-info">
              <span class="card-username">{{ user.username }}</span>
              <span v-if="user.race" class="card-race">{{ user.race }}</span>
              <span class="card-last-login" :class="lastLoginClass(user)" :title="lastLoginFull(user)">
                <svg width="8" height="8" viewBox="0 0 8 8"><circle cx="4" cy="4" r="4" fill="currentColor"/></svg>
                {{ lastLoginShort(user) }}
              </span>
            </div>
          </router-link>

          <router-link
            v-if="['admin', 'fondatrice'].includes(auth.user?.role)"
            :to="`/membres/${user.id}?ip=1`"
            class="mp-btn ip-shortcut"
            title="Consulter les adresses IP de ce membre"
          >🔒 IP</router-link>

          <router-link
            v-if="['admin', 'fondatrice'].includes(auth.user?.role) && user.role === 'user' && auth.user?.id !== user.id"
            :to="`/membres/${user.id}?supprimer=1`"
            class="mp-btn"
            title="Ouvrir la confirmation de suppression de ce personnage"
          >Supprimer</router-link>

          <!-- Bouton MP (connecté + pas soi-même) -->
          <router-link
            v-if="auth.isAuthenticated && auth.user?.id !== user.id"
            :to="`/messageries?to=${user.id}&username=${user.username}`"
            class="mp-btn"
            title="Envoyer un message privé"
          >
            <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            </svg>
            MP
          </router-link>

        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onBeforeUnmount, onMounted } from 'vue'
import api from '../composables/useApi'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const users = ref([])
const loading = ref(true)
const error = ref('')
const search = ref('')

const roleLabels = {
  fondatrice: 'Fondatrice',
  admin: 'Administrateur',
  moderator: 'Modérateur',
  user: 'Membre',
}

function getRoleLabel(role) {
  return roleLabels[role] || 'Membre'
}

// ── Dernière connexion ──────────────────────────────────────────
function activityDate(user) {
  return user.last_seen || user.last_login
}

function lastLoginClass(user) {
  const raw = activityDate(user)
  if (!raw) return 'login-never'
  const diff = Date.now() - new Date(raw).getTime()
  const h = diff / 3600000
  if (diff < 120000) return 'login-online'
  if (h < 24)   return 'login-today'
  if (h < 168)  return 'login-week'
  return 'login-old'
}

function lastLoginShort(user) {
  const raw = activityDate(user)
  if (raw && Date.now() - new Date(raw).getTime() < 120000) return 'en ligne'
  if (!raw) return 'jamais connecté'
  const d = new Date(raw)
  const diff = Date.now() - d.getTime()
  const mins  = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days  = Math.floor(diff / 86400000)
  if (mins < 2)   return 'à l\'instant'
  if (mins < 60)  return `il y a ${mins} min`
  if (hours < 24) return `il y a ${hours} h`
  if (days === 1) return 'hier'
  if (days < 7)   return `il y a ${days} jours`
  // Au-delà d'une semaine : afficher le jour abrégé + heure
  return d.toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit', year: '2-digit' })
}

function lastLoginFull(user) {
  const raw = activityDate(user)
  if (raw && Date.now() - new Date(raw).getTime() < 120000) return 'Membre actuellement en ligne'
  if (!raw) return 'Jamais connecté'
  const d = new Date(raw)
  const date = d.toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })
  const heure = d.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
  return `Dernière connexion : ${date} à ${heure}`
}

const filteredUsers = computed(() => {
  const q = search.value.trim().toLowerCase()
  const matchingUsers = q ? users.value.filter(u =>
    u.username?.toLowerCase().includes(q) ||
    u.pseudo?.toLowerCase().includes(q) ||
    u.race?.toLowerCase().includes(q) ||
    u.groupe?.toLowerCase().includes(q)
  ) : users.value

  return [...matchingUsers].sort((a, b) => {
    const aDate = Date.parse(activityDate(a)) || 0
    const bDate = Date.parse(activityDate(b)) || 0
    return bDate - aDate
  })
})

async function fetchUsers() {
  try {
    const { data } = await api.get('/users/')
    users.value = data.results || data
  } catch {
    error.value = 'Impossible de recenser les membres de Nexus Arcana.'
  } finally {
    loading.value = false
  }
}

onMounted(fetchUsers)
const refreshTimer = window.setInterval(fetchUsers, 30000)
onBeforeUnmount(() => window.clearInterval(refreshTimer))
</script>

<style scoped>
.page-header { margin-bottom: 1.5rem; }

.page-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
.page-title svg { color: var(--accent); flex-shrink: 0; }
.page-subtitle { color: var(--text-secondary); font-size: 0.9rem; margin-top: 0.4rem; }

/* Toolbar */
.toolbar {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}
.search-wrap { position: relative; flex: 1; min-width: 180px; }
.search-icon {
  position: absolute;
  left: 0.7rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-secondary);
  pointer-events: none;
}
.search-input {
  width: 100%;
  padding: 0.5rem 0.875rem 0.5rem 2.1rem;
  background: var(--glass-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  color: var(--text);
  font-size: 0.875rem;
  transition: border-color var(--transition);
}
.search-input:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(139,92,246,0.1);
}
.member-count {
  font-size: 0.78rem;
  color: var(--text-secondary);
  white-space: nowrap;
  padding: 0.35rem 0.75rem;
  background: var(--glass-bg);
  border: 1px solid var(--border);
  border-radius: 99px;
}

/* States */
.loading-state {
  text-align: center;
  padding: 3rem;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
}
.empty-state { text-align: center; padding: 3rem; color: var(--text-secondary); font-style: italic; }
.alert { padding: 1rem 1.5rem; border-radius: var(--radius); text-align: center; }
.alert-danger { background: rgba(239,68,68,0.1); color: #ef4444; border: 1px solid rgba(239,68,68,0.3); }

/* Grid */
.members-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(110px, 1fr));
  gap: 0.875rem;
}

/* Card wrapper */
.member-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  border-radius: var(--radius);
  background: var(--glass-bg);
  border: 1px solid var(--border);
  overflow: hidden;
  transition: transform var(--transition), box-shadow var(--transition), border-color var(--transition);
}
.member-card:hover {
  transform: translateY(-3px);
  border-color: rgba(139,92,246,0.45);
  box-shadow: 0 6px 24px rgba(109,40,217,0.18);
}

/* Lien profil */
.card-link {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 0.5rem 0.5rem;
  text-decoration: none;
  width: 100%;
}

/* Portrait */
.portrait-wrap {
  position: relative;
  width: 72px;
  height: 96px;
  border-radius: 6px;
  overflow: hidden;
  flex-shrink: 0;
  box-shadow: 0 2px 12px rgba(0,0,0,0.35);
}
.portrait-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: top center;
  transition: transform 0.35s ease;
}
.member-card:hover .portrait-img { transform: scale(1.06); }
.portrait-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(109,40,217,0.3), rgba(139,92,246,0.1));
  font-family: var(--font-display);
  font-size: 2rem;
  font-weight: 700;
  color: var(--primary-light);
}

/* Pip rôle */
.role-pip {
  position: absolute;
  top: 4px;
  right: 4px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  border: 1.5px solid rgba(0,0,0,0.4);
}
.role-fondatrice { background: #f5d76e; box-shadow: 0 0 5px rgba(245,215,110,0.7); }
.role-admin      { background: #f87171; box-shadow: 0 0 5px rgba(248,113,113,0.7); }
.role-moderator  { background: #a78bfa; box-shadow: 0 0 5px rgba(167,139,250,0.7); }
.role-user       { background: #64748b; }

/* Infos */
.card-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.1rem;
  width: 100%;
  min-width: 0;
}
.card-username {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}
.card-pseudo {
  font-size: 0.65rem;
  color: var(--gold);
  font-style: italic;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}
.card-race {
  font-size: 0.62rem;
  color: var(--text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}

/* Dernière connexion */
.card-last-login {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.58rem;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
  cursor: default;
  opacity: 0.85;
}
.login-online { color: #22c55e; font-weight: 700; } /* vert vif — actif */
.login-today  { color: #4ade80; }   /* vert  — < 24 h    */
.login-week   { color: #fb923c; }   /* orange — < 7 jours */
.login-old    { color: var(--text-secondary); }  /* gris  — > 7 jours  */
.login-never  { color: var(--text-secondary); font-style: italic; }

/* Bouton MP */
.mp-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
  width: 100%;
  padding: 0.35rem 0;
  background: rgba(139,92,246,0.1);
  border-top: 1px solid rgba(139,92,246,0.2);
  color: var(--accent);
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-decoration: none;
  transition: background var(--transition), color var(--transition);
  cursor: pointer;
}
.mp-btn:hover {
  background: rgba(139,92,246,0.25);
  color: #c4b5fd;
}

/* Spinner */
.spinner-small {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255,255,255,0.2);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  display: inline-block;
  flex-shrink: 0;
}
@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 480px) {
  .members-grid { grid-template-columns: repeat(auto-fill, minmax(90px, 1fr)); gap: 0.6rem; }
}
</style>
