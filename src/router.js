import VueRouter from "vue-router"
import workflow from './components/workflow'
import { pairs } from './settings.json'

const router = new VueRouter({
  routes: [
    { path: '/:id', name: 'pair', component: workflow },
    { path: '', redirect: pairs[0].path },
  ]
})

export default router