<template>
  <router-link :to="`/topics/${topic.slug}`" class="card topic-card">
    <div class="topic-author-avatar">
      <img
        v-if="topic.author?.avatar"
        :src="topic.author.avatar"
        :alt="topic.author?.username"
        class="author-avatar"
      />
      <div v-else class="author-avatar author-avatar-placeholder">
        {{ (topic.author?.username || '?')[0].toUpperCase() }}
      </div>
    </div>

    <div class="topic-main">
      <div class="topic-title-row">
        <span v-if="topic.is_pinned" class="badge badge-warning" title="Épinglé">📌</span>
        <span v-if="topic.is_locked" class="badge badge-danger" title="Verrouillé">🔒</span>
        <h3 class="topic-title">{{ topic.title }}</h3>
      </div>
      <div class="topic-meta">
        <span class="topic-author-name">{{ topic.author?.username }}</span>
        <span class="topic-date">{{ formatDate(topic.created_at) }}</span>
      </div>
    </div>

    <div class="topic-stats">
      <div class="stat">
        <span class="stat-value">{{ topic.post_count || 0 }}</span>
        <span class="stat-label">messages</span>
      </div>
    </div>
  </router-link>
</template>

<script setup>
defineProps({
  topic: { type: Object, required: true },
})

function formatDate(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  })
}
</script>

<style scoped>
.topic-card {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  text-decoration: none;
  color: var(--text);
  cursor: pointer;
}

.topic-author-avatar {
  flex-shrink: 0;
}

.author-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid var(--border);
}

.author-avatar-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--surface-2, #1e1e3a);
  color: var(--primary);
  font-weight: 700;
  font-size: 0.9rem;
}

.topic-main {
  flex: 1;
  min-width: 0;
}

.topic-title-row {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  flex-wrap: wrap;
}

.topic-title {
  font-size: 1rem;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.topic-meta {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.2rem;
  font-size: 0.78rem;
  color: var(--text-secondary);
  align-items: center;
}

.topic-author-name {
  font-weight: 500;
  color: var(--primary);
}

.topic-date::before {
  content: '·';
  margin-right: 0.4rem;
}

.topic-stats {
  text-align: center;
  flex-shrink: 0;
}

.stat-value {
  display: block;
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--primary);
}

.stat-label {
  font-size: 0.7rem;
  color: var(--text-secondary);
  text-transform: uppercase;
}
</style>
