<template>
    <div>
        <el-table
                class="el-table"
                ref="multipleTable"
                :data="this.metas">
            <el-table-column
                    class="el-table-column"
                    property="createdOn"
                    label="Date">
            </el-table-column>
            <el-table-column
                    class="el-table-column"
                    property="studyName"
                    label="Study Name">
            </el-table-column>
            <el-table-column
                    class="el-table-column"
                    property="researcherName"
                    label="Researcher">
            </el-table-column>
            <el-table-column
                    label="Operations">
                <template slot-scope="scope">
                    <el-button
                            size="mini"
                            type="primary"
                            @click="handleDownload(scope.$index, scope.row)">Download Complete Study</el-button>
                    <el-button
                            size="mini"
                            type="primary"
                            @click="handleDownload(scope.$index, scope.row)">Download Raw Biodicsv</el-button>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>

<script>
    import {mapActions} from 'vuex';
    import * as types from '../../../store/modules/BiodiCsv/BiodiCsvDownloadTypes.js'
    export default {
        name: "BiodiCsvDownload",
        props: {
            metas: Array
        },

        methods: {
            ...mapActions({
                'setBiodiCsvToDownload': types.SET_BIODI_CSV_TO_DOWNLOAD
            }),
            handleDownload(index, row) {
                this.setBiodiCsvToDownload({biodiCsvToDownload: row.id});
                this.$emit('download');
            }
        }
    }
</script>

<style scoped>
    .el-table {
        width: 95%;
        height: 100%;
        margin-left: auto;
        margin-right: auto;
        margin-top: 5%;
    }
    .el-table-column{
        width: 100%;
    }

</style>