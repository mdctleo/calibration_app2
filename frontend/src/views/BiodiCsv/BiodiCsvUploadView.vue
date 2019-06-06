<template>
    <div>
        <el-steps :active="step" align-center class="stepper" finish-status="success">
            <el-step title="Step 1" description="Study Info"></el-step>
            <el-step title="Step 2" description="Gamma Counter Info"></el-step>
            <el-step title="Step 3" description="Mouse Info"></el-step>
            <el-step title="Step 4" description="Upload Csv"></el-step>
            <el-step title="Step 5" description="Review Information"></el-step>
        </el-steps>
        <BiodiCsvStudyInformation v-if="step === 0"></BiodiCsvStudyInformation>
        <BiodiCsvGammaCounterInformation v-if="step === 1"></BiodiCsvGammaCounterInformation>
        <BiodiCsvMouseInfo v-if="step === 2"></BiodiCsvMouseInfo>
        <BiodiCsvUpload v-if="step === 3"></BiodiCsvUpload>
        <BiodiCsvReviewInformation v-if="step === 4"></BiodiCsvReviewInformation>
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

    export default {
        name: "BiodiCsvUploadView",
        components: {
            BiodiCsvReviewInformation,
            BiodiCsvUpload, BiodiCsvGammaCounterInformation, BiodiCsvMouseInfo, BiodiCsvStudyInformation
        },
        data() {
            return {
                step: 0
            }
        },
        methods: {
            handleNext() {
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
        float: right;
    }

    .previous {
        margin-left: 5%;
        float: left;
    }
</style>