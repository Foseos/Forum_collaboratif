<template>
  <div class="app">
    <AppHeader />
    <main class="container">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import AppHeader from './components/AppHeader.vue'
import { useAuthStore } from './stores/auth'
import { useNotificationStore } from './stores/notifications'

const auth = useAuthStore()
const notifications = useNotificationStore()

onMounted(async () => {
  await auth.init()
  if (auth.isAuthenticated) {
    notifications.startPolling()
  }
})
</script>

<style scoped>
.app {
  min-height: 100vh;
}
</style>
