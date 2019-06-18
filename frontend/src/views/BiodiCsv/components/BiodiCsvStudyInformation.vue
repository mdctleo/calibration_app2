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
                        <el-date-picker type="date" placeholder="Pick a date" v-model="form.studyDate"
                                        style="width: 100%;"></el-date-picker>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Researcher Name" prop="researcherName">
                        <el-input  v-model="form.researcherName"></el-input>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Principal Investigator Name" prop="piName">
                        <el-select v-model="form.piName" placeholder="Please select the radio isotope">
                            <el-option label="Francois Bernard" value="shanghai"></el-option>
                            <el-option label="Francois Bernard" value="beijing"></el-option>
                        </el-select>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Radioisotope" prop="radioIsotope">
                        <el-select v-model="form.radioIsotope" placeholder="Please select the radio isotope">
                            <el-option label="Zone one" value="shanghai"></el-option>
                            <el-option label="Zone two" value="beijing"></el-option>
                        </el-select>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Chelator" prop="chelator">
                        <el-select v-model="form.chelator" placeholder="Please select the chelator">
                            <el-option label="Zone one" value="shanghai"></el-option>
                            <el-option label="Zone two" value="beijing"></el-option>
                        </el-select>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Vector" prop="vector">
                        <el-select v-model="form.vector" placeholder="Please select the vector">
                            <el-option label="Zone one" value="shanghai"></el-option>
                            <el-option label="Zone two" value="beijing"></el-option>
                        </el-select>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Target" prop="target">
                        <el-input v-model="form.target" placeholder="Please input the target"></el-input>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Cell Line" prop="cellLine">
                        <el-select v-model="form.cellLine"  @input="setCellLine" placeholder="Please select the cell line">
                            <el-option label="Zone one" value="shanghai"></el-option>
                            <el-option label="Zone two" value="beijing"></el-option>
                        </el-select>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Radio Activity" prop="radioActivity">
                        <el-input v-model.number="form.radioActivity" type="number">
                            <el-option label="Zone one" value="shanghai"></el-option>
                            <el-option label="Zone two" value="beijing"></el-option>
                        </el-input>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Radio Purity" prop="radioPurity">
                        <el-input v-model.number="form.radioPurity" type="number"></el-input>
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
    import {mapActions, mapGetters} from "vuex";
    import * as types from '../../../store/modules/BiodiCsv/BiodiCsvUploadTypes.js'

    export default {
        name: "BiodiCsvStudyInformation",
        props: {
            bus: Object
        },
        data() {
            return {
                form: {
                    studyName: "",
                    studyDate: "",
                    researcherName: "",
                    piName: "",
                    radioIsotope: "",
                    chelator: "",
                    vector: "",
                    target: "",
                    cellLine: "",
                    radioActivity: "",
                    radioPurity: "",
                    comments: "",
                },
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
                    radioActivity: [
                        {required: true, message: 'Please input radio activity', trigger: 'blur'},
                        {type: 'number', message: 'Format of this field must be a number', trigger: 'blur'}
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
                getStudyName: 'biodiCsvUpload/studyName',
                studyDate: 'biodiCsvUpload/studyDate',
                piName: 'biodiCsvUpload/piName',
                radioIsotope: 'biodiCsvUpload/radioIsotope',
                chelator: 'biodiCsvUpload/chelator',
                vector: 'biodiCsvUpload/vector',
                target: 'biodiCsvUpload/target',
                cellLine: 'biodiCsvUpload/cellLine',
                radioActivity: 'biodiCsvUpload/radioActivity',
                radioPurity: 'biodiCsvUpload/radioPurity',
                comments: 'biodiCsvUpload/comments'
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
                'setRadioActivity': types.SET_RADIO_ACTIVITY,
                'setRadioPurity': types.SET_RADIO_PURITY,
                'SET_COMMENTS': types.SET_COMMENTS
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

    .form .el-select {
        display: block;
    }

</style>