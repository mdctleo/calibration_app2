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
                    <el-form-item label="Radioisotope" prop="radioIsotope">
                        <el-select v-model="radioIsotope" placeholder="Please select the radio isotope">
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
                    <el-form-item label="Chelator" prop="chelator">
                        <el-select v-model="chelator" placeholder="Please select the chelator">
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
                    <el-form-item label="Vector" prop="vector">
                        <el-select v-model="vector" placeholder="Please select the vector">
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
                    <el-form-item label="Cell Line" prop="cellLine">
                        <el-select v-model="cellLine"
                                   placeholder="Please select the cell line">
                            <el-option
                                v-for="cellLine in cellLines"
                                :key="cellLine.name"
                                :label="cellLine.name"
                                :value="cellLine.name"
                            ></el-option>
                        </el-select>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Mouse Strain" prop="mouseStrain">
                        <el-select v-model="mouseStrain"
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
                    <el-form-item label="Tumor Model" prop="tumorModel">
                        <el-select v-model="tumorModel"
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
                    <el-form-item label="Radio Purity" prop="radioPurity">
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
            <el-form-item>
                <el-button @click="resetForm('form')">Reset</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script>
    import {mapActions, mapGetters} from "vuex";
    import * as types from '../../../store/modules/BiodiCsv/BiodiCsvUploadTypes.js'

    export default {
        name: "BiodiCsvStudyInformation",
        props: {
            bus: Object
        },
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
                    radioIsotope: [
                        {required: true, message: 'Please select an isotope', trigger: 'change'}
                    ],
                    chelator: [
                        {required: true, message: 'Please select a chelator', trigger: 'change'}
                    ],
                    vector: [
                        {required: true, message: 'Please select a vector', trigger: 'change'},
                    ],
                    target: [
                        {required: true, message: 'Please input a target', trigger: 'blur'}
                    ],
                    cellLine: [
                        {required: true, message: 'Please input a cell line', trigger: 'change'}
                    ],
                    mouseStrain: [
                        {required: true, message: 'Please select a mouse strain', trigger: 'change'}
                    ],
                    tumorModel: [
                        {required: true, message: 'Please select a tumor model', trigger: 'change'}
                    ],
                    radioPurity: [
                        {required: true, message: 'Please input radio purity', trigger: 'blur'},
                        {type: 'number', message: 'Format of this field must be a number'}
                    ],
                    comments: [
                        {min: 0, max: 5000, message: 'Length should be less than 5000', trigger: 'blur'}
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
                getRadioIsotope: 'biodiCsvUpload/radioIsotope',
                getChelator: 'biodiCsvUpload/chelator',
                getVector: 'biodiCsvUpload/vector',
                getTarget: 'biodiCsvUpload/target',
                getCellLine: 'biodiCsvUpload/cellLine',
                getMouseStrain: 'biodiCsvUpload/mouseStrain',
                getTumorModel: 'biodiCsvUpload/tumorModel',
                getRadioPurity: 'biodiCsvUpload/radioPurity',
                getComments: 'biodiCsvUpload/comments',
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

            radioIsotope: {
                get() {
                    return this.getRadioIsotope
                },

                set(value) {
                    this.setRadioIsotope({radioIsotope: value})
                }
            },

            chelator: {
                get() {
                    return this.getChelator
                },

                set(value) {
                    this.setChelator({chelator: value})
                }
            },

            vector: {
                get() {
                    return this.getVector
                },

                set(value) {
                    this.setVector({vector: value})
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

            cellLine: {
                get() {
                    return this.getCellLine
                },

                set(value) {
                    this.setCellLine({cellLine: value})
                }
            },

            mouseStrain: {
                get() {
                    return this.getMouseStrain
                },

                set(value) {
                    this.setMouseStrain({mouseStrain: value})
                }
            },

            tumorModel: {
                get() {
                    return this.getTumorModel
                },

                set(value) {
                    this.setTumorModel({tumorModel: value})
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
                    return this.getComments
                },

                set(value) {
                    this.setComments({comments: value})
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
                'setRadioIsotope': types.SET_RADIO_ISOTOPE,
                'setChelator': types.SET_CHELATOR,
                'setVector': types.SET_VECTOR,
                'setTarget': types.SET_TARGET,
                'setCellLine': types.SET_CELL_LINE,
                'setMouseStrain': types.SET_MOUSE_STRAIN,
                'setTumorModel': types.SET_TUMOR_MODEL,
                'setRadioPurity': types.SET_RADIO_PURITY,
                'setComments': types.SET_COMMENTS,
                'getIsotopes': types.GET_ISOTOPES,
                'getChelators': types.GET_CHELATORS,
                'getVectors': types.GET_VECTORS,
                'getCellLines': types.GET_CELL_LINES,
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
            this.getCellLines()
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