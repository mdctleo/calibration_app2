import {login} from "../../../api/api";

const defaultState = {
    loginForm: {
        email: "",
        password: ""
    }
}

const actions = {
    setEmail: (context, payload) => {
        context.commit('SET_EMAIL', payload)
    },

    setPassword: (context, payload) => {
        context.commit('SET_PASSWORD', payload)
    },

    login: (context, payload) => {
        login(payload.loginForm)
            .then((response) => {
                let token = response.data
                console.log(response)
                localStorage.setItem('token', token)
            })
            .catch((error) => {
                console.log(error)
            })
    }
}

const mutations = {
    SET_EMAIL: (state, payload) => {
        return state.loginForm.email = payload.email
    },

    SET_PASSWORD: (state, payload) => {
        return state.loginForm.password = payload.password
    }
}

const getters = {
    loginForm: state => state.loginForm,
    email: state => state.loginForm.email,
    password: state => state.loginForm.password
}


export default {
    state: defaultState,
    getters,
    actions,
    mutations,
    namespaced: true
}
