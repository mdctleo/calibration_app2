<template>
    <div>
        <el-steps :active="step" align-center class="stepper" finish-status="success">
            <el-step title="Step 1" description="Study Info"></el-step>
            <el-step title="Step 2" description="Gamma Counter Info"></el-step>
            <el-step title="Step 3" description="Mouse Info"></el-step>
            <el-step title="Step 4" description="Organ Order"></el-step>
            <el-step title="Step 5" description="Upload Csv"></el-step>
            <el-step title="Step 6" description="Review Info"></el-step>
        </el-steps>
        <BiodiCsvStudyInformation @validated="moveNext" :bus="bus" v-if="step === 0"></BiodiCsvStudyInformation>
        <BiodiCsvGammaCounterInformation @validated="moveNext" :bus="bus" v-if="step === 1"></BiodiCsvGammaCounterInformation>
        <BiodiCsvMouseInfo @validated="moveNext" :bus="bus" v-if="step === 2"></BiodiCsvMouseInfo>
        <BiodiCsvTubeInformation v-if="step === 3"></BiodiCsvTubeInformation>
        <BiodiCsvUpload v-if="step === 4"></BiodiCsvUpload>
        <el-button @click="handleNext" class="next">Next</el-button>
        <el-button @click="handlePrevious" class="previous">Previous</el-button>
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
                bus: new Vue()
            }
        },
        methods: {
            handleNext() {
                this.bus.$emit('startValidation');
            },

            moveNext() {
                this.step++;

            },

            handlePrevious() {
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