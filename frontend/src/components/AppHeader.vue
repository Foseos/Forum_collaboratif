<template>
  <header class="header" :class="{ scrolled: isScrolled }">
    <div class="container header-inner">
      <!-- Logo -->
      <router-link to="/" class="logo" @click="closeMobile">
        <svg class="logo-triquetra" viewBox="0 0 40 40" width="32" height="32">
          <path d="M20 2C20 2 8 14 8 22c0 5 3 8 6 9c-2-2-3-5-3-8c0-6 9-16 9-16s9 10 9 16c0 3-1 6-3 8c3-1 6-4 6-9c0-8-12-20-12-20z" fill="url(#triquetra-grad)" opacity="0.9"/>
          <path d="M20 38c-4 0-8-3-9-7c2 2 5 3 9 3s7-1 9-3c-1 4-5 7-9 7z" fill="url(#triquetra-grad)" opacity="0.7"/>
          <circle cx="20" cy="22" r="3" fill="url(#triquetra-grad)" opacity="0.8"/>
          <defs>
            <linearGradient id="triquetra-grad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#c084fc" />
              <stop offset="100%" stop-color="#f0c674" />
            </linearGradient>
          </defs>
        </svg>
        <span class="logo-text">
          <span class="logo-main">Nexus Arcana</span>
        </span>
      </router-link>

      <!-- Desktop Navigation -->
      <nav class="nav-desktop" aria-label="Navigation principale">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="nav-link"
          :class="{ active: isActive(item.path) }"
        >
          <span class="nav-icon" v-html="item.icon"></span>
          <span class="nav-label">{{ item.label }}</span>
          <span v-if="item.path === '/messageries' && notifications.unreadMsgCount > 0" class="nav-msg-badge">{{ notifications.unreadMsgCount }}</span>
        </router-link>
      </nav>

      <!-- Right Actions -->
      <div class="header-actions">
        <template v-if="auth.isAuthenticated">
          <!-- Notifications Bell -->
          <router-link to="/notifications" class="btn-icon notification-btn" title="Notifications">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
              <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
            </svg>
            <!-- Badge part if notification system connects -->
            <span class="notification-badge" v-if="notifications.unreadCount > 0">{{ notifications.unreadCount }}</span>
          </router-link>

          <div class="user-menu" @click="menuOpen = !menuOpen" ref="menuRef">
            <div class="user-avatar-small">
              <img v-if="auth.user?.avatar" :src="auth.user.avatar" :alt="auth.user?.username" class="header-avatar-img" />
              <span v-else>{{ auth.user?.username?.[0]?.toUpperCase() || '?' }}</span>
            </div>
            <span class="hide-mobile user-name">{{ auth.user?.username }}</span>

            <Transition name="dropdown">
              <div v-if="menuOpen" class="dropdown">
                <router-link to="/profile" class="dropdown-item" @click="menuOpen = false">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                  Profil
                </router-link>
                <router-link v-if="['admin', 'fondatrice'].includes(auth.user?.role)" to="/administration/alertes-activite" class="dropdown-item" @click="menuOpen = false">
                  <span aria-hidden="true">⚑</span>
                  Alertes d’activité
                </router-link>
                <router-link v-if="['admin', 'fondatrice'].includes(auth.user?.role)" to="/administration/demandes" class="dropdown-item" @click="menuOpen = false">
                  <span aria-hidden="true">✉</span>
                  Demandes des visiteurs
                </router-link>
                <router-link v-if="['admin', 'fondatrice'].includes(auth.user?.role)" to="/administration/signalements" class="dropdown-item" @click="menuOpen = false">
                  <span aria-hidden="true">⚑</span>
                  Signalements
                </router-link>
                <button class="dropdown-item" @click="handleLogout">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
                  Déconnexion
                </button>
              </div>
            </Transition>
          </div>
        </template>

        <template v-else>
          <router-link to="/login" class="btn btn-ghost btn-sm hide-mobile">Connexion</router-link>
          <router-link to="/register" class="btn btn-primary btn-sm">Inscription</router-link>
        </template>

        <!-- Mobile Menu Toggle -->
        <button class="mobile-toggle" @click="mobileOpen = !mobileOpen" :class="{ active: mobileOpen }">
          <span class="hamburger-line"></span>
          <span class="hamburger-line"></span>
          <span class="hamburger-line"></span>
        </button>
      </div>
    </div>

    <!-- Mobile Navigation -->
    <Transition name="slide-mobile">
      <nav v-if="mobileOpen" class="nav-mobile" @click="closeMobile">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="nav-mobile-link"
          :class="{ active: isActive(item.path) }"
        >
          <span class="nav-icon" v-html="item.icon"></span>
          <span>{{ item.label }}</span>
        </router-link>

        <div class="nav-mobile-divider"></div>

        <router-link v-if="['admin', 'fondatrice'].includes(auth.user?.role)" to="/administration/alertes-activite" class="nav-mobile-link">⚑ Alertes d’activité</router-link>
        <router-link v-if="['admin', 'fondatrice'].includes(auth.user?.role)" to="/administration/demandes" class="nav-mobile-link">✉ Demandes des visiteurs</router-link>
        <router-link v-if="['admin', 'fondatrice'].includes(auth.user?.role)" to="/administration/signalements" class="nav-mobile-link">⚑ Signalements</router-link>

        <template v-if="!auth.isAuthenticated">
          <router-link to="/login" class="nav-mobile-link">Connexion</router-link>
          <router-link to="/register" class="nav-mobile-link highlight">Inscription</router-link>
        </template>
      </nav>
    </Transition>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useNotificationStore } from '../stores/notifications'

