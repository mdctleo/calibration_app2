<template>
    <div class="form">
        <el-form :model="loginForm" ref="form" :rules="rules" label-width="120px" label-position="top">
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Email" prop="email">
                        <el-input v-model="email" placeholder="Enter your BCCRC email"></el-input>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="Password" prop="password">
                        <el-input v-model="password" type="password" placeholder="Enter your password"
                                  show-password></el-input>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-button type="success"@click="handleLogin">Login</el-button>
                </el-col>
            </el-row>
        </el-form>
    </div>
</template>

<script>
    import {mapActions, mapGetters} from "vuex";
    import * as types from "../../store/modules/User/types.js"

    export default {
        name: "Login",
        data() {
            return {
                rules: {
                    email: [
                        {required: true, message: 'Please input your BCCRC email', trigger: 'blur'},
                        {type: 'email', message: 'Please input a valid email format', trigger: 'blur'}
                    ],

                    password: [
                        {required: true, message: 'Please input your password', trigger: 'blur'}
                    ]
                }
            }
        },

        computed: {
            ...mapGetters({
                getLoginForm: 'user/loginForm',
                getEmail: 'user/email',
                getPassword: 'user/password'
            }),

            loginForm: {
                get() {
                    return this.getLoginForm
                },

                set(value) {
                }
            },

            email: {
                get() {
                    return this.getEmail
                },

                set(value) {
                    this.setEmail({email: value})
                }
            },

            password: {
                get() {
                    return this.getPassword
                },

                set(value) {
                    this.setPassword({password: value})
                }
            }
        },

        methods: {
            ...mapActions({
                'setEmail': types.SET_EMAIL,
                'setPassword': types.SET_PASSWORD,
                'login': types.LOGIN
            }),

            handleLogin() {
                this.login({loginForm: this.loginForm})
            }
        }
    }
</script>

<style scoped>
    .form {
        margin-top: 2%;
    }
</style>