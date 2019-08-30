<template>
    <BiodiCsvUploadForm tips="Upload your Biodi Csv File"
                        @upload-file="handleUploadfile"
                        @remove-file="handleRemoveFile(gammaRun)"
                        :fileList="biodiCsvs"></BiodiCsvUploadForm>
</template>

<script>
    import BiodiCsvUploadForm from "./BiodiCsvUploadForm";
    import * as types from "../../../store/modules/BiodiCsvUpload/BiodiCsvUploadTypes"
    import {mapActions, mapGetters} from "vuex";

    export default {
        name: "BiodiCsvUpload",
        components: {BiodiCsvUploadForm},
        props: {
            biodiCsvs: Array,
            gammaRun: Number
        },

        methods: {
            ...mapActions({
                'setBiodiCsv': types.SET_BIODI_CSV,
            }),

            handleUploadfile(fileList) {
                this.setBiodiCsv({index: this.gammaRun, biodiCsv: fileList[0]})
            },

            handleRemoveFile(gammaRun) {
                this.setBiodiCsv({index: gammaRun, biodiCsv: null})
            }
        }

    }
</script>

<style scoped>

</style>