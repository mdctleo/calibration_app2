<template>
    <div class="form">
        <el-form :model="gammaForm" :rules="rules" ref="form" label-width="120px" label-position="top" class="demo-ruleForm">
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Gamma Counter ID" prop="gammaCounter">
                        <el-select v-model="gammaCounter" placeholder="Please select the gamma counter">
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
                                v-model="gammaCounterRunDateTime"
                                type="datetime"
                                placeholder="Select date and time">
                        </el-date-picker>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Gamma Counter Run Time Offset" prop="gammaCounterRunTimeOffset">
                        <el-input v-model="gammaCounterRunTimeOffset"></el-input>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Gamma Counter Run Comments" prop="gammaCounterRunComments">
                        <el-input type="textarea" v-model="gammaCounterRunComments"></el-input>
                    </el-form-item>
                </el-col>
            </el-row>
        </el-form>
    </div>
</template>

<script>
    import GammaCounterForm from "./GammaCounterForm";
    import {mapActions, mapGetters} from "vuex";
    import * as types from '../../../store/modules/BiodiCsv/BiodiCsvUploadTypes.js'


    export default {
        name: "BiodiCsvGammaCounterInformation",
        components: {GammaCounterForm},
        props: {
            bus: Object
        },
        data () {
            return {
                rules: {
                    gammaCounter: [
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
                startValidation: 'biodiCsvUpload/startValidation',
                getGammaForm: 'biodiCsvUpload/gammaForm',
                getGammaCounter: 'biodiCsvUpload/gammaCounter',
                getGammaCounterRunDateTime: 'biodiCsvUpload/gammaCounterRunDateTime',
                getGammaCounterRunTimeOffset: 'biodiCsvUpload/gammaCounterRunTimeOffset',
                getGammaCounterRunComments: 'biodiCsvUpload/gammaCounterRunComments'
            }),

            gammaForm: {
                get () {
                    return this.getGammaForm
                },

                set (value) {
                }
            },

            gammaCounter: {
                get () {
                    return this.getGammaCounter
                },

                set (value) {
                    this.setGammaCounter({gammaCounter: value})
                }
            },

            gammaCounterRunDateTime: {
                get () {
                    return this.getGammaCounterRunDateTime
                },

                set (value) {
                    this.setGammaCounterRunDateTime({gammaCounterRunDateTime: value})
                }
            },

            gammaCounterRunTimeOffset: {
                get () {
                    return this.getGammaCounterRunTimeOffset
                },

                set (value) {
                    this.setGammaCounterRunTimeOffset({gammaCounterRunTimeOffset: value})
                }
            },

            gammaCounterRunComments: {
                get() {
                    return this.getGammaCounterRunComments
                },

                set(value) {
                    this.setGammaCounterRunComments({gammaCounterRunComments: value})
                }
            }
        },

        watch: {
            startValidation: function (val) {
                if (val === true) {
                    this.submitForm('form')
                }
            }
        },

        methods: {
            ...mapActions({
                'setGammaCounter': types.SET_GAMMA_COUNTER,
                'setGammaCounterRunDateTime': types.SET_GAMMA_COUNTER_RUN_DATE_TIME,
                'setGammaCounterRunTimeOffset': types.SET_GAMMA_COUNTER_RUN_TIME_OFFSET,
                'setGammaCounterRunComments': types.SET_GAMMA_COUNTER_RUN_COMMENTS
            }),
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