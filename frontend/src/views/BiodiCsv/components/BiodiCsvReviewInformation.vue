<template>
    <el-button type="success"@click="handleSubmit">Submit</el-button>
</template>

<script>
    import {mapActions, mapGetters} from "vuex";
    import * as types from "../../../store/modules/BiodiCsv/BiodiCsvUploadTypes"

    export default {
        name: "BiodiCsvReviewInformation",
        computed: {
            ...mapGetters({
                studyForm: "biodiCsvUpload/studyForm",
                gammaForm: "biodiCsvUpload/gammaForm",
                mouseCsvJson: "biodiCsvUpload/mouseCsvJson",
                selectedOrgans: "biodiCsvUpload/selectedOrgans",
                biodiCsvJson: "biodiCsvUpload/biodiCsvJson"
            })
        },

        methods: {
            ...mapActions({
                'postBiodiCsv': types.POST_BIODI_CSV
            }),

            handleSubmit() {
                let selectedOrgans = this.selectedOrgans(-1).map((organ) => {
                    return organ.value
                })
                this.postBiodiCsv({
                    biodiCsv: this.biodiCsvJson,
                    studyInfo: this.studyForm,
                    gammaInfo: this.gammaForm,
                    mouseInfo: this.mouseCsvJson,
                    organInfo: selectedOrgans})
            }
        }
    }
</script>

<style scoped>

</style>