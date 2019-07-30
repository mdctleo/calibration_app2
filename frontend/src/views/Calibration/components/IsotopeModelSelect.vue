<template>
    <div>
        <el-select v-model="selectedIsotope" clearable placeholder="Select Isotope" class="select"
        @clear="handleIsotopeClear()">
            <el-option
                    v-for="item in isotopes"
                    :key="item.isotopeName"
                    :label="item.isotopeName"
                    :value="item.isotopeName">
            </el-option>
        </el-select>
        <el-select v-model="selectedCounter" clearable placeholder="Select Model" class="select" @clear="handleCounterClear()">
            <el-option
                    v-for="item in counters"
                    :key="item.model"
                    :label="item.model"
                    :value="item.model">
            </el-option>
        </el-select>
        <el-button @click="$emit('query')" type="success" class="button">Query</el-button>
    </div>
</template>

<script>
    import * as types from '../../../store/modules/Calibration/types'
    import {mapState, mapGetters} from 'vuex';


    export default {
        name: 'IsotopeModelSelect',
        props:{
            counters: Array,
            isotopes: Array
        },
        computed: {
            selectedIsotope: {
                get () {
                    return this.$store.state.calibration.selectedIsotope
                },
                set (value) {
                    this.$store.dispatch({
                        type: types.SET_SELECTED_ISOTOPE,
                        selectedIsotope: value
                    })
                }
            },

            selectedCounter: {
                get () {
                    return this.$store.state.calibration.selectedCounter
                },
                set (value) {
                    this.$store.dispatch({
                        type: types.SET_SELECTED_COUNTER,
                        selectedCounter: value
                    })
                }
            }
        },

        methods: {
            handleIsotopeClear() {
                this.selectedIsotope = null;
            },

            handleCounterClear() {
                this.selectedCounter = null;
            }
        }
    }
</script>

<style scoped>
    .select {
        padding: 15px;
    }
    .button{
    }
</style>
