<template>
  <div class="rte-wrapper card">
    <!-- Header -->
    <div class="rte-header">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="color:var(--accent)"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
      <span>{{ isFiche ? 'Créer ma fiche de présentation' : 'Nouveau sujet' }}</span>
    </div>

    <!-- Title field -->
    <div class="rte-fields">
      <div class="form-group">
        <label class="rte-label">Titre du sujet <span class="rte-required">*</span></label>
        <input
          v-model="topicTitle"
          class="form-input rte-title-input"
          :placeholder="isFiche ? 'Ex : Présentation de Léa Moreau' : 'Titre du sujet'"
        />
      </div>
    </div>

    <!-- Editor body: emoji panel + text area -->
    <div class="rte-body">

      <!-- Emoji panel (left) -->
      <div class="rte-emoji-panel" :class="{ 'is-open': showEmojis }">
        <div class="rte-emoji-header">Emojis</div>
        <div class="rte-emoji-categories">
          <button
            v-for="cat in emojiCategories"
            :key="cat.label"
            class="rte-emoji-cat-btn"
            :class="{ active: activeCategory === cat.label }"
            :title="cat.label"
            @click="activeCategory = cat.label"
          >{{ cat.icon }}</button>
        </div>
        <div class="rte-emoji-grid">
          <button
            v-for="e in currentEmojis"
            :key="e"
            class="rte-emoji-btn"
            @mousedown.prevent="insertEmoji(e)"
          >{{ e }}</button>
        </div>
      </div>

      <!-- Text editor area -->
      <div class="rte-editor-col">
        <!-- Toolbar -->
        <div class="rte-toolbar">
          <!-- Formatting -->
          <button class="rte-tool" title="Gras (Ctrl+B)" @mousedown.prevent="exec('bold')">
            <strong>B</strong>
          </button>
          <button class="rte-tool rte-tool--italic" title="Italique (Ctrl+I)" @mousedown.prevent="exec('italic')">
            <em>I</em>
          </button>
          <button class="rte-tool rte-tool--underline" title="Souligné (Ctrl+U)" @mousedown.prevent="exec('underline')">
            <span style="text-decoration:underline">U</span>
          </button>
          <button class="rte-tool" title="Barré" @mousedown.prevent="exec('strikeThrough')">
            <span style="text-decoration:line-through">S</span>
          </button>

          <div class="rte-tool-sep"></div>

          <!-- Alignment -->
          <button class="rte-tool" title="Aligner à gauche" @mousedown.prevent="exec('justifyLeft')">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="15" y2="12"/><line x1="3" y1="18" x2="18" y2="18"/></svg>
          </button>
          <button class="rte-tool" title="Centrer" @mousedown.prevent="exec('justifyCenter')">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="6" y1="12" x2="18" y2="12"/><line x1="4" y1="18" x2="20" y2="18"/></svg>
          </button>
          <button class="rte-tool" title="Aligner à droite" @mousedown.prevent="exec('justifyRight')">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="9" y1="12" x2="21" y2="12"/><line x1="6" y1="18" x2="21" y2="18"/></svg>
          </button>

          <div class="rte-tool-sep"></div>

          <!-- Lists -->
          <button class="rte-tool" title="Liste à puces" @mousedown.prevent="exec('insertUnorderedList')">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><line x1="9" y1="6" x2="20" y2="6"/><line x1="9" y1="12" x2="20" y2="12"/><line x1="9" y1="18" x2="20" y2="18"/><circle cx="4" cy="6" r="1.5" fill="currentColor" stroke="none"/><circle cx="4" cy="12" r="1.5" fill="currentColor" stroke="none"/><circle cx="4" cy="18" r="1.5" fill="currentColor" stroke="none"/></svg>
          </button>
          <button class="rte-tool" title="Liste numérotée" @mousedown.prevent="exec('insertOrderedList')">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><line x1="10" y1="6" x2="21" y2="6"/><line x1="10" y1="12" x2="21" y2="12"/><line x1="10" y1="18" x2="21" y2="18"/><text x="2" y="8" font-size="7" fill="currentColor" stroke="none" font-family="monospace">1.</text><text x="2" y="14" font-size="7" fill="currentColor" stroke="none" font-family="monospace">2.</text><text x="2" y="20" font-size="7" fill="currentColor" stroke="none" font-family="monospace">3.</text></svg>
          </button>

          <div class="rte-tool-sep"></div>

          <!-- Link -->
          <button class="rte-tool" title="Insérer un lien" @mousedown.prevent="insertLink">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>
          </button>

          <!-- Emoji toggle -->
          <button
            class="rte-tool rte-tool--emoji"
            :class="{ active: showEmojis }"
            title="Emojis"
            @mousedown.prevent="showEmojis = !showEmojis"
          >😊</button>
        </div>

        <!-- Contenteditable zone -->
        <div
          ref="editorEl"
          class="rte-content"
          contenteditable="true"
          :data-placeholder="isFiche ? 'Rédigez votre fiche de présentation ici…' : 'Contenu du message…'"
          @input="onInput"
          @keydown="onKeydown"
        ></div>

        <div class="rte-hint">Conseil : sélectionnez du texte puis cliquez un bouton pour le mettre en forme.</div>
      </div>
    </div>

    <!-- Preview -->
    <Transition name="rte-preview">
      <div v-if="showPreview && contentHtml" class="rte-preview">
        <div class="rte-preview-label">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
          Prévisualisation
        </div>
        <div class="rte-preview-body" v-html="contentHtml"></div>
      </div>
    </Transition>

    <!-- Actions -->
    <div class="rte-actions">
      <button class="btn btn-secondary btn-sm" @click="togglePreview">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
        {{ showPreview ? 'Masquer' : 'Prévisualiser' }}
      </button>
      <div class="rte-actions-right">
        <button class="btn btn-secondary btn-sm" @click="$emit('cancel')">Annuler</button>
        <button
          class="btn btn-primary btn-sm"
          :disabled="!topicTitle.trim() || !contentHtml.trim() || loading"
          @click="submit"
        >
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
          {{ loading ? 'Envoi…' : isFiche ? '✨ Envoyer la fiche' : 'Envoyer' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  isFiche: { type: Boolean, default: false },
  loading: { type: Boolean, default: false },
})

