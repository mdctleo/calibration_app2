<template>
    <div>
        <el-upload
                class="upload"
                drag
                action=""
                :auto-upload="false"
                :on-remove="handleRemove"
                :on-change="handleUpload"
                multiple
                ref="upload">
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">Drop file here or <em>click to upload</em></div>
            <div class="el-upload__tip" slot="tip">Drag your BioDi files here</div>
        </el-upload>
        <el-button type="success" class="upload-submit" @click="$emit('submit')">Submit</el-button>
    </div>
</template>

<script>
    import store from '../store/Store.js'
    import * as type from '../store/Types'

    export default {
        name: "BiodiCsvUpload",
        methods: {

            clearData() {
                store.dispatch({
                    type: type.setFiles,
                    files: []
                });
                this.$refs.upload.clearFiles();
            },

            handleRemove(file, fileList) {
                store.dispatch({
                    type: type.setFiles,
                    files: fileList
                });

            },
            handleUpload(file, fileList) {
                store.dispatch({
                    type: type.setFiles,
                    files: fileList
                });
            },
        }
    }


</script>

<style scoped>
    .upload {
        margin-top: 10px;
    }
    .upload-submit {
        margin-top: 10px;
    }

</style>