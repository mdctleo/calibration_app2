<template>
    <div>
        <el-upload
                class="upload-demo"
                drag
                action=""
                :auto-upload="false"
                :on-remove="handleRemove"
                :on-change="handleUpload"
                multiple>
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">Drop file here or <em>click to upload</em></div>
            <div class="el-upload__tip" slot="tip">Drag your BioDi files here</div>
        </el-upload>
        <el-button type="success" class="upload-submit" @click="handleSubmit">Submit</el-button>
    </div>
</template>

<script>
    import * as api from '../../api/CalibrationAPI'
    export default {
        name: "Csv.vue",
        data () {
          return {
              files: [],
          }
        },
        methods: {
            handleSubmit() {
                api.postCsvFiles(this.files)
                    .then((response) => {
                        console.log(response.data)

                    })
                    .catch((error) => {
                        console.log(error)
                    })

            },

            handleRemove(file, fileList) {
                this.files = fileList

            },
            handleUpload(file, fileList) {
                this.files = fileList;
            }
        }
    }
</script>

<style scoped>
    .upload-submit {
        margin-top: 10px;
    }

</style>