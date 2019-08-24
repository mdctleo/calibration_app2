<template>
    <div v-loading="loading">
        <el-alert
                v-show="error"
                :title="error"
                type="error"
                show-icon
                @close="setError({error: null})">
        </el-alert>
        <el-row>
            <BiodiCsvDownloadQuery></BiodiCsvDownloadQuery>
        </el-row>
        <el-row>
            <BiodiCsvDownload :metas="metas" @download-complete="handleDownloadComplete"
                              @download-raw="handleDownloadRaw"
                              @download-analysis="handleDownloadAnalysis"
            ></BiodiCsvDownload>
        </el-row>
    </div>
</template>

<script>
    import {mapActions, mapGetters} from 'vuex';
    import * as types from '../../store/modules/BiodiCsvDownload/BiodiCsvDownloadTypes.js'
    import BiodiCsvDownload from "./components/BiodiCsvDownload";
    import BiodiCsvDownloadQuery from "./components/BiodiCsvDownloadQuery";
    export default {
        name: "BiodiCsvDownloadView",
        components: {BiodiCsvDownloadQuery, BiodiCsvDownload},
        computed: {
            ...mapGetters({
                metas: 'biodiCsvDownload/metas',
                biodiCsvToDownload: 'biodiCsvDownload/biodiCsvToDownload',
                error: 'biodiCsvDownload/error',
                loading: 'biodiCsvDownload/loading'
            })
        },
        methods: {
            ...mapActions({
                'downloadBiodiCsvComplete': types.DOWNLOAD_BIODI_CSV_COMPLETE,
                'downloadBiodiCsvRaw': types.DOWNLOAD_BIODI_CSV_RAW,
                'downloadBiodiCsvAnalysis': types.DOWNLOAD_BIODI_CSV_ANALYSIS,
                'getBiodiCsvMetas': types.GET_BIODI_CSV_METAS,
                'setError': types.SET_ERROR
            }),

            handleDownloadComplete() {
                console.log(this.biodiCsvToDownload)
                this.downloadBiodiCsvComplete({biodiCsvToDownload: this.biodiCsvToDownload})
            },

            handleDownloadRaw() {
                console.log(this.biodiCsvToDownload)
                this.downloadBiodiCsvRaw({biodiCsvToDownload: this.biodiCsvToDownload})
            },

            handleDownloadAnalysis() {
                console.log(this.biodiCsvToDownload)
                this.downloadBiodiCsvAnalysis({biodiCsvToDownload: this.biodiCsvToDownload})
            }

        },

        created() {
            this.getBiodiCsvMetas()
        }
    }
</script>

<style scoped>

</style>