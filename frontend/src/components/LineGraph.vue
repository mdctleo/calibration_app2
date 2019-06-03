<template>
    <div v-bind:id="this.graphId" class="graph" v-loading="this.loading">

    </div>

</template>

<script>
    import * as Plotly from "plotly.js";
    export default {
        name: "LineGraph",
        props: {
            graphId: String,
            graph: Object
        },
        data () {
            return {
                loading: false
            }
        },
        watch: {
            graph: function () {
                this.plot()
            }
        },
        methods: {
            plot () {
                this.loading = true;
                if (this.graph.layout !== undefined) {
                    Plotly.newPlot(this.graphId, this.graph.data, this.graph.layout);
                } else {
                    Plotly.newPlot(this.graphId, this.graph.data);
                }
                this.loading = false;
            }
        },

        mounted () {
            this.plot()
        }
    }
</script>

<style scoped>
    .graph {
        width: 90%;
        height: 100%;
        margin-left: auto;
        margin-right: auto;
        margin-top: 5%;
    }

</style>