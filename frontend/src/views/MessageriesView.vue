<template>
  <div class="page msg-page">
    <div class="container">

      <!-- ── Layout principal ── -->
      <div class="msg-layout">

        <!-- ══ SIDEBAR ══ -->
        <aside class="msg-sidebar">
          <button class="btn btn-primary btn-new-msg" @click="openCompose(null)">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
            Nouveau message
          </button>

          <nav class="msg-nav">
            <button class="msg-nav-item" :class="{ active: tab === 'inbox' }" @click="tab = 'inbox'">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/></svg>
              Réception
              <span v-if="unreadCount > 0" class="nav-badge">{{ unreadCount }}</span>
            </button>
            <button class="msg-nav-item" :class="{ active: tab === 'sent' }" @click="tab = 'sent'">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
              Envoyés
            </button>
            <button class="msg-nav-item" :class="{ active: tab === 'trash' }" @click="tab = 'trash'">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/></svg>
              Corbeille
            </button>
          </nav>
        </aside>

        <!-- ══ LISTE ══ -->
        <section class="msg-list-pane">

          <!-- Barre de recherche -->
          <div class="msg-list-toolbar">
            <div class="search-wrap">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="search-icon"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
              <input v-model="search" class="search-input" placeholder="Rechercher…" />
            </div>
            <span class="list-title">{{ tabLabel }}</span>
          </div>

          <div v-if="listLoading" class="list-loading">
            <span class="spinner-small"></span>
          </div>

          <div v-else-if="filteredList.length === 0" class="list-empty">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1"><path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/></svg>
            <p>{{ tab === 'trash' ? 'Corbeille vide' : 'Aucun message' }}</p>
          </div>

          <ul v-else class="msg-list">
            <li
              v-for="msg in filteredList"
              :key="msg.id"
              class="msg-item"
              :class="{ unread: tab === 'inbox' && !msg.is_read, active: selected?.id === msg.id }"
              @click="openMessage(msg)"
            >
              <div class="msg-item-avatar">
                <img v-if="correspondentAvatar(msg)" :src="correspondentAvatar(msg)" class="item-avatar-img" />
                <span v-else class="item-avatar-placeholder">{{ correspondentName(msg)[0]?.toUpperCase() }}</span>
              </div>
              <div class="msg-item-body">
                <div class="msg-item-top">
                  <span class="msg-item-name">{{ correspondentName(msg) }}</span>
                  <span class="msg-item-date">{{ formatDate(msg.created_at) }}</span>
                </div>
                <div class="msg-item-subject">{{ msg.subject || '(Sans objet)' }}</div>
                <div class="msg-item-preview">{{ stripHtml(msg.body) }}</div>
              </div>
              <span v-if="tab === 'inbox' && !msg.is_read" class="unread-dot"></span>
            </li>
          </ul>
        </section>

        <!-- ══ DÉTAIL ══ -->
        <section class="msg-detail-pane">
          <div v-if="!selected && !composing" class="detail-empty">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
            <p>Sélectionnez un message</p>
          </div>

          <!-- Formulaire de composition -->
          <div v-else-if="composing" class="compose-form">
            <div class="compose-header">
              <h3>{{ replyTo ? 'Répondre' : 'Nouveau message' }}</h3>
              <button class="btn-icon" @click="composing = false; replyTo = null">✕</button>
            </div>

            <div class="compose-field">
              <label>À</label>
              <div class="recipient-input-wrap">
                <input
                  v-model="compose.recipientSearch"
                  class="form-input"
                  placeholder="Nom d'utilisateur…"
                  @input="searchRecipients"
                  :disabled="!!compose.recipient"
                />
                <span v-if="compose.recipient" class="recipient-chip">
                  {{ compose.recipientName }}
                  <button @click="compose.recipient = null; compose.recipientName = ''; compose.recipientSearch = ''">✕</button>
                </span>
              </div>
              <ul v-if="recipientSuggestions.length && !compose.recipient" class="suggestions">
                <li v-for="u in recipientSuggestions" :key="u.id" @click="selectRecipient(u)">
                  <img v-if="u.avatar" :src="u.avatar" class="suggest-avatar" />
                  <span v-else class="suggest-placeholder">{{ u.username[0] }}</span>
                  {{ u.username }}
                </li>
              </ul>
            </div>

            <div class="compose-field">
              <label>Objet</label>
              <input v-model="compose.subject" class="form-input" placeholder="Sujet du message…" />
            </div>

            <div class="compose-field compose-body-field">
              <label>Message</label>
              <textarea v-model="compose.body" class="form-input compose-textarea" rows="10" placeholder="Votre message…"></textarea>
            </div>

            <div class="compose-actions">
              <button class="btn btn-primary" :disabled="sending || !compose.recipient || !compose.body.trim()" @click="sendMessage">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
                {{ sending ? 'Envoi…' : 'Envoyer' }}
              </button>
              <button class="btn btn-ghost" @click="composing = false; replyTo = null">Annuler</button>
            </div>
            <p v-if="sendError" class="send-error">{{ sendError }}</p>
          </div>

          <!-- Message ouvert -->
          <div v-else-if="selected" class="msg-detail">
            <div class="detail-header">
              <h3 class="detail-subject">{{ selected.subject || '(Sans objet)' }}</h3>
              <div class="detail-meta">
                <div class="detail-avatar">
                  <img v-if="correspondentAvatar(selected)" :src="correspondentAvatar(selected)" class="detail-avatar-img" />
                  <span v-else class="detail-avatar-placeholder">{{ correspondentName(selected)[0]?.toUpperCase() }}</span>
                </div>
                <div class="detail-from">
                  <span class="detail-from-name">{{ tab === 'sent' ? `À : ${selected.recipient_username}` : `De : ${selected.sender_username}` }}</span>
                  <span class="detail-from-date">{{ formatDateFull(selected.created_at) }}</span>
                </div>
              </div>
            </div>

            <div class="detail-body">{{ selected.body }}</div>

            <div class="detail-actions">
              <button v-if="tab === 'inbox'" class="btn btn-secondary btn-sm" @click="openCompose(selected)">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 17 4 12 9 7"/><path d="M20 18v-2a4 4 0 0 0-4-4H4"/></svg>
                Répondre
              </button>
              <button v-if="tab === 'inbox'" class="btn btn-ghost btn-sm" @click="toggleRead(selected)">
                {{ selected.is_read ? 'Marquer non lu' : 'Marquer lu' }}
              </button>
              <button class="btn btn-danger btn-sm" @click="deleteMessage(selected)">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/></svg>
                Supprimer
              </button>
            </div>
          </div>
        </section>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../composables/useApi'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const route = useRoute()