const auth = useAuthStore()
const notifications = useNotificationStore()
const router = useRouter()
const route = useRoute()
const menuOpen = ref(false)
const mobileOpen = ref(false)
const isScrolled = ref(false)

const navItems = [
  { path: '/mes-rp', label: 'Mes RP', icon: '📜' },
  {
    path: '/',
    label: 'Accueil',
    icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>'
  },
  {
    path: '/membres',
    label: 'Membres',
    icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>'
  },
  {
    path: '/groupes',
    label: 'Groupes',
    icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg>'
  },
  {
    path: '/profile',
    label: 'Profil',
    icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>'
  },
  {
    path: '/messageries',
    label: 'Messagerie',
    icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>'
  }
]

function isActive(path) {
  if (path === '/') return route.path === '/'
  return route.path.startsWith(path)
}

function closeMobile() {
  mobileOpen.value = false
}

function handleLogout() {
  notifications.stopPolling()
  auth.logout()
  menuOpen.value = false
  router.push('/login')
}

function handleScroll() {
  isScrolled.value = window.scrollY > 20
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--glass-bg);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--glass-border);
  transition: all var(--transition);
}

.header.scrolled {
  background: rgba(10, 10, 20, 0.85);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3), 0 0 40px rgba(139, 92, 246, 0.05);
}

html.light .header.scrolled {
  background: rgba(245, 243, 250, 0.9);
  box-shadow: 0 4px 30px rgba(100, 80, 140, 0.1);
}

.header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: var(--navbar-height);
  gap: 1rem;
}

/* === Logo === */
.logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-decoration: none;
  color: var(--text);
  flex-shrink: 0;
}

.logo:hover {
  color: var(--text);
}

.logo-triquetra {
  filter: drop-shadow(0 0 8px rgba(192, 132, 252, 0.4));
  transition: filter var(--transition);
}

.logo:hover .logo-triquetra {
  filter: drop-shadow(0 0 14px rgba(192, 132, 252, 0.7));
}

.logo-text {
  display: flex;
  flex-direction: column;
  line-height: 1.2;
}

.logo-main {
  font-family: var(--font-display);
  font-size: 1.15rem;
  font-weight: 700;
  background: linear-gradient(135deg, var(--accent), var(--gold));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 0.02em;
}

/* === Desktop Nav === */
.nav-desktop {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.875rem;
  border-radius: var(--radius);
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 0.85rem;
  font-weight: 500;
  transition: all var(--transition);
  position: relative;
  white-space: nowrap;
}

.nav-link:hover {
  color: var(--text);
  background: var(--primary-light);
}

.nav-link.active {
  color: var(--accent);
  background: var(--primary-light);
}

.nav-link.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 50%;
  transform: translateX(-50%);
  width: 60%;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--accent), transparent);
  border-radius: 1px;
}

