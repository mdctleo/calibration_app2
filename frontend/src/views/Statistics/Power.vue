<template>
    <div v-loading="loading">
        <el-row>
            <el-alert
                    v-show="error"
                    :title="error"
                    type="error"
                    show-icon
                    @close="setError({error: null})">
            </el-alert>
        </el-row>
        <StatisticsFormBase label0="Effect" label1="Number of Observation" v-on:submit="handleSubmit"></StatisticsFormBase>
        <el-row>
            <span class="result" v-show="this.result !== null">{{'Power is :' + this.result}}</span>
        </el-row>
        <el-row>
            <LineGraph graph-id="PowerGraph" :graph="powerGraph"></LineGraph>
        </el-row>
        <el-row>
            <PowerTable :table="powerTable"></PowerTable>
        </el-row>
    </div>
</template>

<script>
    import StatisticsFormBase from "./components/StatisticsFormBase";
    import * as types from '../../store/modules/Statistics/types'
    import {mapActions, mapGetters} from 'vuex';
    import PowerTable from "./components/PowerTable";
    import LineGraph from "../../components/LineGraph";

    export default {
        name: "Power",
        components: {LineGraph, PowerTable, StatisticsFormBase},
        computed: {
            ...mapGetters({
                input0: 'statistics/input0',
                input1: 'statistics/input1',
                alpha: 'statistics/alpha',
                test: 'statistics/test',
                alternative: 'statistics/alternative',
                loading: 'statistics/loading',
                error: 'statistics/error',
                result: 'statistics/result',
                powerGraph: 'statistics/powerGraph',
                powerTable: 'statistics/powerTable'
            })
        },
        methods: {
            ...mapActions({
                'calculatePower': types.CALCULATE_POWER,
                'setError': types.SET_ERROR,
                'getPowerGraph': types.GET_POWER_GRAPH,
                'getPowerTable': types.GET_POWER_TABLE
            }),
            handleSubmit() {
                let statisticForm = {
                    effect: this.input0,
                    nobs: this.input1,
                    alpha: this.alpha,
                    test: this.test,
                    alternative: this.alternative
                };
                this.calculatePower({statisticForm: statisticForm});
                this.getPowerGraph({statisticForm: statisticForm});
                this.getPowerTable({statisticForm: statisticForm});
            }
        }
    }
</script>

<style scoped>
    .result {
        margin-top: 100px;
    }
</style>