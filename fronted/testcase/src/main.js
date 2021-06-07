import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus';
import 'element-plus/lib/theme-chalk/index.css';
import axios from "axios";
import router from "./router"
import mitt from "mitt"

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