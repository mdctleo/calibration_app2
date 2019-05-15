<template>
    <div id="calibrationGraph" class="calibrationGraph">

    </div>
    
</template>

<script>
    import * as Plotly from "plotly.js";
    export default {
        name: "CalibrationGraph",
        props: {
            traces: Array
        },
        methods: {
            plot () {
                var trace1 = {
                    x: this.time,
                    y: this.calibrationFactors,
                    mode: 'lines+markers'
                };

                var data = [ trace1 ];

                var layout = {
                    title:'Line and Scatter Plot'
                };

                Plotly.newPlot('calibrationGraph', data, layout);

            }

        },
        mounted() {
            this.plot();

        }
    }
</script>

<style scoped>
    .calibrationGraph {
        width: 90%;
        height: 100%;
        margin-left: auto;
        margin-right: auto;
        margin-top: 5%;
    }

</style>