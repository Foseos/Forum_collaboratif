import { defineStore } from 'pinia'
import api from '../composables/useApi'
import { useAuthStore } from './auth'

export const useNotificationStore = defineStore('notifications', {
  state: () => ({
    notifications: [],
    unreadCount: 0,
    unreadMsgCount: 0,
    pendingReports: 0,
    pendingQuestions: 0,
    pagination: { count: 0, next: null, previous: null },
    _intervalId: null,
  }),

  actions: {
    async fetchNotifications(page = 1) {
      const { data } = await api.get(`/notifications/?page=${page}`)
      this.notifications = data.results
      this.pagination = {
        count: data.count,
        next: data.next,
        previous: data.previous,
      }
    },

    async fetchUnreadCount() {
      try {
        const { data } = await api.get('/notifications/unread-count/')
        this.unreadCount = data.unread_count
      } catch {
        // Silently fail if not authenticated
      }
    },

    async fetchUnreadMessages() {
      try {
        const { data } = await api.get('/messages/unread/')
        this.unreadMsgCount = data.unread ?? 0
      } catch {
        // Silently fail if not authenticated
      }
    },

    async fetchAdminContactCounts() {
      const auth = useAuthStore()
      if (!['admin', 'fondatrice'].includes(auth.user?.role)) {
        this.pendingReports = 0
        this.pendingQuestions = 0
        return
      }
      try {
        const { data } = await api.get('/administration/contact/', { params: { counts: 1 } })
        this.pendingReports = data.reports ?? 0
        this.pendingQuestions = data.questions ?? 0
      } catch {
        // Conserver le dernier compteur si l'actualisation échoue.
      }
    },

    async markRead(id) {
      if (!useAuthStore().isAuthenticated) return
      await api.post(`/notifications/${id}/read/`)
      const notif = this.notifications.find((n) => n.id === id)
      if (notif) notif.is_read = true
      this.unreadCount = Math.max(0, this.unreadCount - 1)
    },

    async markAllRead() {
      if (!useAuthStore().isAuthenticated) return
      await api.post('/notifications/read-all/')
      this.notifications.forEach((n) => (n.is_read = true))
      this.unreadCount = 0
    },

    startPolling() {
      this.fetchUnreadCount()
      this.fetchUnreadMessages()
      this.fetchAdminContactCounts()
      this._intervalId = setInterval(() => {
        this.fetchUnreadCount()
        this.fetchUnreadMessages()
        this.fetchAdminContactCounts()
      }, 30000)
    },

    stopPolling() {
      if (this._intervalId) {
        clearInterval(this._intervalId)
        this._intervalId = null
      }
      this.pendingReports = 0
      this.pendingQuestions = 0
    },
  },
})
