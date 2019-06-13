<template>
    <div>
<!--        <el-button-->
<!--                type="primary"-->
<!--                @click="addTab()"-->
<!--                class="controls"-->
<!--        >-->
<!--            Add Mouse-->
<!--        </el-button>-->
<!--        <el-tabs v-model="currTab" type="card" closable @tab-remove="removeTab">-->
<!--            <el-tab-pane-->
<!--                    v-for="(item, index) in mouseForms"-->
<!--                    :key="item.name"-->
<!--                    :name="item.name"-->
<!--                    :label="item.title"-->
<!--            >-->
<!--               <MouseForm :bus="bus" @validated-one-form="handleValidated"></MouseForm>-->
<!--            </el-tab-pane>-->
<!--        </el-tabs>-->
        <el-button type="success" @click="downloadMouseCsvFormat">Download Csv Format</el-button>
    </div>
</template>

<script>
    import MouseForm from "./MouseForm";
    import {mapActions, mapGetters} from "vuex";
    import * as types from '../../../store/modules/BiodiCsv/types'
    export default {
        name: "BiodiCsvMouseInfo",
        components: {MouseForm},
        props: {
            bus: Object
        },
        data() {
            return {
                mouseForms: [],
                index: 0,
                currTab: "",
                numValidatedForms: 0
            }
        },

        methods: {
            ...mapActions({
                'downloadMouseCsvFormat': types.DOWNLOAD_MOUSE_CSV_FORMAT
            }),
            addTab () {
                let newTabName = String("Mouse " + this.index);
                this.mouseForms.push({
                    title: 'New Mouse',
                    name: newTabName,
                    content: "MouseForm"
                });
                this.currTab = newTabName;
                this.index++;
            },
            removeTab (targetName) {
                let tabs = this.mouseForms;
                let activeName = this.currTab;
                if (activeName === targetName) {
                    // if you close the current tab you are on right now
                    tabs.forEach((tab, index) => {
                        if (tab.name === targetName) {
                            // find the closing active tab, set the active tab to
                            // either the previous or next one
                            // if it exists
                            let nextTab = tabs[index + 1] || tabs[index - 1];
                            if (nextTab) {
                                activeName = nextTab.name;
                            }
                        }
                    });
                }
                // set new active tab
                this.currTab = activeName;
                // remove the closed tab
                this.mouseForms = tabs.filter(tab => tab.name !== targetName);
            },

            handleValidated () {
                this.numValidatedForms++;

                if (this.numValidatedForms === this.mouseForms.length) {
                    console.log("mouse forms validated");
                    this.$emit('validated', true)
                } else {
                    console.log("mouse forms not validated")
                    this.$emit('validated', false)
                }
            }
        },
    }
</script>

<style scoped>
    .controls {
        margin-top: 2%;
        margin-bottom: 2%;
    }
</style>