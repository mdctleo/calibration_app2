<template>
    <el-table
            class="el-table"
            id="table"
            v-loading="this.loading"
            :data="this.calibrationFactors"
            stripe>
        <el-table-column
                class="el-table-column"
                fixed
                prop="createdOn"
                label="Date"
                width="width: 100%">
        </el-table-column>
        <el-table-column
                class="el-table-column"
                fixed
                prop="isotopeName"
                label="Isotope Name"
                width="width: 100%">
        </el-table-column>
        <el-table-column
                class="el-table-column"
                prop="factor"
                label="Calibration Factor"
                width="width: 100%">
        </el-table-column>
        <el-table-column
                class="el-table-column"
                prop="gammaCounter"
                label="Gamma Counter"
                width="width: 100%">
        </el-table-column>
        <el-table-column
                class="el-table-column"
                prop="createdBy"
                label="Created By"
                width="width: 100%">
        </el-table-column>
    </el-table>
</template>

<script>
    export default {
        name: 'CalibrationTable',
        props: {
          calibrationFactors: Array,
          loading: Boolean
        }
    }
</script>

<style scoped>
    .el-table {
        width: 90%;
        height: 100%;
        margin-left: auto;
        margin-right: auto;
        margin-top: 5%;
    }
    .el-table-column{
        width: 100%;
    }
</style>