import {getCounters, getIsotopes, getCalibrationFactorsGraph, getCalibrationFactors} from "../../../api/api";

const moment = require('moment/moment');

const getDefaultState = () => {
    return {
        selectedCounter: null,
        selectedIsotope: null,
        counters: [],
        isotopes: [],
        calibrationFactores: [],
        calibrationGraph: {},
        loading: false,
        error: null
    }
}

const defaultState = getDefaultState()

const actions = {
    resetState: (context) => {
        context.commit('RESET_STATE')
    },
    setSelectedCounter: (context, payload) => {
        context.commit('SET_SELECTED_COUNTER', payload)
    },

    setSelectedIsotope: (context, payload) => {
        context.commit('SET_SELECTED_ISOTOPE', payload)
    },

    setError: (context, payload) => {
        context.commit('SET_ERROR', payload)
    },

    getCounters: async (context) => {
        try {
            context.commit('SET_LOADING', {loading: true})
            let response = await getCounters()
            let counters = response.data
            context.commit('SET_COUNTERS', {counters: counters})
        } catch (error) {
            context.commit('SET_ERROR', {error: error.response.data.msg})
        } finally {
            context.commit('SET_LOADING', {loading: false})
        }
    },

    getIsotopes: async (context) => {
        try {
            context.commit('SET_LOADING', {loading: true})
            let response = await getIsotopes()
            let isotopes = response.data
            context.commit('SET_ISOTOPES', {isotopes: isotopes})
        } catch (error) {
            context.commit('SET_ERROR', {error: error.response.data.msg})
        } finally {
            context.commit('SET_LOADING', {loading: false})
        }
    },

    getCalibrationFactors: async (context, payload) => {
        try {
            context.commit('SET_LOADING', {loading: true})
            let response = await getCalibrationFactors(payload.selectedCounter, payload.selectedIsotope)
            let calibrationFactors = response.data
            calibrationFactors.forEach((calibrationFactor) => {
                // format display date
                calibrationFactor.createdOn = moment(calibrationFactor.createdOn).format('DD-MM-YYYY, h:mm:ss')
            });
            context.commit('SET_CALIBRATION_FACTORS', {calibrationFactors: calibrationFactors})
        } catch (error) {
            context.commit('SET_ERROR', {error: error.response.data.msg})
        } finally {
            context.commit('SET_LOADING', {loading: false})
        }
    },

    getCalibrationFactorsGraph: async (context, payload) => {
        try {
            context.commit('SET_LOADING', {loading: true})
            let graph = {}
            let response = await getCalibrationFactorsGraph(payload.selectedCounter, payload.selectedIsotope)
            if (response.status === 200) {
                graph = response.data;
                graph.data.forEach((trace) => {
                    trace.x.forEach((date, index) => {
                        trace.x[index] = moment(date).format('DD-MM-YYYY, h:mm:ss');
                    })
                })
            }
            context.commit('SET_CALIBRATION_GRAPH', {calibrationGraph: graph});
        } catch (error) {
            context.commit('SET_ERROR', {error: error.response.data.msg})
        } finally {
            context.commit('SET_LOADING', {loading: false});
        }
    }
};

const mutations = {
    // sate setters
    RESET_STATE: (state) => {
        return Object.assign(state, getDefaultState())
    },
    SET_SELECTED_COUNTER: (state, payload) => {
        return state.selectedCounter = payload.selectedCounter;
    },

    SET_SELECTED_ISOTOPE: (state, payload) => {
        return state.selectedIsotope = payload.selectedIsotope;
    },

    SET_ISOTOPES: (state, payload) => {
        return state.isotopes = payload.isotopes
    },

    SET_COUNTERS: (state, payload) => {
        return state.counters = payload.counters
    },

    SET_CALIBRATION_FACTORS: (state, payload) => {
        return state.calibrationFactors = payload.calibrationFactors
    },

    SET_CALIBRATION_GRAPH: (state, payload) => {
        return state.calibrationGraph = payload.calibrationGraph
    },

    SET_LOADING: (state, payload) => {
        return state.loading = payload.loading
    },

    SET_ERROR: (state, payload) => {
        return state.error = payload.error
    }
};

const getters = {
    // state getters
    selectedCounter: state => state.selectedCounter,
    selectedIsotope: state => state.selectedIsotope,
    counters: state => state.counters,
    isotopes: state => state.isotopes,
    calibrationFactors: state => state.calibrationFactors,
    calibrationGraph: state => state.calibrationGraph,
    loading: state => state.loading,
    error: state => state.error
};


export default {
    state: defaultState,
    getters,
    actions,
    mutations,
    namespaced: true
};