<template>
    <div v-loading="this.loading">
        <el-alert
                v-show="error"
                :title="error"
                type="error"
                show-icon
                @close="error = null">
        </el-alert>
        <BiodiCsvUpload v-on:submit="handleSubmit" ref="upload"></BiodiCsvUpload>
        <BiodiCsvDownload :metas="this.metas" @download="downloadBiodiCsvs"></BiodiCsvDownload>
    </div>
</template>

<script>
    import * as api from '../../api/CalibrationAPI'
    import BiodiCsvUpload from "../../components/BiodiCsvUpload";
    import store from '../../store/Store.js'
    import BiodiCsvDownload from "../../components/BiodiCsvDownload";
    import {getBiodiCsvMetas} from "../../api/CalibrationAPI";

    const moment = require('moment');
    const csv = require('csvtojson');
    export default {
        name: "BiodiCsv.vue",
        components: {BiodiCsvDownload, BiodiCsvUpload},
        data() {
            return {
                filesJson: [],
                loading: false,
                metas: [],
                error: null
            }
        },
        computed: {
            files: {
                get () {
                    return store.state.files
                }
            }
        },
        methods: {

            handleSubmit() {
                this.loading = true;
                let csv2jsonPromises = [];
                let readFilePromises = [];
                this.files.forEach((file) => {
                    // read uploaded file data
                    readFilePromises.push(this.readFile(file.raw))
                });

                Promise.all(readFilePromises)
                    .then((csvFiles) => {
                        // transform each csv file to json
                        csvFiles.forEach((csvFile) => {
                            csv2jsonPromises.push(csv().fromString(csvFile))
                        });

                        return Promise.all(csv2jsonPromises);
                    })
                    .then((csvJsonFiles) => {
                        // replace explicit protocol names and create json to send
                        csvJsonFiles.forEach((csvJsonFile, index) => {
                            csvJsonFile.forEach((csvRow) => {
                                this.replaceProtocolKey(csvRow);
                            });
                            this.filesJson.push({
                                fileName: this.files[index].name,
                                file: csvJsonFile
                            })
                        });

                        return api.postBiodiCsvFiles(this.filesJson)
                    })
                    .then((response) => {
                        console.log(response.data);
                    })
                    .catch((error) => {
                        this.error = error.data.response.message;
                    })
                    .finally(() => {
                        this.$refs.upload.clearData();
                        this.filesJson =[];
                        this.loading = false;
                    })
            },

            replaceProtocolKey(csvRow) {
                let protocolName = csvRow['Protocol name'];
                let oldCountKey = protocolName + ' Counts';
                let oldCPMKey = protocolName + ' CPM';
                let oldErrorKey = protocolName + ' Error %';
                let oldInfoKey = protocolName + ' Info';

                csvRow['Counts'] = csvRow[oldCountKey];
                csvRow['CPM'] = csvRow[oldCPMKey];
                csvRow['Error %'] = csvRow[oldErrorKey];
                csvRow['Info'] = csvRow[oldInfoKey];

                delete csvRow[oldCountKey];
                delete csvRow[oldCPMKey];
                delete csvRow[oldErrorKey];
                delete csvRow[oldInfoKey];
                delete csvRow['Protocol name'];
            },


            readFile(file) {
                return new Promise((resolve, reject) => {
                    let fileReader = new FileReader();

                    fileReader.onerror = () => {
                        fileReader.abort();
                        reject("Something went wrong");
                    };

                    fileReader.onload = () => {
                        resolve(fileReader.result);
                    };

                    fileReader.readAsText(file)
                })
            },
            getBiodiCsvMetas() {
                this.loading = true;
                api.getBiodiCsvMetas()
                    .then((response) => {
                        response.data.forEach((meta) => {
                            meta.createdOn = moment(meta.createdOn).format('DD-MM-YYYY, h:mm:ss');
                        });
                        this.metas = response.data;
                    })
                    .catch((error) => {
                        this.error = error.data.response.message

                    })
                    .finally(() => {
                        this.loading = false;
                    })
            },

            downloadBiodiCsvs() {
                this.loading = true;
                api.getBiodiCsvs()
                    .then((response) => {
                        console.log(response.data);
                    })
                    .catch((error) => {
                        this.error = error.response.data.message;
                    })
                    .finally(() => {
                        this.loading = false;
                    })

            }
        },

        created() {
            this.getBiodiCsvMetas();
        }
    }
</script>

<style scoped>

</style>