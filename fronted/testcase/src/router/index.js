import { createRouter, createWebHistory } from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Layout from '@/components/Layout'
import Login from '@/components/Login/Login'
import HomeMain from '@/components/HomeMain'
import TestCaseTable from '@/components/Appmain/TestCaseTable'
import tabletest from '@/components/Appmain/Test/tabletest'
import TableT1 from '@/components/Appmain/Test/TableT1'


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
        component: TestCaseTable
    }, {
        path: '/Test',
        component: tabletest
    }, {
        path: '/Test2',
        component: TableT1
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router