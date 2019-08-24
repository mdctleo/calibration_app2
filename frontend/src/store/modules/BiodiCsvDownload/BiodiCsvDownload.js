import {getBiodiCsvComplete, getBiodiCsv, getBiodiCsvMetas, getBiodiCsvAnalysis} from "../../../api/api";
const moment = require('moment/moment');

const getDefaultState = () => {
    return {
        metas: [],
        biodiCsvToDownload: "",
        error: null,
        loading: false,
    }
}

const state = getDefaultState()

const actions = {
    resetState: (context) => {
        context.commit('RESET_STATE')
    },

    setBiodiCsvToDownload: (context, payload) => {
        context.commit('SET_BIODI_CSV_TO_DOWNLOAD', payload)
    },

    setError: (context, payload) => {
        context.commit('SET_ERROR', payload);
    },

    downloadBiodiCsvComplete: async (context, payload) => {
        try {
            context.commit('SET_LOADING', {loading: true})
            let response = await getBiodiCsvComplete(payload.biodiCsvToDownload)
            console.log(response)
            const url = window.URL.createObjectURL(new Blob([response.data]))
            const link = document.createElement('a')
            link.href = url;
            link.setAttribute('download', 'file.csv')
            document.body.appendChild(link)
            link.click()
            link.parentNode.removeChild(link)
        } catch (error) {
            context.commit('SET_ERROR', {error: error.response.data.msg})
        } finally {
            context.commit('SET_LOADING', {loading: false})
        }
    },

    downloadBiodiCsvRaw: async (context, payload) => {
        try {
            context.commit('SET_LOADING', {loading: true})
            let response = await getBiodiCsv(payload.biodiCsvToDownload)
            const url = window.URL.createObjectURL(new Blob([response.data]))
            const link = document.createElement('a')
            link.href = url
            link.setAttribute('download', 'file.csv')
            document.body.appendChild(link)
            link.click()
            link.parentNode.removeChild(link)
        } catch (error) {
            console.log(error.response.data.msg)
            context.commit('SET_ERROR', {error: error.response.data.msg})
        } finally {
            context.commit('SET_LOADING', {loading: false})
        }
    },

    downloadBiodiCsvAnalysis: async (context, payload) => {
        try {
            context.commit('SET_LOADING', {loading: true})
            let response = await getBiodiCsvAnalysis(payload.biodiCsvToDownload)
            console.log(response)
            const url = window.URL.createObjectURL(new Blob([response.data]))
            const link = document.createElement('a')
            link.href = url
            link.setAttribute('download', 'file.csv')
            document.body.appendChild(link)
            link.click()
            link.parentNode.removeChild(link)
        } catch (error) {
            context.commit('SET_ERROR', {error: error.response.data.msg})
        } finally {
            context.commit('SET_LOADING', {loading: false})
        }
    },

    getBiodiCsvMetas: async (context) => {
        try {
            context.commit('SET_LOADING', {loading: true});
            let response = await getBiodiCsvMetas()
            let metas = response.data
            console.log(metas)
            metas.forEach((meta) => {
                meta.createdOn = moment(meta.createdOn).format('DD-MM-YYYY, h:mm:ss');
            });
            context.commit('SET_METAS', {metas: metas});
        } catch (error) {
            console.log('Got to error')
            context.commit('SET_ERROR', {error: error.response.data.msg});
        } finally {
            context.commit('SET_LOADING', {loading: false})
        }
    }

};

const mutations = {
    RESET_STATE: (state) => {
        return Object.assign(state, getDefaultState())
    },
    SET_LOADING: (state, payload) => {
        return state.loading = payload.loading
    },

    SET_ERROR: (state, payload) => {
        return state.error = payload.error
    },

    SET_METAS: (state, payload) => {
        return state.metas = payload.metas
    },

    SET_BIODI_CSV_TO_DOWNLOAD: (state, payload) => {
        return state.biodiCsvToDownload = payload.biodiCsvToDownload
    }
};

const getters = {
    error: state => state.error,
    loading: state => state.loading,
    biodiCsvToDownload: state => state.biodiCsvToDownload,
    metas: state => state.metas
};

export default {
    state: state,
    getters,
    actions,
    mutations,
    namespaced: true
};