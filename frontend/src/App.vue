<template>
  <div class="app">
    <!-- Floating mystical orbs background -->
    <div class="bg-orbs" aria-hidden="true">
      <div class="orb orb-1"></div>
      <div class="orb orb-2"></div>
      <div class="orb orb-3"></div>
    </div>

    <AppHeader />

    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <footer class="footer">
      <div class="container footer-inner">
        <div class="footer-brand">
          <svg class="footer-triquetra" viewBox="0 0 40 40" width="24" height="24">
            <path d="M20 2C20 2 8 14 8 22c0 5 3 8 6 9c-2-2-3-5-3-8c0-6 9-16 9-16s9 10 9 16c0 3-1 6-3 8c3-1 6-4 6-9c0-8-12-20-12-20z" fill="url(#footer-grad)" opacity="0.9"/>
            <path d="M20 38c-4 0-8-3-9-7c2 2 5 3 9 3s7-1 9-3c-1 4-5 7-9 7z" fill="url(#footer-grad)" opacity="0.7"/>
            <circle cx="20" cy="22" r="3" fill="url(#footer-grad)" opacity="0.8"/>
            <defs>
              <linearGradient id="footer-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#c084fc" />
                <stop offset="100%" stop-color="#f0c674" />
              </linearGradient>
            </defs>
          </svg>
          <span class="footer-title">Nexus Arcana</span>
        </div>
        <p class="footer-text">Quand les mondes se rencontrent</p>
        <div class="footer-links">
          <router-link to="/">Accueil</router-link>
          <span class="footer-dot">·</span>
          <router-link to="/membres">Membres</router-link>
          <span class="footer-dot">·</span>
          <router-link to="/groupes">Groupes</router-link>
        </div>
        <p class="footer-copy">© 2026 Nexus Arcana — Forum RPG crossover non officiel</p>
        <p class="footer-rights">
          <em>Charmed</em> appartient à ses ayants droit, notamment CBS Studios / Paramount ;
          <em>The Vampire Diaries</em>, <em>The Originals</em> et <em>Legacies</em> à leurs ayants droit, notamment Warner Bros. Television, Alloy Entertainment et The CW ;
          <em>Teen Wolf</em> à ses ayants droit, notamment MTV Entertainment.<br>
          Créations : <em>Charmed</em> — Constance M. Burge ; <em>The Vampire Diaries</em> — romans de L. J. Smith, série développée par Kevin Williamson et Julie Plec ;
          <em>The Originals</em> et <em>Legacies</em> — Julie Plec ; <em>Teen Wolf</em> — Jeff Davis. Nexus Arcana est un projet de fans sans but lucratif.
        </p>
      </div>
    </footer>

    <!-- Fixed Theme Toggle (bas-gauche) -->
    <button class="fixed-theme-toggle" @click="toggleTheme" :title="theme === 'dark' ? 'Passer au mode clair' : 'Passer au mode sombre'">
      <span v-if="theme === 'dark'">☀️</span>
      <span v-else>🌙</span>
    </button>

    <!-- Chatbox (bas-droite, membres connectés uniquement) -->
    <ChatBox v-if="auth.isAuthenticated" />
  </div>
</template>

<script setup>
import { onBeforeUnmount, onMounted } from 'vue'
import api from './composables/useApi'
import AppHeader from './components/AppHeader.vue'
import ChatBox from './components/ChatBox.vue'
import { useAuthStore } from './stores/auth'
import { useNotificationStore } from './stores/notifications'
import { useTheme } from './composables/useTheme'

const auth = useAuthStore()
const notifications = useNotificationStore()
const { theme, toggleTheme } = useTheme()
let presenceTimer = null

async function sendPresence() {
  if (!auth.isAuthenticated || document.visibilityState !== 'visible') return
  try { await api.post('/users/presence/') } catch { /* session gérée par auth */ }
}

function onVisibilityChange() {
  if (document.visibilityState === 'visible') sendPresence()
}

onMounted(async () => {
  await auth.init()
  if (auth.isAuthenticated) {
    notifications.startPolling()
    await sendPresence()
    presenceTimer = window.setInterval(sendPresence, 45000)
    document.addEventListener('visibilitychange', onVisibilityChange)
  }
})

onBeforeUnmount(() => {
  if (presenceTimer) window.clearInterval(presenceTimer)
  document.removeEventListener('visibilitychange', onVisibilityChange)
})
</script>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  position: relative;
}

.main-content {
  flex: 1;
}

/* === Floating Orbs Background === */
.bg-orbs {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.15;
  animation: float-orb 20s ease-in-out infinite;
}

.orb-1 {
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, var(--primary), transparent 70%);
  top: -15%;
  left: -10%;
  animation-duration: 25s;
}

.orb-2 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, var(--accent), transparent 70%);
  bottom: -10%;
  right: -10%;
  animation-duration: 30s;
  animation-delay: -5s;
}

.orb-3 {
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, var(--gold), transparent 70%);
  top: 40%;
  left: 50%;
  animation-duration: 35s;
  animation-delay: -10s;
  opacity: 0.08;
}

@keyframes float-orb {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(30px, -40px) scale(1.05); }
  50% { transform: translate(-20px, 20px) scale(0.95); }
  75% { transform: translate(40px, 30px) scale(1.02); }
}

/* === Footer === */
.footer {
  position: relative;
  z-index: 1;
  margin-top: auto;
  padding: 3rem 0 2rem;
  border-top: 1px solid var(--glass-border);
  background: var(--glass-bg);
  backdrop-filter: blur(12px);
}

.footer-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  text-align: center;
}

.footer-brand {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.footer-triquetra {
  filter: drop-shadow(0 0 6px rgba(192, 132, 252, 0.3));
}

.footer-title {
  font-family: var(--font-display);
  font-size: 1rem;
  font-weight: 600;
  background: linear-gradient(135deg, var(--accent), var(--gold));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.footer-text {
  font-size: 0.85rem;
  color: var(--text-muted);
  font-style: italic;
}

.footer-links {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
}

.footer-links a {
  color: var(--text-secondary);
  transition: color var(--transition);
}

.footer-links a:hover {
  color: var(--accent);
}

.footer-dot {
  color: var(--text-muted);
}

.footer-copy {
  font-size: 0.75rem;
  color: var(--text-muted);
  margin-top: 0.5rem;
}

.footer-rights {
  max-width: 760px;
  margin: 0;
  color: var(--text-muted);
  font-size: 0.67rem;
  line-height: 1.55;
}

/* === Fixed Theme Toggle === */
.fixed-theme-toggle {
  position: fixed;
  bottom: 2rem;
  left: 2rem;
  z-index: 999;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: var(--glass-bg);
  backdrop-filter: blur(10px);
  border: 1px solid var(--glass-border);
  color: var(--text);
  font-size: 1.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: var(--shadow-lg), 0 0 15px rgba(139, 92, 246, 0.2);
  transition: all var(--transition);
}

.fixed-theme-toggle:hover {
  transform: translateY(-3px) rotate(15deg);
  background: var(--primary-light);
  border-color: var(--accent);
  box-shadow: var(--shadow-lg), 0 0 20px rgba(139, 92, 246, 0.4);
}

@media (max-width: 768px) {
  .fixed-theme-toggle {
    bottom: 1.5rem;
    left: 1.5rem;
    width: 40px;
    height: 40px;
    font-size: 1.1rem;
  }
}
</style>
