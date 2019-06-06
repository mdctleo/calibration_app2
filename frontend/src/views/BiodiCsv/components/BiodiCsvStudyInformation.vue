<template>
    <div class="form">
        <el-form :model="form" :rules="rules" ref="form" label-width="120px" label-position="top" class="demo-ruleForm">
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Study Name" prop="studyName">
                        <el-input v-model="form.studyName"></el-input>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Study Date" prop="studyDate">
                        <el-date-picker type="date" placeholder="Pick a date" v-model="form.studyDate" style="width: 100%;"></el-date-picker>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Researcher Name" prop="researcherName">
                        <el-input v-model="form.researcherName"></el-input>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Principal Investigator Name" prop="piName">
                        <el-input v-model="form.piName"></el-input>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Radioisotope" prop="radioIsotope">
                        <el-input v-model="form.radioIsotope"></el-input>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Radiotracer" prop="radioTracer">
                        <el-input v-model="form.radioTracer"></el-input>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Comments">
                        <el-input type="textarea" v-model="form.comments"></el-input>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-form-item>
                <el-button @click="resetForm('form')">Reset</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script>
    export default {
        name: "BiodiCsvStudyInformation",
        data() {
            return {
                form: {
                    studyName: '',
                    studyDate: null,
                    researcherName: '',
                    piName: '',
                    radioIsotope: null,
                    radioTracer: null,
                    comments: '',
                },
                rules: {
                    studyName: [
                        {required: true, message: 'Please input study name', trigger: 'blur'},
                    ],
                    studyDate: [
                        {type: 'date', required: true, message: 'Please pick a date', trigger: 'change'}
                    ],
                    researcherName: [
                        {required: true, message: 'Please input researcher name', trigger: 'blur'}
                    ],
                    piName: [
                        {required: true, message: 'Please input a principal investigator name', trigger: 'blur'}
                    ],
                    radioIsotope: [
                        {required: true, message: 'Please select an isotope', trigger: 'change'}
                    ],
                    radioTracer: [
                        {required: true, message: 'Please select a radio tracer', trigger: 'change'}
                    ],
                    comments: [
                        { min: 0, max: 5000, message: 'Length should be less than 5000', trigger: 'blur' }
                    ]
                }
            };
        },
        methods: {
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        alert('submit!');
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },
            resetForm(formName) {
                this.$refs[formName].resetFields();
            }
        }

    }
</script>

<style scoped>
    .form {
        margin-top: 2%;
    }

</style>