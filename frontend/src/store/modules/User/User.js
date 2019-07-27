import {login, logout} from "../../../api/api";
import router from "../../../router.js"
import Vue from 'vue'
const defaultState = {
    loginForm: {
        email: "",
        password: ""
    },
    error: null,
    isLoggedIn: false
}

const actions = {
    setEmail: (context, payload) => {
        context.commit('SET_EMAIL', payload)
    },

    setPassword: (context, payload) => {
        context.commit('SET_PASSWORD', payload)
    },

    setError: (context, payload) => {
        context.commit('SET_ERROR', payload)
    },

    login: (context, payload) => {
        login(payload.loginForm)
            .then((response) => {
                let token = response.data.token
                localStorage.setItem('token', token)
                Vue.prototype.$http.defaults.headers.common['Authorization'] = "Bearer " + token
                context.commit('SET_IS_LOGGED_IN', {isLoggedIn: true})
                router.push("/dashboard")

            })
            .catch((error) => {
                console.log(error)
                context.commit('SET_ERROR', {error: error.response.data.msg})
            })
    },

    logout: (context, payload) => {
        logout()
            .then((response) => {
                context.commit('SET_IS_LOGGED_IN', {isLoggedIn: false})
                router.push({name: 'Login'})
            })
            .catch((error) => {
                console.log(error.response.data.message)
                context.commit('SET_ERROR', {error: error.response.data.msg})
            })
    }
}

const mutations = {
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
    }
}

const getters = {
    loginForm: state => state.loginForm,
    email: state => state.loginForm.email,
    password: state => state.loginForm.password,
    error: state => state.error,
    isLoggedIn: state => state.isLoggedIn
}


export default {
    state: defaultState,
    getters,
    actions,
    mutations,
    namespaced: true
}
