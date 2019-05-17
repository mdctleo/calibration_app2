<template>
  <div>
    <el-alert
            v-show="error"
            :title="error"
            type="error"
            show-icon
            @close="error = null">
    </el-alert>
    <IsotopeModelSelect
    :isotopes="this.isotopes"
    :counters="this.counters"
    v-on:query = "getCalibrationFactors(); getCalibrationFactorsGraph();"></IsotopeModelSelect>
    <CalibrationGraph :traces="this.traces" :loading="this.loading"></CalibrationGraph>
    <CalibrationTable :calibrationFactors="this.calibrationFactors"
      :loading="this.loading"></CalibrationTable>
  </div>
</template>

<script>
// @ is an alias to /src
import CalibrationTable from '@/components/CalibrationTable.vue'
import IsotopeModelSelect from '@/components/IsotopeModelSelect.vue'
import * as api from '../../api/CalibrationAPI'
import { mapState } from 'vuex';
import CalibrationGraph from '@/components/CalibrationGraph.vue'
const moment = require('moment');


export default {
  name: 'Calibration',
  components: {
    CalibrationGraph,
    CalibrationTable,
    IsotopeModelSelect
  },
  data () {
    return {
      counters:  [],
      isotopes: [],
      calibrationFactors: [],
      traces: {},
      loading: false,
      error: null
    }
  },
  computed: {
    ...mapState(['selectedCounter', 'selectedIsotope'])
  },

  methods: {

    // TODO: Refactor this
    getCalibrationFactors() {
      this.loading = true;
      api.getCalibrationFactors(this.selectedCounter, this.selectedIsotope)
              .then((response) => {
                this.calibrationFactors = response.data;
                this.calibrationFactors.forEach((calibrationFactor) => {
                  // format display date
                  calibrationFactor.createdOn = moment(calibrationFactor.createdOn).format('DD-MM-YYYY, h:mm:ss');
                });
              })
              .catch((error) => {
                console.log(error);
                this.error = error.response.data.message;
              })
              .finally(() => {
                this.loading = false;
              })
    },
    getCalibrationFactorsGraph() {
      this.loading = true;
      api.getCalibrationFactorsGraph(this.selectedCounter, this.selectedIsotope)
              .then((response) => {
                this.traces = response.data;
                this.traces.forEach((trace) => {
                  trace[0].forEach((time, index) => {
                    trace[0][index] = moment(time).format('DD-MM-YYYY, h:mm:ss');
                  })
                })
              })
              .catch((error) => {
                console.log(error);
                this.errror = error.response.data.message;

              })
              .finally(() => {
                this.loading = false;
              })
    },
    getCounters: api.getCounters,
    getIsotopes: api.getIsotopes,
  },
  created() {
    this.getCounters()
            .then((response) => {
              this.counters = response.data
            })
            .catch((error) => {
              this.error = error.response.data.message
            })
            .finally(() => {
              this.loading = false;
            });
    this.getIsotopes()
            .then((response) => {
              this.isotopes = response.data
            })
            .catch((error) => {
              this.error = error.response.data.message
            })
            .finally(() => {
              this.loading = false;
            })

  }
}
</script>
