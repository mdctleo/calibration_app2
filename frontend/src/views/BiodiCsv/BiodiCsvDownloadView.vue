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
            <BiodiCsvDownload :metas="metas" @download-complete="handleDownloadComplete" @download-raw="handleDownloadRaw"></BiodiCsvDownload>
        </el-row>
    </div>
</template>

<script>
    import {mapActions, mapGetters} from 'vuex';
    import * as types from '../../store/modules/BiodiCsv/BiodiCsvDownloadTypes.js'
    import BiodiCsvDownload from "./components/BiodiCsvDownload";
    export default {
        name: "BiodiCsvDownloadView",
        components: {BiodiCsvDownload},
        computed: {
            ...mapGetters({
                metas: 'biodiCsvDownload/metas',
                biodiCsvCompleteToDownload: 'biodiCsvDownload/biodiCsvCompleteToDownload',
                biodiCsvRawToDownload: 'biodiCsvDownload/biodiCsvRawToDownload',
                error: 'biodiCsvDownload/error',
                loading: 'biodiCsvDownload/loading'
            })
        },
        methods: {
            ...mapActions({
                'downloadBiodiCsvComplete': types.DOWNLOAD_BIODI_CSV_COMPLETE,
                'downloadBiodiCsvRaw': types.DOWNLOAD_BIODI_CSV_RAW,
                'getBiodiCsvMetas': types.GET_BIODI_CSV_METAS,
                'setError': types.SET_ERROR
            }),

            handleDownloadComplete() {
                this.downloadBiodiCsvComplete({biodiCsvCompleteToDownload: this.biodiCsvCompleteToDownload})
            },

            handleDownloadRaw() {
                this.downloadBiodiCsvRaw({biodiCsvRawToDownload: this.biodiCsvRawToDownload})
            }

        },

        created() {
            this.getBiodiCsvMetas()
        }
    }
</script>

<style scoped>

</style>