import {calculateEffect, calculateNobs, calculatePower, getPowerGraph, getPowerTable} from "../../../api/api";

const defaultState = {
    input0: null,
    input1: null,
    alpha: null,
    test: null,
    alternative: null,
    result: null,
    loading: false,
    error: null,
    powerGraph: {},
    powerTable: []
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

    setError: (context, payload) => {
        context.commit('SET_ERROR', payload)
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
    },

    calculateNobs: (context, payload) => {
        context.commit('SET_LOADING', {loading: true});
        calculateNobs(payload.statisticForm)
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
    },

    calculatePower: (context, payload) => {
        context.commit('SET_LOADING', {loading: true});
        calculatePower(payload.statisticForm)
            .then((response) => {
                context.commit('SET_RESULT', {result: response.data.result})
            })
            .catch((error) => {
                context.commit('SET_ERROR', {error: error.response.data.message})
            })
            .finally(() => {
                context.commit('SET_LOADING', {loading: false})
            })
    },

    getPowerGraph: (context, payload) => {
        context.commit('SET_LOADING', {loading: true});
        getPowerGraph(payload.statisticForm)
            .then((response) => {
                console.log(response);
                context.commit('SET_POWER_GRAPH', {powerGraph: response.data});
            })
            .catch((error) => {
                context.commit('SET_ERROR', {error: error.response.data.message})
            })
            .finally(() => {
                context.commit('SET_LOADING', {loading: false})
            })
    },

    getPowerTable: (context, payload) => {
        context.commit('SET_LOADING', {loading: true});
        getPowerTable(payload.statisticForm)
            .then((response) => {
                console.log(response);
                context.commit('SET_POWER_TABLE', {powerTable: response.data});
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
    },

    SET_POWER_GRAPH: (state, payload) => {
        return state.powerGraph = payload.powerGraph;
    },

    SET_POWER_TABLE: (state, payload) => {
        return state.powerTable = payload.powerTable;
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
    statisticsError: state => state.error,
    powerGraph: state => state.powerGraph,
    powerTable: state => state.powerTable
};

export default {
    state: defaultState,
    getters,
    actions,
    mutations,
};