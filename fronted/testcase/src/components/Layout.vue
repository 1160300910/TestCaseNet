<template>
  <div>
    <base href=".components/source/" />
    <!-- 引入样式 -->
    <link
      rel="stylesheet"
      href="https://unpkg.com/element-ui/lib/theme-chalk/index.css"
    />
    <!-- 使用子组件,使用-，不建议使用驼峰 -->
    <app-header></app-header>
    <app-navbar></app-navbar>
    <app-main></app-main>
  </div>
</template>

<script>
// 会导入./AppHeader下面的index.vue组件
import AppHeader from "./Apphead/HeadMain";
import AppNavbar from "./Appnavbar/NavbarMain";
import AppMain from "./Appmain/AppMain";
import { ref } from "vue";

import axios from "axios";
// 导入子组件，缩写格式 AppHeader: AppHeader
export default {
  created() {
    if (this.$route.params.userName && this.$route.params.userWork) {
      this.userName = this.$route.params.userName;
      this.userWork = this.$route.params.userWork;
    }
  },
  setup() {},
  data() {
    return {
      options: {
        QAs: [],
        caseTypes: [],
        peos: [], //策划，qa，和程序,PM
        tags: [],
        test_level: [
          {
            value: "P0",
            label: "P0",
          },
          {
            value: "P1",
            label: "P1",
          },
          {
            value: "P2",
            label: "P2",
          },
          {
            value: "P3",
            label: "P3",
          },
          {
            value: "P4",
            label: "P4",
          },
        ],
      },
      node_data: "",
      choice: "",
      nowChildren: "",
      nowParent: "",
      userName: "西子卡",
      userId: 1,
      userWork: "QA",
      table_datas: {}, //节点数据列表
      nodes_data: "", //节点数据树
    };
  },
  provide() {
    return {
      parentObj: this,
    };
  },
  components: { AppHeader, AppNavbar, AppMain },
  methods: {
    /**
     * 初始化QA组数据（只有QA可以修改和创建测试用例）
     */
    getQAPeoData() {
      axios.get("getQAPeoData").then((res) => {
        console.log(res.data.msg);
        this.options.QAs = res.data.msg;
      });
    },
    /**
     * 初始化项目组人员数据（QA,策划和程序,PM）
     */
    getProjectPeoData() {
      axios.get("getProjectPeos").then((res) => {
        console.log(res.data.msg);
        this.options.peos = res.data.msg;
      });
    },
    /**
     * 初始化项目测试用例类型数据
     */
    getProjectTypeData() {
      axios.get("？？？").then((res) => {
        console.log(res.data.msg);
        this.options.peos = res.data.msg;
      });
    },
    /**
     * 初始化项目测试用例标签数据
     */
    getProjectTestCaseTagData() {
      axios.get("？？？").then((res) => {
        console.log(res.data.msg);
        this.options.peos = res.data.msg;
      });
    },
  },
};
</script>

<style scoped>
/* 头部样式 */
.header {
  align-items: center;
  display: flex;
  flex: 1;
  justify-content: space-around;
  flex-direction: row;
  color: aliceblue;
  position: absolute;
  line-height: 50px;
  top: 0px;
  left: 0px;
  right: 0px;
  background-color: #2d3a4b;
}

/* 左侧样式 */
.navbar {
  position: absolute;
  width: 280px;
  top: 50px; /* 距离上面50像素 */
  left: 0px;
  bottom: 0px;
  overflow-y: auto; /* 当内容过多时y轴出现滚动条 */
  background-color: #545c64;
}

/* 主区域 */
.main {
  display: flex;
  flex: 1;
  flex-direction: column;
  position: absolute;
  top: 50px;
  left: 280px;
  bottom: 0px;
  right: 0px; /* 距离右边0像素 */
  padding: 10px;
  overflow-y: auto; /* 当内容过多时y轴出现滚动条 */
  /* background-color: red; */
}
</style>
