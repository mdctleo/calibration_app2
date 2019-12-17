<template>
    <div class="form">
                <el-form :model="gammaForm" :rules="rules" ref="form" label-width="120px" label-position="top"
                         class="demo-ruleForm">
                    <el-row>
                        <el-col :span="12" :offset="6">
                            <el-form-item label="Gamma Counter ID" prop="gammaCounter">
                                <el-select v-model="gammaCounter" placeholder="Please select the gamma counter">
                                    <el-option
                                            v-for="gammaCounter in gammaCounters"
                                            :key="gammaCounter.model"
                                            :label="gammaCounter.model"
                                            :value="gammaCounter.model"
                                    ></el-option>
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
                <BiodiCsvMouseInfo :mouseCsvs="mouseCsv(gammaRun)" :gammaRun="gammaRun"></BiodiCsvMouseInfo>
                <el-divider class="divider"></el-divider>
                <h4>Upload your Organ Csv</h4>
                <BiodiCsvOrganOrder :organCsvs="organCsv(gammaRun)" :gammaRun="gammaRun"></BiodiCsvOrganOrder>
                <el-divider class="divider"></el-divider>
                <h4>Upload your Biodi Csv</h4>
                <BiodiCsvUpload :biodiCsvs="biodiCsv(gammaRun)" :gammaRun="gammaRun"></BiodiCsvUpload>
                <el-divider class="divider"></el-divider>
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
            gammaRun: Number,
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
                getGammaCounterRunTimeOffset: 'biodiCsvUpload/gammaCounterRunTimeOffset',
                getGammaCounterRunComments: 'biodiCsvUpload/gammaCounterRunComments',
                gammaCounters: 'biodiCsvUpload/gammaCounters',
                mouseCsv: 'biodiCsvUpload/mouseCsv',
                biodiCsv: 'biodiCsvUpload/biodiCsv',
                organCsv: 'biodiCsvUpload/organCsv'
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
                    return this.getGammaCounter(this.gammaRun)
                },

                set(value) {
                    this.setGammaCounter({index: this.gammaRun, gammaCounter: value})
                }
            },

            gammaCounterRunTimeOffset: {
                get() {
                    return this.getGammaCounterRunTimeOffset(this.gammaRun)
                },

                set(value) {
                    this.setGammaCounterRunTimeOffset({index: this.gammaRun, gammaCounterRunTimeOffset: value})
                }
            },

            gammaCounterRunComments: {
                get() {
                    return this.getGammaCounterRunComments(this.gammaRun)
                },

                set(value) {
                    this.setGammaCounterRunComments({index: this.gammaRun, gammaCounterRunComments: value})
                }
            }
        },

        watch: {
            startValidation: function (val) {
                if (val === true) {
                    this.$refs['form'].validate((valid) => {
                        if (valid) {
                            console.log("validated")
                            this.$emit('validated', true)
                        } else {
                            console.log("invalidated")
                            this.$emit('validated', false)
                        }
                    })

                    // let validationArr = [
                    //     this.$refs['form'].validate(),
                    //     this.handleMouseCsvs({mouseCsvs: this.mouseCsvs}),
                    //     this.handleOrganCsvs({organCsvs: this.organCsvs}),
                    //     // this.handleBiodiCsvs({biodiCsvs: this.biodiCsvs})
                    // ]


                    // Promise.all(validationArr)
                    //     .then((result) => {
                    //         let formValid = result[0]
                    //         let mouseCsvValid = true
                    //         let organCsvValid = true
                    //         console.log(result)
                    //         // let biodiCsvValid = result[3]
                    //         let biodiCsvValid = true
                    //         if (formValid && mouseCsvValid && organCsvValid && biodiCsvValid) {
                    //             console.log("emittint validated")
                    //             this.$emit('validated', true)
                    //         } else {
                    //             console.log("emitted invalid")
                    //             this.$emit('validated', false)
                    //         }
                    //     })
                    //     .catch((error) => {
                    //         this.$emit('validated', false)
                    //     })
                }
            }
        },

        methods: {
            ...mapActions({
                'setGammaCounter': types.SET_GAMMA_COUNTER,
                'setGammaCounterRunTimeOffset': types.SET_GAMMA_COUNTER_RUN_TIME_OFFSET,
                'setGammaCounterRunComments': types.SET_GAMMA_COUNTER_RUN_COMMENTS,
                'handleHidexBiodiCsvs': types.HANDLE_HIDEX_BIODI_CSVS,
                'handleBiodiCsvs': types.HANDLE_BIODI_CSVS,
                'handleOrganCsvs': types.HANDLE_ORGAN_CSVS,
                'handleMouseCsvs': types.HANDLE_MOUSE_CSVS,
                'getCounters': types.GET_COUNTERS
            }),
        },

        created() {
            this.getCounters()
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