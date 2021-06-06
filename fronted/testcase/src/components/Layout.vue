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
    <app-main ></app-main>
  </div>
</template>

<script>
// 会导入./AppHeader下面的index.vue组件
import AppHeader from "./Apphead/HeadMain";
import AppNavbar from "./Appnavbar/NavbarMain";
import AppMain from "./Appmain/AppMain";
import { ref } from "vue";

// 导入子组件，缩写格式 AppHeader: AppHeader
export default {
   created() {
    this.userName = this.$route.params.userName;
    this.userWork = this.$route.params.userWork;
  },
  setup() {
    
  },
  data() {
    return {
      nowId: "",
      nowLabel: "",
      choice: "",
      nowChild:'',
      nowParent:'',
      userName:"",
      userWork:""
    };
  },
  provide() {
    return {
      parentObj: this,
    };
  },
  components: { AppHeader, AppNavbar, AppMain },
  methods: {},
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
  width: 230px;
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
  left: 230px;
  bottom: 0px;
  right: 0px; /* 距离右边0像素 */
  padding: 10px;
  overflow-y: auto; /* 当内容过多时y轴出现滚动条 */
  /* background-color: red; */
}
</style>
