<template>
    <div>
        <component
                v-for="gammaForm in gammaForms"
                :key="gammaForm.key"
                :is="gammaForm.type"
                v-bind="gammaForm"
        >
        </component>
        <el-row class="controls">
            <el-col :span="12" :offset="6">
                <el-button type="primary" @click="addCounter">New Counter</el-button>
                <el-button type="danger" @click="removeCounter">Remove Counter</el-button>
            </el-col>
        </el-row>
    </div>
</template>

<script>
    import GammaCounterForm from "./GammaCounterForm";

    export default {
        name: "BiodiCsvGammaCounterInformation",
        components: {GammaCounterForm},
        data() {
            return {
                gammaForms: [],
                index: 0
            }
        },

        methods: {
            addCounter() {
                this.gammaForms.push({
                    key: this.index,
                    label: this.index,
                    type: 'GammaCounterForm'
                });
                this.index++;
            },

            removeCounter() {
                this.gammaForms.pop();
                this.index--;
            }
        }
    }
</script>

<style scoped>
    .controls {
        margin-top: 2%;
    }


</style>