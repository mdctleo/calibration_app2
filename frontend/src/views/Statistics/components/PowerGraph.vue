<template>
    <div id="PowerGraph" class="power-graph" v-loading="this.loading">
    </div>
</template>

<script>
    import * as Plotly from "plotly.js";
    export default {
        name: "PowerGraph",
        data () {
            return {
                loading: false
            }
        },
        props: {
            graph: Object
        },
        watch: {
            graph: function () {
                this.plot()
            }
        },
        methods: {
            plot () {
                this.loading = true;
                Plotly.newPlot('PowerGraph', this.graph.data, this.graph.layout);
                this.loading = false;
            }
        },

        mounted () {
            this.plot()
        }

    }
</script>

<style scoped>
    .power-graph {
        width: 90%;
        height: 100%;
        margin-left: auto;
        margin-right: auto;
        margin-top: 5%;
    }
</style>