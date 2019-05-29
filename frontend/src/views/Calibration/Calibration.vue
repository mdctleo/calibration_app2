<template>
    <div>
        <el-row>
        <el-alert
                v-show="error"
                :title="error"
                type="error"
                show-icon
                @close="error = null">
        </el-alert>
        </el-row>
        <el-row>
        <IsotopeModelSelect
                :isotopes="isotopes"
                :counters="counters"
                v-on:query="getCalibrationFactors(); getCalibrationFactorsGraph();"></IsotopeModelSelect>
        </el-row>
        <el-row>
        <CalibrationGraph :traces="traces"></CalibrationGraph>
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
    import * as api from '../../api/api'
    import {mapState, mapGetters} from 'vuex';
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
                counters: 'counters',
                isotopes: 'isotopes',
                calibrationFactors: 'calibrationFactors',
                traces: 'traces',
                loading: 'loading',
                error: 'error'
            })
        },

        methods: {
            getCalibrationFactors() {
                this.$store.dispatch(types.GET_CALIBRATION_FACTORS)
            },

            getCalibrationFactorsGraph() {
                this.$store.dispatch(types.GET_CALIBRATION_FACTORS_GRAPH)
            }
        },

        created() {
            this.$store.dispatch(types.GET_COUNTERS);
            this.$store.dispatch(types.GET_ISOTOPES);
        }
    }


    // export default {
    //     name: 'Calibration',
    //     components: {
    //         CalibrationGraph,
    //         CalibrationTable,
    //         IsotopeModelSelect
    //     },
    //     data() {
    //         return {
    //             counters: [],
    //             isotopes: [],
    //             calibrationFactors: [],
    //             traces: {},
    //             loading: false,
    //             error: null
    //         }
    //     },
    //     computed: {
    //         ...mapState(['selectedCounter', 'selectedIsotope'])
    //     },
    //
    //     methods: {
    //
    //         // TODO: Refactor this
    //         getCalibrationFactors() {
    //             this.loading = true;
    //             api.getCalibrationFactors(this.selectedCounter, this.selectedIsotope)
    //                 .then((response) => {
    //                     this.calibrationFactors = response.data;
    //                     this.calibrationFactors.forEach((calibrationFactor) => {
    //                         // format display date
    //                         calibrationFactor.createdOn = moment(calibrationFactor.createdOn).format('DD-MM-YYYY, h:mm:ss');
    //                     });
    //                 })
    //                 .catch((error) => {
    //                     console.log(error);
    //                     this.error = error.response.data.message;
    //                 })
    //                 .finally(() => {
    //                     this.loading = false;
    //                 })
    //         },
    //         getCalibrationFactorsGraph() {
    //             this.loading = true;
    //             api.getCalibrationFactorsGraph(this.selectedCounter, this.selectedIsotope)
    //                 .then((response) => {
    //                     this.traces = response.data;
    //                     Object.values(this.traces).forEach((trace) => {
    //                         trace[0].forEach((time, index) => {
    //                             trace[0][index] = moment(time).format('DD-MM-YYYY, h:mm:ss');
    //                         })
    //                     })
    //                 })
    //                 .catch((error) => {
    //                     console.log(error);
    //                     this.error = error.response.data.message;
    //
    //                 })
    //                 .finally(() => {
    //                     this.loading = false;
    //                 })
    //         },
    //
    //         getCounters() {
    //             this.loading = true;
    //             api.getCounters()
    //                 .then((response) => {
    //                     this.counters = response.data
    //                 })
    //                 .catch((error) => {
    //                     this.error = error.response.data.message
    //                 })
    //                 .finally(() => {
    //                     this.loading = false;
    //                 });
    //
    //         },
    //
    //         getIsotopes() {
    //             this.loading = true;
    //             api.getIsotopes()
    //                 .then((response) => {
    //                     this.isotopes = response.data
    //                 })
    //                 .catch((error) => {
    //                     this.error = error.response.data.message
    //                 })
    //                 .finally(() => {
    //                     this.loading = false;
    //                 })
    //         }
    //     },
    //     created() {
    //         this.getCounters();
    //         this.getIsotopes();
    //
    //     }
    // }
</script>
