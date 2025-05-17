import { createRouter, createWebHistory } from 'vue-router'
import Tenis from '../components/tenis.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'tenis',
      component: Tenis,
    },
  ]
})


export default router