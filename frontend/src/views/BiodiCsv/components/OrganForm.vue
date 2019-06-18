<template>
    <div class="form">
        <el-form :model="form" :rules="rules" ref="form" label-width="120px" label-position="top" class="demo-ruleForm">
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item id="test" :label="'Tube ' +  $attrs.label + ' Organ'" prop="organ">
                        <el-select v-model="form.organ" placeholder="Please select an organ">
                            <el-option label="Lungs" value="Lungs"></el-option>
                            <el-option label="Brain" value="Brain"></el-option>
                            <el-option label="Liver" value="Liver"></el-option>
                        </el-select>
                    </el-form-item>
                </el-col>
            </el-row>
        </el-form>
    </div>

</template>

<script>
    import {mapGetters} from "vuex";

    export default {
        name: "OrganForm",
        props: {
          selectedValue: String,
          availableOrgans: Array
        },
        data () {
            return {
                form: {
                    organ: ""
                },

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
            })
        },

        methods: {
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

            organValidation (rule, value, callback) {
                if (value === "") {
                    callback(new Error('Please select an organ'))
                } else if (!this.availableOrgans.includes(value)) {
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
        },

        created () {
            this.form.organ = this.selectedValue;
        }
    }
</script>

<style scoped>

</style>