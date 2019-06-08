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
         <LineGraph graph-id="CalibrationGraph" :graph="calibrationGraph"></LineGraph>
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
    import {mapActions, mapGetters} from 'vuex';
    import LineGraph from "../../components/LineGraph";

    export default {
        name: 'Calibration',
        components: {
            LineGraph,
            CalibrationTable,
            IsotopeModelSelect
        },
        computed: {
            ...mapGetters({
                selectedCounter: 'calibration/selectedCounter',
                selectedIsotope: 'calibration/selectedIsotope',
                counters: 'calibration/counters',
                isotopes: 'calibration/isotopes',
                calibrationFactors: 'calibration/calibrationFactors',
                calibrationGraph: 'calibration/calibrationGraph',
                loading: 'calibration/loading',
                error: 'calibration/error'
            })
        },

        methods: {
            ...mapActions({
                'getCalibrationFactors': types.GET_CALIBRATION_FACTORS,
                'getCalibrationFactorsGraph': types.GET_CALIBRATION_FACTORS_GRAPH,
                'getCounters': types.GET_COUNTERS,
                'getIsotopes': types.GET_ISOTOPES,
                'setError': types.SET_CALIBRATION_ERROR
            }),
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
