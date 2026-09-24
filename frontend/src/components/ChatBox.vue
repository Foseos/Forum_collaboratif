<template>
  <div class="chatbox-wrapper" :class="{ open: isOpen }">

    <!-- Bouton toggle -->
    <button class="chatbox-toggle" @click="openChat" :title="isOpen ? 'Fermer le chat' : 'Ouvrir le chat'">
      <svg v-if="!isOpen" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
      </svg>
      <svg v-else width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
      </svg>
      <span v-if="!isOpen" class="chatbox-label">Chat de Nexus Arcana</span>
      <span v-if="unreadCount > 0 && !isOpen" class="chatbox-badge">{{ unreadCount > 99 ? '99+' : unreadCount }}</span>
    </button>

    <!-- Panneau chat -->
    <div class="chatbox-panel card">
      <!-- Header -->
      <div class="chatbox-header">
        <span class="chatbox-header-icon">✦</span>
        <span class="chatbox-header-title">Chat de Nexus Arcana</span>
        <span class="chatbox-online">{{ members.length }} connecté{{ members.length > 1 ? 's' : '' }}</span>
      </div>

      <div class="chatbox-members" aria-label="Membres présents dans le chat">
        <span v-if="presenceError" class="chatbox-presence-error">Présence indisponible momentanément</span>
        <span v-for="member in members" :key="member.id" class="chatbox-member">
          <img v-if="member.avatar" :src="member.avatar" alt="" class="chatbox-avatar" />
          <span class="chatbox-presence-dot" aria-hidden="true"></span>
          {{ member.username }}
        </span>
      </div>
      <p class="chatbox-history-note">Messages des dernières 24 heures</p>

      <!-- Messages -->
      <div class="chatbox-messages" ref="messagesEl">
        <div v-if="messages.length === 0" class="chatbox-empty">
          Aucun message pour l'instant. Soyez le premier à écrire !
        </div>
        <div
          v-for="msg in messages"
          :key="msg.id"
          class="chatbox-msg"
          :class="{ 'chatbox-msg--own': msg.author_username === auth.user?.username }"
        >
          <img
            v-if="msg.author_avatar"
            :src="msg.author_avatar"
            class="chatbox-avatar"
            :alt="msg.author_username"
          />
          <div v-else class="chatbox-avatar chatbox-avatar--placeholder">
            {{ msg.author_username?.charAt(0).toUpperCase() }}
          </div>
          <div class="chatbox-msg-body">
            <span class="chatbox-msg-author">{{ msg.author_username }}</span>
            <span class="chatbox-msg-text">{{ msg.content }}</span>
            <span class="chatbox-msg-time">{{ formatTime(msg.created_at) }}</span>
          </div>
        </div>
      </div>

      <!-- Emoji picker -->
      <div v-if="showEmojis" class="chatbox-emoji-panel">
        <div v-for="group in emojiGroups" :key="group.label" class="chatbox-emoji-section">
          <span class="chatbox-emoji-label">{{ group.label }}</span>
          <div class="chatbox-emoji-grid">
            <button v-for="e in group.emojis" :key="e" type="button" class="chatbox-emoji-btn" :aria-label="`Insérer ${e}`" @click="insertEmoji(e)">{{ e }}</button>
          </div>
        </div>
      </div>

      <!-- Input -->
      <div class="chatbox-input-row">
        <button class="chatbox-emoji-toggle" @click="showEmojis = !showEmojis" :title="showEmojis ? 'Fermer les smileys' : 'Smileys'" :class="{ active: showEmojis }">
          😊
        </button>
        <input
          ref="inputEl"
          v-model="inputText"
          class="chatbox-input"
          type="text"
          placeholder="Votre message…"
          maxlength="500"
          @keyup.enter="sendMessage"
        />
        <button class="chatbox-send" @click="sendMessage" :disabled="!inputText.trim() || sending">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="22" y1="2" x2="11" y2="13"/>
            <polygon points="22 2 15 22 11 13 2 9 22 2"/>
          </svg>
        </button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useAuthStore } from '../stores/auth'
import api from '../composables/useApi'

const auth = useAuthStore()
const isOpen = ref(false)
const messages = ref([])
const members = ref([])
const presenceError = ref(false)
const inputText = ref('')
const sending = ref(false)
const messagesEl = ref(null)
const inputEl = ref(null)
const showEmojis = ref(false)
const lastSeenId = ref(0)
const unreadCount = computed(() => isOpen.value ? 0 : messages.value.filter(msg => msg.id > lastSeenId.value).length)
let pollInterval = null
let fetching = false

