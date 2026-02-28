<template>
  <div class="page">
    <h1 class="page-title">Catégories</h1>

    <LoadingSpinner v-if="forum.loading" />

    <div v-else class="grid-categories">
      <router-link
        v-for="cat in forum.categories"
        :key="cat.id"
        :to="`/categories/${cat.slug}`"
        class="card category-card"
      >
        <h2 class="category-name">{{ cat.name }}</h2>
        <p v-if="cat.description" class="category-desc">{{ cat.description }}</p>
        <div class="category-stats">
          <span class="badge badge-primary">{{ cat.topic_count }} sujets</span>
          <span class="badge badge-primary">{{ cat.post_count }} messages</span>
        </div>
      </router-link>

      <div v-if="forum.categories.length === 0" class="text-center text-secondary" style="grid-column: 1 / -1; padding: 3rem">
        Aucune catégorie pour le moment.
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useForumStore } from '../stores/forum'
import LoadingSpinner from '../components/LoadingSpinner.vue'

const forum = useForumStore()

onMounted(() => {
  forum.fetchCategories()
})
</script>

<style scoped>
.category-card {
  text-decoration: none;
  color: var(--text);
  cursor: pointer;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.category-name {
  font-size: 1.125rem;
  font-weight: 600;
}

.category-desc {
  font-size: 0.875rem;
  color: var(--text-secondary);
  flex: 1;
}

.category-stats {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.25rem;
}
</style>
