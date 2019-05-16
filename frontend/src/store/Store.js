import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        selectedCounter: null,
        selectedIsotope: null
    },
    mutations: {
        setSelectedCounter (state, payload) {
            return state.selectedCounter = payload.selectedCounter;
        },

        setSelectedIsotope (state, payload) {
            return state.selectedIsotope = payload.selectedIsotope;
        }
    },
    actions: {
        setSelectedCounter (context, payload) {
            context.commit('setSelectedCounter', payload)
        },

        setSelectedIsotope (context, payload) {
            context.commit('setSelectedIsotope', payload)
        }
    }
});

// export var store = {
//     state: {
//         selectedCounter: "",
//         selectedIsotope: ""
//     },
//     setSelectedCounter(counter) {
//         this.state.selectedCounter = counter;
//     },
//     getSelectedCounter() {
//         return this.state.selectedCounter
//     },
//
//     setSelectedIsotope(isotope) {
//         this.state.selectedIsotope = isotope
//     },
//
//     getSelectedIsotope() {
//         return this.state.selectedIsotope
//     }
// };
