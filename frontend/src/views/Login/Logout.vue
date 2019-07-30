<template>
    <div>
        <el-alert
                v-show="error"
                :title="error"
                type="error"
                show-icon
                @close="setError({error: null})">
        </el-alert>
        <el-row>
            <el-col :span="12" :offset="6">
                <el-button class="logout" type="success" @click="handleLogout">Logout</el-button>
            </el-col>
        </el-row>
    </div>
</template>

<script>
    import {mapActions, mapGetters} from "vuex";
    import * as types from "../../store/modules/User/types.js"

    export default {
        name: "Logout",
        computed: {
            ...mapGetters({
                error: 'user/error'
            })
        },
        methods: {
            ...mapActions({
                'logout': types.LOGOUT,
                'setError': types.SET_ERROR

            }),

            handleLogout() {
                this.logout()
            }
        }
    }
</script>

<style scoped>
    .logout {
        margin-top: 2%;
    }
</style>