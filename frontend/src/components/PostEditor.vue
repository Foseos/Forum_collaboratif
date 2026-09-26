<template>
  <div class="post-editor card">
    <!-- En-tête avec onglets -->
    <div class="editor-header">
      <h4>{{ editPost ? 'Modifier le message' : 'Répondre' }}</h4>
      <div class="editor-tabs">
        <button :class="['tab-btn', { active: tab === 'write' }]" @click="tab = 'write'">✏️ Rédiger</button>
        <button :class="['tab-btn', { active: tab === 'preview' }]" @click="tab = 'preview'">👁 Aperçu</button>
      </div>
    </div>

    <!-- Barre d'outils (mode rédaction uniquement) -->
    <div v-if="tab === 'write'" class="editor-toolbar">
      <template v-if="!sourceMode">
      <button type="button" class="tool-btn" title="Gras" aria-label="Gras" @mousedown.prevent="format('bold')"><strong>G</strong></button>
      <button type="button" class="tool-btn" title="Italique" aria-label="Italique" @mousedown.prevent="format('italic')"><em>I</em></button>
      <button type="button" class="tool-btn" title="Souligné" aria-label="Souligné" @mousedown.prevent="format('underline')"><u>S</u></button>
      <button type="button" class="tool-btn" title="Barré" aria-label="Barré" @mousedown.prevent="format('strikeThrough')"><s>B</s></button>
      <span class="tool-sep"></span>
      <button type="button" class="tool-btn" title="Aligner à gauche" aria-label="Aligner à gauche" @mousedown.prevent="align('justifyLeft')">☰</button>
      <button type="button" class="tool-btn" title="Centrer" aria-label="Centrer" @mousedown.prevent="align('justifyCenter')">≡</button>
      <button type="button" class="tool-btn" title="Aligner à droite" aria-label="Aligner à droite" @mousedown.prevent="align('justifyRight')">☷</button>
      <span class="tool-sep"></span>
      <label class="color-tool" title="Choisir la couleur du texte">Couleur <input type="color" value="#a78bfa" aria-label="Couleur du texte" @pointerdown="rememberSelection" @input="applyColor($event.target.value)" /></label>
      <button type="button" class="tool-btn" title="Citation" @mousedown.prevent="format('formatBlock', 'blockquote')">❝</button>
      <span class="tool-sep"></span>
      <button type="button" class="tool-btn image-tool" title="Ajouter une image ou un GIF depuis votre ordinateur" :disabled="uploadingImage" @mousedown.prevent="imageInput?.click()">{{ uploadingImage ? 'Envoi…' : '🖼 Image / GIF' }}</button>
      <button type="button" class="tool-btn image-tool" title="Ajouter une image par adresse web" @mousedown.prevent="showImageUrl = !showImageUrl">🔗 Adresse d’image</button>
      <button type="button" class="tool-btn image-tool" title="Insérer un lien vers une page ou un sujet" @mousedown.prevent="openLinkInput">🔗 Lien</button>
      <button v-if="selectedImage" type="button" class="tool-btn image-tool" title="Supprimer l’image sélectionnée" @mousedown.prevent="removeSelectedImage">🗑️ Image</button>
      <input ref="imageInput" type="file" accept="image/png,image/jpeg,image/gif,image/webp" hidden @change="uploadImage" />
      <span class="tool-sep"></span>
      <button type="button" :class="['tool-btn', 'emoji-toggle', { active: showEmoji }]" @mousedown.prevent="showEmoji = !showEmoji">😊 Smileys</button>
      </template>
      <button v-if="editPost" type="button" :class="['tool-btn', 'source-tool', { active: sourceMode }]" @mousedown.prevent="toggleSourceMode">{{ sourceMode ? '✏️ Visuel' : '〈/〉 Code HTML' }}</button>
    </div>

    <div v-if="showImageUrl && tab === 'write' && !sourceMode" class="image-url-bar">
      <input v-model="imageUrl" class="form-input" type="url" placeholder="https://exemple.fr/image.gif" aria-label="Adresse de l’image" @keydown.enter.prevent="insertImageUrl" />
      <button type="button" class="btn btn-secondary btn-sm" @click="insertImageUrl">Insérer</button>
    </div>
    <p v-if="showImageUrl && tab === 'write' && !sourceMode" class="external-image-note">Une image externe est chargée depuis son site d’origine, qui peut recevoir les données techniques du visiteur. Utilisez seulement une image que vous êtes autorisé à partager.</p>
    <div v-if="showLinkUrl && tab === 'write' && !sourceMode" class="image-url-bar">
      <input v-model="linkLabel" class="form-input" type="text" placeholder="Texte du lien" aria-label="Texte du lien" />
      <input v-model="linkUrl" class="form-input" type="text" placeholder="/topics/mon-sujet ou https://…" aria-label="Adresse du lien" @keydown.enter.prevent="insertLink" />
      <button type="button" class="btn btn-secondary btn-sm" @click="insertLink">Insérer</button>
    </div>
    <p v-if="imageError" class="image-error" role="alert">{{ imageError }}</p>
    <p v-if="selectedImage && tab === 'write' && !sourceMode" class="image-hint">Image sélectionnée : choisissez « Image / GIF » ou « Adresse d’image » pour la remplacer.</p>

    <!-- Panneau d'émojis -->
    <div v-if="showEmoji && tab === 'write' && !sourceMode" class="emoji-panel">
      <div v-for="cat in EMOJI_CATS" :key="cat.label" class="emoji-cat">
        <span class="emoji-cat-label">{{ cat.label }}</span>
        <div class="emoji-grid">
          <button
            v-for="e in cat.items"
            :key="e"
            class="emoji-btn"
            :title="e"
            @mousedown.prevent="insertEmoji(e)"
          >{{ e }}</button>
        </div>
      </div>
    </div>

    <!-- Zone de rédaction visuelle -->
    <div v-show="tab === 'write'" class="form-group">
      <div v-show="!sourceMode" ref="editorRef" class="form-input editor-textarea" contenteditable="true" role="textbox" aria-label="Texte de la réponse" aria-multiline="true" data-placeholder="Écrivez votre message…" @input="syncContent" @paste="pastePlainText" @keyup="rememberSelection" @mouseup="rememberSelection" @click="selectImage"></div>
      <textarea v-if="sourceMode" v-model="content" class="form-input source-textarea" aria-label="Code HTML de la fiche" rows="18"></textarea>
    </div>

    <!-- Aperçu -->
    <div v-if="tab === 'preview'" class="preview-panel">
      <div v-if="hasContent" class="preview-content" v-html="content"></div>
      <p v-else class="preview-empty">Rien à prévisualiser pour l'instant…</p>
    </div>

    <!-- Actions -->
    <p v-if="draftStatus" class="text-sm text-secondary" role="status">{{ draftStatus }}</p>
    <div class="editor-actions">
      <span class="char-count">{{ content.length }} caractères</span>
      <button v-if="editPost" class="btn btn-secondary btn-sm" @click="$emit('cancel')">
        Annuler
      </button>
      <button
        class="btn btn-primary btn-sm"
        :disabled="!hasContent || loading || uploadingImage"
        @click="submit"
      >
        {{ loading ? 'Envoi…' : editPost ? 'Modifier' : 'Envoyer' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useLocalDraft } from '../composables/useLocalDraft'
import api from '../composables/useApi'

const props = defineProps({
  editPost: { type: Object, default: null },
  loading:  { type: Boolean, default: false },
  startInSourceMode: { type: Boolean, default: false },
})
const emit = defineEmits(['submit', 'cancel'])

const tab         = ref('write')
const content     = ref(props.editPost?.content || '')
const showEmoji   = ref(false)
const sourceMode = ref(props.startInSourceMode)
const selectedImage = ref(null)
const showImageUrl = ref(false)
const showLinkUrl = ref(false)
const imageUrl = ref('')
const linkUrl = ref('')
const linkLabel = ref('')
const imageError = ref('')
const uploadingImage = ref(false)
const imageInput = ref(null)
const editorRef = ref(null)
let savedRange = null
const hasContent = computed(() => sourceMode.value ? !!content.value.trim() : !!(editorRef.value?.textContent?.trim() || editorRef.value?.querySelector('img') || content.value.replace(/<[^>]*>/g, '').trim()))

const route = useRoute()
const auth = useAuthStore()
const draftKey = computed(() => auth.user?.id ? `nexus:draft:${auth.user.id}:post:${route.params.slug}:${props.editPost?.id || 'reply'}` : null)
const { status: draftStatus, clear: clearDraft } = useLocalDraft(
  draftKey, () => ({ content: content.value }), value => { content.value = value.content },
  () => ({ content: props.editPost?.content || '' }),
)

onMounted(() => { if (editorRef.value) editorRef.value.innerHTML = content.value })

function syncContent() { content.value = editorRef.value?.innerHTML || '' }

function toggleSourceMode() {
  sourceMode.value = !sourceMode.value
  selectedImage.value = null
  if (!sourceMode.value && editorRef.value) editorRef.value.innerHTML = content.value
}

function selectImage(event) {
  selectedImage.value = event.target instanceof HTMLImageElement ? event.target : null
}

function removeSelectedImage() {
  selectedImage.value?.remove()
  selectedImage.value = null
  syncContent()
}

function rememberSelection() {
  const selection = window.getSelection()
  if (selection?.rangeCount && editorRef.value?.contains(selection.anchorNode)) savedRange = selection.getRangeAt(0).cloneRange()
}

function restoreSelection() {
  editorRef.value?.focus()
  if (savedRange && editorRef.value?.contains(savedRange.commonAncestorContainer)) {
    const selection = window.getSelection()
    selection.removeAllRanges()
    selection.addRange(savedRange)
  }
}

function format(command, value = null) {
  restoreSelection()
  document.execCommand(command, false, value)
  syncContent()
  rememberSelection()
}

function applyColor(color) {
  restoreSelection()
  document.execCommand('styleWithCSS', false, true)
  document.execCommand('foreColor', false, color)
  syncContent()
  rememberSelection()
}

function align(command) {
  restoreSelection()
  document.execCommand('styleWithCSS', false, true)
  document.execCommand(command, false, null)
  syncContent()
  rememberSelection()
}

function insertEmoji(emoji) { format('insertText', emoji) }

function pastePlainText(event) {
  event.preventDefault()
  format('insertText', event.clipboardData?.getData('text/plain') || '')
}

function insertImage(src) {
  if (selectedImage.value && editorRef.value?.contains(selectedImage.value)) {
    selectedImage.value.src = src
    selectedImage.value = null
    syncContent()
    return
  }
  restoreSelection()
  const image = document.createElement('img')
  image.src = src
  image.alt = 'Image du message'
  image.style.cssText = 'display:block;max-width:100%;max-height:500px;object-fit:contain;margin:0.7rem 0;border-radius:6px;'
  document.execCommand('insertHTML', false, image.outerHTML)
  syncContent()
  rememberSelection()
}

function insertImageUrl() {
  imageError.value = ''
  let url
  try { url = new URL(imageUrl.value.trim()) } catch { imageError.value = 'Indiquez une adresse d’image valide.'; return }
  if (!['http:', 'https:'].includes(url.protocol)) { imageError.value = 'Utilisez une adresse commençant par https:// ou http://.'; return }
  insertImage(url.href)
  imageUrl.value = ''
  showImageUrl.value = false
}

function openLinkInput() {
  rememberSelection()
  linkLabel.value = window.getSelection()?.toString() || ''
  showLinkUrl.value = !showLinkUrl.value
}

function insertLink() {
  imageError.value = ''
  const raw = linkUrl.value.trim()
  let href = raw
  if (!/^\/(?!\/)/.test(raw)) {
    try {
      const parsed = new URL(raw)
      if (!['http:', 'https:'].includes(parsed.protocol)) throw new Error('protocol')
      href = parsed.href
    } catch { imageError.value = 'Indiquez une adresse de page valide.'; return }
  }
  restoreSelection()
  const anchor = document.createElement('a')
  anchor.href = href
  anchor.textContent = linkLabel.value.trim() || href
  document.execCommand('insertHTML', false, anchor.outerHTML)
  syncContent()
  rememberSelection()
  linkUrl.value = ''
  linkLabel.value = ''
  showLinkUrl.value = false
}

async function uploadImage(event) {
  const file = event.target.files?.[0]
  if (!file) return
  imageError.value = ''
  if (file.size > 5 * 1024 * 1024) { imageError.value = 'L’image doit peser moins de 5 Mo.'; event.target.value = ''; return }
  uploadingImage.value = true
  try {
    const data = new FormData()
    data.append('image', file)
    const response = await api.post('/posts/images/', data)
    insertImage(response.data.url)
  } catch (error) {
    imageError.value = error.response?.data?.detail || 'Impossible d’ajouter cette image.'
  } finally {
    uploadingImage.value = false
    event.target.value = ''
  }
}

// ── Émojis ──────────────────────────────────────────────────────
const EMOJI_CATS = [
  {
    label: 'Smileys',
    items: ['😀','😂','🤣','😊','😍','🥰','😘','😎','🤔','😅','😭','😤','😱','🤩','😏',
            '🥺','😴','🤗','😇','🙃','😈','🤫','😬','🫠','😵','🥹','😻'],
  },
  {
    label: 'Cœurs & Sentiments',
    items: ['❤️','🧡','💛','💚','💙','💜','🖤','🤍','💕','💖','💗','💘','💝','💞','💓','💔','🫶','✨'],
  },
  {
    label: 'Fantastique & Magie',
    items: ['🧙','🧝','🧜','🧛','🦋','🐉','🦅','🌺','🌸','🔮','🪄','📜','🕯️','⚔️','🗡️','🛡️','👑','💎','🌙','⭐','🌟','💫','🔥','🌈'],
  },
  {
    label: 'Gestes & Réactions',
    items: ['👍','👎','👏','🙌','🤝','💪','✌️','🖖','🤜','🤛','🫂','🙏','🤦','🤷','💁'],
  },
  {
    label: 'Divers',
    items: ['🎉','🎊','🎭','🎩','📸','🎵','🎶','🌹','🍀','🦄','🐺','🌊','⚡','🌿','🍄'],
  },
]

// ── Envoi ────────────────────────────────────────────────────────
function submit() {
  if (!hasContent.value || uploadingImage.value) return
  const raw = content.value
  const savedKey = draftKey.value
  emit('submit', raw, () => {
    if (draftKey.value === savedKey && content.value !== raw) return
    clearDraft(savedKey)
    if (!props.editPost && draftKey.value === savedKey) {
      content.value = ''
      if (editorRef.value) editorRef.value.innerHTML = ''
      tab.value = 'write'
      showEmoji.value = false
    }
  })
}
</script>

<style scoped>
.external-image-note { margin: .35rem .5rem .65rem; color: var(--text-secondary); font-size: .78rem; line-height: 1.5; }
.post-editor { padding: 1.25rem; }

/* En-tête */
.editor-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.75rem;
  gap: 1rem;
  flex-wrap: wrap;
}
.editor-header h4 {
  margin: 0;
  font-size: 0.9375rem;
}

