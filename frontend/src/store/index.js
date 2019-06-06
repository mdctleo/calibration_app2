import Vue from 'vue'
import Vuex from 'vuex'
import calibration from './modules/Calibration/Calibration'
import statistics from './modules/Statistics/Statistics'
import biodiCsvDownload from './modules/BiodiCsv/BiodiCsvDownload'

Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
        calibration: calibration,
        statistics: statistics,
        biodiCsvDownload: biodiCsvDownload
    }
})