import { defineStore } from 'pinia'
import api from '../composables/useApi'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    accessToken: localStorage.getItem('accessToken') || null,
    refreshToken: localStorage.getItem('refreshToken') || null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken,
    isModerator: (state) =>
      state.user?.role === 'admin' || state.user?.role === 'moderator' || state.user?.role === 'fondatrice',
  },

  actions: {
    async login(credentials) {
      const { data } = await api.post('/auth/login/', credentials)
      this.accessToken = data.access
      this.refreshToken = data.refresh
      localStorage.setItem('accessToken', data.access)
      localStorage.setItem('refreshToken', data.refresh)
      await this.fetchProfile()
    },

    async register(userData) {
      await api.post('/auth/register/', userData)
    },

    async fetchProfile() {
      try {
        const { data } = await api.get('/users/me/')
        this.user = data
      } catch {
        this.logout()
      }
    },

    async updateProfile(profileData) {
      const { data } = await api.patch('/users/me/', profileData)
      this.user = data
    },

    logout() {
      this.user = null
      this.accessToken = null
      this.refreshToken = null
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
    },

    async init() {
      if (this.accessToken) {
        await this.fetchProfile()
      }
    },
  },
})
