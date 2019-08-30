<template>
    <div>
        <el-button type="primary" class="controls" @click="downloadOrganCsvFormat">Download Organ Csv</el-button>
        <BiodiCsvUploadForm tips="Upload your organ list"
                        @upload-file="handleUploadFile"
                        @remove-file="handleRemoveFile(gammaRun)"
                        :fileList="organCsvs"></BiodiCsvUploadForm>
    </div>
</template>

<script>
    import OrganForm from "./OrganForm";
    import BiodiCsvUploadForm from "./BiodiCsvUploadForm";
    import {mapActions, mapGetters} from "vuex";
    import * as types from "../../../store/modules/BiodiCsvUpload/BiodiCsvUploadTypes"
    export default {
        name: "BiodiCsvOrganOrder",
        components: {BiodiCsvUploadForm, OrganForm},
        props: {
            organCsvs: Array,
            gammaRun: Number
        },

        methods: {
            ...mapActions({
                'downloadOrganCsvFormat': types.DOWNLOAD_ORGAN_CSV_FORMAT,
                'setOrganCsv': types.SET_ORGAN_CSV,
            }),

            handleUploadFile(fileList) {
                this.setOrganCsv({index: this.gammaRun, organCsv: fileList[0]})
            },

            handleRemoveFile(gammaRun) {
                this.setOrganCsv({index: gammaRun, organCsv: null})
            }
        }
    }
</script>

<style scoped>
    .controls {
        margin-top: 2%;
    }
</style>