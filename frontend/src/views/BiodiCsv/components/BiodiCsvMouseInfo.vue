<template>
    <div>
        <el-button type="primary" class="controls" @click="downloadMouseCsvFormat">Download Mouse Csv</el-button>
        <BiodiCsvUploadForm tips="Upload your completed mouse info file" @upload-file="handleUploadfile"
                        @remove-file="handleRemovefile"
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
            mouseCsvs: Array
        },

        methods: {
            ...mapActions({
                'downloadMouseCsvFormat': types.DOWNLOAD_MOUSE_CSV_FORMAT,
                'setMouseCsvs': types.SET_MOUSE_CSVS
            }),

            handleUploadfile(fileList) {
                this.setMouseCsvs({mouseCsvs: fileList})
            },

            handleRemovefile() {
                this.setMouseCsvs({mouseCsvs: []})
            },
        },
    }
</script>

<style scoped>
    .controls {
        margin-top: 2%;
    }
</style>