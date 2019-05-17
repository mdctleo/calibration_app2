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
    const converter = require('json-2-csv');
    const utils = require('util');
    const csv2jsonAsync = utils.promisify(converter.csv2json);
    export default {
        name: "Csv.vue",
        data () {
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
                    readFilePromises.push(this.readFile(file.raw))
                });

                Promise.all(readFilePromises)
                    .then((csvFiles) => {
                        return csvFiles.forEach((csvFile) => {
                            csv2jsonPromises.push(csv2jsonAsync(csvFile))
                        })
                    })
                    .then(() => {
                        return Promise.all(csv2jsonPromises)
                    })
                    .then((csvJsons) => {
                        return csvJsons.forEach((csvJson, index) => {
                            this.filesJson.push({
                              filename: this.files[index].name,
                              file: csvJson
                            })
                        })
                    })
                    .then(() => {
                        return api.postCsvFiles(this.filesJson)
                    })
                    .then((response) => {
                        console.log(response.data);
                        this.clearData();
                    })
                    .catch((error) => {
                        console.log(error);
                        this.$refs.upload.abort();
                    })
                    .finally(() => {
                        this.loading = false;
                    })
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

            clearData () {
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