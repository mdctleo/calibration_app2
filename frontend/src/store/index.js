import Vue from 'vue'
import Vuex from 'vuex'
import calibration from './modules/Calibration/Calibration'
import statistics from './modules/Statistics/Statistics'
import biodiCsvDownload from './modules/BiodiCsv/BiodiCsvDownload'
import biodiCsvUpload from './modules/BiodiCsv/BiodiCsvUpload'
import user from './modules/User/User'
import createPersistedState from 'vuex-persistedstate'

Vue.use(Vuex);

export default new Vuex.Store({
    plugins: [createPersistedState()],
    modules: {
        calibration: calibration,
        statistics: statistics,
        biodiCsvDownload: biodiCsvDownload,
        biodiCsvUpload: biodiCsvUpload,
        user: user
    }
})