<template>
    <div>
        <el-button type="primary" @click="downloadOrganCsvFormat">Download Csv Format</el-button>
        <BiodiCsvUpload tips="Upload your organ list" @upload-file="handleUploadfile"  @remove-file="handleRemovefile"></BiodiCsvUpload>
        <component
                v-for="organForm in selectedOrgans"
                :key="organForm.key"
                :is="organForm.type"
                v-bind="organForm"
                :index="index"
                :selectedValue="organForm.value"
        >
        </component>
<!--        <el-row class="controls">-->
<!--            <el-col :span="12" :offset="6">-->
<!--                <el-button type="primary" @click="addOrgan">Add Organ</el-button>-->
<!--                <el-button type="danger" @click="removeOrgan">Remove Organ</el-button>-->
<!--            </el-col>-->
<!--        </el-row>-->
    </div>
</template>

<script>
    import OrganForm from "./OrganForm";
    import BiodiCsvUpload from "./BiodiCsvUpload";
    import {mapActions, mapGetters} from "vuex";
    import * as types from "../../../store/modules/BiodiCsv/BiodiCsvUploadTypes"
    export default {
        name: "BiodiCsvOrganOrder",
        components: {BiodiCsvUpload, OrganForm},
        data() {
            return {
                organForms: [],
                index: 0
            }
        },

        computed: {
          ...mapGetters({
              startValidation: 'biodiCsvUpload/startValidation',
              organCsv: 'biodiCsvUpload/organCsv',
              selectedOrgans: 'biodiCsvUpload/selectedOrgans'
          })
        },

        methods: {
            ...mapActions({
                'downloadOrganCsvFormat': types.DOWNLOAD_ORGAN_CSV_FORMAT,
                'setOrganCsv': types.SET_ORGAN_CSV,
                'handleOrganCsv': types.HANDLE_ORGAN_CSV
            }),

            handleUploadfile(fileList) {
                this.setOrganCsv({organCsv: fileList});
                this.handleOrganCsv({organCsv: this.organCsv})
                    .then(() =>  {
                        console.log(this.selectedOrgans)
                    })
            },

            handleRemovefile() {
                this.setOrganCsv({organCsv: null})
            },

            handleStartValidation() {
                this.handleOrganCsv({organCsv: this.organCsv})
                    .then((validated) => {
                        if (validated) {
                            console.log("organ forms validated");
                            this.$emit('validated', true)
                        } else {
                            console.log("organ forms not validated");
                            this.$emit('validated', false);
                        }
                    })
                    .catch((err) => {
                        this.$emit('validated', false)
                    });
            },
        }
    }
</script>

<style scoped>
    .controls {
        margin-top: 2%;
    }
</style>