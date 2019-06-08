<template>
    <div>
        <el-button
                type="primary"
                @click="addTab()"
                class="controls"
        >
            Add Mouse
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
                    title: 'New Mouse',
                    name: newTabName
                });
                this.currTab = newTabName;
                this.index++;
            },
            removeTab(targetName) {
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
            }
        }
    }
</script>

<style scoped>
    .controls {
        margin-top: 2%;
        margin-bottom: 2%;
    }
</style>