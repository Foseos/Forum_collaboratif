<template>
  <div class="card post-card">
    <div class="post-header">
      <div class="post-author">
        <div class="author-avatar">
          {{ post.author?.username?.[0]?.toUpperCase() || '?' }}
        </div>
        <div>
          <div class="author-name">{{ post.author?.username }}</div>
          <div class="post-date">
            {{ formatDate(post.created_at) }}
            <span v-if="post.is_edited" class="edited-badge">(modifié)</span>
          </div>
        </div>
      </div>

      <div v-if="canEdit" class="post-actions">
        <button class="btn-icon btn-sm" title="Modifier" @click="$emit('edit', post)">✏️</button>
        <button class="btn-icon btn-sm" title="Supprimer" @click="$emit('delete', post.id)">🗑️</button>
      </div>
    </div>

    <div class="post-content">{{ post.content }}</div>

    <ReactionBar
      :counts="post.reactions_count || {}"
      :user-reactions="post.user_reactions || []"
      @react="(type) => $emit('react', post.id, type)"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '../stores/auth'
import ReactionBar from './ReactionBar.vue'

const props = defineProps({
  post: { type: Object, required: true },
})

defineEmits(['edit', 'delete', 'react'])

const auth = useAuthStore()

const canEdit = computed(() => {
  if (!auth.isAuthenticated) return false
  return auth.user?.id === props.post.author?.id || auth.isModerator
})

function formatDate(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}
</script>

<style scoped>
.post-card {
  margin-bottom: 0.75rem;
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.75rem;
}

.post-author {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.author-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--primary);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 1rem;
  flex-shrink: 0;
}

.author-name {
  font-weight: 600;
  font-size: 0.9375rem;
}

.post-date {
  font-size: 0.75rem;
  color: var(--text-secondary);
}

.edited-badge {
  font-style: italic;
}

.post-actions {
  display: flex;
  gap: 0.25rem;
}

.post-content {
  margin-bottom: 0.75rem;
  white-space: pre-wrap;
  word-break: break-word;
  line-height: 1.7;
}
</style>
