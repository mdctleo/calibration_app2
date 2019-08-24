<template>
    <div>
        <el-table
                class="el-table"
                ref="multipleTable"
                :data="metas">
            <el-table-column
                    class="el-table-column"
                    property="studyDate"
                    label="Study Date">
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
                <template slot="header" slot-scope="scope">
                    <el-input

                            v-model="search"
                            size="mini"
                            placeholder="Type to search"/>
                </template>
                <template slot-scope="scope">
                    <el-button
                            size="mini"
                            type="primary"
                            @click="handleDownloadComplete(scope.$index, scope.row)">Download Complete</el-button>
                    <el-button
                            size="mini"
                            type="primary"
                            @click="handleDownloadRaw(scope.$index, scope.row)">Download Raw</el-button>
                    <el-button
                        size="mini"
                        type="primary"
                        @click="handleDownloadAnalysis(scope.$index, scope.row)"
                    >Download Analysis</el-button>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>

<script>
    import {mapActions} from 'vuex';
    import * as types from '../../../store/modules/BiodiCsvDownload/BiodiCsvDownloadTypes.js'
    export default {
        name: "BiodiCsvDownload",
        props: {
            metas: Array
        },

        data() {
            return {
                search: ''
            }
        },

        methods: {
            ...mapActions({
                'setBiodiCsvToDownload': types.SET_BIODI_CSV_TO_DOWNLOAD
            }),
            handleDownloadComplete(index, row) {
                this.setBiodiCsvToDownload({biodiCsvToDownload: row.id});
                this.$emit('download-complete');
            },

            handleDownloadRaw(index, row) {
                this.setBiodiCsvToDownload({biodiCsvToDownload: row.id})
                this.$emit('download-raw')
            },

            handleDownloadAnalysis(index, row) {
                this.setBiodiCsvToDownload({biodiCsvToDownload: row.id})
                this.$emit('download-analysis')
            },

            filterMetas(metas, search) {
                console.log(metas)
                metas.filter((meta) => {
                    return meta.studyName.toLowerCase().includes(search) ||
                            meta.studyDate.toLowerCase().includes(search) ||
                            meta.piName.toLowerCase().includes(search) ||
                            meta.isotopeName.toLowerCase().includes(search) ||
                            meta.chelatorName.toLowerCase().includes(search) ||
                            meta.vectorName.toLowerCase().includes(search) ||
                            meta.target.toLowerCase().includes(search) ||
                            meta.cellLineName.toLowerCase().includes(search) ||
                            meta.tumorModelName.toLowerCase().includes(search) ||
                            meta.mouseStrainName.toLowerCase().includes(search) ||
                            meta.gammaCounger.toLowerCase().includes(search)

                })
            }
        },
    }
</script>

<style scoped>
    .el-table {
        width: 95%;
        height: 100%;
        margin-left: auto;
        margin-right: auto;
        margin-top: 2%;
    }
    .el-table-column{
        width: 100%;
    }

    .el-table th {
        text-align: center !important;
    }

</style>