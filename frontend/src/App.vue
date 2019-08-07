<template>
    <div id="app" class="app-container">
        <el-container>
            <el-header id="header">Pre-Clinic</el-header>
        </el-container>
        <el-container>
                <el-menu class="nav"
                         default-active="1"
                         :router="true"
                         :collapse=isCollapse
                         v-show="isLoggedIn">
                    <el-menu-item index="1" route="/dashboard">
                        <i class="el-icon-s-home"></i>
                        <span slot="title">Dashboard</span>
                    </el-menu-item>
                    <el-submenu index="2">
                        <template slot="title">
                            <i class="el-icon-s-data"></i>
                            <span slot="title">Biodi</span>
                        </template>
                        <el-menu-item index="2-1" route="/calibration">Calibration Factors</el-menu-item>
                        <el-menu-item index="2-2" route="/biodicsv/upload">Biodi CSV Upload</el-menu-item>
                        <el-menu-item index="2-3" route="/biodicsv/download">Biodi CSV Download</el-menu-item>
                    </el-submenu>
                    <el-submenu index="3" route="/statistics">
                        <template slot="title">
                            <i class="el-icon-s-operation"></i>
                            <span slot="title">Statistics</span>
                        </template>
                        <el-menu-item index="3-1" route="/effect">Effect Size</el-menu-item>
                        <el-menu-item index="3-2" route="/nobs">Sample Size</el-menu-item>
                        <el-menu-item index="3-3" route="/power">Statistical Power</el-menu-item>
                    </el-submenu>
                    <el-menu-item index="4" route="/logout">
                        <i class="el-icon-user-solid"></i>
                        <span slot="title">Logout</span>
                    </el-menu-item>
                </el-menu>
            <el-main class="view">
                <router-view/>
            </el-main>
        </el-container>
    </div>
</template>

<script>
    import {mapGetters} from "vuex";

    export default {
        data() {
            return {
                isCollapse: false,
                windowWidth: 0
            }
        },
        computed: {
            ...mapGetters({
                isLoggedIn: 'user/isLoggedIn',
            })
        },

        watch: {
            windowWidth: function (newWidth, oldWidth) {
                if (newWidth <= 700) {
                    this.isCollapse = true
                } else {
                    this.isCollapse = false
                }
            }
        },

        mounted() {
            this.$nextTick(() => {
                window.addEventListener('resize', () => {
                    this.windowWidth = window.innerWidth
                });
            })
        }
    }

</script>

<style scoped>
    #app {
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
        position: relative;
        height: 100%;
        width: 100%;
    }

    .app-container {
        height: 100%;
        min-height: 100vh;
    }

    #header {
        font-size: xx-large;
        float: left;
        text-align: left;
        color: #0DBFD5;
        border-bottom: 2px solid #0DBFD5;
    }

    .nav {
        height: 100%;
        min-height: 100vh;
        width: 15% !important;
        text-align: center;
    }

    .menu {
        height: 100%;
        min-height: 100vh;
        /*background-color: #0e0c28;*/
    }

    .view {
        min-height: calc(100vh - 50px);
        width: 85%;
        position: relative;
        overflow: hidden;
        /*width:100vw;*/
        /*height: 100%;*/
        /*min-height: 100vh;*/
        background-color: #efeff6;
    }


</style>
