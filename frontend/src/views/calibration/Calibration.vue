<template>
  <div>
    <IsotopeModelSelect
    :isotopes="this.isotopes"
    :counters="this.counters"
    v-on:query = getCalibrationFactors></IsotopeModelSelect>
    <CalibrationTable :calibrationFactors="this.calibrationFactors"></CalibrationTable>
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
      calibrationFactors: []
    }
  },
  methods: {
    getCalibrationFactors() {
      api.getCalibrationFactors(store.getSelectedCounter(), store.getSelectedIsotope())
              .then((response) => {
                this.calibrationFactors = response.data;
                this.calibrationFactors.forEach((calibrationFactor) => {
                  console.log(moment(calibrationFactor.createdOn).format('DD-MM-YYYY, h:mm:ss'));
                  calibrationFactor.createdOn = moment(calibrationFactor.createdOn).format('DD-MM-YYYY, h:mm:ss')
                });
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
