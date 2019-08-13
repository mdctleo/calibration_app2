<template>
    <el-button type="success"@click="handleSubmit">Submit</el-button>
</template>

<script>
    import {mapActions, mapGetters} from "vuex";
    import * as types from "../../../store/modules/BiodiCsvUpload/BiodiCsvUploadTypes"

    export default {
        name: "BiodiCsvReviewInformation",
        computed: {
            ...mapGetters({
                studyForm: "biodiCsvUpload/studyForm",
                gammaForm: "biodiCsvUpload/gammaForm",
                biodiCsvs: "biodiCsvUpload/biodiCsvs",
                mouseCsvs: "biodiCsvUpload/mouseCsvs",
                organCsvs: "biodiCsvUpload/organCsvs",
                biodiCsvFile: "biodiCsvUpload/biodiCsvFile",
                mouseCsvJson: "biodiCsvUpload/mouseCsvJson",
                organCsvJson: "biodiCsvUpload/organCsvJson",
                biodiCsvJson: "biodiCsvUpload/biodiCsvJson"
            })
        },

        methods: {
            ...mapActions({
                'postBiodiCsv': types.POST_BIODI_CSV,
                'postBiodiCsvTest': types.POST_BIODI_CSV_TEST
            }),

            handleSubmit() {
                console.log(this.biodiCsvFile)
                this.postBiodiCsvTest({biodiCsv: this.biodiCsvFile,
                                       mouseCsv: this.mouseCsvs[0].raw,
                                       organCsv: this.organCsvs[0].raw })
                // this.postBiodiCsv({
                //     biodiCsv: this.biodiCsvJson,
                //     studyInfo: this.studyForm,
                //     gammaInfo: this.gammaForm,
                //     mouseInfo: this.mouseCsvJson,
                //     organInfo: this.organCsvJson})
            }
        }
    }
</script>

<style scoped>

</style>