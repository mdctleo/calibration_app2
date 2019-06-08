<template>
    <div>
        <component
                v-for="organForm in organForms"
                :key="organForm.key"
                :is="organForm.type"
                v-bind="organForm"
                :index="index"
        >
        </component>
        <el-row class="controls">
            <el-col :span="12" :offset="6">
                <el-button type="primary" @click="addOrgan">Add Organ</el-button>
                <el-button type="danger" @click="removeOrgan">Remove Organ</el-button>
            </el-col>
        </el-row>
    </div>
</template>

<script>
    import OrganForm from "./OrganForm";
    export default {
        name: "BiodiCsvOrganOrder",
        components: {OrganForm},
        data() {
            return {
                organForms: [],
                index: 0
            }
        },

        methods: {
            addOrgan() {
                this.organForms.push({
                    key: this.index,
                    label: this.index,
                    type: 'OrganForm'
                });
                this.index++;
            },

            removeOrgan() {
                this.organForms.pop();
                this.index--;
            }
        }
    }
</script>

<style scoped>
    .controls {
        margin-top: 2%;
    }
</style>