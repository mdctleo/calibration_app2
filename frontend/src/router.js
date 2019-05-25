import Vue from 'vue'
import Router from 'vue-router'
import Calibration from "./views/Calibration/Calibration";
import Login from "./views/Login/Login";


Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Login',
      component: Login
    },
    {
      path: '/calibrationfactor',
      name: 'calibrationFactor',
      component: () => import(/* webpackChunkName: "about" */ './views/Calibration/Calibration.vue')
    },
    {
      path: '/biodicsv',
      name: 'BiodiCsv',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "about" */ './views/BiodiCsv/BiodiCsv.vue')
    }
  ]
})
