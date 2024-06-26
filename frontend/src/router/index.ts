import { createRouter, createWebHistory } from 'vue-router'
import RankingView from '@/views/RankingView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'ranking',
      component: RankingView
    }
  ]
})

export default router
