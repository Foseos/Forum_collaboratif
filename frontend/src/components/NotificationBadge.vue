<template>
  <span v-if="notifications.unreadCount > 0" class="badge-count">
    {{ notifications.unreadCount > 99 ? '99+' : notifications.unreadCount }}
  </span>
</template>

<script setup>
import { useNotificationStore } from '../stores/notifications'

const notifications = useNotificationStore()
</script>

<style scoped>
.badge-count {
  position: absolute;
  top: -4px;
  right: -4px;
  min-width: 18px;
  height: 18px;
  padding: 0 4px;
  border-radius: 999px;
  background: var(--danger);
  color: #fff;
  font-size: 0.65rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
}
</style>
