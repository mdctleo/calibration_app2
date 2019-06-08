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
            <BiodiCsvDownload :metas="metas" @download="handleDownload"></BiodiCsvDownload>
        </el-row>
    </div>
</template>

<script>
    import {mapActions, mapGetters} from 'vuex';
    import * as types from '../../store/modules/BiodiCsv/types.js'
    import BiodiCsvDownload from "./components/BiodiCsvDownload";
    export default {
        name: "BiodiCsvDownloadView",
        components: {BiodiCsvDownload},
        computed: {
            ...mapGetters({
                metas: 'biodiCsvDownload/metas',
                biodiCsvToDownload: 'biodiCsvDownload/biodiCsvToDownload',
                error: 'biodiCsvdownload/error',
                loading: 'biodiCsvDownload/loading'
            })
        },
        methods: {
            ...mapActions({
                'downloadBiodiCsv': types.DOWNLOAD_BIODI_CSV,
                'getBiodiCsvMetas': types.GET_BIODI_CSV_METAS,
                'setError': types.SET_ERROR
            }),

            handleDownload() {
                this.downloadBiodiCsv({biodiCsvToDownload: this.biodiCsvToDownload})
            }

        },

        created() {
            this.getBiodiCsvMetas()
        }
    }
</script>

<style scoped>

</style>