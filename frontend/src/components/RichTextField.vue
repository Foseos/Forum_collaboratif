<template>
  <div class="rich-field">
    <div class="rich-toolbar" role="toolbar" aria-label="Mise en forme du message">
      <template v-if="!sourceMode">
      <button type="button" title="Gras" @mousedown.prevent="format('bold')"><strong>G</strong></button>
      <button type="button" title="Italique" @mousedown.prevent="format('italic')"><em>I</em></button>
      <button type="button" title="Souligné" @mousedown.prevent="format('underline')"><u>S</u></button>
      <button type="button" title="Barré" @mousedown.prevent="format('strikeThrough')"><s>B</s></button>
      <span class="separator"></span>
      <button type="button" title="Aligner à gauche" aria-label="Aligner à gauche" @mousedown.prevent="align('justifyLeft')">☰</button>
      <button type="button" title="Centrer" aria-label="Centrer" @mousedown.prevent="align('justifyCenter')">≡</button>
      <button type="button" title="Aligner à droite" aria-label="Aligner à droite" @mousedown.prevent="align('justifyRight')">☷</button>
      <span class="separator"></span>
      <label class="color-label">Couleur <input type="color" value="#a78bfa" aria-label="Couleur du texte" @pointerdown="rememberSelection" @input="applyColor($event.target.value)" /></label>
      <span class="separator"></span>
      <button type="button" :disabled="uploading" @mousedown.prevent="fileInput?.click()">{{ uploading ? 'Envoi…' : '🖼 Image / GIF' }}</button>
      <button type="button" @mousedown.prevent="showUrl = !showUrl">🔗 Adresse d’image</button>
      <button type="button" @mousedown.prevent="openLinkInput">🔗 Lien</button>
      <input ref="fileInput" type="file" accept="image/png,image/jpeg,image/gif,image/webp" hidden @change="uploadImage" />
      </template>
      <button type="button" class="source-toggle" :class="{ active: sourceMode }" @click="toggleSource">{{ sourceMode ? '✏️ Éditeur visuel' : '〈/〉 Code HTML' }}</button>
    </div>
    <div v-if="showUrl && !sourceMode" class="url-row">
      <input v-model="urlInput" type="url" class="form-input" placeholder="https://exemple.fr/image.gif" aria-label="Adresse de l’image" @keydown.enter.prevent="insertImageUrl" />
      <button type="button" class="btn btn-secondary btn-sm" @click="insertImageUrl">Insérer</button>
    </div>
    <div v-if="showLink && !sourceMode" class="url-row">
      <input v-model="linkLabel" type="text" class="form-input" placeholder="Texte du lien" aria-label="Texte du lien" />
      <input v-model="linkUrl" type="text" class="form-input" placeholder="/topics/mon-sujet ou https://…" aria-label="Adresse du lien" @keydown.enter.prevent="insertLink" />
      <button type="button" class="btn btn-secondary btn-sm" @click="insertLink">Insérer</button>
    </div>
    <div v-show="!sourceMode" ref="editor" class="rich-content" contenteditable="true" role="textbox" aria-multiline="true" :aria-label="label" :data-placeholder="placeholder" @input="emitContent" @paste="pastePlainText" @keyup="rememberSelection" @mouseup="rememberSelection"></div>
    <textarea v-if="sourceMode" class="source-content" :value="modelValue" aria-label="Code HTML du message" placeholder="Collez le code du modèle ici…" @input="emit('update:modelValue', $event.target.value)"></textarea>
    <p v-if="error" class="rich-error" role="alert">{{ error }}</p>
  </div>
</template>

<script setup>
import { nextTick, onMounted, ref, watch } from 'vue'
import api from '../composables/useApi'

const props = defineProps({
  modelValue: { type: String, default: '' },
  label: { type: String, default: 'Contenu du message' },
  placeholder: { type: String, default: 'Écrivez votre message…' },
})
const emit = defineEmits(['update:modelValue'])
const editor = ref(null)
const fileInput = ref(null)
const uploading = ref(false)
const showUrl = ref(false)
const showLink = ref(false)
const sourceMode = ref(false)
const urlInput = ref('')
const linkUrl = ref('')
const linkLabel = ref('')
const error = ref('')
let savedRange = null

onMounted(() => { if (editor.value) editor.value.innerHTML = props.modelValue })
watch(() => props.modelValue, value => {
  if (editor.value && editor.value.innerHTML !== value) editor.value.innerHTML = value || ''
})

