import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ProfileView from '../views/ProfileView.vue'
import CategoryView from '../views/CategoryView.vue'
import TopicView from '../views/TopicView.vue'
import NotificationsView from '../views/NotificationsView.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { guest: true },
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView,
    meta: { guest: true },
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfileView,
    meta: { auth: true },
  },
  {
    path: '/categories/:slug',
    name: 'category',
    component: CategoryView,
    props: true,
  },
  {
    path: '/topics/:slug',
    name: 'topic',
    component: TopicView,
    props: true,
  },
  {
    path: '/notifications',
    name: 'notifications',
    component: NotificationsView,
    meta: { auth: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.auth && !auth.isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }
  if (to.meta.guest && auth.isAuthenticated) {
    return { name: 'home' }
  }
})

export default router
