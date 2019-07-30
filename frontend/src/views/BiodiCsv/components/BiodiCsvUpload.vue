<template>
    <BiodiCsvUploadForm tips="Upload your Biodi Csv File"
                        @upload-file="handleUploadfile"
                        @remove-file="handleRemovefile"
                        :fileList="biodiCsvs"></BiodiCsvUploadForm>
</template>

<script>
    import BiodiCsvUploadForm from "./BiodiCsvUploadForm";
    import * as types from "../../../store/modules/BiodiCsv/BiodiCsvUploadTypes"
    import {mapActions, mapGetters} from "vuex";

    export default {
        name: "BiodiCsvUpload",
        components: {BiodiCsvUploadForm},
        props: {
            biodiCsvs: Array
        },

        methods: {
            ...mapActions({
                'setBiodiCsvs': types.SET_BIODI_CSVS,
            }),

            handleUploadfile(fileList) {
                this.setBiodiCsvs({biodiCsvs: fileList})
            },

            handleRemovefile() {
                this.setBiodiCsvs({biodiCsvs: []})

            },
        }

    }
</script>

<style scoped>

</style>