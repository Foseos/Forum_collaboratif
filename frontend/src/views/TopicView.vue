<template>
  <div class="page">
    <div v-if="forum.currentTopic">
      <router-link
        v-if="forum.currentTopic.category"
        :to="`/categories/${forum.currentTopic.category_name ? forum.currentTopic.slug : ''}`"
        class="text-sm text-secondary"
      >
        &larr; Retour
      </router-link>

      <div class="topic-header">
        <h1 class="page-title" style="margin-bottom: 0.25rem">{{ forum.currentTopic.title }}</h1>
        <div class="flex gap-1 items-center">
          <span v-if="forum.currentTopic.is_pinned" class="badge badge-warning">📌 Epinglé</span>
          <span v-if="forum.currentTopic.is_locked" class="badge badge-danger">🔒 Verrouillé</span>
          <span class="text-sm text-secondary">
            par <strong>{{ forum.currentTopic.author?.username }}</strong>
            &middot; {{ formatDate(forum.currentTopic.created_at) }}
          </span>
        </div>
      </div>
    </div>

    <LoadingSpinner v-if="forum.loading && forum.posts.length === 0" />

    <div v-else>
      <TransitionGroup name="slide" tag="div">
        <PostCard
          v-for="post in forum.posts"
          :key="post.id"
          :post="post"
          @edit="startEdit"
          @delete="handleDelete"
          @react="handleReaction"
        />
      </TransitionGroup>

      <PaginationBar
        :page="forum.pagination.page"
        :count="forum.pagination.count"
        @change="loadPage"
      />

      <!-- Post Editor -->
      <div v-if="editingPost" class="mt-2">
        <PostEditor
          :edit-post="editingPost"
          :loading="posting"
          @submit="handleEditSubmit"
          @cancel="editingPost = null"
        />
      </div>

      <div v-else-if="canReply" class="mt-2">
        <PostEditor :loading="posting" @submit="handleNewPost" />
      </div>

      <div
        v-else-if="forum.currentTopic?.is_locked"
        class="card text-center text-secondary mt-2"
        style="padding: 1.5rem"
      >
        🔒 Ce sujet est verrouillé. Vous ne pouvez plus y répondre.
      </div>

      <div
        v-else-if="!auth.isAuthenticated"
        class="card text-center text-secondary mt-2"
        style="padding: 1.5rem"
      >
        <router-link to="/login">Connectez-vous</router-link> pour répondre.
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useForumStore } from '../stores/forum'
import { useAuthStore } from '../stores/auth'
import PostCard from '../components/PostCard.vue'
import PostEditor from '../components/PostEditor.vue'
import PaginationBar from '../components/PaginationBar.vue'
import LoadingSpinner from '../components/LoadingSpinner.vue'

const props = defineProps({
  slug: { type: String, required: true },
})

const forum = useForumStore()
const auth = useAuthStore()
const editingPost = ref(null)
const posting = ref(false)

const canReply = computed(() => {
  return auth.isAuthenticated && !forum.currentTopic?.is_locked
})

async function load() {
  await forum.fetchTopic(props.slug)
  await forum.fetchPosts(props.slug)
}

onMounted(load)
watch(() => props.slug, load)

function loadPage(page) {
  forum.fetchPosts(props.slug, page)
}

async function handleNewPost(content) {
  posting.value = true
  try {
    await forum.createPost(props.slug, content)
    // Go to last page to see the new post
    const lastPage = Math.ceil((forum.pagination.count + 1) / 20)
    await forum.fetchPosts(props.slug, lastPage)
  } finally {
    posting.value = false
  }
}

function startEdit(post) {
  editingPost.value = post
}

async function handleEditSubmit(content) {
  posting.value = true
  try {
    await forum.updatePost(editingPost.value.id, content)
    editingPost.value = null
  } finally {
    posting.value = false
  }
}

async function handleDelete(postId) {
  if (!confirm('Supprimer ce message ?')) return
  await forum.deletePost(postId)
}

async function handleReaction(postId, reactionType) {
  if (!auth.isAuthenticated) return
  await forum.toggleReaction(postId, reactionType)
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  })
}
</script>

<style scoped>
.topic-header {
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border);
}
</style>