const emojiGroups = [
  { label: 'Sourires & expressions', emojis: ['😀','😃','😄','😁','😆','😅','😂','🤣','🥲','🥹','😊','😇','🙂','🙃','😉','😍','🥰','😘','😗','😚','😙','😋','😛','😜','🤪','😝','🤑','🤗','🤭','🫢','🫣','🤫','🤔','🫡','😎','🤩','🥳','😏','🫠','🤓','🧐','🤠'] },
  { label: 'Humeurs & réactions', emojis: ['😐','😑','😶','🙄','😬','😮‍💨','😔','😪','😴','🤤','😷','🤒','🤕','🤢','🤮','🤧','🥵','🥶','🥴','😵','🤯','😕','🫤','😟','🙁','☹️','😮','😯','😲','😳','🥺','😦','😧','😨','😰','😥','😢','😭','😱','😖','😣','😞','😓','😩','😫','🥱','😤','😡','🤬'] },
  { label: 'Gestes & amitié', emojis: ['👋','🤚','🖐️','✋','🖖','👌','🤌','🤏','✌️','🤞','🤟','🤘','🤙','👈','👉','👆','👇','☝️','👍','👎','✊','👊','🤛','🤜','👏','🙌','👐','🤲','🤝','🙏','🫶','💪','👀','💯'] },
  { label: 'Cœurs & émotions', emojis: ['❤️','🧡','💛','💚','💙','💜','🖤','🤍','🤎','🩷','🩵','🩶','💔','❤️‍🔥','❤️‍🩹','💕','💞','💓','💗','💖','💘','💝','💟','❣️','💌','💋','🫂'] },
  { label: 'Magie & mystères', emojis: ['✨','🔮','🪄','🧙','🧙‍♀️','🧙‍♂️','🧚','🧛','🧛‍♀️','🧛‍♂️','🧜','🧞','🧟','🦸','🦹','👼','😈','👿','👹','👺','👻','💀','☠️','👽','🤖','🐉','🐲','🦄','🦇','🕷️','🕸️','🦂','🌙','🌛','🌜','🌑','🌕','⭐','🌟','💫','⚡','🔥','🌀','💎','🗡️','⚔️','🛡️','🕯️','⚗️','📜','🗝️','⚰️','🪦'] },
  { label: 'Animaux & nature', emojis: ['🐶','🐱','🐭','🐹','🐰','🦊','🐻','🐼','🐨','🐯','🦁','🐺','🐸','🐵','🙈','🙉','🙊','🦉','🦅','🐦','🐧','🦆','🦢','🦜','🦋','🐝','🐞','🐢','🐍','🦎','🐙','🐬','🐳','🦈','🦌','🐎','🐾','🌸','🌺','🌹','🥀','🌻','🌼','🌷','🪷','🌿','🍀','🍁','🍂','🍄','🌲','🌳','🌵','🌈','☀️','🌤️','☁️','⛈️','❄️','☃️','🌊'] },
  { label: 'Fêtes & gourmandises', emojis: ['🎉','🎊','🎈','🎁','🎀','🎂','🍰','🧁','🍪','🍩','🍫','🍬','🍭','🍯','🍎','🍓','🍒','🍉','🍇','🍑','🍋','🍍','🥐','🥖','🧀','🍕','🍔','🍟','🌮','🍿','🍣','🍜','🍦','☕','🍵','🧋','🥤','🍹','🍸','🍷','🍻','🥂','🎃','🎄','🎆','🎇'] },
  { label: 'Objets & loisirs', emojis: ['📚','📖','✍️','📝','💬','💭','📢','🔔','🎵','🎶','🎤','🎧','🎸','🎹','🎬','🎭','🎨','🎮','🎲','🧩','♟️','🏆','🥇','⚽','🏀','🏹','🎯','🚀','🏰','🏠','🌍','🧭','⏳','⌛','⏰','✅','❌','❓','❗','💤'] },
]

function insertEmoji(emoji) {
  const el = inputEl.value
  if (!el) { inputText.value += emoji; return }
  const start = el.selectionStart ?? inputText.value.length
  const end = el.selectionEnd ?? start
  inputText.value = inputText.value.slice(0, start) + emoji + inputText.value.slice(end)
  nextTick(() => {
    el.focus()
    el.setSelectionRange(start + emoji.length, start + emoji.length)
  })
}