function emitContent() { emit('update:modelValue', editor.value?.innerHTML || '') }
async function toggleSource() {
  sourceMode.value = !sourceMode.value
  if (!sourceMode.value) {
    await nextTick()
    if (editor.value) editor.value.innerHTML = props.modelValue
  }
}
function rememberSelection() {
  const selection = window.getSelection()
  if (selection?.rangeCount && editor.value?.contains(selection.anchorNode)) savedRange = selection.getRangeAt(0).cloneRange()
}
function restoreSelection() {
  editor.value?.focus()
  if (savedRange && editor.value?.contains(savedRange.commonAncestorContainer)) {
    const selection = window.getSelection()
    selection.removeAllRanges()
    selection.addRange(savedRange)
  }
}
function format(command, value = null) {
  restoreSelection()
  document.execCommand(command, false, value)
  emitContent()
  rememberSelection()
}
function applyColor(color) {
  restoreSelection()
  document.execCommand('styleWithCSS', false, true)
  document.execCommand('foreColor', false, color)
  emitContent()
  rememberSelection()
}
function align(command) {
  restoreSelection()
  document.execCommand('styleWithCSS', false, true)
  document.execCommand(command, false, null)
  emitContent()
  rememberSelection()
}
function pastePlainText(event) {
  event.preventDefault()
  format('insertText', event.clipboardData?.getData('text/plain') || '')
}
function insertImage(src) {
  restoreSelection()
  const image = document.createElement('img')
  image.src = src
  image.alt = 'Image du message'
  image.style.cssText = 'display:block;max-width:100%;max-height:500px;object-fit:contain;margin:0.7rem 0;border-radius:6px;'
  document.execCommand('insertHTML', false, image.outerHTML)
  emitContent()
  rememberSelection()
}
function insertImageUrl() {
  error.value = ''
  let url
  try { url = new URL(urlInput.value.trim()) } catch { error.value = 'Indiquez une adresse d’image valide.'; return }
  if (!['http:', 'https:'].includes(url.protocol)) { error.value = 'Utilisez une adresse commençant par https:// ou http://.'; return }
  insertImage(url.href)
  urlInput.value = ''
  showUrl.value = false
}
function openLinkInput() {
  rememberSelection()
  linkLabel.value = window.getSelection()?.toString() || ''
  showLink.value = !showLink.value
}
function insertLink() {
  error.value = ''
  const raw = linkUrl.value.trim()
  let href = raw
  if (!/^\/(?!\/)/.test(raw)) {
    try {
      const parsed = new URL(raw)
      if (!['http:', 'https:'].includes(parsed.protocol)) throw new Error('protocol')
      href = parsed.href
    } catch { error.value = 'Indiquez une adresse de page valide.'; return }
  }
  restoreSelection()
  const anchor = document.createElement('a')
  anchor.href = href
  anchor.textContent = linkLabel.value.trim() || href
  document.execCommand('insertHTML', false, anchor.outerHTML)
  emitContent()
  rememberSelection()
  linkUrl.value = ''
  linkLabel.value = ''
  showLink.value = false
}
async function uploadImage(event) {
  const file = event.target.files?.[0]
  if (!file) return
  error.value = ''
  if (file.size > 5 * 1024 * 1024) { error.value = 'L’image doit peser moins de 5 Mo.'; event.target.value = ''; return }
  uploading.value = true
  try {
    const body = new FormData()
    body.append('image', file)
    const response = await api.post('/posts/images/', body)
    insertImage(response.data.url)
  } catch (failure) {
    error.value = failure.response?.data?.detail || 'Impossible d’ajouter cette image.'
  } finally {
    uploading.value = false
    event.target.value = ''
  }
}
</script>

<style scoped>
.rich-field { border: 1px solid rgba(124,58,237,.28); border-radius: 7px; overflow: hidden; }
.rich-toolbar { display: flex; align-items: center; gap: .25rem; flex-wrap: wrap; padding: .45rem .55rem; background: rgba(109,40,217,.08); border-bottom: 1px solid rgba(124,58,237,.2); }
.rich-toolbar button { min-height: 2rem; padding: 0 .55rem; border: 1px solid transparent; border-radius: 5px; background: transparent; color: #c4b5d4; cursor: pointer; }
.rich-toolbar button:hover { background: rgba(124,58,237,.25); color: #e2d9f3; }
.rich-toolbar .source-toggle { margin-left: auto; }
.rich-toolbar .source-toggle.active { background: rgba(124,58,237,.25); color: #e2d9f3; }
.rich-toolbar button:disabled { opacity: .6; cursor: wait; }
.separator { width: 1px; height: 1.4rem; background: rgba(124,58,237,.3); margin: 0 .25rem; }
.color-label { display: inline-flex; align-items: center; gap: .3rem; color: #c4b5d4; font-size: .78rem; }
.color-label input { width: 1.75rem; height: 1.75rem; padding: 0; border: 0; background: transparent; cursor: pointer; }
.url-row { display: flex; flex-wrap: wrap; gap: .5rem; padding: .5rem; border-bottom: 1px solid rgba(124,58,237,.2); }
.url-row input { flex: 1; min-width: 0; }
.rich-content { min-height: 175px; padding: .85rem 1rem; color: #e2d9f3; line-height: 1.7; white-space: pre-wrap; overflow-wrap: anywhere; outline: none; }
.rich-content:empty::before { content: attr(data-placeholder); color: #8b7ca9; pointer-events: none; }
.rich-content :deep(img) { max-width: 100%; height: auto; border-radius: 6px; }
.rich-content :deep(a) { color: #f5d76e; text-decoration: underline; }
.source-content { display: block; width: 100%; min-height: 220px; padding: .85rem 1rem; resize: vertical; border: 0; outline: none; background: #100c1b; color: #e2d9f3; font: .83rem/1.5 monospace; }
.rich-error { margin: .4rem .7rem; color: #fca5a5; font-size: .8rem; }
</style>