const emit = defineEmits(['submit', 'cancel'])

// ── State ──────────────────────────────────────────────────────────────────
const topicTitle = ref('')
const contentHtml = ref('')
const showEmojis = ref(false)
const showPreview = ref(false)
const activeCategory = ref('Expressions')
const editorEl = ref(null)

// ── Emoji data ─────────────────────────────────────────────────────────────
const emojiCategories = [
  {
    label: 'Expressions',
    icon: '😊',
    emojis: ['😊','😂','😍','🥰','😎','😏','🤔','😮','😢','😡','🤣','😅','😇','🙄','😬','🥺','😴','🤯','😤','🥳','😌','😋','🤩','😜'],
  },
  {
    label: 'Magie',
    icon: '✨',
    emojis: ['✨','🔮','🌙','⚡','🌟','💫','🔥','🌹','🌿','🦋','🌊','🌸','🍃','🌺','🌙','☀️','🌈','💨','❄️','🌙','🕯️','📿','🔯','☯️'],
  },
  {
    label: 'RPG',
    icon: '⚔️',
    emojis: ['⚔️','🛡️','🏰','🐉','🧙','🧝','🧜','👑','💎','📜','🗡️','🏹','🪄','🔐','💰','⚗️','🗺️','🧿','🪬','🧲','🐦‍⬛','🦅','🐺','🐍'],
  },
  {
    label: 'Cœurs',
    icon: '❤️',
    emojis: ['❤️','💙','💚','💛','🧡','💜','🖤','🤍','💕','💖','💗','💝','💞','💓','💘','🩷','🩵','🩶','❣️','💔','🫀','🫶','🤝','🤜'],
  },
]

