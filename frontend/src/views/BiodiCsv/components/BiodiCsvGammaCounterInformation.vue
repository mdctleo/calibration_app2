<template>
    <div class="form">
        <el-form :model="form" :rules="rules" ref="form" label-width="120px" label-position="top" class="demo-ruleForm">
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Gamma Counter ID" prop="gammaCounterId">
                        <el-select v-model="form.gammaCounterId" placeholder="Please select the gamma counter">
                            <el-option label="Zone one" value="shanghai"></el-option>
                            <el-option label="Zone two" value="beijing"></el-option>
                        </el-select>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Gamma Counter Run Date & Time" prop="gammaCounterRunDateTime">
                        <el-date-picker
                                v-model="form.gammaCounterRunDateTime"
                                type="datetime"
                                placeholder="Select date and time">
                        </el-date-picker>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Gamma Counter Run Time Offset" prop="gammaCounterRunTimeOffset">
                        <el-input v-model="form.gammaCounterRunTimeOffset"></el-input>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Gamma Counter Run Comments" prop="gammaCounterRunComments">
                        <el-input type="textarea" v-model="form.gammaCounterRunComments"></el-input>
                    </el-form-item>
                </el-col>
            </el-row>
        </el-form>
    </div>
</template>

<script>
    import GammaCounterForm from "./GammaCounterForm";
    import {mapGetters} from "vuex";

    export default {
        name: "BiodiCsvGammaCounterInformation",
        components: {GammaCounterForm},
        props: {
            bus: Object
        },
        data () {
            return {
                form: {
                    gammaCounterId: "",
                    gammaCounterRunDateTime: "",
                    gammaCounterRunTimeOffset: "",
                    gammaCounterRunComments: ""
                },

                rules: {
                    gammaCounterId: [
                        {required: true, message: 'Please select a gamma counter', trigger: 'change'},
                    ],
                    gammaCounterRunDateTime: [
                        {required: true, type: 'date', message: 'Please pick a date & time', trigger: 'change'},
                        {type: 'date', message: 'Format for this field must be a date', trigger:'change'}
                    ],
                    comments: [
                        { min: 0, max: 5000, message: 'Length should be less than 5000', trigger: 'blur' }
                    ]
                }
            }
        },

        computed: {
            ...mapGetters({
                startValidation: 'biodiCsvUpload/startValidation'
            })
        },

        watch: {
            startValidation: function (val) {
                if (val === true) {
                    this.submitForm('form')
                }
            }
        },

        methods: {
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        this.$emit('validated', true);
                    } else {
                        console.log('error submit!!');
                        this.$emit('validated', false);
                    }
                });
            }
        }
    }
</script>

<style scoped>
    .form {
        margin-top: 2%;
    }

    .form .el-select {
        display: block;
    }

    .form .el-date-picker {
        width: 100%;
    }


</style>