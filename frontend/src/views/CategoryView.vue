<template>
  <div class="page">
    <div v-if="forum.currentCategory" class="category-header">
      <div>
        <router-link to="/" class="text-sm text-secondary">&larr; Catégories</router-link>
        <h1 class="page-title" style="margin-bottom: 0.25rem">{{ forum.currentCategory.name }}</h1>
        <p v-if="forum.currentCategory.description" class="text-secondary">
          {{ forum.currentCategory.description }}
        </p>
      </div>
      <button
        v-if="auth.isAuthenticated"
        class="btn btn-primary"
        @click="showNewTopic = true"
      >
        + Nouveau sujet
      </button>
    </div>

    <!-- New Topic Form -->
    <div v-if="showNewTopic" class="card mb-2">
      <h3 style="margin-bottom: 0.75rem">Créer un sujet</h3>
      <div class="form-group">
        <label>Titre</label>
        <input v-model="newTopic.title" class="form-input" placeholder="Titre du sujet" />
      </div>
      <div class="form-group">
        <label>Premier message</label>
        <textarea v-model="newTopic.content" class="form-input" rows="4" placeholder="Contenu..."></textarea>
      </div>
      <div class="flex gap-1" style="justify-content: flex-end">
        <button class="btn btn-secondary btn-sm" @click="showNewTopic = false">Annuler</button>
        <button class="btn btn-primary btn-sm" :disabled="!newTopic.title.trim() || !newTopic.content.trim()" @click="handleCreateTopic">
          Créer
        </button>
      </div>
    </div>

    <LoadingSpinner v-if="forum.loading" />

    <div v-else class="topics-list">
      <TopicCard
        v-for="topic in forum.topics"
        :key="topic.id"
        :topic="topic"
      />

      <div v-if="forum.topics.length === 0" class="text-center text-secondary" style="padding: 3rem">
        Aucun sujet dans cette catégorie.
      </div>

      <PaginationBar
        :page="forum.pagination.page"
        :count="forum.pagination.count"
        @change="loadPage"
      />
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, reactive, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useForumStore } from '../stores/forum'
import { useAuthStore } from '../stores/auth'
import TopicCard from '../components/TopicCard.vue'
import PaginationBar from '../components/PaginationBar.vue'
import LoadingSpinner from '../components/LoadingSpinner.vue'

const props = defineProps({
  slug: { type: String, required: true },
})

const forum = useForumStore()
const auth = useAuthStore()
const router = useRouter()

const showNewTopic = ref(false)
const newTopic = reactive({ title: '', content: '' })

async function load() {
  await forum.fetchCategory(props.slug)
  await forum.fetchTopics(props.slug)
}

onMounted(load)
watch(() => props.slug, load)

function loadPage(page) {
  forum.fetchTopics(props.slug, page)
}

async function handleCreateTopic() {
  const data = await forum.createTopic(props.slug, {
    title: newTopic.title,
    first_post_content: newTopic.content,
  })
  showNewTopic.value = false
  newTopic.title = ''
  newTopic.content = ''
  router.push(`/topics/${data.slug}`)
}
</script>

<style scoped>
.category-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
  gap: 1rem;
}

.topics-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

@media (max-width: 768px) {
  .category-header {
    flex-direction: column;
  }
}
</style>
