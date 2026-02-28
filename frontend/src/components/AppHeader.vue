<template>
  <header class="header">
    <div class="container header-inner">
      <div class="header-left">
        <router-link to="/" class="logo">Forum</router-link>
      </div>

      <nav class="header-right">
        <button class="btn-icon" @click="toggleTheme" :title="theme === 'dark' ? 'Mode clair' : 'Mode sombre'">
          {{ theme === 'dark' ? '☀️' : '🌙' }}
        </button>

        <template v-if="auth.isAuthenticated">
          <router-link to="/notifications" class="btn-icon notification-btn">
            🔔
            <NotificationBadge />
          </router-link>

          <div class="user-menu" @click="menuOpen = !menuOpen" ref="menuRef">
            <div class="user-avatar-small">
              {{ auth.user?.username?.[0]?.toUpperCase() || '?' }}
            </div>
            <span class="hide-mobile">{{ auth.user?.username }}</span>

            <div v-if="menuOpen" class="dropdown">
              <router-link to="/profile" class="dropdown-item" @click="menuOpen = false">
                Profil
              </router-link>
              <button class="dropdown-item" @click="handleLogout">
                Déconnexion
              </button>
            </div>
          </div>
        </template>

        <template v-else>
          <router-link to="/login" class="btn btn-secondary btn-sm">Connexion</router-link>
          <router-link to="/register" class="btn btn-primary btn-sm">Inscription</router-link>
        </template>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useNotificationStore } from '../stores/notifications'
import { useTheme } from '../composables/useTheme'
import NotificationBadge from './NotificationBadge.vue'

const auth = useAuthStore()
const notifications = useNotificationStore()
const router = useRouter()
const { theme, toggleTheme } = useTheme()
const menuOpen = ref(false)

function handleLogout() {
  notifications.stopPolling()
  auth.logout()
  menuOpen.value = false
  router.push('/login')
}
</script>

<style scoped>
.header {
  background: var(--card-bg);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
  transition: background var(--transition), border-color var(--transition);
}

.header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 56px;
}

.logo {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--primary);
  text-decoration: none;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.notification-btn {
  position: relative;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  position: relative;
  padding: 0.25rem 0.5rem;
  border-radius: var(--radius);
  transition: background var(--transition);
}

.user-menu:hover {
  background: var(--bg);
}

.user-avatar-small {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--primary);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
  font-weight: 600;
}

.dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 0.25rem;
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow-lg);
  min-width: 160px;
  overflow: hidden;
  z-index: 200;
}

.dropdown-item {
  display: block;
  width: 100%;
  padding: 0.625rem 1rem;
  text-align: left;
  border: none;
  background: none;
  color: var(--text);
  font-size: 0.875rem;
  cursor: pointer;
  text-decoration: none;
  transition: background var(--transition);
}

.dropdown-item:hover {
  background: var(--bg);
  color: var(--text);
}
</style>
