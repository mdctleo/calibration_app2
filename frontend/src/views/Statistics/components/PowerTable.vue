<template>
    <div id="PowerTable" class="el-table"></div>
</template>

<script>
    import * as Plotly from "plotly.js";
    export default {
        name: "PowerTable",
        props: {
            table: Array
        },
        watch: {
            table: function () {
                this.plot()
            }
        },
        methods: {
            plot () {
                this.loading = true;
                Plotly.newPlot('PowerTable', this.table);
                this.loading = false;
            }
        },

        mounted () {
            this.plot()
        }
    }
</script>

<style scoped>
    .el-table {
        width: 90%;
        margin: 5% auto;
    }
    .el-table.el-table-column{
        width: 100%;
    }

</style>