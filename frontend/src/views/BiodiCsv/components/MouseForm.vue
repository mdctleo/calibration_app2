<template>
    <div class="form">
        <el-form :model="form" :rules="rules" ref="form" label-width="120px" label-position="top" class="demo-ruleForm">
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Mouse ID" prop="mouseId">
                        <el-input v-model="form.mouseId"></el-input>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Group ID" prop="groupId">
                        <el-input v-model="form.groupId"></el-input>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Time Point" prop="timePoint">
                        <el-time-picker
                                v-model="form.timePoint"
                                placeholder="Select time point">
                        </el-time-picker>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Weight (g)" prop="weight">
                        <el-input v-model.number="form.weight"></el-input>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Injection Date" prop="injectionDate">
                        <el-date-picker
                                v-model="form.injectionDate"
                                type="date"
                                placeholder="Select injection date">
                        </el-date-picker>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Pre-inj Time" prop="preInjTime">
                        <el-time-picker
                                v-model="form.preInjTime"
                                placeholder="Select pre-inj time">
                        </el-time-picker>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Post-inj Time" prop="postInjTime">
                        <el-time-picker
                                v-model="form.postInjTime"
                                placeholder="Select post-inj time">
                        </el-time-picker>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Pre-inj MBq" prop="preInjMBq">
                        <el-input v-model.number="form.preInjMBq"></el-input>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Post-inj MBq" prop="postInjMBq">
                        <el-input v-model.number="form.postInjMBq"></el-input>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Comments" prop="comments">
                        <el-input type="textarea" v-model="form.comments"></el-input>
                    </el-form-item>
                </el-col>
            </el-row>
        </el-form>
    </div>
</template>

<script>
    import {mapGetters} from "vuex";

    export default {
        name: "MouseForm",
        props: {
            bus: Object
        },
        data () {
            return {
                form: {
                    mouseId: "",
                    groupId: "",
                    timePoint: "",
                    weight: null,
                    injectionDate: "",
                    preInjTime: "",
                    postInjTime: "",
                    preInjMBq: "",
                    postInjMBq: "",
                    comments: "",
                },

                rules: {
                    mouseId: [
                        {required: true, message: 'Please input a mouse id', trigger: 'blur'}
                    ],
                    groupId: [
                        {required: true, message: 'Please input a group id', trigger: 'blur'}
                    ],
                    timePoint: [
                        {required: true, type:'date', message: 'Please select a time point', trigger: 'change'}
                    ],
                    weight: [
                        {required: true, message: 'Please input a weight', trigger: 'blur'},
                        {type: 'number', message: 'Format of this field needs to be a number', trigger: 'blur'}
                    ],
                    injectionDate: [
                        {required: true, message: 'Please input an injection date', trigger: 'change'},
                        {type: 'date', message: 'Format of this field needs to be a date', trigger: 'change'}
                    ],
                    preInjTime: [
                        {required: true, message: 'Please input a pre injection time', trigger: 'change'},
                        {type: 'date', message: 'Format of this field needs to be a date', trigger: 'change'}
                    ],
                    postInjTime: [
                        {required: true, message: 'Please input a post injection time', trigger: 'change'},
                        {type: 'date', message: 'Format of this field needs to be a date', trigger: 'change'}
                    ],
                    preInjMBq: [
                        {required: true, message: 'Please input a pre injection level', trigger: 'blur'},
                        {type: 'number', message: 'Format of this field needs to be a number'}
                    ],
                    postInjMBq: [
                        {required: false, message: 'Please input a number for this field', trigger: 'blur'},
                        {type: 'number', message: 'Format of this field needs to be a number'}
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
                        this.$emit('validated-one-form');
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            }
        },
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