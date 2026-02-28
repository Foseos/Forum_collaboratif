<template>
  <div class="reaction-bar">
    <button
      v-for="r in reactions"
      :key="r.type"
      class="reaction-btn"
      :class="{ active: userReactions.includes(r.type) }"
      :title="r.label"
      @click="$emit('react', r.type)"
    >
      {{ r.emoji }}
      <span v-if="counts[r.type]" class="reaction-count">{{ counts[r.type] }}</span>
    </button>
  </div>
</template>

<script setup>
defineProps({
  counts: { type: Object, default: () => ({}) },
  userReactions: { type: Array, default: () => [] },
})

defineEmits(['react'])

const reactions = [
  { type: 'like', emoji: '👍', label: "J'aime" },
  { type: 'dislike', emoji: '👎', label: "Je n'aime pas" },
  { type: 'love', emoji: '❤️', label: "J'adore" },
  { type: 'laugh', emoji: '😂', label: 'Haha' },
  { type: 'think', emoji: '🤔', label: 'Intéressant' },
]
</script>

<style scoped>
.reaction-bar {
  display: flex;
  gap: 0.375rem;
  flex-wrap: wrap;
}

.reaction-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.5rem;
  border: 1px solid var(--border);
  border-radius: 999px;
  background: transparent;
  cursor: pointer;
  font-size: 0.8rem;
  transition: all var(--transition);
  color: var(--text);
}

.reaction-btn:hover {
  background: var(--bg);
  border-color: var(--primary);
}

.reaction-btn.active {
  background: var(--primary-light);
  border-color: var(--primary);
}

.reaction-count {
  font-size: 0.75rem;
  font-weight: 600;
}
</style>
