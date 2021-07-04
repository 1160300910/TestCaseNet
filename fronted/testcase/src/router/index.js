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
import TestToDo from '@/components/Test/TestToDo'
import RightMenu from '@/components/Appnavbar/ChooseOption/RightMenu'

import UserDataManager from '@/components/AppUserManager/UserDataManager'

const routes = [{
        path: '/UserDataManager',
        component: UserDataManager
    }, {
        path: '/RightMenu',
        component: RightMenu
    }, {
        path: '/TestToDo',
        component: TestToDo
    },
    {
        path: '/HelloWorld',
        component: HelloWorld
    },
    {
        path: '/Layout',
        name: 'Layout', // 路由名称
        component: Layout, // 组件对象
        meta: {
            needLogin: true
        },
    },
    {
        path: '/Login',
        name: 'Login', // 路由名称
        component: Login, // 组件对象
        meta: {
            needLogin: false
        }
    },
    {
        path: '/',
        name: 'HomeMain',
        component: HomeMain, // 组件对象
        meta: {
            needLogin: false
        }
    }, {
        path: '/Testcase',
        component: TestCaseTable
    }, {
        path: '/RegisterPage',
        name: 'RegisterPage',
        component: RegisterPage,
        meta: {
            needLogin: false
        }
    },
    {
        path: '/ModifyUserInfoPage',
        name: 'ModifyUserInfoPage',
        component: ModifyUserInfoPage,

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