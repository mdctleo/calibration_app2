<template>
    <div id="calibrationGraph" class="calibrationGraph" v-loading="this.loading">

    </div>
    
</template>

<script>
    import * as Plotly from "plotly.js";
    export default {
        name: "CalibrationGraph",
        props: {
            traces: Object
        },
        data () {
            return {
                loading: false
            }
        },
        watch: {
          traces: function () {
              console.log(this.traces);
              this.plot()
          }
        },
        methods: {
            plot () {
                this.loading = true;
                let data = [];
                Object.entries(this.traces).forEach((trace) => {
                    let isotopeName = trace[0];
                    let values = trace[1];
                    let traceFormat = {
                        x: values[0],
                        y: values[1],
                        mode: 'lines+markers',
                        name: isotopeName
                    };
                    data.push(traceFormat)
                });

                let layout = {
                    title:'Calibration Factor v.s. Time'
                };
                console.log(data);
                Plotly.newPlot('calibrationGraph', data, layout);
                this.loading = false;
            }
        },

        mounted () {
            this.plot()
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