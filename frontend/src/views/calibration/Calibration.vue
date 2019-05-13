<template>
  <div>
    <IsotopeModelSelect
    :isotopes="this.isotopes"
    :counters="this.counters"
    v-on:query = getCalibrationFactors></IsotopeModelSelect>
    <CalibrationTable :calibrationFactors="this.calibrationFactors"
      :loading="this.loading"></CalibrationTable>
  </div>
</template>

<script>
// @ is an alias to /src
import CalibrationTable from '@/components/CalibrationTable.vue'
import IsotopeModelSelect from '@/components/IsotopeModelSelect.vue'
// import {getCalibrationFactors, getIsotopes, getCounters} from "./Controller";
import * as api from '../../api/CalibrationAPI'
import {store} from '../../Store'
const moment = require('moment');


export default {
  name: 'home',
  components: {
    CalibrationTable,
    IsotopeModelSelect
  },
  data () {
    return {
      counters:  [],
      isotopes: [],
      calibrationFactors: [],
      loading: false
    }
  },
  methods: {
    getCalibrationFactors() {
      this.loading = true;
      api.getCalibrationFactors(store.getSelectedCounter(), store.getSelectedIsotope())
              .then((response) => {
                this.calibrationFactors = response.data;
                this.calibrationFactors.forEach((calibrationFactor) => {
                  calibrationFactor.createdOn = moment(calibrationFactor.createdOn).format('DD-MM-YYYY, h:mm:ss')
                });
                console.log(this.calibrationFactors);
                this.loading = false;
              })
              .catch((error) => {
                console.log(error)
              })
    },
    getCounters: api.getCounters,
    getIsotopes: api.getIsotopes
  },
  created() {
    this.getCounters()
            .then((response) => {
              this.counters = response.data
            })
            .catch((error) => {
              console.log(error)
            });
    this.getIsotopes()
            .then((response) => {
              this.isotopes = response.data
            })
            .catch((error) => {
              console.log(error)
            });

  }
}
</script>
