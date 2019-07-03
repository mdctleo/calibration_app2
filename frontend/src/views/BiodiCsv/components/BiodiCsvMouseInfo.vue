<template>
    <div>
        <el-button type="primary" class="controls" @click="downloadMouseCsvFormat">Download Mouse Csv</el-button>
        <BiodiCsvUploadForm tips="Upload your completed mouse info file" @upload-file="handleUploadfile"
                        @remove-file="handleRemovefile"></BiodiCsvUploadForm>
    </div>
</template>

<script>
    import MouseForm from "./MouseForm";
    import {mapActions, mapGetters} from "vuex";
    import * as types from '../../../store/modules/BiodiCsv/BiodiCsvUploadTypes'
    import BiodiCsvUploadForm from "./BiodiCsvUploadForm";

    export default {
        name: "BiodiCsvMouseInfo",
        components: {BiodiCsvUploadForm, MouseForm},
        props: {
            bus: Object
        },

        computed: {
            ...mapGetters({
                // startValidation: 'biodiCsvUpload/startValidation',
                mouseCsv: 'biodiCsvUpload/mouseCsv',
            })
        },

        // watch: {
        //     startValidation: function (val) {
        //         if (val === true) {
        //             this.handleStartValidation()
        //         }
        //     }
        // },

        methods: {
            ...mapActions({
                'downloadMouseCsvFormat': types.DOWNLOAD_MOUSE_CSV_FORMAT,
                // 'handleMouseCsvs': types.HANDLE_MOUSE_CSVS,
                'setMouseCsvs': types.SET_MOUSE_CSVS
            }),

            handleUploadfile(fileList) {
                this.setMouseCsvs({mouseCsvs: fileList})
            },

            handleRemovefile() {
                this.setMouseCsvs({mouseCsvs: null})
            },

            // handleStartValidation() {
            //     this.handleMouseCsv({mouseCsv: this.mouseCsv})
            //         .then((validated) => {
            //             if (validated) {
            //                 this.$emit('validated', true)
            //             } else {
            //                 this.$emit('validated', false);
            //             }
            //         })
            //         .catch((err) => {
            //             this.$emit('validated', false)
            //         });
            // }
        },
    }
</script>

<style scoped>
    .controls {
        margin-top: 2%;
    }
</style>