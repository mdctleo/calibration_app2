<template>
    <div>
        <el-upload
                class="upload"
                drag
                action=""
                :auto-upload="false"
                :on-remove="handleRemove"
                :on-change="handleUpload"
                ref="upload"
                :multiple="false">
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">Drop file here or <em>click to upload</em></div>
            <div class="el-upload__tip" slot="tip">{{tips}}</div>
        </el-upload>
    </div>
</template>

<script>
    export default {
        name: "BiodiCsvUpload",
        props: {
          tips: String
        },
        methods: {
            clearData() {
                this.$refs.upload.clearFiles();
            },

            handleRemove(file, fileList) {
                this.$emit('remove-file', fileList)
            },
            handleUpload(file, fileList) {
                this.$emit('upload-file', fileList)
            },
        }
    }


</script>

<style scoped>
    .upload {
        margin-top: 2%;
    }
    .upload-submit {
        margin-top: 10px;
    }

</style>