import {calculateEffect} from "../../../api/api";

const defaultState = {
    input0: null,
    input1: null,
    alpha: null,
    test: null,
    alternative: null,
    result: null,
    loading: false,
    error: null
};

const actions = {
    setInput0: (context, payload) => {
        context.commit('SET_INPUT_0', payload);
    },

    setInput1: (context, payload) => {
        context.commit('SET_INPUT_1', payload);
    },

    setAlpha: (context, payload) => {
        context.commit('SET_ALPHA', payload);
    },

    setTest: (context, payload) => {
        context.commit('SET_TEST', payload);
    },

    setAlternative: (context, payload) => {
        context.commit('SET_ALTERNATIVE', payload)
    },

    setResult: (context, payload) => {
        context.commit('SET_RESULT', payload)
    },

    calculateEffect: (context, payload) => {
        context.commit('SET_LOADING', {loading: true});
        calculateEffect(payload.statisticForm)
            .then((response) => {
                console.log(response);
                context.commit('SET_RESULT', {result: response.data.result})
            })
            .catch((error) => {
                context.commit('SET_ERROR', {error: error.response.data.message})
            })
            .finally(() => {
                context.commit('SET_LOADING', {loading: false})
            })
    }
};

const mutations = {
    SET_INPUT_0: (state, payload) => {
        return state.input0 = payload.input0;
    },

    SET_INPUT_1: (state, payload) => {
        return state.input1 = payload.input1;
    },

    SET_ALPHA: (state, payload) => {
        return state.alpha = payload.alpha;
    },

    SET_TEST: (state, payload) => {
        return state.test = payload.test;
    },

    SET_ALTERNATIVE: (state, payload) => {
        return state.alternative = payload.alternative;
    },

    SET_RESULT: (state, payload) => {
        return state.result = payload.result;
    },

    SET_LOADING: (state, payload) => {
        return state.loading = payload.loading;
    },

    SET_ERROR: (state, payload) => {
        return state.error = payload.error;
    }

};

const getters = {
    input0: state => state.input0,
    input1: state => state.input1,
    alpha: state => state.alpha,
    test: state => state.test,
    alternative: state => state.alternative,
    result: state => state.result,
    statisticsLoading: state => state.loading,
    statisticsError: state => state.error
};

export default {
    state: defaultState,
    getters,
    actions,
    mutations,
};