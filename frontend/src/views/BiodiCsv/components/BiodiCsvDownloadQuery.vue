<template>
        <el-collapse v-model="activeNames" @change="handleChange">
            <el-collapse-item title="Query" name="1">
                <el-form :inline="true" :model="formInline" class="demo-form-inline">
                    <el-form-item label="Approved by">
                        <el-input v-model="formInline.user" placeholder="Study Name"></el-input>
                    </el-form-item>
                    <el-form-item label="Approved by">
                        <el-input v-model="formInline.user" placeholder="Study Name"></el-input>
                    </el-form-item>
                    <el-form-item label="Approved by">
                        <el-input v-model="formInline.user" placeholder="Study Name"></el-input>
                    </el-form-item>
                    <el-form-item label="Approved by">
                        <el-input v-model="formInline.user" placeholder="Study Name"></el-input>
                    </el-form-item>
                    <el-form-item label="Approved by">
                        <el-input v-model="formInline.user" placeholder="Study Name"></el-input>
                    </el-form-item>
                    <el-form-item label="Approved by">
                        <el-input v-model="formInline.user" placeholder="Study Name"></el-input>
                    </el-form-item>
                    <el-form-item label="Approved by">
                        <el-input v-model="formInline.user" placeholder="Study Name"></el-input>
                    </el-form-item>
                    <el-form-item label="Approved by">
                        <el-input v-model="formInline.user" placeholder="Study Name"></el-input>
                    </el-form-item>
                    <el-form-item label="Approved by">
                        <el-input v-model="formInline.user" placeholder="Study Name"></el-input>
                    </el-form-item>
                    <el-form-item label="Approved by">
                        <el-input v-model="formInline.user" placeholder="Study Name"></el-input>
                    </el-form-item>
                    <el-form-item label="Approved by">
                        <el-input v-model="formInline.user" placeholder="Study Name"></el-input>
                    </el-form-item>
                    <el-form-item label="Approved by">
                        <el-input v-model="formInline.user" placeholder="Study Name"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="onSubmit">Query</el-button>
                    </el-form-item>
                </el-form>
                </el-collapse-item>
        </el-collapse>
</template>

<script>
    export default {
        name: "BiodiCsvDownloadQuery",
        data() {
            return {
                formInline: {
                    user: '',
                    region: ''
                },
                activeNames: ['1']
            }
        },

        methods: {
            onSubmit() {
                console.log('submit!');
            }
        }
    }
</script>

<style scoped>

</style>