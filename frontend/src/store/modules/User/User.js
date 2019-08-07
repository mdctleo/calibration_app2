import {login, logout} from "../../../api/api";
import router from "../../../router.js"
import Vue from 'vue'
import {RESET_STATE as RESET_BIODI_CSV_UPLOAD_STATE} from "../BiodiCsvUpload/BiodiCsvUploadTypes"
import {RESET_STATE as RESET_BIODI_CSV_DOWNLOAD_STATE} from "../BiodiCsvDownload/BiodiCsvDownloadTypes"
import {RESET_STATE as RESET_CALIBRATION_STATE} from "../Calibration/types"
import {RESET_STATE as RESET_STATISTICS_STATE} from "../Statistics/types"
import {RESET_STATE as RESET_USER_STATE} from "../User/types"

const getDefaultState = () => {
    return {
        loginForm: {
            email: "",
            password: ""
        },
        error: null,
        loading: false,
        isLoggedIn: false
    }
}
const state = getDefaultState()

const actions = {
    resetState: (context) => {
        context.commit('RESET_STATE')
    },
    setEmail: (context, payload) => {
        context.commit('SET_EMAIL', payload)
    },

    setPassword: (context, payload) => {
        context.commit('SET_PASSWORD', payload)
    },

    setError: (context, payload) => {
        context.commit('SET_ERROR', payload)
    },

    login: async (context, payload) => {
        try {
            context.commit('SET_LOADING', {loading: true})
            let response = await login(payload.loginForm)
            let token = response.data.token
            localStorage.setItem('token', token)
            Vue.prototype.$http.defaults.headers.common['Authorization'] = "Bearer " + token
            context.commit('SET_IS_LOGGED_IN', {isLoggedIn: true})
            router.push({name: 'Dashboard'})
        } catch (error) {
            context.commit('SET_ERROR', {error: error.response.data.msg})
        } finally {
            context.commit('SET_LOADING', {loading: false})
        }
    },

    logout: async (context, payload) => {
        context.commit('SET_LOADING', {loading: true})
        logout()
            .then((response) => {
                let promiseArr = [
                    context.dispatch(RESET_BIODI_CSV_UPLOAD_STATE, null, {root: true}),
                    context.dispatch(RESET_BIODI_CSV_DOWNLOAD_STATE, null, {root: true}),
                    context.dispatch(RESET_CALIBRATION_STATE, null, {root: true}),
                    context.dispatch(RESET_STATISTICS_STATE, null, {root: true}),
                    context.dispatch(RESET_USER_STATE, null, {root: true})
                ]

                return Promise.all(promiseArr)
            })
            .then(() => {
                router.push({name: 'Login'})
            })
            .catch((error) => {
                console.log(error.response.data.message)
                context.commit('SET_ERROR', {error: error.response.data.msg})
            })
            .finally(() => {
                context.commit('SET_LOADING', {loading: false})
            })
    }
}

const mutations = {
    RESET_STATE: (state) => {
        return Object.assign(state, getDefaultState())
    },
    SET_EMAIL: (state, payload) => {
        return state.loginForm.email = payload.email
    },

    SET_PASSWORD: (state, payload) => {
        return state.loginForm.password = payload.password
    },

    SET_ERROR: (state, payload) => {
        return state.error = payload.error
    },

    SET_IS_LOGGED_IN: (state, payload) => {
        return state.isLoggedIn = payload.isLoggedIn
    },

    SET_LOADING: (state, payload) => {
        return state.loading = payload.loading
    }
}

const getters = {
    loginForm: state => state.loginForm,
    email: state => state.loginForm.email,
    password: state => state.loginForm.password,
    error: state => state.error,
    isLoggedIn: state => state.isLoggedIn,
    loading: state => state.loading
}


export default {
    state: state,
    getters,
    actions,
    mutations,
    namespaced: true
}
