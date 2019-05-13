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
        <el-button @click="setState" type="success" class="button">Query</el-button>
    </div>
</template>

<script>
    import {store} from '../Store'
    export default {
        name: 'IsotopeModelSelect',
        props:{
            counters: Array,
            isotopes: Array
        },
        methods: {
            setState (event) {
                store.setSelectedCounter(this.selectedCounter);
                store.setSelectedIsotope(this.selectedIsotope);
                this.$emit('query');
            }
        },
        data() {
            return {
                selectedCounter: null,
                selectedIsotope: null
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
