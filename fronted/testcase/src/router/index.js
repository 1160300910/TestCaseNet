import { createRouter, createWebHistory } from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Layout from '@/components/Layout'
import Login from '@/components/Login/Login'
import HomeMain from '@/components/HomeMain'
import TestCaseTable from '@/components/Appmain/TestCaseTable'
import RegisterPage from '@/components/Login/RegisterPage'
import ModifyUserInfoPage from '@/components/Login/ModifyUserInfoPage'
import TableT1 from '@/components/Appmain/Test/TableT1'
import test from '@/components/Appnavbar/Test/test'
import TreeTest from '@/components/Appnavbar/Test/TreeTest'
import NavbarMain from '@/components/Appnavbar/NavbarMain'


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
        path: '/RegisterPage',
        name: 'RegisterPage',
        component: RegisterPage
    },
    {
        path: '/ModifyUserInfoPage',
        name: 'ModifyUserInfoPage',
        component: ModifyUserInfoPage
    }, {
        path: '/Test1',
        component: TableT1
    }, {
        path: '/Test2',
        component: test
    }, {
        path: '/TestTree',
        component: TreeTest
    }, {
        path: '/NavbarMain',
        component: NavbarMain
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router