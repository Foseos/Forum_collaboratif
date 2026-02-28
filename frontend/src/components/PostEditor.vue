<template>
  <div class="post-editor card">
    <h4 v-if="editPost">Modifier le message</h4>
    <h4 v-else>Répondre</h4>
    <div class="form-group">
      <textarea
        v-model="content"
        class="form-input"
        :placeholder="editPost ? '' : 'Écrivez votre message...'"
        rows="4"
      ></textarea>
    </div>
    <div class="editor-actions">
      <button v-if="editPost" class="btn btn-secondary btn-sm" @click="$emit('cancel')">
        Annuler
      </button>
      <button class="btn btn-primary btn-sm" :disabled="!content.trim() || loading" @click="submit">
        {{ loading ? 'Envoi...' : editPost ? 'Modifier' : 'Envoyer' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  editPost: { type: Object, default: null },
  loading: { type: Boolean, default: false },
})

const emit = defineEmits(['submit', 'cancel'])

const content = ref(props.editPost?.content || '')

watch(
  () => props.editPost,
  (val) => {
    content.value = val?.content || ''
  }
)

function submit() {
  if (!content.value.trim()) return
  emit('submit', content.value)
  if (!props.editPost) {
    content.value = ''
  }
}
</script>

<style scoped>
.post-editor h4 {
  margin-bottom: 0.75rem;
  font-size: 0.9375rem;
}

.editor-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}
</style>
