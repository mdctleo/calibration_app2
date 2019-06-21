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
                startValidation: 'biodiCsvUpload/startValidation',
                biodiCsvs: 'biodiCsvUpload/biodiCsvs'
            })
        },
        watch: {
            startValidation: function (val) {
                console.log('saw starValidation change')
                if (val === true) {
                    this.handleStartValidation()
                }
            }
        },
        methods: {
            ...mapActions({
                'setBiodiCsv': types.SET_BIODI_CSV,
                'handleBiodiCsv': types.HANDLE_BIODI_CSV
            }),

            handleUploadfile(fileList) {
                this.setBiodiCsv({biodiCsvs: fileList})
            },

            handleRemovefile() {
                this.setBiodiCsv({biodiCsvs: null})

            },

            handleStartValidation() {
                // TODO: Add in front end validationa and refactor the other two csvs validate -> handle logic
                this.handleBiodiCsv({biodiCsvs: this.biodiCsvs})
                this.$emit('validated', true)
                console.log("got here")
            }
        }

    }
</script>

<style scoped>

</style>