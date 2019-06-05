<template>
    <div v-loading="loading">
        <el-alert
                v-show="error"
                :title="error"
                type="error"
                show-icon
                @close="error = null">
        </el-alert>
        <el-row>
            <BiodiCsvDownload :metas="this.metas" @download="this.downloadBiodiCsv()"></BiodiCsvDownload>
        </el-row>
    </div>
</template>

<script>
    import {mapActions, mapGetters} from 'vuex';
    import * as types from '../../store/modules/BiodiCsv/types.js'
    export default {
        name: "BiodiCsvDownload",
        computed: {
            ...mapGetters({
                metas: 'metas',
                error: 'biodiCsvDownloadError',
                loading: 'biodiCsvDownloadLoading'
            })
        },
        methods: {
            ...mapActions([
                types.DOWNLOAD_BIODI_CSV,
                types.GET_BIODI_CSV_METAS
            ])

        },

        created() {
            this.getBiodiCsvMetas()
        }
    }
</script>

<style scoped>

</style>