import {getBiodiCsvComplete, getBiodiCsvRaw, getBiodiCsvMetas} from "../../../api/api";
const moment = require('moment/moment');

const getDefaultState = () => {
    return {
        metas: [],
        biodiCsvCompleteToDownload: "",
        biodiCsvRawToDownload: "",
        error: null,
        loading: false,
    }
}

const state = getDefaultState()

const actions = {
    resetState: (context) => {
        context.commit('RESET_STATE')
    },

    setBiodiCsvCompleteToDownload: (context, payload) => {
      context.commit('SET_BIODI_CSV_COMPLETE_TO_DOWNLOAD', payload)
    },

    setBiodiCsvRawToDownload: (context, payload) => {
        context.commit('SET_BIODI_CSV_RAW_TO_DOWNLOAD', payload)
    },

    setError: (context, payload) => {
        context.commit('SET_ERROR', payload);
    },

    downloadBiodiCsvComplete: (context, payload) => {
        context.commit('SET_LOADING', {loading: true});
        getBiodiCsvComplete(payload.biodiCsvCompleteToDownload)
            .then((response) => {
                const url = window.URL.createObjectURL(new Blob([response.data]));
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', 'file.csv');
                document.body.appendChild(link);
                link.click();
                link.parentNode.removeChild(link);
            })
            .catch((error) => {
                context.commit('SET_ERROR', {error: error.response.data.msg});
            })
            .finally(() => {
                context.commit('SET_LOADING', {loading: false});
            })
    },

    downloadBiodiCsvRaw: (context, payload) => {
        context.commit('SET_LOADING', {loading: true})
        getBiodiCsvRaw(payload.biodiCsvRawToDownload)
            .then((response) => {
                const url = window.URL.createObjectURL(new Blob([response.data]))
                const link = document.createElement('a')
                link.href = url
                link.setAttribute('download', 'file.csv')
                document.body.appendChild(link)
                link.click()
                link.parentNode.removeChild(link)
            })
            .catch((error) => {
                console.log(error)
                context.commit('SET_ERROR', {error: error.response.data.msg})
            })
            .finally(() => {
                context.commit('SET_LOADING', {loading: false})
            })

    },

    getBiodiCsvMetas: (context) => {
        context.commit('SET_LOADING', {loading: true});
        getBiodiCsvMetas()
            .then((response) => {
                console.log('Got to fulfill')
                let metas = response.data;
                metas.forEach((meta) => {
                    meta.createdOn = moment(meta.createdOn).format('DD-MM-YYYY, h:mm:ss');
                });
               context.commit('SET_METAS', {metas: metas});
            })
            .catch((error) => {
                console.log('Got to error')
                context.commit('SET_ERROR', {error: error.response.data.msg});
            })
            .finally(() => {
                context.commit('SET_LOADING', {loading: false});
            })
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

    SET_BIODI_CSV_COMPLETE_TO_DOWNLOAD: (state, payload) => {
        return state.biodiCsvCompleteToDownload = payload.biodiCsvCompleteToDownload
    },

    SET_BIODI_CSV_RAW_TO_DOWNLOAD: (state, payload) => {
        return state.biodiCsvRawToDownload = payload.biodiCsvRawToDownload
    }
};

const getters = {
    error: state => state.error,
    loading: state => state.loading,
    biodiCsvCompleteToDownload: state => state.biodiCsvCompleteToDownload,
    biodiCsvRawToDownload: state => state.biodiCsvRawToDownload,
    metas: state => state.metas
};

export default {
    state: state,
    getters,
    actions,
    mutations,
    namespaced: true
};