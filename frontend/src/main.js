import Vue from 'vue'
import App from './App.vue'
import router from './router'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import locale from 'element-ui/lib/locale/lang/en'
// import store from './store/Store'
import store from './store/index'
import Axios from 'axios'
import {RESET_STATE as RESET_BIODI_CSV_UPLOAD_STATE} from "./store/modules/BiodiCsvUpload/BiodiCsvUploadTypes";
import {RESET_STATE as RESET_BIODI_CSV_DOWNLOAD_STATE} from "./store/modules/BiodiCsvDownload/BiodiCsvDownloadTypes";
import {RESET_STATE as RESET_CALIBRATION_STATE} from "./store/modules/Calibration/types";
import {RESET_STATE as RESET_STATISTICS_STATE} from "./store/modules/Statistics/types";
import {RESET_STATE as RESET_USER_STATE} from "./store/modules/User/types";

Vue.prototype.$http = Axios;

// adds authorization header to every request
Axios.defaults.withCredentials = true
const token = localStorage.getItem('token')
if (token) {
  Vue.prototype.$http.defaults.headers.common['Authorization'] = "Bearer " + token
}

// navigation guard
router.beforeEach((to, from, next) => {
  if (to.path !== '/' && !store.getters['user/isLoggedIn']) {
    next('/')
  } else {
    next()
  }
})

Vue.config.productionTip = false;
Vue.use(ElementUI, {locale});
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app');


// response interceptor for 401
Vue.prototype.$http.interceptors.response.use(
    (response) => {
      console.log('intercepted it on fulfilled')
      return response
    },
    (error) => {
      console.log('intercepted it on error')
      if (error.response.status === 401) {
        let promiseArr = [
          store.dispatch(RESET_BIODI_CSV_UPLOAD_STATE, null, {root: true}),
          store.dispatch(RESET_BIODI_CSV_DOWNLOAD_STATE, null, {root: true}),
          store.dispatch(RESET_CALIBRATION_STATE, null, {root: true}),
          store.dispatch(RESET_STATISTICS_STATE, null, {root: true}),
          store.dispatch(RESET_USER_STATE, null, {root: true})
        ]

        Promise.all(promiseArr)
            .then(() => {
              router.push('/')
            })
            .catch((error) => {

            })
      }
    })