<template>
    <div id="app">
        <el-container class="app-container">
            <el-header id="header">Pre-Clinic</el-header>
            <el-container>
                <el-aside id="nav" class="nav" v-show="isLoggedIn">
                    <el-menu class="menu"
                             default-active="1"
                             :router="true">
                        <el-menu-item index="1" route="/dashboard">
                            <template slot="title">
                                <i class="el-icon-s-home"></i>
                                <span>Dashboard</span>
                            </template>
                        </el-menu-item>
                        <el-submenu index="2">
                            <template slot="title">
                                <i class="el-icon-s-data"></i>
                                <span>Biodi</span>
                            </template>
                            <el-menu-item index="2-1" route="/calibration">Calibration Factors</el-menu-item>
                            <el-menu-item index="2-2" route="/biodicsv/upload">Biodi CSV Upload</el-menu-item>
                            <el-menu-item index="2-3" route="/biodicsv/download">Biodi CSV Download</el-menu-item>
                        </el-submenu>
                        <el-submenu index="3" route="/statistics">
                            <template slot="title">
                                <i class="el-icon-s-operation"></i>
                                <span>Statistics</span>
                            </template>
                            <el-menu-item index="3-1" route="/effect">Effect Size</el-menu-item>
                            <el-menu-item index="3-2" route="/nobs">Sample Size</el-menu-item>
                            <el-menu-item index="3-3" route="/power">Statistical Power</el-menu-item>
                        </el-submenu>
                        <el-menu-item index="4" route="/logout">
                            <template slot="title">
                                <i class="el-icon-user-solid"></i>
                                <span>Logout</span>
                            </template>
                        </el-menu-item>
                    </el-menu>
                </el-aside>
                <router-view class="view"/>
            </el-container>
        </el-container>
    </div>
</template>

<script>
    import {mapActions, mapGetters} from "vuex";
    export default {
        computed: {
            ...mapGetters({
                isLoggedIn: 'user/isLoggedIn'
            })
        }
    }

</script>

<style>
    #app {
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
        height: 100%;
        min-height: 100vh;
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
    }

    .menu {
        height: 100%;
        min-height: 100vh;
        /*background-color: #0e0c28;*/
    }

    .view {
        width:100vw;
        height: 100%;
        min-height: 100vh;
        background-color: #efeff6;
    }


</style>
