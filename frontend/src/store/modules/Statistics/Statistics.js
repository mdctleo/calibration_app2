import {calculateEffect, calculateNobs, calculatePower, getPowerGraph, getPowerTable} from "../../../api/api";

const getDefaultState = () => {
    return {
        input0: "",
        input1: "",
        alpha: "",
        test: "",
        alternative: "",
        result: "",
        loading: false,
        error: null,
        powerGraph: {},
        powerTable: []
    }
}

const state = getDefaultState()

const actions = {
    resetState: (context) => {
        context.commit('RESET_STATE')
    },
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

    calculateEffect: async (context, payload) => {
        try {
            context.commit('SET_LOADING', {loading: true})
            let response = await calculateEffect(payload.statisticForm)
            let result = response.data.result
            context.commit('SET_RESULT', {result: result})
        } catch (error) {
            context.commit('SET_ERROR', {error: error.response.data.msg})
        } finally {
            context.commit('SET_LOADING', {loading: false})
        }
    },

    calculateNobs: async (context, payload) => {
        try {
            context.commit('SET_LOADING', {loading: true})
            let response = await calculateNobs(payload.statisticForm)
            let result = response.data.result
            context.commit('SET_RESULT', {result: result})
        } catch (error) {
            context.commit('SET_ERROR', {error: error.response.data.msg})
        } finally {
            context.commit('SET_LOADING', {loading: false})
        }
    },

    calculatePower: async (context, payload) => {
        try {
            context.commit('SET_LOADING', {loading: true})
            let response = await calculatePower(payload.statisticForm)
            let result = response.data.result
            context.commit('SET_RESULT', {result: result})
        } catch (error) {
            context.commit('SET_ERROR', {error: error.response.data.msg})
        } finally {
            context.commit('SET_LOADING', {loading: false})
        }
    },

    getPowerGraph: async (context, payload) => {
        try {
            context.commit('SET_LOADING', {loading: true})
            let response = await getPowerGraph(payload.statisticForm)
            let graph = response.data
            context.commit('SET_POWER_GRAPH', {powerGraph: graph});
        } catch (error) {
            context.commit('SET_ERROR', {error: error.response.data.msg})
        } finally {
            context.commit('SET_LOADING', {loading: false})
        }
    },

    getPowerTable: async (context, payload) => {
        try {
            context.commit('SET_LOADING', {loading: true})
            let response = await getPowerTable(payload.statisticForm)
            let table = response.data
            context.commit('SET_POWER_TABLE', {powerTable: table});
        } catch (error) {
            context.commit('SET_ERROR', {error: error.response.data.msg})
        } finally {
            context.commit('SET_LOADING', {loading: false})
        }
    }
};

const mutations = {
    RESET_STATE: (state) => {
        return Object.assign(state, getDefaultState())
    },

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
    loading: state => state.loading,
    error: state => state.error,
    powerGraph: state => state.powerGraph,
    powerTable: state => state.powerTable
};

export default {
    state: state,
    getters,
    actions,
    mutations,
    namespaced: true
};