<template>
  <div class="page">
    <div class="flex justify-between items-center mb-2">
      <h1 class="page-title" style="margin-bottom: 0">Notifications</h1>
      <button
        v-if="notifications.notifications.length > 0"
        class="btn btn-secondary btn-sm"
        @click="notifications.markAllRead()"
      >
        Tout marquer comme lu
      </button>
    </div>

    <LoadingSpinner v-if="loading" />

    <div v-else>
      <TransitionGroup name="slide" tag="div" class="notification-list">
        <div
          v-for="notif in notifications.notifications"
          :key="notif.id"
          class="card notification-card"
          :class="{ unread: !notif.is_read }"
          @click="handleClick(notif)"
        >
          <div class="notification-icon">
            {{ typeIcon(notif.notification_type) }}
          </div>
          <div class="notification-body">
            <div class="notification-message">{{ notif.message }}</div>
            <div class="notification-time text-sm text-secondary">
              {{ formatDate(notif.created_at) }}
            </div>
          </div>
          <div v-if="!notif.is_read" class="unread-dot"></div>
        </div>
      </TransitionGroup>

      <div v-if="notifications.notifications.length === 0" class="text-center text-secondary" style="padding: 3rem">
        Aucune notification.
      </div>

      <PaginationBar
        :page="page"
        :count="notifications.pagination.count"
        @change="loadPage"
      />
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useNotificationStore } from '../stores/notifications'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import PaginationBar from '../components/PaginationBar.vue'

const notifications = useNotificationStore()
const loading = ref(true)
const page = ref(1)

onMounted(async () => {
  await notifications.fetchNotifications()
  loading.value = false
})

async function loadPage(p) {
  page.value = p
  loading.value = true
  await notifications.fetchNotifications(p)
  loading.value = false
}

async function handleClick(notif) {
  if (!notif.is_read) {
    await notifications.markRead(notif.id)
  }
}

function typeIcon(type) {
  const icons = {
    new_post: '💬',
    mention: '@',
    reaction: '👍',
    topic_reply: '↩️',
  }
  return icons[type] || '🔔'
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now - date
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)

  if (minutes < 1) return "À l'instant"
  if (minutes < 60) return `Il y a ${minutes} min`
  if (hours < 24) return `Il y a ${hours}h`
  if (days < 7) return `Il y a ${days}j`
  return date.toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'short',
  })
}
</script>

<style scoped>
.notification-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.notification-card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  transition: background var(--transition);
}

.notification-card.unread {
  border-left: 3px solid var(--primary);
}

.notification-icon {
  font-size: 1.25rem;
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg);
  border-radius: 50%;
}

.notification-body {
  flex: 1;
  min-width: 0;
}

.notification-message {
  font-size: 0.9375rem;
}

.notification-time {
  margin-top: 0.125rem;
}

.unread-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--primary);
  flex-shrink: 0;
}
</style>