const currentEmojis = computed(() => {
  const cat = emojiCategories.find(c => c.label === activeCategory.value)
  return cat ? cat.emojis : []
})

// ── Editor actions ─────────────────────────────────────────────────────────
function exec(command, value = null) {
  editorEl.value?.focus()
  document.execCommand(command, false, value)
  onInput()
}

function onInput() {
  contentHtml.value = editorEl.value?.innerHTML || ''
}

function onKeydown(e) {
  // Tab inserts spaces instead of losing focus
  if (e.key === 'Tab') {
    e.preventDefault()
    exec('insertText', '    ')
  }
}

function insertEmoji(emoji) {
  editorEl.value?.focus()
  exec('insertText', emoji)
}

function insertLink() {
  const url = prompt('URL du lien :')
  if (url) exec('createLink', url)
}

function togglePreview() {
  showPreview.value = !showPreview.value
}

function submit() {
  if (!topicTitle.value.trim() || !contentHtml.value.trim()) return
  emit('submit', {
    title: topicTitle.value,
    content: contentHtml.value,
  })
  topicTitle.value = ''
  contentHtml.value = ''
  if (editorEl.value) editorEl.value.innerHTML = ''
  showPreview.value = false
}
</script>

<style scoped>
/* ── Wrapper ─────────────────────────────────────────────────────────────── */
.rte-wrapper {
  padding: 0;
  overflow: hidden;
  margin-bottom: 1.5rem;
}

/* ── Header ──────────────────────────────────────────────────────────────── */
.rte-header {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.875rem 1.25rem;
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text);
  border-bottom: 1px solid var(--border);
  background: rgba(139, 92, 246, 0.05);
}

/* ── Fields (title) ──────────────────────────────────────────────────────── */
.rte-fields {
  padding: 1rem 1.25rem 0;
}

.rte-label {
  font-size: 0.78rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-secondary);
  display: block;
  margin-bottom: 0.4rem;
}

.rte-required {
  color: var(--ember);
}

.rte-title-input {
  font-size: 1rem;
  font-weight: 500;
}

/* ── Body layout ─────────────────────────────────────────────────────────── */
.rte-body {
  display: flex;
  gap: 0;
  margin-top: 1rem;
  border-top: 1px solid var(--border);
  min-height: 300px;
}

/* ── Emoji panel ─────────────────────────────────────────────────────────── */
.rte-emoji-panel {
  width: 0;
  min-width: 0;
  overflow: hidden;
  transition: width 0.22s ease, min-width 0.22s ease;
  border-right: 0 solid var(--border);
  background: var(--bg-secondary);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.rte-emoji-panel.is-open {
  width: 200px;
  min-width: 200px;
  border-right-width: 1px;
}

.rte-emoji-header {
  padding: 0.6rem 0.75rem 0.4rem;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-muted);
  white-space: nowrap;
}

.rte-emoji-categories {
  display: flex;
  gap: 0.2rem;
  padding: 0 0.5rem 0.5rem;
  flex-wrap: wrap;
}

.rte-emoji-cat-btn {
  background: transparent;
  border: 1px solid transparent;
  border-radius: 6px;
  padding: 0.2rem 0.35rem;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.15s;
  line-height: 1;
}

.rte-emoji-cat-btn:hover,
.rte-emoji-cat-btn.active {
  background: var(--primary-light);
  border-color: var(--border-strong);
}

.rte-emoji-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.15rem;
  padding: 0 0.5rem 0.75rem;
  overflow-y: auto;
  flex: 1;
}

.rte-emoji-btn {
  background: transparent;
  border: none;
  border-radius: 6px;
  padding: 0.3rem;
  font-size: 1.1rem;
  cursor: pointer;
  text-align: center;
  transition: all 0.12s;
  line-height: 1;
}

.rte-emoji-btn:hover {
  background: var(--primary-light);
  transform: scale(1.2);
}

