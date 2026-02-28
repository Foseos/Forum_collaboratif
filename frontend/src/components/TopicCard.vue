<template>
  <router-link :to="`/topics/${topic.slug}`" class="card topic-card">
    <div class="topic-main">
      <div class="topic-title-row">
        <span v-if="topic.is_pinned" class="badge badge-warning" title="Epinglé">📌 Epinglé</span>
        <span v-if="topic.is_locked" class="badge badge-danger" title="Verrouillé">🔒 Verrouillé</span>
        <h3 class="topic-title">{{ topic.title }}</h3>
      </div>
      <div class="topic-meta">
        <span class="topic-author">par <strong>{{ topic.author?.username }}</strong></span>
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
  justify-content: space-between;
  text-decoration: none;
  color: var(--text);
  cursor: pointer;
}

.topic-title-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.topic-title {
  font-size: 1rem;
  font-weight: 600;
}

.topic-meta {
  display: flex;
  gap: 1rem;
  margin-top: 0.25rem;
  font-size: 0.8rem;
  color: var(--text-secondary);
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
