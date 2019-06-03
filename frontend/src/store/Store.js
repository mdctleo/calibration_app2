import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        selectedCounter: null,
        selectedIsotope: null,
        files: [],
        biodiCsvToDownload: null
    },
    mutations: {
        setSelectedCounter (state, payload) {
            return state.selectedCounter = payload.selectedCounter;
        },

        setSelectedIsotope (state, payload) {
            return state.selectedIsotope = payload.selectedIsotope;
        },

        setFiles (state, payload) {
            return state.files = payload.files;
        },

        setBiodiCsvToDownload (state, payload) {
            return state.biodiCsvToDownload = payload.biodiCsvToDownload;
        }
    },
    actions: {
        setSelectedCounter (context, payload) {
            context.commit('setSelectedCounter', payload)
        },

        setSelectedIsotope (context, payload) {
            context.commit('setSelectedIsotope', payload)
        },

        setFiles (context, payload){
            context.commit('setFiles', payload)
        },

        setBiodiCsvToDownload (context, payload) {
            context.commit('setBiodiCsvToDownload', payload)
        }
    }
});

