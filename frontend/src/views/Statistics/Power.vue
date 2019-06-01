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
            <PowerGraph :graph="powerGraph"></PowerGraph>
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
    import PowerGraph from "./components/PowerGraph";
    import PowerTable from "./components/PowerTable";

    export default {
        name: "Power",
        components: {PowerTable, PowerGraph, StatisticsFormBase},
        computed: {
            ...mapGetters({
                input0: 'input0',
                input1: 'input1',
                alpha: 'alpha',
                test: 'test',
                alternative: 'alternative',
                loading: 'statisticsLoading',
                error: 'statisticsError',
                result: 'result',
                powerGraph: 'powerGraph',
                powerTable: 'powerTable'
            })
        },
        methods: {
            ...mapActions([
                types.CALCULATE_POWER,
                types.SET_ERROR,
                types.GET_POWER_GRAPH,
                types.GET_POWER_TABLE
            ]),
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