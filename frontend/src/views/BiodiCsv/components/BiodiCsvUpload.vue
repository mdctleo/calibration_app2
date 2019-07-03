<template>
    <BiodiCsvUploadForm tips="Upload your Biodi Csv File"
                        @upload-file="handleUploadfile"
                        @remove-file="handleRemovefile"></BiodiCsvUploadForm>
</template>

<script>
    import BiodiCsvUploadForm from "./BiodiCsvUploadForm";
    import * as types from "../../../store/modules/BiodiCsv/BiodiCsvUploadTypes"
    import {mapActions, mapGetters} from "vuex";

    export default {
        name: "BiodiCsvUpload",
        components: {BiodiCsvUploadForm},
        computed: {
            ...mapGetters({
                biodiCsvs: 'biodiCsvUpload/biodiCsvs'
            })
        },

        methods: {
            ...mapActions({
                'setBiodiCsvs': types.SET_BIODI_CSVS,
            }),

            handleUploadfile(fileList) {
                this.setBiodiCsvs({biodiCsvs: fileList})
            },

            handleRemovefile() {
                this.setBiodiCsvs({biodiCsvs: null})

            },
        }

    }
</script>

<style scoped>

</style>