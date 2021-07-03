import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus';
import 'element-plus/lib/theme-chalk/index.css';
import axios from "axios";
import router from "./router"
import mitt from "mitt"
import { store } from '@/store/store.js'

//const app = createApp(App).mount('#app')
const app = createApp(App)
app.use(ElementPlus)
app.use(router)
app.mount('#app')
    //挂载事务总线
app.config.globalProperties.$bus = new mitt()
    //app.prototype.GLOBAL = global_

axios.defaults.timeout = 5000 // 请求超时
axios.defaults.baseURL = '/testcase/';

router.beforeEach((to, from, next) => {
    //获取用户登录成功后储存的登录标志
    //let getFlag = localStorage.getItem("FLAG");console.log(getFlag)
    if (to.meta.needLogin) {

        let TOKEN = localStorage.getItem("TOKEN")
        if (TOKEN != -1) {
            //如果有token，监测token是否过期，
            axios
                .post("/parseUserToken", {
                    token: TOKEN
                })
                .then((res) => {
                    console.log(res.data);
                    if (!res.data.expiled && to.meta.needLogin) {
                        //alert("没有过期")
                        //如果已登录，还想想进入登录注册界面，则定向回已经注册后的界面
                        store.setUserData(res.data.userId, res.data.userName, res.data.peoType)
                        next()
                    } else if (res.data.expiled) {
                        store.setUserData('', '', '')
                        localStorage.setItem("TOKEN", -1)
                        alert("登录态过期了或者异常!!")
                        next({
                            path: '/Login',
                        })
                    }
                })
                .catch(function(error) {
                    localStorage.setItem("TOKEN", -1)
                    alert("Error " + error);
                    store.setUserData('', '', '')
                    next()
                });

        } else {
            //如果登录标志不存在，即未登录
            //用户想进入需要登录的页面，则定向回登录界面
            if (to.meta.isLogin) {
                next({
                    path: '/Login',
                })
                alert("请先登录")
                    //用户进入无需登录的界面，则跳转继续
            } else {
                next()
            }

        }
    } else {
        console.log("不需要登录")
        next()
    }
});

router.afterEach(route => {
    window.scroll(0, 0);
});