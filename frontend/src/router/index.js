import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ConfirmEmailView from '../views/ConfirmEmailView.vue'
import ForgotPasswordView from '../views/ForgotPasswordView.vue'
import ResetPasswordView from '../views/ResetPasswordView.vue'
import ProfileView from '../views/ProfileView.vue'
import CategoryView from '../views/CategoryView.vue'
import TopicView from '../views/TopicView.vue'
import NotificationsView from '../views/NotificationsView.vue'
import MembresView from '../views/MembresView.vue'
import MemberProfileView from '../views/MemberProfileView.vue'
import GroupesView from '../views/GroupesView.vue'
import MessageriesView from '../views/MessageriesView.vue'
import CreateFicheView from '../views/CreateFicheView.vue'
import DemandeDoubleCompteView from '../views/DemandeDoubleCompteView.vue'
import AvatarDirectoryView from '../views/AvatarDirectoryView.vue'
import DemonicFormsView from '../views/DemonicFormsView.vue'
import ArrivalGuideView from '../views/ArrivalGuideView.vue'

const routes = [
  { path: '/mes-rp', name: 'my-rp', component: () => import('../views/MyRPView.vue'), meta: { auth: true } },
  { path: '/administration/alertes-activite', name: 'activity-alerts', component: () => import('../views/ActivityAlertsView.vue'), meta: { auth: true, admin: true } },
  { path: '/', name: 'home', component: HomeView },
  { path: '/bienvenue/parcours-arrivee', name: 'arrival-guide', component: ArrivalGuideView },
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
    path: '/categories/bottin-des-avatars',
    name: 'avatar-directory',
    component: AvatarDirectoryView,
  },
  { path: '/confirmation-email', name: 'confirm-email', component: ConfirmEmailView },
  { path: '/mot-de-passe-oublie', name: 'forgot-password', component: ForgotPasswordView },
  { path: '/reinitialiser-mot-de-passe', name: 'reset-password', component: ResetPasswordView },
  {
    path: '/categories/bottin-des-formes-demoniaques',
    name: 'demonic-forms',
    component: DemonicFormsView,
  },
  {
    path: '/categories/:slug',
    name: 'category',
    component: CategoryView,
    props: true,
  },
  {
    path: '/topics/coop-swann',
    redirect: '/topics/coop-everhart',
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
  {
    path: '/membres',
    name: 'membres',
    component: MembresView,
  },
  {
    path: '/membres/:id',
    name: 'membre-profil',
    component: MemberProfileView,
    props: true,
  },
  {
    path: '/groupes',
    name: 'groupes',
    component: GroupesView,
  },
  {
    path: '/messageries',
    name: 'messageries',
    component: MessageriesView,
    meta: { auth: true },
  },
  {
    path: '/fiches/nouvelle',
    name: 'create-fiche',
    component: CreateFicheView,
    meta: { auth: true },
  },
  {
    path: '/demande-double-compte/nouvelle',
    name: 'demande-double-compte',
    component: DemandeDoubleCompteView,
    meta: { auth: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.auth && !auth.isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }
  if (to.meta.admin && !['admin', 'fondatrice'].includes(auth.user?.role)) {
    return { name: 'home' }
  }
  if (to.meta.guest && auth.isAuthenticated) {
    return { name: 'home' }
  }
})

export default router
