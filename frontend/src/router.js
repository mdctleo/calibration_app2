import Vue from 'vue'
import Router from 'vue-router'
import Calibration from "./views/Calibration/Calibration";
import Login from "./views/Login/Login";
import DashBoard from "./views/Dashboard/Dashboard";


Vue.use(Router);

export default new Router({
    routes: [
        {
            path: '/',
            name: 'Login',
            component: Login
        },
        {
            path: '/dashboard',
            name: 'Dashboard',
            component: () => import(/* webpackChunkName: "about" */ './views/Dashboard/Dashboard.vue')
        },
        {
            path: '/calibration',
            name: 'calibration',
            component: () => import(/* webpackChunkName: "about" */ './views/Calibration/Calibration.vue')
        },
        {
            path: '/biodicsv',
            name: 'BiodiCsv',
            // route level code-splitting
            // this generates a separate chunk (about.[hash].js) for this route
            // which is lazy-loaded when the route is visited.
            component: () => import(/* webpackChunkName: "about" */ './views/BiodiCsv/BiodiCsv.vue')
        },
        {
            path: '/effect',
            name: 'Effect',
            component: () => import(/* webpackChunkName: "about" */ './views/Statistics/Effect.vue')
        },

        {
            path: '/nobs',
            name: 'Nobs',
            component: () => import('./views/Statistics/Nobs.vue')
        },

        {
            path: '/power',
            name: 'Power',
            component: () => import('./views/Statistics/Power.vue')
        }
    ]
})
