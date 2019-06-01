<template>
    <div>
        <el-row>
            <el-alert
                    v-show="error"
                    :title="error"
                    type="error"
                    show-icon
                    @close="setError({error: null})">
            </el-alert>
        </el-row>
        <StatisticsFormBase label0="Effect" label1="Power" v-on:submit="handleSubmit"></StatisticsFormBase>
        <el-row>
            <span class="result" v-show="this.result !== null">{{'Number of Observations is :' + this.result}}</span>
        </el-row>
    </div>
</template>

<script>
    import StatisticsFormBase from "./components/StatisticsFormBase";
    import * as types from '../../store/modules/Statistics/types'
    import {mapActions, mapGetters} from 'vuex';

    export default {
        name: "Nobs",
        components: {StatisticsFormBase},
        computed: {
            ...mapGetters({
                input0: 'input0',
                input1: 'input1',
                alpha: 'alpha',
                test: 'test',
                alternative: 'alternative',
                loading: 'statisticsLoading',
                error: 'statisticsError',
                result: 'result'
            })
        },
        methods: {
            ...mapActions([
                types.CALCULATE_NOBS,
                types.SET_ERROR
            ]),
            handleSubmit() {
                let statisticForm = {
                    effect: this.input0,
                    power: this.input1,
                    alpha: this.alpha,
                    test: this.test,
                    alternative: this.alternative
                };
                this.calculateNobs({statisticForm: statisticForm})
            }
        }
    }
</script>

<style scoped>
    .result {
        margin-top: 100px;
    }
</style>