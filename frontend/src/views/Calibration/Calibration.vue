<template>
    <div>
        <el-row>
        <el-alert
                v-show="error"
                :title="error"
                type="error"
                show-icon
                @close="setError({error: null})">
        </el-alert>
        </el-row>
        <el-row>
        <IsotopeModelSelect
                :isotopes="isotopes"
                :counters="counters"
                v-on:query="getCalibrationFactors(); getCalibrationFactorsGraph();"></IsotopeModelSelect>
        </el-row>
        <el-row>
        <CalibrationGraph :traces="this.traces"></CalibrationGraph>
        </el-row>
        <el-row>
        <CalibrationTable :calibrationFactors="calibrationFactors"
                          :loading="this.loading"></CalibrationTable>
        </el-row>
    </div>
</template>

<script>
    // @ is an alias to /src
    import * as types from '../../store/modules/Calibration/types'
    import CalibrationTable from './components/CalibrationTable'
    import IsotopeModelSelect from './components/IsotopeModelSelect.vue'
    import {mapActions, mapState, mapGetters} from 'vuex';
    import CalibrationGraph from './components/CalibrationGraph.vue'

    const moment = require('moment');

    export default {
        name: 'Calibration',
        components: {
            CalibrationGraph,
            CalibrationTable,
            IsotopeModelSelect
        },
        computed: {
            ...mapGetters({
                selectedCounter: 'selectedCounter',
                selectedIsotope: 'selectedIsotope',
                counters: 'counters',
                isotopes: 'isotopes',
                calibrationFactors: 'calibrationFactors',
                traces: 'traces',
                loading: 'calibrationLoading',
                error: 'calibrationError'
            })
        },

        methods: {
            ...mapActions([
                types.GET_CALIBRATION_FACTORS,
                types.GET_CALIBRATION_FACTORS_GRAPH,
                types.GET_COUNTERS,
                types.GET_ISOTOPES,
                types.SET_ERROR
            ]),
            getCalibrationFactors() {
                this.$store.dispatch({
                    type: types.GET_CALIBRATION_FACTORS,
                    selectedIsotope: this.selectedIsotope,
                    selectedCounter: this.selectedCounter
                })
            },
            //
            getCalibrationFactorsGraph() {
                this.$store.dispatch({
                    type: types.GET_CALIBRATION_FACTORS_GRAPH,
                    selectedIsotope: this.selectedIsotope,
                    selectedCounter: this.selectedCounter
                })
            }
        },

        created() {
            this.getIsotopes();
            this.getCounters();
        }
    }
</script>