/* ── Editor column ───────────────────────────────────────────────────────── */
.rte-editor-col {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

/* ── Toolbar ─────────────────────────────────────────────────────────────── */
.rte-toolbar {
  display: flex;
  align-items: center;
  gap: 0.15rem;
  padding: 0.5rem 0.75rem;
  border-bottom: 1px solid var(--border);
  flex-wrap: wrap;
  background: rgba(0, 0, 0, 0.1);
}

.rte-tool {
  background: transparent;
  border: 1px solid transparent;
  border-radius: 5px;
  padding: 0.25rem 0.4rem;
  cursor: pointer;
  color: var(--text-secondary);
  font-size: 0.85rem;
  line-height: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 28px;
  min-height: 28px;
  transition: all 0.15s;
  font-family: inherit;
}

.rte-tool:hover,
.rte-tool.active {
  background: var(--primary-light);
  border-color: var(--border-strong);
  color: var(--text);
}

.rte-tool--italic em { font-style: italic; }
.rte-tool--underline span { text-decoration: underline; }
.rte-tool--emoji { font-size: 1rem; }

.rte-tool-sep {
  width: 1px;
  height: 20px;
  background: var(--border);
  margin: 0 0.2rem;
  flex-shrink: 0;
}

/* ── Contenteditable ─────────────────────────────────────────────────────── */
.rte-content {
  flex: 1;
  min-height: 220px;
  padding: 1rem 1.25rem;
  outline: none;
  color: var(--text);
  font-size: 0.9rem;
  line-height: 1.7;
  overflow-y: auto;
  white-space: pre-wrap;
  word-break: break-word;
}

.rte-content:empty::before {
  content: attr(data-placeholder);
  color: var(--text-muted);
  pointer-events: none;
}

.rte-content :deep(a) { color: var(--accent); text-decoration: underline; }
.rte-content :deep(strong) { color: var(--text); font-weight: 700; }
.rte-content :deep(em) { font-style: italic; }
.rte-content :deep(ul) { padding-left: 1.5rem; }
.rte-content :deep(ol) { padding-left: 1.5rem; }

.rte-hint {
  padding: 0.35rem 1.25rem 0.5rem;
  font-size: 0.68rem;
  color: var(--text-muted);
  font-style: italic;
  border-top: 1px solid var(--border);
}

/* ── Preview ─────────────────────────────────────────────────────────────── */
.rte-preview {
  border-top: 1px solid var(--border);
  padding: 1rem 1.25rem;
  background: rgba(139, 92, 246, 0.03);
}

.rte-preview-label {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-muted);
  margin-bottom: 0.75rem;
}

.rte-preview-body {
  font-size: 0.9rem;
  line-height: 1.7;
  color: var(--text);
}

.rte-preview-body :deep(a) { color: var(--accent); }
.rte-preview-body :deep(strong) { font-weight: 700; }
.rte-preview-body :deep(ul) { padding-left: 1.5rem; }
.rte-preview-body :deep(ol) { padding-left: 1.5rem; }

.rte-preview-enter-active,
.rte-preview-leave-active {
  transition: opacity 0.2s, transform 0.2s;
}
.rte-preview-enter-from,
.rte-preview-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}

/* ── Actions ─────────────────────────────────────────────────────────────── */
.rte-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  padding: 0.875rem 1.25rem;
  border-top: 1px solid var(--border);
  background: rgba(0, 0, 0, 0.1);
  flex-wrap: wrap;
}

.rte-actions-right {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

/* ── Responsive ──────────────────────────────────────────────────────────── */
@media (max-width: 640px) {
  .rte-emoji-panel.is-open {
    width: 160px;
    min-width: 160px;
  }

  .rte-emoji-grid {
    grid-template-columns: repeat(4, 1fr);
  }

  .rte-toolbar {
    gap: 0.1rem;
    padding: 0.4rem 0.5rem;
  }

  .rte-tool {
    min-width: 26px;
    min-height: 26px;
    font-size: 0.8rem;
  }

  .rte-actions {
    flex-direction: column;
    align-items: stretch;
  }

  .rte-actions-right {
    justify-content: flex-end;
  }
}
</style>
