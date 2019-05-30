<template>
    <div>
        <StatisticsFormBase label0="Number of Observation" label1="Power" v-on:submit="handleSubmit"></StatisticsFormBase>
    </div>
</template>

<script>
    import StatisticsFormBase from "./components/StatisticsFormBase";

    export default {
        name: "Effect",
        components: {StatisticsFormBase},
        methods: {
            handleSubmit() {}

        }
    }
</script>

<style scoped>

</style>