async function fetchMessages() {
  if (fetching) return
  fetching = true
  try {
    const { data } = await api.get('/chat/')
    const list = Array.isArray(data) ? data : (data.results ?? [])
    const next = [...list].reverse()
    if (JSON.stringify(next) !== JSON.stringify(messages.value)) messages.value = next
  } catch {
    // silencieux
  } finally {
    fetching = false
  }
}

async function refreshPresence() {
  if (!isOpen.value || document.hidden) return
  try {
    const { data } = await api.post('/chat/presence/')
    if (isOpen.value) members.value = data
    presenceError.value = false
  } catch {
    members.value = []
    presenceError.value = true
  }
}

function refreshChat() {
  fetchMessages()
  refreshPresence()
}

function markRead() {
  lastSeenId.value = Math.max(lastSeenId.value, ...messages.value.map(msg => msg.id))
}

async function sendMessage() {
  const text = inputText.value.trim()
  if (!text || sending.value) return
  sending.value = true
  try {
    await api.post('/chat/', { content: text })
    inputText.value = ''
    await fetchMessages()
  } finally {
    sending.value = false
  }
}

function formatTime(iso) {
  const d = new Date(iso)
  return d.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
}

async function scrollToBottom() {
  await nextTick()
  if (messagesEl.value) {
    messagesEl.value.scrollTop = messagesEl.value.scrollHeight
  }
}

watch(messages, () => {
  if (isOpen.value) markRead()
  scrollToBottom()
})
watch(isOpen, (val) => {
  if (val) {
    markRead()
    refreshChat()
    scrollToBottom()
  } else {
    members.value = []
  }
})

function openChat() {
  isOpen.value = !isOpen.value
}

onMounted(() => {
  fetchMessages()
  pollInterval = setInterval(refreshChat, 5000)
  document.addEventListener('visibilitychange', refreshChat)
})

onUnmounted(() => {
  clearInterval(pollInterval)
  document.removeEventListener('visibilitychange', refreshChat)
})
</script>

<style scoped>
.chatbox-wrapper {
  position: fixed;
  bottom: 1.5rem;
  right: 1.5rem;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.75rem;
}

/* ── Bouton toggle ── */
.chatbox-toggle {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: linear-gradient(135deg, #6d28d9, #4c1d95);
  color: #f5d76e;
  border: 1px solid rgba(245,215,110,0.3);
  border-radius: 2rem;
  padding: 0.65rem 1.1rem;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 600;
  letter-spacing: 0.03em;
  box-shadow: 0 4px 20px rgba(109,40,217,0.4);
  transition: transform 0.2s, box-shadow 0.2s;
}
.chatbox-toggle:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 24px rgba(109,40,217,0.55);
}
.chatbox-label { white-space: nowrap; }

.chatbox-badge {
  position: absolute;
  top: -6px;
  right: -6px;
  background: #ef4444;
  color: #fff;
  font-size: 0.6rem;
  font-weight: 700;
  min-width: 18px;
  height: 18px;
  border-radius: 999px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 4px;
  border: 2px solid #0d0a1a;
  animation: badge-pop 0.25s cubic-bezier(0.34,1.56,0.64,1);
}
@keyframes badge-pop {
  from { transform: scale(0); opacity: 0; }
  to   { transform: scale(1); opacity: 1; }
}

/* ── Panneau ── */
.chatbox-panel {
  width: 340px;
  max-height: 480px;
  display: none;
  flex-direction: column;
  background: rgba(13,10,26,0.97);
  border: 1px solid rgba(124,58,237,0.35);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 8px 40px rgba(0,0,0,0.5), 0 0 0 1px rgba(124,58,237,0.1);
  backdrop-filter: blur(12px);
}
.chatbox-wrapper.open .chatbox-panel {
  display: flex;
}

