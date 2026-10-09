import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import TripsTableView from '../views/TripsTableView.vue'
import ReviewsTableView from '../views/ReviewsTableView.vue'
import MapView from '../views/MapView.vue'
import EmailView from '../views/EmailView.vue'
import CloudStatsView from '../views/CloudStatsView.vue'

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/login', name: 'Login', component: LoginView },
  { path: '/trips', name: 'TripsTable', component: TripsTableView },
  { path: '/reviews', name: 'ReviewsTable', component: ReviewsTableView },
  { path: '/map', name: 'Map', component: MapView },
  { path: '/email', name: 'Email', component: EmailView },
  { path: '/cloud-stats', name: 'CloudStats', component: CloudStatsView }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
