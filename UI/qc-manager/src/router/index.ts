import { createRouter, createWebHistory } from 'vue-router'
// @ts-ignore
import AnalysisView from '@/views/AnalysisView.vue'
// @ts-ignore
import CleanView from '@/views/CleanView.vue'
// @ts-ignore
import ReviewView from '@/views/ReviewView.vue'
// @ts-ignore
import UploadView from '@/views/UploadView.vue'
// @ts-ignore
import NormalizeView from '@/views/NormalizeView.vue'
// @ts-ignore
import SaveView from '@/views/SaveView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/analysis',
      name: 'analysis',
      component: AnalysisView
    },
    {
      path: '/clean',
      name: 'clean',
      component: CleanView
    },
    {
      path: '/review',
      name: 'review',
      component: ReviewView
    },
    {
      path: '/upload',
      name: 'upload',
      component: UploadView
    },
    {
      path: '/normalize',
      name: 'normalize',
      component: NormalizeView
    },
    {
      path: '/save',
      name: 'save',
      component: SaveView
    }
  ]
})

export default router
