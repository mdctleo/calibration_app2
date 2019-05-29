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
                    property="fileName"
                    label="file name">
            </el-table-column>
            <el-table-column
                    class="el-table-column"
                    property="createdBy"
                    label="created By">
            </el-table-column>
            <el-table-column
                    label="Operations">
                <template slot-scope="scope">
                    <el-button
                            size="mini"
                            type="primary"
                            @click="handleDownload(scope.$index, scope.row); $emit('download')">Download</el-button>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>

<script>
    import store from '../../../store/Store.js'
    import * as type from '../../../store/Types'
    export default {
        name: "BiodiCsvDownload",
        props: {
            metas: Array
        },
        computed: {
          biodiCsvToDownload: {
              get () {
                  return store.state.biodiCsvToDownload
              },
              set (id) {
                  store.dispatch({
                      type: type.setBiodiCsvToDownload,
                      biodiCsvToDownload: id
                  })
              }
          }
        },

        methods: {
            handleDownload(index, row) {
                this.biodiCsvToDownload = row.id
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