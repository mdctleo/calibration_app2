<template>
    <div id="app">
        <!--    <div id="nav">-->
        <!--      <router-link to="/">Calibration</router-link> |-->
        <!--      <router-link to="/csv">Csv</router-link>-->
        <!--    </div>-->
        <el-col :span="12" type="flex">
            <el-menu
                    default-active="2"
                    @open="handleOpen"
                    @close="handleClose">
                <el-menu-item index="1">
                    <template slot="title">
                        <i class="el-icon-location"></i>
                        <span>Navigator One</span>
                    </template>
                </el-menu-item>
                <el-menu-item index="2">
                    <i class="el-icon-menu"></i>
                    <span>Navigator Two</span>
                </el-menu-item>
                <el-menu-item index="3">
                    <i class="el-icon-setting"></i>
                    <span>Navigator Four</span>
                </el-menu-item>
            </el-menu>
        </el-col>
        <router-view/>
    </div>
</template>

<script>

</script>

<style>
    #app {
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
        height: 100vh;
    }

    #nav {
        height: 100%;
    }


</style>
