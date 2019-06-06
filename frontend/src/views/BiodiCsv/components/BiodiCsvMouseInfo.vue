<template>
    <div>
        <el-button
                size="small"
                @click="addTab()"
        >
            add tab
        </el-button>
        <el-tabs v-model="currTab" type="card" closable @tab-remove="removeTab">
            <el-tab-pane
                    v-for="(item, index) in mouseForms"
                    :key="item.name"
                    :name="item.name"
                    :label="item.title"
            >
                <MouseForm></MouseForm>
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script>
    import MouseForm from "./MouseForm";
    export default {
        name: "BiodiCsvMouseInfo",
        components: {MouseForm},
        data() {
            return {
                mouseForms: [],
                index: 0,
                currTab: ""
            }
        },

        methods: {
            addTab() {
                let newTabName = String("Mouse " + this.index);
                this.mouseForms.push({
                    title: newTabName,
                    name: newTabName
                });
                this.currTab = newTabName;
                this.index++;
            },
            removeTab(targetName) {
                let tabs = this.editableTabs;
                let activeName = this.editableTabsValue;
                if (activeName === targetName) {
                    tabs.forEach((tab, index) => {
                        if (tab.name === targetName) {
                            let nextTab = tabs[index + 1] || tabs[index - 1];
                            if (nextTab) {
                                activeName = nextTab.name;
                            }
                        }
                    });
                }

                this.editableTabsValue = activeName;
                this.editableTabs = tabs.filter(tab => tab.name !== targetName);
            }
        }
    }
</script>

<style scoped>
   .tabs {

   }
</style>