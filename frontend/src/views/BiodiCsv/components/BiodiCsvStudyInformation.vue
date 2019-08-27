<template>
    <div class="form">
        <el-form :model="studyForm" :rules="rules" ref="form" label-width="120px" label-position="top" class="demo-ruleForm">
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Study Name" prop="studyName">
                        <el-input v-model="studyName"></el-input>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Study Date" prop="studyDate">
                        <el-date-picker type="date" placeholder="Pick a date" v-model="studyDate"
                                        style="width: 100%;"></el-date-picker>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Researcher Name" prop="researcherName">
                        <el-input v-model="researcherName"></el-input>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Principal Investigator Name" prop="piName">
                        <el-select v-model="piName" placeholder="Please select the radio isotope">
                            <el-option label="Francois Bernard" value="Francois Bernard"></el-option>
                            <el-option label="Francois Bernard" value="Francois Bernard"></el-option>
                        </el-select>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Radioisotope" prop="isotopeName">
                        <el-select v-model="isotopeName" placeholder="Please select the radio isotope">
                           <el-option
                               v-for="isotope in isotopes"
                               :key="isotope.isotopeName"
                               :label="isotope.isotopeName"
                               :value="isotope.isotopeName"
                               ></el-option>
                        </el-select>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Chelator" prop="chelatorName">
                        <el-select v-model="chelatorName" placeholder="Please select the chelator">
                            <el-option
                                v-for="chelator in chelators"
                                :key="chelator.name"
                                :label="chelator.name"
                                :value="chelator.name"
                                ></el-option>
                        </el-select>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Vector" prop="vectorName">
                        <el-select v-model="vectorName" placeholder="Please select the vector">
                            <el-option
                                v-for="vector in vectors"
                                :key="vector.name"
                                :label="vector.name"
                                :value="vector.name"
                            ></el-option>
                        </el-select>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Target" prop="target">
                        <el-input v-model="target" placeholder="Please input the target"></el-input>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Mouse Strain" prop="mouseStrainName">
                        <el-select v-model="mouseStrainName"
                                   placeholder="Please select a mouseStrain">
                            <el-option
                                v-for="mouseStrain in mouseStrains"
                                :key="mouseStrain.name"
                                :label="mouseStrain.name"
                                :value="mouseStrain.name"
                            ></el-option>
                        </el-select>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Tumor Model" prop="tumorModelName">
                        <el-select v-model="tumorModelName"
                                   placeholder="Please select a tumor model">
                            <el-option
                                    v-for="tumorModel in tumorModels"
                                    :key="tumorModel.name"
                                    :label="tumorModel.name"
                                    :value="tumorModel.name"
                            ></el-option>
                        </el-select>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Specific Activity" prop="radioPurity">
                        <el-input v-model.number="radioPurity" type="number"></el-input>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Comments">
                        <el-input type="textarea" v-model="comments"></el-input>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Gamma Runs" prop="numGammaRuns">
                        <el-input v-model.number="numGammaRuns" placeholder="Please input number of gamma runs"></el-input>
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
    import {mapActions, mapGetters} from "vuex";
    import * as types from '../../../store/modules/BiodiCsvUpload/BiodiCsvUploadTypes.js'

    export default {
        name: "BiodiCsvStudyInformation",
        data() {
            return {
                rules: {
                    studyName: [
                        {required: true, message: 'Please input study name', trigger: 'blur'},
                    ],
                    studyDate: [
                        {required: true, message: 'Please pick a date', trigger: 'change'},
                        {type: 'date', message: 'format for this field must be a date', trigger: 'change'}
                    ],
                    researcherName: [
                        {required: true, message: 'Please input researcher name', trigger: 'blur'}
                    ],
                    piName: [
                        {required: true, message: 'Please input a principal investigator name', trigger: 'change'}
                    ],
                    isotopeName: [
                        {required: true, message: 'Please select an isotope', trigger: 'change'}
                    ],
                    chelatorName: [
                        {required: true, message: 'Please select a chelator', trigger: 'change'}
                    ],
                    vectorName: [
                        {required: true, message: 'Please select a vector', trigger: 'change'},
                    ],
                    target: [
                        {required: true, message: 'Please input a target', trigger: 'blur'}
                    ],
                    cellLineName: [
                        {required: true, message: 'Please input a cell line', trigger: 'change'}
                    ],
                    mouseStrainName: [
                        {required: true, message: 'Please select a mouse strain', trigger: 'change'}
                    ],
                    tumorModelName: [
                        {required: true, message: 'Please select a tumor model', trigger: 'change'}
                    ],
                    radioPurity: [
                        {required: true, message: 'Please input radio purity', trigger: 'blur'},
                        {type: 'number', message: 'Format of this field must be a number'}
                    ],
                    comments: [
                        {min: 0, max: 5000, message: 'Length should be less than 5000', trigger: 'blur'}
                    ],

                    numGammaRuns: [
                        {required: true, message: 'Please input the number of gamma runs you plan to upload', trigger: 'blur'},
                        {type: 'number', min: 1, max: 100, message: 'You must upload between 1 to 100 files'}
                    ]
                }
            };
        },
        computed: {
            ...mapGetters({
                startValidation: 'biodiCsvUpload/startValidation',
                getStudyForm: 'biodiCsvUpload/studyForm',
                getStudyName: 'biodiCsvUpload/studyName',
                getStudyDate: 'biodiCsvUpload/studyDate',
                getResearcherName: 'biodiCsvUpload/researcherName',
                getPiName: 'biodiCsvUpload/piName',
                getIsotopeName: 'biodiCsvUpload/isotopeName',
                getChelatorName: 'biodiCsvUpload/chelatorName',
                getVectorName: 'biodiCsvUpload/vectorName',
                getTarget: 'biodiCsvUpload/target',
                getMouseStrainName: 'biodiCsvUpload/mouseStrainName',
                getTumorModelName: 'biodiCsvUpload/tumorModelName',
                getRadioPurity: 'biodiCsvUpload/radioPurity',
                getComment: 'biodiCsvUpload/comment',
                getNumGammaRuns: 'biodiCsvUpload/numGammaRuns',
                isotopes: 'biodiCsvUpload/isotopes',
                chelators: 'biodiCsvUpload/chelators',
                vectors: 'biodiCsvUpload/vectors',
                cellLines: 'biodiCsvUpload/cellLines',
                mouseStrains: 'biodiCsvUpload/mouseStrains',
                tumorModels: 'biodiCsvUpload/tumorModels'
            }),

            studyForm: {
                get() {
                    return this.getStudyForm
                },

                set(value) {
                },
            },

            studyName: {
                get() {
                    return this.getStudyName
                },

                set(value) {
                    this.setStudyName({studyName: value})
                }
            },

            studyDate: {
                get() {
                    return this.getStudyDate
                },

                set(value) {
                    this.setStudyDate({studyDate: value})
                }
            },

            researcherName: {
                get() {
                    return this.getResearcherName
                },

                set(value) {
                    this.setResearcherName({researcherName: value})
                }
            },

            piName: {
                get() {
                    return this.getPiName
                },

                set(value) {
                    this.setPiName({piName: value})
                }
            },

            isotopeName: {
                get() {
                    return this.getIsotopeName
                },

                set(value) {
                    this.setIsotopeName({isotopeName: value})
                }
            },

            chelatorName: {
                get() {
                    return this.getChelatorName
                },

                set(value) {
                    this.setChelatorName({chelatorName: value})
                }
            },

            vectorName: {
                get() {
                    return this.getVectorName
                },

                set(value) {
                    this.setVectorName({vectorName: value})
                }
            },

            target: {
                get() {
                    return this.getTarget
                },

                set(value) {
                    this.setTarget({target: value})
                }
            },

            cellLineName: {
                get() {
                    return this.getCellLineName
                },

                set(value) {
                    this.setCellLineName({cellLineName: value})
                }
            },

            mouseStrainName: {
                get() {
                    return this.getMouseStrainName
                },

                set(value) {
                    this.setMouseStrainName({mouseStrainName: value})
                }
            },

            tumorModelName: {
                get() {
                    return this.getTumorModelName
                },

                set(value) {
                    this.setTumorModelName({tumorModelName: value})
                }

            },

            radioPurity: {
                get() {
                    return this.getRadioPurity
                },

                set(value) {
                    this.setRadioPurity({radioPurity: value})
                }
            },

            comments: {
                get() {
                    return this.getComment
                },

                set(value) {
                    this.setComment({comment: value})
                }
            },

            numGammaRuns: {
                get() {
                    return this.getNumGammaRuns
                },

                set(value) {
                    this.setNumGammaRuns({numGammaRuns: value})
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
                'setStudyName': types.SET_STUDY_NAME,
                'setStudyDate': types.SET_STUDY_DATE,
                'setResearcherName': types.SET_RESEARCHER_NAME,
                'setPiName': types.SET_PI_NAME,
                'setIsotopeName': types.SET_RADIO_ISOTOPE,
                'setChelatorName': types.SET_CHELATOR,
                'setVectorName': types.SET_VECTOR,
                'setTarget': types.SET_TARGET,
                'setMouseStrainName': types.SET_MOUSE_STRAIN,
                'setTumorModelName': types.SET_TUMOR_MODEL,
                'setRadioPurity': types.SET_RADIO_PURITY,
                'setComment': types.SET_COMMENT,
                'setNumGammaRuns': types.SET_NUM_GAMMA_RUNS,
                'getIsotopes': types.GET_ISOTOPES,
                'getChelators': types.GET_CHELATORS,
                'getVectors': types.GET_VECTORS,
                'getMouseStrains': types.GET_MOUSE_STRAINS,
                'getTumorModels': types.GET_TUMOR_MODELS
            }),
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        this.$emit('validated', true);
                    } else {
                        this.$emit('validated', false);
                    }
                });
            },
            resetForm(formName) {
                this.$refs[formName].resetFields();
            }
        },

        created() {
            this.getIsotopes()
            this.getChelators()
            this.getVectors()
            this.getMouseStrains()
            this.getTumorModels()
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

</style>