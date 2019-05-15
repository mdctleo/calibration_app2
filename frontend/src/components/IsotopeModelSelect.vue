<template>
    <div>
        <el-select v-model="selectedIsotope" clearable placeholder="Select Isotope" class="select">
            <el-option
                    v-for="item in isotopes"
                    :key="item.isotopeName"
                    :label="item.isotopeName"
                    :value="item.isotopeName">
            </el-option>
        </el-select>
        <el-select v-model="selectedCounter" clearable placeholder="Select Model" class="select">
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
    import store from '../store/Store.js'
    import * as type from '../store/Types'

    export default {
        name: 'IsotopeModelSelect',
        props:{
            counters: Array,
            isotopes: Array
        },
        computed: {
            selectedIsotope: {
                get () {
                    return store.state.selectedIsotope
                },
                set (value) {
                    store.dispatch({
                        type: type.setSelectedIsotope,
                        selectedIsotope: value
                    })
                }
            },

            selectedCounter: {
                get () {
                    return store.state.selectedCounter
                },
                set (value) {
                    store.dispatch({
                        type: type.setSelectedCounter,
                        selectedCounter: value
                    })
                }
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