// ── State ──
const tab = ref('inbox')
const inbox = ref([])
const sent = ref([])
const trash = ref([])
const unreadCount = ref(0)
const listLoading = ref(false)
const selected = ref(null)
const composing = ref(false)
const replyTo = ref(null)
const search = ref('')
const sending = ref(false)
const sendError = ref('')

const compose = ref({
  recipient: null,
  recipientName: '',
  recipientSearch: '',
  subject: '',
  body: '',
})
const recipientSuggestions = ref([])
let allUsers = []

// ── Tab label ──
const tabLabel = computed(() => ({ inbox: 'Boîte de réception', sent: 'Messages envoyés', trash: 'Corbeille' }[tab.value]))

// ── Current list ──
const currentList = computed(() => {
  if (tab.value === 'inbox') return inbox.value
  if (tab.value === 'sent')  return sent.value
  return trash.value
})

const filteredList = computed(() => {
  const q = search.value.trim().toLowerCase()
  if (!q) return currentList.value
  return currentList.value.filter(m =>
    m.subject?.toLowerCase().includes(q) ||
    m.body?.toLowerCase().includes(q) ||
    m.sender_username?.toLowerCase().includes(q) ||
    m.recipient_username?.toLowerCase().includes(q)
  )
})

// ── Helpers ──
function correspondentName(msg) {
  return tab.value === 'sent' ? msg.recipient_username : msg.sender_username
}
function correspondentAvatar(msg) {
  return tab.value === 'sent' ? msg.recipient_avatar : msg.sender_avatar
}
function stripHtml(str) {
  return (str || '').replace(/<[^>]+>/g, '').slice(0, 80)
}
function formatDate(d) {
  if (!d) return ''
  const date = new Date(d)
  const now = new Date()
  if (date.toDateString() === now.toDateString()) {
    return date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
  }
  return date.toLocaleDateString('fr-FR', { day: 'numeric', month: 'short' })
}
function formatDateFull(d) {
  if (!d) return ''
  return new Date(d).toLocaleString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

// ── Fetch ──
async function fetchInbox() {
  listLoading.value = true
  try {
    const { data } = await api.get('/messages/')
    inbox.value = data.results || data
  } finally { listLoading.value = false }
}
async function fetchSent() {
  listLoading.value = true
  try {
    const { data } = await api.get('/messages/sent/')
    sent.value = data.results || data
  } finally { listLoading.value = false }
}
async function fetchUnread() {
  try {
    const { data } = await api.get('/messages/unread/')
    unreadCount.value = data.unread
  } catch { /* silent */ }
}

// Trash = messages supprimés de l'inbox ou envoyés
async function fetchTrash() {
  // Re-fetch both avec deleted flags exposés en combinant les deux listes filtrées côté front
  // Pour simplifier : on recharge inbox+sent complets depuis une vue dédiée
  // Ici on montre juste les messages supprimés déjà dans les listes locales
  listLoading.value = false
}

watch(tab, async (val) => {
  selected.value = null
  composing.value = false
  search.value = ''
  if (val === 'inbox') await fetchInbox()
  else if (val === 'sent') await fetchSent()
})

// ── Actions ──
async function openMessage(msg) {
  selected.value = msg
  composing.value = false
  if (tab.value === 'inbox' && !msg.is_read) {
    try {
      await api.get(`/messages/${msg.id}/`)
      msg.is_read = true
      unreadCount.value = Math.max(0, unreadCount.value - 1)
    } catch { /* silent */ }
  }
}

function openCompose(replyMsg) {
  composing.value = true
  selected.value = null
  replyTo.value = replyMsg
  sendError.value = ''
  compose.value = {
    recipient: replyMsg ? replyMsg.sender : null,
    recipientName: replyMsg ? replyMsg.sender_username : '',
    recipientSearch: replyMsg ? replyMsg.sender_username : '',
    subject: replyMsg ? `Re: ${replyMsg.subject}` : '',
    body: '',
  }
  recipientSuggestions.value = []
}

async function searchRecipients() {
  const q = compose.value.recipientSearch.trim().toLowerCase()
  if (!q) { recipientSuggestions.value = []; return }
  if (!allUsers.length) {
    const { data } = await api.get('/users/')
    allUsers = data.results || data
  }
  recipientSuggestions.value = allUsers
    .filter(u => u.username.toLowerCase().includes(q) && u.id !== auth.user?.id)
    .slice(0, 6)
}

function selectRecipient(u) {
  compose.value.recipient = u.id
  compose.value.recipientName = u.username
  compose.value.recipientSearch = u.username
  recipientSuggestions.value = []
}

async function sendMessage() {
  sending.value = true
  sendError.value = ''
  try {
    await api.post('/messages/send/', {
      recipient: compose.value.recipient,
      subject: compose.value.subject || '(Sans objet)',
      body: compose.value.body,
    })
    composing.value = false
    replyTo.value = null
    if (tab.value === 'sent') await fetchSent()
    else await fetchSent() // refresh silently
  } catch (e) {
    sendError.value = e.response?.data?.detail || e.response?.data?.recipient?.[0] || 'Erreur lors de l\'envoi.'
  } finally { sending.value = false }
}

async function toggleRead(msg) {
  try {
    const { data } = await api.patch(`/messages/${msg.id}/read/`)
    msg.is_read = data.is_read
    await fetchUnread()
  } catch { /* silent */ }
}

async function deleteMessage(msg) {
  try {
    await api.delete(`/messages/${msg.id}/`)
    if (tab.value === 'inbox') inbox.value = inbox.value.filter(m => m.id !== msg.id)
    else if (tab.value === 'sent') sent.value = sent.value.filter(m => m.id !== msg.id)
    selected.value = null
    await fetchUnread()
  } catch { /* silent */ }
}

// ── Init ──
onMounted(async () => {
  await fetchInbox()
  await fetchUnread()

  // Pré-remplir depuis ?to=id&username=xxx (bouton MP de MembresView)
  if (route.query.to && route.query.username) {
    openCompose(null)
    compose.value.recipient = Number(route.query.to)
    compose.value.recipientName = route.query.username
    compose.value.recipientSearch = route.query.username
  }
})
</script>

<style scoped>
.msg-page { padding: 1.5rem 0 3rem; }

/* Layout 3 colonnes */
.msg-layout {
  display: grid;
  grid-template-columns: 200px 320px 1fr;
  grid-template-rows: auto;
  gap: 0;
  min-height: 600px;
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  background: var(--glass-bg);
}

/* ── Sidebar ── */
.msg-sidebar {
  background: var(--bg-deep);
  border-right: 1px solid var(--border);
  padding: 1rem 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.btn-new-msg {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-size: 0.82rem;
  padding: 0.6rem 0.75rem;
}

.msg-nav { display: flex; flex-direction: column; gap: 0.2rem; }

.msg-nav-item {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.55rem 0.75rem;
  border-radius: var(--radius);
  background: none;
  border: none;
  color: var(--text-secondary);
  font-size: 0.82rem;
  cursor: pointer;
  text-align: left;
  transition: background var(--transition), color var(--transition);
  position: relative;
}
.msg-nav-item:hover { background: rgba(139,92,246,0.1); color: var(--text); }
.msg-nav-item.active { background: rgba(139,92,246,0.18); color: var(--accent); }
.msg-nav-item svg { flex-shrink: 0; }

.nav-badge {
  margin-left: auto;
  background: var(--accent);
  color: #fff;
  font-size: 0.6rem;
  font-weight: 700;
  padding: 0.1rem 0.4rem;
  border-radius: 99px;
  min-width: 18px;
  text-align: center;
}

/* ── Liste ── */
.msg-list-pane {
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.msg-list-toolbar {
  padding: 0.75rem;
  border-bottom: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  background: var(--bg-secondary);
}

.list-title {
  font-size: 0.68rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-secondary);
  font-weight: 600;
}

.search-wrap { position: relative; }
.search-icon { position: absolute; left: 0.6rem; top: 50%; transform: translateY(-50%); color: var(--text-secondary); pointer-events: none; }
.search-input {
  width: 100%;
  padding: 0.4rem 0.75rem 0.4rem 2rem;
  background: var(--glass-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  color: var(--text);
  font-size: 0.8rem;
}
.search-input:focus { outline: none; border-color: var(--accent); }

.list-loading, .list-empty {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  color: var(--text-secondary);
  font-size: 0.85rem;
  padding: 2rem;
  text-align: center;
}
.list-empty svg { opacity: 0.3; }

.msg-list { list-style: none; margin: 0; padding: 0; overflow-y: auto; flex: 1; }

.msg-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 0.85rem 0.875rem;
  border-bottom: 1px solid var(--border);
  cursor: pointer;
  transition: background var(--transition);
  position: relative;
}
.msg-item:hover { background: rgba(139,92,246,0.06); }
.msg-item.active { background: rgba(139,92,246,0.12); }
.msg-item.unread { background: rgba(139,92,246,0.05); }
.msg-item.unread .msg-item-name { color: var(--text); font-weight: 700; }
.msg-item.unread .msg-item-subject { color: var(--text); font-weight: 600; }

.msg-item-avatar { flex-shrink: 0; }
.item-avatar-img { width: 36px; height: 36px; border-radius: 50%; object-fit: cover; }
.item-avatar-placeholder {
  width: 36px; height: 36px; border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  display: flex; align-items: center; justify-content: center;
  font-size: 0.9rem; font-weight: 700; color: #fff;
}

.msg-item-body { flex: 1; min-width: 0; }
.msg-item-top { display: flex; justify-content: space-between; align-items: baseline; gap: 0.5rem; margin-bottom: 0.15rem; }
.msg-item-name { font-size: 0.82rem; color: var(--text-secondary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.msg-item-date { font-size: 0.68rem; color: var(--text-secondary); flex-shrink: 0; }
.msg-item-subject { font-size: 0.82rem; color: var(--text-secondary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.msg-item-preview { font-size: 0.75rem; color: var(--text-secondary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; opacity: 0.7; margin-top: 0.1rem; }

.unread-dot {
  position: absolute;
  left: 0.35rem;
  top: 50%;
  transform: translateY(-50%);
  width: 6px; height: 6px;
  border-radius: 50%;
  background: var(--accent);
  box-shadow: 0 0 6px rgba(139,92,246,0.7);
}

/* ── Détail ── */
.msg-detail-pane {
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.detail-empty {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  color: var(--text-secondary);
  opacity: 0.5;
}
.detail-empty svg { opacity: 0.4; }

/* ── Message ouvert ── */
.msg-detail { display: flex; flex-direction: column; height: 100%; }

.detail-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid var(--border);
  background: var(--bg-secondary);
}
.detail-subject { font-size: 1.05rem; font-weight: 700; color: var(--text); margin: 0 0 0.75rem; }
.detail-meta { display: flex; align-items: center; gap: 0.75rem; }
.detail-avatar-img { width: 40px; height: 40px; border-radius: 50%; object-fit: cover; }
.detail-avatar-placeholder {
  width: 40px; height: 40px; border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  display: flex; align-items: center; justify-content: center;
  font-size: 1rem; font-weight: 700; color: #fff;
}
.detail-from { display: flex; flex-direction: column; gap: 0.15rem; }
.detail-from-name { font-size: 0.875rem; font-weight: 600; color: var(--text); }
.detail-from-date { font-size: 0.72rem; color: var(--text-secondary); }

.detail-body {
  flex: 1;
  padding: 1.5rem;
  font-size: 0.9rem;
  line-height: 1.8;
  color: var(--text);
  white-space: pre-wrap;
  overflow-y: auto;
}

.detail-actions {
  padding: 1rem 1.5rem;
  border-top: 1px solid var(--border);
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  background: var(--bg-secondary);
}

.btn-danger {
  background: rgba(239,68,68,0.15);
  color: #f87171;
  border: 1px solid rgba(239,68,68,0.3);
}
.btn-danger:hover { background: rgba(239,68,68,0.25); }

/* ── Composer ── */
.compose-form {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 1.25rem 1.5rem;
  gap: 1rem;
  overflow-y: auto;
}
.compose-header { display: flex; align-items: center; justify-content: space-between; }
.compose-header h3 { font-size: 1rem; font-weight: 700; color: var(--text); margin: 0; }
.btn-icon { background: none; border: none; color: var(--text-secondary); cursor: pointer; font-size: 1rem; padding: 0.25rem; border-radius: 4px; }
.btn-icon:hover { color: var(--text); background: rgba(255,255,255,0.06); }

.compose-field { display: flex; flex-direction: column; gap: 0.35rem; }
.compose-field label { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.06em; font-weight: 700; color: var(--text-secondary); }
.compose-body-field { flex: 1; }
.compose-textarea { resize: vertical; min-height: 180px; font-size: 0.875rem; line-height: 1.7; }

.recipient-input-wrap { position: relative; display: flex; align-items: center; gap: 0.5rem; }
.recipient-chip {
  display: inline-flex; align-items: center; gap: 0.35rem;
  background: rgba(139,92,246,0.15); border: 1px solid rgba(139,92,246,0.3);
  color: var(--accent); border-radius: 99px; padding: 0.2rem 0.6rem; font-size: 0.8rem;
}
.recipient-chip button { background: none; border: none; color: var(--accent); cursor: pointer; font-size: 0.75rem; padding: 0; }

.suggestions {
  list-style: none; margin: 0; padding: 0;
  border: 1px solid var(--border-strong); border-radius: var(--radius);
  background: var(--bg-elevated); max-height: 180px; overflow-y: auto;
}
.suggestions li {
  display: flex; align-items: center; gap: 0.6rem;
  padding: 0.5rem 0.875rem; cursor: pointer; font-size: 0.85rem;
  transition: background var(--transition);
}
.suggestions li:hover { background: rgba(139,92,246,0.1); }
.suggest-avatar { width: 26px; height: 26px; border-radius: 50%; object-fit: cover; }
.suggest-placeholder {
  width: 26px; height: 26px; border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  display: flex; align-items: center; justify-content: center;
  font-size: 0.75rem; font-weight: 700; color: #fff; flex-shrink: 0;
}

.compose-actions { display: flex; gap: 0.75rem; }
.send-error { margin: 0; font-size: 0.82rem; color: #f87171; }

/* ── Spinner ── */
.spinner-small {
  width: 20px; height: 20px;
  border: 2px solid rgba(255,255,255,0.2);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  display: inline-block;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ── Responsive ── */
@media (max-width: 900px) {
  .msg-layout {
    grid-template-columns: 1fr;
    grid-template-rows: auto auto 1fr;
  }
  .msg-sidebar { flex-direction: row; align-items: center; border-right: none; border-bottom: 1px solid var(--border); padding: 0.75rem; }
  .msg-nav { flex-direction: row; }
  .btn-new-msg { width: auto; }
  .msg-list-pane { border-right: none; border-bottom: 1px solid var(--border); max-height: 300px; }
}
</style>
