<template>
    <div>
        <el-button type="primary" class="controls" @click="downloadMouseCsvFormat">Download Mouse Csv</el-button>
        <BiodiCsvUploadForm tips="Upload your completed mouse info file" @upload-file="handleUploadfile"
                        @remove-file="handleRemoveFile(gammaRun)"
        :fileList="mouseCsvs"></BiodiCsvUploadForm>
    </div>
</template>

<script>
    import MouseForm from "./MouseForm";
    import {mapActions, mapGetters} from "vuex";
    import * as types from '../../../store/modules/BiodiCsvUpload/BiodiCsvUploadTypes'
    import BiodiCsvUploadForm from "./BiodiCsvUploadForm";

    export default {
        name: "BiodiCsvMouseInfo",
        components: {BiodiCsvUploadForm, MouseForm},
        props: {
            mouseCsvs: Array,
            gammaRun: Number
        },

        methods: {
            ...mapActions({
                'downloadMouseCsvFormat': types.DOWNLOAD_MOUSE_CSV_FORMAT,
                'setMouseCsv': types.SET_MOUSE_CSV,
            }),

            handleUploadfile(fileList) {
                this.setMouseCsv({index: this.gammaRun, mouseCsv: fileList[0]})
            },

            handleRemoveFile(gammaRun) {
                this.setMouseCsv({index: gammaRun, mouseCsv: null})
            }
        },
    }
</script>

<style scoped>
    .controls {
        margin-top: 2%;
    }
</style>