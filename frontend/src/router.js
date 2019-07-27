import Vue from 'vue'
import Router from 'vue-router'
import Login from "./views/Login/Login";


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
            name: 'Calibration',
            component: () => import(/* webpackChunkName: "about" */ './views/Calibration/Calibration.vue')
        },
        {
          path: '/biodicsv/download',
          name: 'BiodiCsvDownload',
            component: () => import(/* webpackChunkName: "about" */ './views/BiodiCsv/BiodiCsvDownloadView.vue')

        },
        {
          path: '/biodicsv/upload',
          name: 'BiodiCsvUpload',
          component: () => import('./views/BiodiCsv/BiodiCsvUploadView.vue')
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
        },

        {
            path: '/logout',
            name: 'Logout',
            component: () => import('./views/Login/Logout.vue')
        }
    ]
})
