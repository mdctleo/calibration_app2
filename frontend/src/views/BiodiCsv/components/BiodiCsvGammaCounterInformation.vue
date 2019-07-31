<template>
    <div class="form">
        <el-form :model="gammaForm" :rules="rules" ref="form" label-width="120px" label-position="top"
                 class="demo-ruleForm">
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Gamma Counter ID" prop="gammaCounter">
                        <el-select v-model="gammaCounter" placeholder="Please select the gamma counter">
                            <el-option label="gammaCounter1" value="gammaCounter1"></el-option>
                            <el-option label="gammaCounter2" value="gammaCounter2"></el-option>
                        </el-select>
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
        <el-divider class="divider"></el-divider>
        <h4>Upload your Mouse Csv</h4>
        <BiodiCsvMouseInfo :mouseCsvs="mouseCsvs"></BiodiCsvMouseInfo>
        <el-divider class="divider"></el-divider>
        <h4>Upload your Organ Csv</h4>
        <BiodiCsvOrganOrder :organCsvs="organCsvs"></BiodiCsvOrganOrder>
        <el-divider class="divider"></el-divider>
        <h4>Upload your Biodi Csv</h4>
        <BiodiCsvUpload :biodiCsvs="biodiCsvs"></BiodiCsvUpload>
    </div>
</template>

<script>
    import {mapActions, mapGetters} from "vuex";
    import * as types from '../../../store/modules/BiodiCsvUpload/BiodiCsvUploadTypes.js'
    import BiodiCsvMouseInfo from "./BiodiCsvMouseInfo";
    import BiodiCsvUpload from "./BiodiCsvUpload";
    import BiodiCsvOrganOrder from "./BiodiCsvOrganOrder";

    export default {
        name: "BiodiCsvGammaCounterInformation",
        components: {BiodiCsvOrganOrder, BiodiCsvUpload, BiodiCsvMouseInfo},
        props: {
        },
        data() {
            return {
                rules: {
                    gammaCounter: [
                        {required: true, message: 'Please select a gamma counter', trigger: 'change'},
                    ],
                    gammaCounterRunDateTime: [
                        {required: true, type: 'date', message: 'Please pick a date & time', trigger: 'change'},
                        {type: 'date', message: 'Format for this field must be a date', trigger: 'change'}
                    ],
                    comments: [
                        {min: 0, max: 5000, message: 'Length should be less than 5000', trigger: 'blur'}
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
                getGammaCounterRunComments: 'biodiCsvUpload/gammaCounterRunComments',
                mouseCsvs: 'biodiCsvUpload/mouseCsvs',
                biodiCsvs: 'biodiCsvUpload/biodiCsvs',
                organCsvs: 'biodiCsvUpload/organCsvs'
            }),

            gammaForm: {
                get() {
                    return this.getGammaForm
                },

                set(value) {
                }
            },

            gammaCounter: {
                get() {
                    return this.getGammaCounter
                },

                set(value) {
                    this.setGammaCounter({gammaCounter: value})
                }
            },

            gammaCounterRunDateTime: {
                get() {
                    return this.getGammaCounterRunDateTime
                },

                set(value) {
                    this.setGammaCounterRunDateTime({gammaCounterRunDateTime: value})
                }
            },

            gammaCounterRunTimeOffset: {
                get() {
                    return this.getGammaCounterRunTimeOffset
                },

                set(value) {
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
                    let validationArr = [
                        this.$refs['form'].validate(),
                        this.handleMouseCsvs({mouseCsvs: this.mouseCsvs}),
                        this.handleOrganCsvs({organCsvs: this.organCsvs}),
                        this.handleBiodiCsvs({biodiCsvs: this.biodiCsvs}),
                    ]

                    Promise.all(validationArr)
                        .then((result) => {
                            let formValid = result[0]
                            let mouseCsvValid = result[1]
                            let organCsvValid = result[2]
                            let biodiCsvValid = result[3]
                            if (formValid && mouseCsvValid && organCsvValid && biodiCsvValid) {
                                this.$emit('validated', true)
                            } else {
                                this.$emit('validated', false)
                            }
                        })
                        .catch((error) => {
                            this.$emit('validated', false)
                        })
                }
            }
        },

        methods: {
            ...mapActions({
                'setGammaCounter': types.SET_GAMMA_COUNTER,
                'setGammaCounterRunDateTime': types.SET_GAMMA_COUNTER_RUN_DATE_TIME,
                'setGammaCounterRunTimeOffset': types.SET_GAMMA_COUNTER_RUN_TIME_OFFSET,
                'setGammaCounterRunComments': types.SET_GAMMA_COUNTER_RUN_COMMENTS,
                'handleBiodiCsvs': types.HANDLE_BIODI_CSVS,
                'handleOrganCsvs': types.HANDLE_ORGAN_CSVS,
                'handleMouseCsvs': types.HANDLE_MOUSE_CSVS,
            }),
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        this.$emit('validated', true);
                    } else {
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

    .divider {
        width: 90% !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }


</style>