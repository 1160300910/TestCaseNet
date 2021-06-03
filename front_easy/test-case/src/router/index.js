import { createRouter, createWebHistory } from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Layout from '@/components/Layout'
import Login from '@/components/Login/Login'

const routerHistory = createWebHistory()
const router = createRouter({
    history: routerHistory,
    routes: [{
            path: '/HelloWorld',
            name: 'HelloWorld',
            component: HelloWorld
        },
        {
            path: '/',
            name: 'Login', // 路由名称
            component: Login // 组件对象
        },
        {
            path: '/Layout',
            name: 'Layout', // 路由名称
            component: Layout // 组件对象
        }
    ]
})
export default router