<template>
    <div>
        <el-button type="primary" class="controls" @click="downloadOrganCsvFormat">Download Organ Csv</el-button>
        <BiodiCsvUploadForm tips="Upload your organ list"
                        @upload-file="handleUploadfile"
                        @remove-file="handleRemovefile"
                        :fileList="organCsvs"></BiodiCsvUploadForm>
    </div>
</template>

<script>
    import OrganForm from "./OrganForm";
    import BiodiCsvUploadForm from "./BiodiCsvUploadForm";
    import {mapActions, mapGetters} from "vuex";
    import * as types from "../../../store/modules/BiodiCsv/BiodiCsvUploadTypes"
    export default {
        name: "BiodiCsvOrganOrder",
        components: {BiodiCsvUploadForm, OrganForm},
        props: {
            organCsvs: Array
        },

        methods: {
            ...mapActions({
                'downloadOrganCsvFormat': types.DOWNLOAD_ORGAN_CSV_FORMAT,
                'setOrganCsvs': types.SET_ORGAN_CSVS,
            }),

            handleUploadfile(fileList) {
                this.setOrganCsvs({organCsvs: fileList})
            },

            handleRemovefile() {
                this.setOrganCsvs({organCsvs: []})
            },

        }
    }
</script>

<style scoped>
    .controls {
        margin-top: 2%;
    }
</style>