/* Header */
.chatbox-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: linear-gradient(90deg, rgba(109,40,217,0.25), rgba(109,40,217,0.08));
  border-bottom: 1px solid rgba(124,58,237,0.25);
}
.chatbox-header-icon { color: #f5d76e; font-size: 0.75rem; }
.chatbox-header-title {
  flex: 1;
  font-size: 0.85rem;
  font-weight: 600;
  color: #e2d9f3;
  letter-spacing: 0.05em;
}
.chatbox-online {
  font-size: 0.7rem;
  color: #a78bfa;
}
.chatbox-members { display: flex; flex-wrap: wrap; gap: 0.45rem; padding: 0.6rem 0.75rem; max-height: 90px; overflow-y: auto; flex-shrink: 0; }
.chatbox-member { display: inline-flex; align-items: center; gap: 0.3rem; color: #e2d9f3; font-size: 0.72rem; overflow-wrap: anywhere; }
.chatbox-presence-dot { width: 6px; height: 6px; border-radius: 50%; background: #4ade80; flex-shrink: 0; }
.chatbox-history-note, .chatbox-presence-error { margin: 0; padding: 0 0.75rem 0.4rem; color: #a99abb; font-size: 0.68rem; }

/* Messages */
.chatbox-messages {
  min-height: 0;
  flex: 1;
  overflow-y: auto;
  padding: 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  scrollbar-width: thin;
  scrollbar-color: rgba(124,58,237,0.3) transparent;
}
.chatbox-empty {
  text-align: center;
  color: #4b3a6b;
  font-size: 0.8rem;
  font-style: italic;
  margin: auto;
  padding: 2rem 0;
}

/* Message */
.chatbox-msg {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.chatbox-msg--own {
  flex-direction: row-reverse;
}
.chatbox-avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid rgba(124,58,237,0.4);
  flex-shrink: 0;
}
.chatbox-avatar--placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(109,40,217,0.3);
  color: #a78bfa;
  font-size: 0.7rem;
  font-weight: 700;
}
.chatbox-msg-body {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
  max-width: 75%;
}
.chatbox-msg--own .chatbox-msg-body { align-items: flex-end; }

.chatbox-msg-author {
  font-size: 0.65rem;
  color: #7c3aed;
  font-weight: 600;
  letter-spacing: 0.04em;
}
.chatbox-msg-text {
  background: rgba(109,40,217,0.15);
  border: 1px solid rgba(124,58,237,0.2);
  border-radius: 8px;
  padding: 0.35rem 0.6rem;
  font-size: 0.8rem;
  color: #e2d9f3;
  line-height: 1.4;
  word-break: break-word;
}
.chatbox-msg--own .chatbox-msg-text {
  background: rgba(109,40,217,0.3);
  border-color: rgba(124,58,237,0.4);
}
.chatbox-msg-time {
  font-size: 0.6rem;
  color: #4b3a6b;
}

/* Emoji picker */
.chatbox-emoji-panel {
  border-top: 1px solid rgba(124,58,237,0.2);
  background: rgba(13,10,26,0.8);
  padding: 0.5rem 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  max-height: 160px;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: rgba(124,58,237,0.3) transparent;
}
.chatbox-emoji-section { display: flex; flex-direction: column; gap: 0.2rem; }
.chatbox-emoji-label {
  font-size: 0.6rem;
  color: #7c3aed;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-weight: 600;
}
.chatbox-emoji-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 2px;
}
.chatbox-emoji-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.15rem;
  line-height: 1;
  padding: 3px 4px;
  border-radius: 4px;
  transition: background 0.15s, transform 0.1s;
}
.chatbox-emoji-btn:hover {
  background: rgba(124,58,237,0.2);
  transform: scale(1.2);
}

.chatbox-emoji-toggle {
  background: none;
  border: 1px solid rgba(124,58,237,0.2);
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  padding: 0.3rem 0.4rem;
  line-height: 1;
  transition: background 0.15s, border-color 0.15s;
  flex-shrink: 0;
}
.chatbox-emoji-toggle:hover,
.chatbox-emoji-toggle.active {
  background: rgba(124,58,237,0.2);
  border-color: rgba(124,58,237,0.5);
}

/* Input */
.chatbox-input-row {
  display: flex;
  gap: 0.5rem;
  padding: 0.6rem 0.75rem;
  border-top: 1px solid rgba(124,58,237,0.2);
  background: rgba(13,10,26,0.6);
}
.chatbox-input {
  flex: 1;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(124,58,237,0.25);
  border-radius: 6px;
  color: #e2d9f3;
  font-size: 0.8rem;
  padding: 0.4rem 0.7rem;
  outline: none;
  transition: border-color 0.2s;
}
.chatbox-input:focus { border-color: rgba(124,58,237,0.6); }
.chatbox-input::placeholder { color: #4b3a6b; }

.chatbox-send {
  background: linear-gradient(135deg, #6d28d9, #4c1d95);
  border: none;
  border-radius: 6px;
  color: #f5d76e;
  padding: 0.4rem 0.65rem;
  cursor: pointer;
  transition: opacity 0.2s, transform 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}
.chatbox-send:hover:not(:disabled) { transform: translateY(-1px); opacity: 0.9; }
.chatbox-send:disabled { opacity: 0.4; cursor: not-allowed; }

@media (max-width: 480px) {
  .chatbox-wrapper { bottom: 1rem; right: 1rem; }
  .chatbox-panel { width: calc(100vw - 2rem); }
}
</style>
