import Vue from 'vue'
import VueRouter from 'vue-router'
import URLReports from '../components/URLReports.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'URLReports',
    component: URLReports
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
