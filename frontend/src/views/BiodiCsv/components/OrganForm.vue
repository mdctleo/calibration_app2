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
    export default {
        name: "OrganForm",
        props: {
          selectedValue: String
        },
        data () {
            return {
                form: {
                    organ: ""
                },

                rules: {
                    organ: [
                        {required: true, message: 'Please select a valid organ in the database', trigger: 'change'},
                    ]
                }
            }
        },
        computed: {

        },

        created () {
            this.form.organ = this.selectedValue;
        }
    }
</script>

<style scoped>

</style>