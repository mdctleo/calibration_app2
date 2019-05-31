<template>
    <div>
        <el-form ref="form" class="form" :model="form" :rules="rules" label-width="120px" label-position="top">
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item :label="this.label0" prop="input0">
                        <el-input v-model.number="form.input0" type="number"></el-input>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item :label="this.label1" prop="input1">
                        <el-input v-model.number="form.input1" type="number"></el-input>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Alpha" prop="alpha">
                        <el-select v-model.number="form.alpha" placeholder="Select Alpha">
                            <el-option label="0.05" value=0.05></el-option>
                            <el-option label="0.01" value=0.01></el-option>
                        </el-select>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Test" prop="test">
                        <el-select v-model="form.test" placeholder="Select Test">
                            <el-option label="Independent Samples" value="independent"></el-option>
                            <el-option label="Paired Samples" value="paired"></el-option>
                        </el-select>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Alternative" prop="alternative">
                        <el-select v-model="form.alternative" placeholder="Select Alternative">
                            <el-option label="Two-sided" value="two-sided"></el-option>
                            <el-option label="Larger" value="larger"></el-option>
                            <el-option label="Smaller" value="smaller"></el-option>
                        </el-select>
                    </el-form-item>
                </el-col>
            </el-row>
        </el-form>
        <el-row>
            <el-col :span="12" :offset="6">
                <el-button type="primary" @click="submitForm('form')">Calculate</el-button>
            </el-col>
        </el-row>
    </div>
</template>

<script>
    import {mapActions} from "vuex";
    import * as types from '../../../store/modules/Statistics/types'

    export default {
        name: "StatisticsFormBase",
        data() {
            return {
                form: {
                    input0: null,
                    input1: null,
                    alpha: null,
                    test: null,
                    alternative: null
                },
                rules: {
                    input0: [
                        {required: true, message: 'This field is required', trigger: 'blur'},
                        {type: 'number', message: 'This field must be a number'}
                    ],

                    input1: [
                        {required: true, message: 'This field is required', trigger: 'blur'},
                        {type: 'number', message: 'This field must be a number'}
                    ],

                    alpha: [
                        {required: true, message: 'Please choose an Alpha', trigger: 'blur'}
                    ],

                    test: [
                        {required: true, message: 'Please choose a test', trigger: 'blur'}
                    ],

                    alternative: [
                        {required: true, message: 'Please choose an alternative', trigger: 'blur'}
                    ]
                }
            }
        },
        props: {
            label0: null,
            label1: null
        },
        methods: {
            ...mapActions([
                types.SET_INPUT_0,
                types.SET_INPUT_1,
                types.SET_ALPHA,
                types.SET_TEST,
                types.SET_ALTERNATIVE
            ]),

            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        this.setInput0({input0: this.form.input0});
                        this.setInput1({input1: this.form.input1});
                        this.setAlpha({alpha: this.form.alpha});
                        this.setTest({test: this.form.test});
                        this.setAlternative({alternative: this.form.alternative});
                        return this.$emit('submit')
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            }
        }
    }
</script>

<style scoped>
    .form {
        margin-top: 30px;
    }

</style>