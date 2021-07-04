<template>
  <div>
    <!--base href=".components/source/" /-->
    <!-- 引入样式 -->
    <!--link
      rel="stylesheet"
      href="https://unpkg.com/element-ui/lib/theme-chalk/index.css"
    /-->
    
    <!-- 使用子组件,使用-，不建议使用驼峰 -->
    <app-header
      :style="{
        'background-color': work_head_bk_color,
        color: work_head_font_color,
      }"
      :headSrc="headSrc"
    ></app-header>
    
    <app-navbar :style="{ 'background-color': work_nav_bk_color }"></app-navbar>

    <selector-main></selector-main>
    <app-main></app-main>

    <right-menu></right-menu>
    <second-menu-dialogs></second-menu-dialogs>>
  </div>
</template>

<script>
// 会导入./AppHeader下面的index.vue组件
import AppHeader from "./Apphead/HeadMain";
import AppNavbar from "./Appnavbar/NavbarMain";
import RightMenu from "./Appnavbar/ChooseOption/RightMenu.vue";
import AppMain from "./Appmain/AppMain";
import SelectorMain from "./AppSelector/SelectorMain";
import { store } from '@/store/store.js'
import { ref } from "vue";

import axios from "axios";
import SecondMenuDialogs from './Appnavbar/ChooseOption/SecondMenu/SecondMenuDialogs.vue';
// 导入子组件，缩写格式 AppHeader: AppHeader
const peoHeads = [
  {
    img: "/icons/048-woman.png",
    work: "QA",
    key: "1",
    background_head: "rgb(94,139,126)",
    background_nav: "rgb(167,196,188)",
    font: "rgb(223,238,234)",
  },
  {
    img: "/icons/010-woman.png",
    work: "策划",
    key: "2",
    background_head: "rgb(144,127,164)",
    background_nav: "rgb(165,143,170)",
    font: "white",
  },
  {
    img: "/icons/005-man.png",
    work: "程序",
    key: "3",
    background_head: "rgb(45,58,75)",
    background_nav: "rgb(84,92,100)",
    font: "white",
  },
  {
    img: "/icons/016-woman.png",
    work: "PM",
    key: "4",
    background_head: "rgb(255,216,204)",
    background_nav: "rgb(252, 229, 222)",
    font: "rgb(10,29,55)",
  },
];
export default {
  components: { AppHeader, AppNavbar, AppMain, RightMenu, SelectorMain, SecondMenuDialogs },
  mounted() {
    this.getRoleData(this.userWork);
  },
  beforeUnmount() {
    //console.log(this.$bus);
    this.$bus.all.clear();
    /*
      this.$bus.all.delete("CHANGE_TESTCASE_FOLDER_BY_POP")
      this.$bus.all.delete("CHANGE_TESTCASE_FOLDER_BY_POP",{});
      this.$bus.all.delete("CHANGE_CURRENT_TREENODE_FROM_TABLE");
      this.$bus.all.delete("UPDATE_FATHER_TABLE_DATAS");
      this.$bus.all.delete("CASE_NAME_TABLE_CHANGE");
      this.$bus.all.delete("SAVE_TABLE_ROW");
      this.$bus.all.delete("CREATE_NEW_TESTCASE_FILE_POP");
      this.$bus.all.delete("CREATE_NEW_TESTCASE_NODE_POP");
      this.$bus.all.delete("DELETE_TESTCASE_NODE_BYPOP");
      this.$bus.all.delete("DELETE_TESTCASE_NODE_BYTABLE");*/

    //console.log(this.$bus);
  },
  unmounted() {},
  activated() {},
  created() {
    var userData = store.getUserData()
    //console.log(userData)
    if (
      userData.userName &&
      userData.work &&
      userData.userId
    ) {
      this.userName = userData.userName;
      this.userWork = userData.work;
      this.userId = userData.userId;
      this.initOptions();
    } else {
      console.log("pushpush___________________________")
      //若尚未登录，跳转到登录界面
      this.$router.push({
        name: "HomeMain",
        params: {},
      });
    }
  },
  data() {
    return {
      headSrc: "",
      work_head_bk_color: "",
      work_head_font_color: "",
      work_nav_bk_color: "",
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
            value: "",
            key: "",
          },
          {
            value: "P0",
            key: "P0",
          },
          {
            value: "P1",
            key: "P1",
          },
          {
            value: "P2",
            key: "P2",
          },
          {
            value: "P3",
            key: "P3",
          },
          {
            value: "P4",
            key: "P4",
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
  methods: {
    /***
     * 注销bus监听器，避免重复注册bus容器的监听
     */
    offTestCaseListener: function() {
      /*
      //App-main
      console.log(this.$bus);
      this.$bus.all.delete("UPDATE_SELETOR_DATA");
      //my-table
      this.$bus.all.delete("CASE_NAME_TREENODE_CHANGE");
      //table
      this.$bus.all.delete("CHANGE_TESTCASE_BY_POP");
      this.$bus.all.delete("SAVE_TESTCASE_TABLE_DATA");
      this.$bus.all.delete("CREATE_NEW_TESTCASE_NOTIFY_TABLE");
      this.$bus.all.delete("UPDATE_CURRENT_NODE_DATA_CHOOSE");
      this.$bus.all.delete("CREATE_NEW_TABLE_POP");
      this.$bus.all.delete("UPDATE_CURRENT_FOLDER_TABLEDATAS");
      //systems
      this.$bus.all.delete("CHANGE_TESTCASE_FOLDER_BY_POP");
      this.$bus.all.delete("CHANGE_CURRENT_TREENODE_FROM_TABLE");
      this.$bus.all.delete("UPDATE_FATHER_TABLE_DATAS");
      this.$bus.all.delete("CASE_NAME_TABLE_CHANGE");
      this.$bus.all.delete("SAVE_TABLE_ROW");
      this.$bus.all.delete("CREATE_NEW_TESTCASE_FILE_POP");
      this.$bus.all.delete("CREATE_NEW_TESTCASE_NODE_POP");
      this.$bus.all.delete("DELETE_TESTCASE_NODE_BYPOP");
      this.$bus.all.delete("DELETE_TESTCASE_NODE_BYTABLE");
      console.log(this.$bus);
      */
    },
    /**
     * 根据角色类型设定工作和头像图片
     */
    getRoleData(work) {
      for (var t = 0; t < peoHeads.length; t++) {
        //console.log(work);
        //console.log(peoHeads[t]);
        if (peoHeads[t].work == work || peoHeads[t].key == work) {
          //this.headSrc =require(peoHeads[t].img)
          this.work = peoHeads[t].work;
          try {
            this.work_head_bk_color = peoHeads[t].background_head;
            this.work_head_font_color = peoHeads[t].font;
            this.work_nav_bk_color = peoHeads[t].background_nav;
            this.headSrc = peoHeads[t].img;
          } catch (err) {
            alert(err);
          }
        }
      }
    },
    /**
     * 初始化全局选项
     */
    initOptions() {
      this.getQAPeoData();
    },
    /**
     * 初始化QA组数据（只有QA可以修改和创建测试用例）
     */
    getQAPeoData() {
      axios.get("getQAPeoData").then((res) => {
        //console.log(res.data.msg);
        var option = this.initOptionArray(res.data.msg, "peoId", "peoName");
        this.options.QAs = option;
        this.$bus.emit("UPDATE_SELETOR_DATA", {
          options: this.options,
        }); //更新选项数据
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
  },
};
</script>

<style>
/* 头部样式 */
.header_left {
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
  /*background-color: #2d3a4b;*/
}

/* 左侧样式 */
.navbar {
  position: absolute;
  width: 340px;
  top: 50px; /* 距离上面50像素 */
  left: 0px;
  bottom: 0px;
  overflow-y: auto; /* 当内容过多时y轴出现滚动条 */
  /*background-color: #545c64;*/
}

/* 主区域 */
.main {
  display: flex;
  flex: 1;
  flex-direction: column;
  position: absolute;
  top: 100px;
  left: 340px;
  bottom: 0px;
  right: 0px; /* 距离右边0像素 */
  padding-left: 10px;
  overflow-y: auto; /* 当内容过多时y轴出现滚动条 */
  /* background-color: red; */
}
/* 筛选器区域 */
.select_main_css {
  position: absolute;
  display: flex;
  flex-grow: 1;
  justify-content: left;
  flex-direction: row;
  color: rgb(2, 24, 44);
  top: 50px;
  left: 340px;
  right: 0px;
  line-height: 50px;
  font-size: 18px;
  align-items: center;
}
</style>
