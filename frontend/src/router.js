import Vue from 'vue'
import Router from 'vue-router'
import Calibration from "./views/calibration/Calibration";


Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Calibration',
      component: Calibration
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "about" */ './views/About.vue')
    },
  ]
})
