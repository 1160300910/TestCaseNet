import { createRouter, createWebHistory } from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Layout from '@/components/Layout'
import Login from '@/components/Login/Login'
import HomeMain from '@/components/HomeMain'
import TestCaseTableTest from '@/components/Appmain/TestCaseTableTest'
import tabletest from '@/components/Appmain/Test/tabletest'


const routes = [{
        path: '/HelloWorld',
        component: HelloWorld
    },
    {
        path: '/Layout',
        name: 'Layout', // 路由名称
        component: Layout // 组件对象
    },
    {
        path: '/Login',
        name: 'Login', // 路由名称
        component: Login // 组件对象
    },
    {
        path: '/',
        component: HomeMain // 组件对象
    }, {
        path: '/Testcase',
        component: TestCaseTableTest
    }, {
        path: '/Test',
        component: tabletest
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router