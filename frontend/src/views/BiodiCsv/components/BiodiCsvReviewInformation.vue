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
            }),

            handleSubmit() {
                this.postBiodiCsv({studyInfo: this.studyForm,
                                       gammaInfo: this.gammaForm,
                                       biodiCsvs: this.biodiCsvs,
                                       mouseCsvs: this.mouseCsvs,
                                       organCsvs: this.organCsvs })
            }
        }
    }
</script>

<style scoped>

</style>