import Vue from 'vue'
import Vuex from 'vuex'
import calibration from './modules/Calibration/Calibration'

Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
        calibration
    }
})