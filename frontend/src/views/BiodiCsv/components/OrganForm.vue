<template>
    <div class="form">
        <el-form :model="form" :rules="rules" ref="form" label-width="120px" label-position="top" class="demo-ruleForm">
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item :label="'Tube ' +  $attrs.label + ' Organ'" prop="organ">
                        <el-select v-model="form.organ" placeholder="Please select an organ">
                            <el-option label="Zone one" value="shanghai"></el-option>
                            <el-option label="Zone two" value="beijing"></el-option>
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
        data () {
            return {
                form: {
                    organ: ""
                },

                rules: {
                    organ: [
                        {required: true, message: 'Please select a organ', trigger: 'change'},
                    ]
                }
            }
        }
    }
</script>

<style scoped>

</style>