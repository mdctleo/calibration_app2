import Vue from 'vue'
import App from './App.vue'
import router from './router'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import locale from 'element-ui/lib/locale/lang/en'
// import store from './store/Store'
import store from './store/index'
import Axios from 'axios'

Vue.prototype.$http = Axios;
Axios.defaults.withCredentials = true
const token = localStorage.getItem('token')
if (token) {
  Vue.prototype.$http.defaults.headers.common['Authorization'] = "Bearer " + token
}

Vue.config.productionTip = false;
Vue.use(ElementUI, {locale});
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app');
