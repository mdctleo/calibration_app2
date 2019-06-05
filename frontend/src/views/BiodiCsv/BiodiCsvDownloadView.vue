<template>
    <div>
        <el-alert
                v-show="error"
                :title="error"
                type="error"
                show-icon
                @close="error = null">
        </el-alert>
        <el-row>
            <BiodiCsvDownload :metas="this.metas" @download="downloadBiodiCsvs"></BiodiCsvDownload>
        </el-row>
    </div>
</template>

<script>
    export default {
        name: "BiodiCsvDownload"
    }
</script>

<style scoped>

</style>