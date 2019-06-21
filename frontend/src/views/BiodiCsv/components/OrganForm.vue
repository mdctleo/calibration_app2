<template>
    <div class="form">
        <el-form :model="organForm" :rules="rules" ref="form" label-width="120px" label-position="top">
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item id="test" :label="'Tube ' +  ($attrs.label + 1) + ' Organ'" prop="organ">
                        <el-select v-model="organ" placeholder="Please select an organ">
                            <el-option
                                    v-for="organ in availableOrgans"
                                    :key="organ"
                                    :label="organ"
                                    :value="organ"
                            ></el-option>
                        </el-select>
                    </el-form-item>
                </el-col>
            </el-row>
        </el-form>
    </div>

</template>

<script>
    import {mapActions, mapGetters} from "vuex";
    import * as types from "../../../store/modules/BiodiCsv/BiodiCsvUploadTypes"

    export default {
        name: "OrganForm",
        props: {
            availableOrgans: Array
        },
        data() {
            return {
                rules: {
                    organ: [
                        {validator: this.organValidation, trigger: 'change'},
                    ]
                }
            }
        },
        computed: {
            ...mapGetters({
                startValidation: 'biodiCsvUpload/startValidation',
                getSelectedOrgans: 'biodiCsvUpload/selectedOrgans',
                getOrganForm: 'biodiCsvUpload/organForm'
            }),

            organForm: {
                get() {
                    return this.getOrganForm
                },

                set(value) {

                }
            },

            organ: {
                get() {
                    return this.getSelectedOrgans(this.$attrs.label).value
                },

                set(value) {
                    this.setSelectedOrgan({index: this.$attrs.label, organ: value})
                }
            }
        },

        methods: {
            ...mapActions({
                'setSelectedOrgan': types.SET_SELECTED_ORGAN
            }),
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        this.$emit('validated-one-organ-form', true)
                    } else {
                        console.log('error submit!!');
                        this.$emit('validated-one-organ-form', false)
                    }
                });
            },

            organValidation(rule, organ, callback) {
                if (organ === "") {
                    callback(new Error('Please select an organ'))
                } else if (!this.availableOrgans.includes(this.organ)) {
                    console.log(this.availableOrgans)
                    console.log(this.organ)
                    callback(new Error('The organ you have entered is not in the database, please select one'))
                } else {
                    callback();
                }
            }
        },

        watch: {
            startValidation: function (val) {
                if (val === true) {
                    this.submitForm('form')
                }
            }
        }
    }
</script>

<style scoped>

    .form .el-select {
        display: block;
    }

</style>