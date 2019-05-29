import {getCounters, getIsotopes, getCalibrationFactorsGraph, getCalibrationFactors} from "../../../api/api";
const moment = require('moment/moment');


const defaultState = {
    selectedCounter: null,
    selectedIsotope: null,
    counters: [],
    isotopes: [],
    calibrationFactors: [],
    traces: {},
    loading: false,
    error: null
};

const actions = {
    setSelectedCounter: (context, payload) => {
        context.commit('SET_SELECTED_COUNTER', payload)
    },

    setSelectedIsotope: (context, payload) => {
      context.commit('SET_SELECTED_ISOTOPE', payload)
    },

  // api calls
  getCounters: (context) => {
        console.log("Got Here");
      context.commit('SET_LOADING', {loading: true});
      getCounters()
          .then((response) => {
              context.commit('SET_COUNTERS', {counters: response.data})
          })
          .catch((error) => {
              context.commit('SET_ERROR', {error: error.response.data.message})
          })
          .finally(() => {
              context.commit('SET_LOADING', {loading: false});
          });
  },

  getIsotopes: (context) => {
      context.commit('SET_LOADING', {loading: true});
      getIsotopes()
          .then((response) => {
              context.commit('SET_ISOTOPES', {isotopes: response.data})
          })
          .catch((error) => {
              context.commit('SET_ERROR', {error: error.response.data.message})
          })
          .finally(() => {
              context.commit('SET_LOADING', {loading: false});
          });
  },

    getCalibrationFactors: (context) => {
        context.commit('SET_LOADING', {loading: true});
      getCalibrationFactors(context.selectedCounter, context.selectedIsotope)
          .then((response) => {
              let calibrationFactors = response.data;
              calibrationFactors.forEach((calibrationFactor) => {
                  // format display date
                  calibrationFactor.createdOn = moment(calibrationFactor.createdOn).format('DD-MM-YYYY, h:mm:ss');
              });
              context.commit('SET_CALIBRATION_FACTORS', {calibrationFactors: calibrationFactors})

          })
          .catch((error) => {
              context.commit('SET_ERROR', {error: error.response.data.message})
          })
          .finally(() => {
              context.commit('SET_LOADING', {loading: false});
          })
    },

    getCalibrationFactorsGraph: (context) => {
        context.commit('SET_LOADING', {loading: true});
        console.log(context.get());
        console.log(context.state.selectedIsotope);
        getCalibrationFactorsGraph(context.selectedCounter, context.selectedIsotope)
            .then((response) => {
                console.log(response.data);
                let traces = response.data;
                Object.values(traces).forEach((trace) => {
                    trace[0].forEach((time, index) => {
                        trace[0][index] = moment(time).format('DD-MM-YYYY, h:mm:ss');
                    })
                });
                context.commit('SET_TRACES', {traces: traces})
            })
            .catch((error) => {
                console.log(error);
                context.commit('SET_ERROR', {error: error.response.data.message})
            })
            .finally(() => {
                context.commit('SET_LOADING', {loading: false});
            })
    }
};

const mutations = {
    // sate setters
    SET_SELECTED_COUNTER:  (state, payload) => {
        return state.selectedCounter = payload.selectedCounter;
    },

    SET_SELECTED_ISOTOPE: (state, payload) => {
        return state.selectedIsotope = payload.selectedIsotope;
    },

    SET_ISOTOPES: (state, payload) => {
        console.log(payload.isotopes);
        return state.isotopes = payload.isotopes
    },

    SET_COUNTERS: (state, payload) => {
        console.log(payload.counters);
        return state.counters = payload.counters
    },

    SET_CALIBRATION_FACTORS: (state, payload) => {
        return state.calibrationFactors = payload.calibrationFactors
    },

    SET_TRACES: (state, payload) => {
        return state.traces = payload.traces
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
    traces: state => state.traces,
    loading: state => state.loading,
    error: state => state.error
};


export default {
    state: defaultState,
    getters,
    actions,
    mutations
};