/* Onglets */
.editor-tabs { display: flex; gap: 0.25rem; }
.tab-btn {
  padding: 0.3rem 0.85rem;
  border-radius: 6px;
  font-size: 0.78rem;
  border: 1px solid rgba(124,58,237,0.3);
  background: transparent;
  color: var(--text-muted, #a78bfa);
  cursor: pointer;
  transition: all 0.18s;
}
.tab-btn.active,
.tab-btn:hover {
  background: rgba(109,40,217,0.25);
  color: #e2d9f3;
  border-color: rgba(124,58,237,0.6);
}

/* Barre d'outils */
.editor-toolbar {
  display: flex;
  align-items: center;
  gap: 0.2rem;
  padding: 0.4rem 0.6rem;
  background: rgba(109,40,217,0.08);
  border: 1px solid rgba(124,58,237,0.2);
  border-radius: 7px 7px 0 0;
  flex-wrap: wrap;
}
.tool-btn {
  min-width: 2rem;
  height: 2rem;
  padding: 0 0.5rem;
  border-radius: 5px;
  border: 1px solid transparent;
  background: transparent;
  color: #c4b5d4;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.15s;
  display: flex;
  align-items: center;
  justify-content: center;
}
.tool-btn:hover,
.tool-btn.active {
  background: rgba(124,58,237,0.25);
  border-color: rgba(124,58,237,0.4);
  color: #e2d9f3;
}
.emoji-toggle { gap: 0.3rem; font-size: 0.78rem; padding: 0 0.6rem; }
.image-tool { font-size: 0.76rem; white-space: nowrap; }
.color-tool { display: inline-flex; align-items: center; gap: 0.4rem; padding: 0 0.45rem; color: #c4b5d4; font-size: 0.78rem; }
.color-tool input { width: 1.75rem; height: 1.75rem; padding: 0; border: 0; background: transparent; cursor: pointer; }
.image-url-bar { display: flex; flex-wrap: wrap; gap: 0.5rem; padding: 0.5rem; border: 1px solid rgba(124,58,237,0.2); border-top: 0; }
.image-url-bar input { min-width: 0; flex: 1; }
.image-error { margin: 0.4rem 0; color: #fca5a5; font-size: 0.8rem; }
.image-hint { margin: .4rem .5rem; color: #f5d76e; font-size: .78rem; }
.source-tool { margin-left: auto; }
.source-textarea { min-height: 300px; resize: vertical; font: .82rem/1.5 monospace; background: #100c1b; color: #e2d9f3; }
.tool-sep {
  width: 1px;
  height: 1.4rem;
  background: rgba(124,58,237,0.25);
  margin: 0 0.2rem;
}

/* Panneau émojis */
.emoji-panel {
  border: 1px solid rgba(124,58,237,0.2);
  border-top: none;
  background: rgba(13,10,26,0.95);
  padding: 0.7rem 0.9rem;
  max-height: 220px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}
.emoji-cat-label {
  font-size: 0.62rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: #6d28d9;
  display: block;
  margin-bottom: 0.25rem;
}
.emoji-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 0.15rem;
}
.emoji-btn {
  width: 2rem;
  height: 2rem;
  font-size: 1.15rem;
  background: transparent;
  border: 1px solid transparent;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.12s;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
}
.emoji-btn:hover {
  background: rgba(124,58,237,0.2);
  border-color: rgba(124,58,237,0.35);
  transform: scale(1.15);
}

/* Textarea */
.editor-textarea {
  border-radius: 0 0 7px 7px;
  border-top: none;
  resize: vertical;
  min-height: 120px;
  font-family: inherit;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
  line-height: 1.7;
}
.editor-textarea:empty::before { content: attr(data-placeholder); color: var(--text-muted, #8b7ca9); pointer-events: none; }
.editor-textarea :deep(img), .preview-content :deep(img) { max-width: 100%; height: auto; border-radius: 6px; }
.editor-textarea :deep(a), .preview-content :deep(a) { color: #f5d76e; text-decoration: underline; }

/* Aperçu */
.preview-panel {
  min-height: 120px;
  border: 1px solid rgba(124,58,237,0.2);
  border-radius: 7px;
  padding: 0.85rem 1rem;
  margin-bottom: 0.75rem;
  background: rgba(109,40,217,0.05);
}
.preview-content {
  font-size: 0.92rem;
  line-height: 1.75;
  color: #e2d9f3;
  word-break: break-word;
}
.preview-content :deep(blockquote) {
  border-left: 3px solid #6d28d9;
  margin: 0.5rem 0;
  padding: 0.4rem 0.9rem;
  color: #a78bfa;
  font-style: italic;
  background: rgba(109,40,217,0.08);
  border-radius: 0 5px 5px 0;
}
.preview-empty {
  color: #4a3a6a;
  font-style: italic;
  font-size: 0.85rem;
  margin: 0;
}

/* Actions */
.editor-actions {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.75rem;
}
.char-count {
  font-size: 0.72rem;
  color: #4a3a6a;
  margin-right: auto;
}
</style>
