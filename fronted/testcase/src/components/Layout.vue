<template>
  <div>
    <base href=".components/source/" />
    <!-- 引入样式 -->
    <link
      rel="stylesheet"
      href="https://unpkg.com/element-ui/lib/theme-chalk/index.css"
    />
    <!-- 使用子组件,使用-，不建议使用驼峰 -->
    <app-header ></app-header>
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
    this.initOptions();
    if (
      this.$route.params.userName &&
      this.$route.params.userWork &&
      this.$route.params.userId
    ) {
      this.userName = this.$route.params.userName;
      this.userWork = this.$route.params.userWork;
      this.userId = this.$route.params.userId;
    } else {
      //若尚未登录，跳转到登录界面
      this.$router.replace({
        name: "Login",
        params: {},
      });
    }
  },
  setup() {},
  data() {
    return {
      userName: "西子卡",
      userId: 1,
      userWork: "QA",
      options: {
        QAs: [],
        caseTypes: [],
        caseSystems: [],
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
     * 初始化全局选项
     */
    initOptions() {
      this.getQAPeoData();
      this.getProjectPeoData();
      this.getProjectSystemsData();
    },
    /**
     * 初始化QA组数据（只有QA可以修改和创建测试用例）
     */
    getQAPeoData() {
      axios.get("getQAPeoData").then((res) => {
        //console.log(res.data.msg);
        var option = this.initOptionArray(res.data.msg, "peoId", "peoName");
        this.options.QAs = option;
      });
    },
    /**
     * 输入数组，选项名，
     * keyName ，valueName
     * 输出option数组(直接引用修改了)
     */
    initOptionArray(data, keyName, valName) {
      var options = [];
      for (var d = 0; d < data.length; d++) {
        options.unshift({
          key: data[d][keyName],
          value: data[d][valName],
        });
      }
      return options;
    },
    /**
     * 初始化项目组人员数据（QA,策划和程序,PM）
     */
    getProjectPeoData() {
      axios.get("getProjectPeos").then((res) => {
        //console.log(res.data.msg);
        var option = this.initOptionArray(res.data.msg, "peoId", "peoName");
        this.options.peos = option;
      });
    },
    /**
     * 初始化项目测试用例系统选项
     * fatherId =-1,且类型是fileType的即为系统名节点
     */
    getProjectSystemsData() {
      axios.get("getProjectSystemsData").then((res) => {
        //console.log(res.data.msg);
        this.options.caseSystems = res.data.msg;
        var option = this.initOptionArray(res.data.msg, "caseId", "caseName");
        this.options.caseSystems = option;

        this.$bus.emit("UPDATE_SELETOR_DATA", {
          options: this.options,
        }); //更新选项数据
      });
    },
    /**
     * 初始化项目测试用例标签数据
     */
    getProjectTestCaseTagData() {
      axios.get("get").then((res) => {
        //console.log(res.data.msg);
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
