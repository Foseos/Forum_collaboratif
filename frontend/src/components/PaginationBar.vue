<template>
  <div v-if="totalPages > 1" class="pagination">
    <button
      class="btn btn-secondary btn-sm"
      :disabled="page <= 1"
      @click="$emit('change', page - 1)"
    >
      &larr; Précédent
    </button>

    <span class="pagination-info">
      Page {{ page }} / {{ totalPages }}
    </span>

    <button
      class="btn btn-secondary btn-sm"
      :disabled="page >= totalPages"
      @click="$emit('change', page + 1)"
    >
      Suivant &rarr;
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  page: { type: Number, required: true },
  count: { type: Number, required: true },
  pageSize: { type: Number, default: 20 },
})

defineEmits(['change'])

const totalPages = computed(() => Math.ceil(props.count / props.pageSize))
</script>

<style scoped>
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-top: 1.5rem;
}

.pagination-info {
  font-size: 0.875rem;
  color: var(--text-secondary);
}
</style>