.nav-icon {
  display: flex;
  align-items: center;
  opacity: 0.8;
}

.nav-link:hover .nav-icon,
.nav-link.active .nav-icon {
  opacity: 1;
}

/* === Actions === */
.header-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-shrink: 0;
}

.notification-btn {
  position: relative;
}

.nav-msg-badge {
  background: var(--accent);
  color: #fff;
  font-size: 0.6rem;
  font-weight: 700;
  min-width: 16px;
  height: 16px;
  border-radius: 8px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0 4px;
  margin-left: 2px;
}

.notification-badge {
  position: absolute;
  top: -2px;
  right: -2px;
  background: var(--accent);
  color: #fff;
  font-size: 0.65rem;
  font-weight: 700;
  min-width: 16px;
  height: 16px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 4px;
}

/* === User Menu === */
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
  background: var(--primary-light);
}

.user-avatar-small {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  font-weight: 700;
  box-shadow: 0 0 12px rgba(139, 92, 246, 0.3);
  overflow: hidden;
}

.header-avatar-img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}

.user-name {
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--text);
}

.dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  background: var(--card-bg-solid);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg), var(--shadow-glow);
  min-width: 180px;
  overflow: hidden;
  z-index: 200;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  width: 100%;
  padding: 0.75rem 1rem;
  text-align: left;
  border: none;
  background: none;
  color: var(--text);
  font-size: 0.875rem;
  font-family: var(--font-body);
  cursor: pointer;
  text-decoration: none;
  transition: all var(--transition);
}

.dropdown-item:hover {
  background: var(--primary-light);
  color: var(--accent);
}

.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-8px) scale(0.95);
}

/* === Mobile Toggle === */
.mobile-toggle {
  display: none;
  flex-direction: column;
  justify-content: center;
  gap: 5px;
  width: 40px;
  height: 40px;
  padding: 8px;
  background: transparent;
  border: 1px solid var(--glass-border);
  border-radius: var(--radius);
  cursor: pointer;
  transition: all var(--transition);
}

.mobile-toggle:hover {
  background: var(--primary-light);
  border-color: var(--border-strong);
}

.hamburger-line {
  display: block;
  width: 100%;
  height: 2px;
  background: var(--text-secondary);
  border-radius: 2px;
  transition: all var(--transition);
}

.mobile-toggle.active .hamburger-line:nth-child(1) {
  transform: translateY(7px) rotate(45deg);
  background: var(--accent);
}

.mobile-toggle.active .hamburger-line:nth-child(2) {
  opacity: 0;
  transform: scaleX(0);
}

.mobile-toggle.active .hamburger-line:nth-child(3) {
  transform: translateY(-7px) rotate(-45deg);
  background: var(--accent);
}

/* === Mobile Nav === */
.nav-mobile {
  display: none;
  flex-direction: column;
  padding: 1rem 1.5rem 1.5rem;
  background: var(--card-bg-solid);
  border-top: 1px solid var(--glass-border);
}

.nav-mobile-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  border-radius: var(--radius);
  transition: all var(--transition);
}

.nav-mobile-link:hover,
.nav-mobile-link.active {
  color: var(--accent);
  background: var(--primary-light);
}

.nav-mobile-link.highlight {
  color: #fff;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  margin-top: 0.5rem;
}

.nav-mobile-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--border-strong), transparent);
  margin: 0.75rem 0;
}

.slide-mobile-enter-active,
.slide-mobile-leave-active {
  transition: all 0.3s ease;
}

.slide-mobile-enter-from,
.slide-mobile-leave-to {
  opacity: 0;
  max-height: 0;
  padding-top: 0;
  padding-bottom: 0;
}

.slide-mobile-enter-to,
.slide-mobile-leave-from {
  max-height: 500px;
}

/* === Responsive === */
@media (max-width: 1024px) {
  .nav-label {
    display: none;
  }
  
  .nav-link {
    padding: 0.5rem;
  }
}

@media (max-width: 768px) {
  .nav-desktop {
    display: none;
  }

  .mobile-toggle {
    display: flex;
  }

  .nav-mobile {
    display: flex;
  }

  .logo-main {
    font-size: 0.95rem;
  }
}
</style>
