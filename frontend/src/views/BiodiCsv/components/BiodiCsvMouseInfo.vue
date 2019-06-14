<template>
    <div>
        <el-button type="primary" @click="downloadMouseCsvFormat">Download Csv Format</el-button>
        <BiodiCsvUpload tips="Upload your completed mouse info file" @upload-file="handleUploadfile"
                        @remove-file="handleRemovefile"></BiodiCsvUpload>
    </div>
</template>

<script>
    import MouseForm from "./MouseForm";
    import {mapActions, mapGetters} from "vuex";
    import * as types from '../../../store/modules/BiodiCsv/types'
    import BiodiCsvUpload from "./BiodiCsvUpload";

    export default {
        name: "BiodiCsvMouseInfo",
        components: {BiodiCsvUpload, MouseForm},
        props: {
            bus: Object
        },

        computed: {
            ...mapGetters({
                startValidation: 'biodiCsvUpload/startValidation',
                mouseCsv: 'biodiCsvUpload/mouseCsv'
            })
        },

        watch: {
            startValidation: function (val) {
                if (val === true) {
                    this.handleStartValidation()
                }
            }
        },

        methods: {
            ...mapActions({
                'downloadMouseCsvFormat': types.DOWNLOAD_MOUSE_CSV_FORMAT,
                'handleMouseCsv': types.HANDLE_MOUSE_CSV,
                'setMouseCsv': types.SET_MOUSE_CSV
            }),

            handleUploadfile(fileList) {
                this.setMouseCsv({mouseCsv: fileList})
            },

            handleRemovefile() {
                this.setMouseCsv({mouseCsv: null})
            },

            handleStartValidation() {
                this.handleMouseCsv({mouseCsv: this.mouseCsv})
                    .then((validated) => {
                        if (validated) {
                            console.log("mouse forms validated");
                            this.$emit('validated', true)
                        } else {
                            console.log("mouse forms not validated");
                            this.$emit('validated', false);
                        }
                    })
                    .catch((err) => {
                        this.$emit('validated', false)
                    });
            }
        },
    }
</script>

<style scoped>
    .controls {
        margin-top: 2%;
        margin-bottom: 2%;
    }
</style>