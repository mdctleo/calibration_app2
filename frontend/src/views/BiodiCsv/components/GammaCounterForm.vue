<template>
    <div class="form">
        <el-form :model="form" :rules="rules" ref="form" label-width="120px" label-position="top" class="demo-ruleForm">
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Gamma Counter ID" prop="gammaCounterId">
                        <el-select v-model="form.gammaCounterId" placeholder="Please select the radio isotope">
                            <el-option label="Zone one" value="shanghai"></el-option>
                            <el-option label="Zone two" value="beijing"></el-option>
                        </el-select>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Gamma Counter Run ID" prop="gammaCounterRunId">
                        <el-input v-model="form.gammaCounterRunId"></el-input>
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
    export default {
        name: "GammaCounterForm",
        props: {
            key: Number
        },
        data () {
            return {
                form: {
                    gammaCounterId: "",
                    gammaCounterRunId: "",
                    gammaCounterRunDateTime: "",
                    gammaCounterRunTimeOffset: "",
                    gammaCounterRunComments: ""
                },

                rules: {
                    gammaCounterId: [
                        {required: true, message: 'Please select a gamma counter', trigger: 'change'},
                    ],
                    gammaCounterRunId: [
                        {required: true, type: 'number', message: 'Please input a run id', trigger: 'blur'}
                    ],
                    gammaCounterRunDateTime: [
                        {required: true, type: 'date', message: 'Please pick a date & time', trigger: 'change'}
                    ],
                    comments: [
                        { min: 0, max: 5000, message: 'Length should be less than 5000', trigger: 'blur' }
                    ]
                }
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