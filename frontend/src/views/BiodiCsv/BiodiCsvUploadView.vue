<template>
    <div>
        <el-steps :active="step" align-center class="stepper" finish-status="success">
            <el-step title="Step 1" description="Study Info"></el-step>
            <el-step title="Step 2" description="Gamma Counter Info"></el-step>
            <el-step title="Step 3" description="Review Info"></el-step>
        </el-steps>
        <el-alert
                v-show="error"
                :title="error"
                type="error"
                show-icon
                @close="setError({error: null})">
        </el-alert>
        <BiodiCsvStudyInformation @validated="moveNext" v-if="step === 0"></BiodiCsvStudyInformation>
        <BiodiCsvGammaCounterInformation
                @validated="addValidation"
                v-for="i in numGammaRuns"
                v-if="step === 1"
                v-bind:gamma-run="i - 1"
                v-bind:index="i"
                v-bind:key="i"
        ></BiodiCsvGammaCounterInformation>
<!--        <BiodiCsvGammaCounterInformation @validated="moveNext" v-if="step === 1"></BiodiCsvGammaCounterInformation>-->
        <BiodiCsvReviewInformation v-if="step === 2"></BiodiCsvReviewInformation>
        <el-button @click="handleNext" class="next">Next</el-button>
        <el-button @click="handlePrevious" class="previous" v-if="this.step !== 0">Previous</el-button>
    </div>
</template>

<script>
    import BiodiCsvStudyInformation from "./components/BiodiCsvStudyInformation";
    import BiodiCsvMouseInfo from "./components/BiodiCsvMouseInfo";
    import BiodiCsvGammaCounterInformation from "./components/BiodiCsvGammaCounterInformation";
    import BiodiCsvUpload from "./components/BiodiCsvUpload";
    import BiodiCsvReviewInformation from "./components/BiodiCsvReviewInformation";
    import BiodiCsvTubeInformation from './components/BiodiCsvOrganOrder'
    import Vue from "vue";
    import {mapActions, mapGetters} from "vuex";
    import * as types from '../../store/modules/BiodiCsvUpload/BiodiCsvUploadTypes.js'

    export default {
        name: "BiodiCsvUploadView",
        components: {
            BiodiCsvTubeInformation,
            BiodiCsvReviewInformation,
            BiodiCsvUpload, BiodiCsvGammaCounterInformation, BiodiCsvMouseInfo, BiodiCsvStudyInformation
        },
        data() {
            return {
                step: 0,
                validationCount: 0
            }
        },
        computed: {
            ...mapGetters({
                error: 'biodiCsvUpload/error',
                numGammaRuns: 'biodiCsvUpload/numGammaRuns'
            })
        },
        methods: {
            ...mapActions({
                'setStartValidation': types.SET_START_VALIDATION,
                'setError': types.SET_ERROR
            }),
            handleNext() {
                this.setStartValidation({startValidation: true})
            },

            addValidation() {
                this.validationCount = this.validationCount + 1
                console.log("validation count: " + this.validationCount)
                if (this.validationCount === this.numGammaRuns) {
                    console.log("before move next")
                    this.moveNext(true)
                }
            },

            moveNext(validated) {
                this.setStartValidation({startValidation: false});
                if (validated) {
                    this.step++;
                    this.validationCount = 0
                }
            },

            handlePrevious() {
                this.setStartValidation({startValidation: false});
                this.step--;
            }
        }
    }
</script>

<style scoped>
    .stepper {
        margin-top: 2%;
    }

    .next {
        margin-right: 5%;
        margin-bottom: 2%;
        float: right;
    }

    .previous {
        margin-left: 5%;
        margin-bottom: 2%;
        float: left;
    }
</style>