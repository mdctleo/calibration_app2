<template>
    <div>
        <el-upload
                class="upload-demo"
                drag
                action=""
                :auto-upload="false"
                :on-remove="handleRemove"
                :on-change="handleUpload"
                multiple
                ref="upload"
                v-loading="loading">
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">Drop file here or <em>click to upload</em></div>
            <div class="el-upload__tip" slot="tip">Drag your BioDi files here</div>
        </el-upload>
        <el-button type="success" class="upload-submit" @click="handleSubmit">Submit</el-button>
    </div>
</template>

<script>
    import * as api from '../../api/CalibrationAPI'

    const csv = require('csvtojson');
    export default {
        name: "Csv.vue",
        data() {
            return {
                files: [],
                filesJson: [],
                loading: false
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

                        return api.postCsvFiles(this.filesJson)
                    })
                    .then((response) => {
                        console.log(response.data);
                        this.clearData();
                    })
                    .catch((error) => {
                        console.log(error.response.data.message);
                        this.$refs.upload.abort();
                    })
                    .finally(() => {
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

            clearData() {
                this.files = [];
                this.filesJson = [];
                this.$refs.upload.clearFiles();
            },

            handleRemove(file, fileList) {
                this.files = fileList

            },
            handleUpload(file, fileList) {
                this.files = fileList;
            },
        }
    }
</script>

<style scoped>
    .upload-submit {
        margin-top: 10px;
    }

</style>