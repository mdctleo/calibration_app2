<template>
    <div>
        <el-button type="primary" class="controls" @click="downloadOrganCsvFormat">Download Organ Csv</el-button>
        <BiodiCsvUploadForm tips="Upload your organ list"
                        @upload-file="handleUploadfile"
                        @remove-file="handleRemovefile"></BiodiCsvUploadForm>
<!--        <component-->
<!--                v-for="organForm in selectedOrgans(-1)"-->
<!--                :key="organForm.key"-->
<!--                :is="organForm.type"-->
<!--                v-bind="organForm"-->
<!--                :index="index"-->
<!--                @validated-one-organ-form="handleValidation"-->
<!--                :availableOrgans="availableOrgans"-->
<!--        >-->
<!--        </component>-->
    </div>
</template>

<script>
    import OrganForm from "./OrganForm";
    import BiodiCsvUploadForm from "./BiodiCsvUploadForm";
    import {mapActions, mapGetters} from "vuex";
    import * as types from "../../../store/modules/BiodiCsv/BiodiCsvUploadTypes"
    export default {
        name: "BiodiCsvOrganOrder",
        components: {BiodiCsvUploadForm, OrganForm},
        data() {
            return {
                organForms: [],
                index: 0,
                validatedOrganForms: 0,
            }
        },

        computed: {
          ...mapGetters({
              // startValidation: 'biodiCsvUpload/startValidation',
              organCsv: 'biodiCsvUpload/organCsv',
              // selectedOrgans: 'biodiCsvUpload/selectedOrgans',
              // availableOrgans: 'biodiCsvUpload/availableOrgans'
          })
        },

        // watch: {
        //   startValidation: function (val) {
        //       if (val === true && this.selectedOrgans.length === 0) {
        //           this.$emit('validated', false)
        //       }
        //   }
        // },

        methods: {
            ...mapActions({
                'downloadOrganCsvFormat': types.DOWNLOAD_ORGAN_CSV_FORMAT,
                'setOrganCsv': types.SET_ORGAN_CSV,
                'handleOrganCsv': types.HANDLE_ORGAN_CSV
            }),

            handleUploadfile(fileList) {
                this.setOrganCsv({organCsv: fileList})
                this.handleOrganCsv({organCsv: this.organCsv})
            },

            handleRemovefile() {
                this.handleOrganCsv({organCsv: null})
            },

            // handleValidation(validated) {
            //     if (validated === true) {
            //         this.validatedOrganForms++
            //         if (this.validatedOrganForms === this.selectedOrgans.length) {
            //             this.$emit('validated', true)
            //         }
            //     } else {
            //         this.validatedOrganForms = 0
            //         this.$emit('validated', false)
            //     }
            // }

        }
    }
</script>

<style scoped>
    .controls {
        margin-top: 2%;
    }
</style>