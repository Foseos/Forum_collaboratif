import { defineStore } from 'pinia'
import api from '../composables/useApi'

export const useForumStore = defineStore('forum', {
  state: () => ({
    categories: [],
    currentCategory: null,
    topics: [],
    currentTopic: null,
    posts: [],
    pagination: { count: 0, next: null, previous: null, page: 1 },
    loading: false,
  }),

  actions: {
    async fetchCategories() {
      this.loading = true
      try {
        const { data } = await api.get('/categories/')
        this.categories = data.results
      } finally {
        this.loading = false
      }
    },

    async fetchCategory(slug) {
      this.loading = true
      try {
        const { data } = await api.get(`/categories/${slug}/`)
        this.currentCategory = data
      } finally {
        this.loading = false
      }
    },

    async fetchTopics(categorySlug, page = 1) {
      this.loading = true
      try {
        const { data } = await api.get(
          `/categories/${categorySlug}/topics/?page=${page}`
        )
        this.topics = data.results
        this.pagination = {
          count: data.count,
          next: data.next,
          previous: data.previous,
          page,
        }
      } finally {
        this.loading = false
      }
    },

    async fetchTopic(slug) {
      const { data } = await api.get(`/topics/${slug}/`)
      this.currentTopic = data
    },

    async createTopic(categorySlug, topicData) {
      const { data } = await api.post(
        `/categories/${categorySlug}/topics/`,
        topicData
      )
      return data
    },

    async fetchPosts(topicSlug, page = 1) {
      this.loading = true
      try {
        const { data } = await api.get(
          `/topics/${topicSlug}/posts/?page=${page}`
        )
        this.posts = data.results
        this.pagination = {
          count: data.count,
          next: data.next,
          previous: data.previous,
          page,
        }
      } finally {
        this.loading = false
      }
    },

    async createPost(topicSlug, content) {
      const { data } = await api.post(`/topics/${topicSlug}/posts/`, {
        content,
      })
      this.posts.push(data)
      return data
    },

    async updatePost(id, content) {
      const { data } = await api.patch(`/posts/${id}/`, { content })
      const index = this.posts.findIndex((p) => p.id === id)
      if (index !== -1) this.posts[index] = data
      return data
    },

    async deletePost(id) {
      await api.delete(`/posts/${id}/`)
      this.posts = this.posts.filter((p) => p.id !== id)
    },

    async toggleReaction(postId, reactionType) {
      const { data, status } = await api.post(
        `/posts/${postId}/reactions/`,
        { reaction_type: reactionType }
      )
      // Refresh posts to get updated reaction counts
      if (this.currentTopic) {
        await this.fetchPosts(this.currentTopic.slug, this.pagination.page)
      }
      return { data, status }
    },
  },
})
