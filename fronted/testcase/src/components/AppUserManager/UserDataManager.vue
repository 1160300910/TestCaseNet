<template>
  <div class="manager_button_css">
    <el-dropdown trigger="click" @visible-change="handleChange" ref="dropDown">
      <el-button type="info" circle>
        <i class="el-icon-user-solid el-icon--right"></i>
      </el-button>
      <template #dropdown>
        <el-dropdown-menu ref="dropDownMenu" style="width:180px;">
          <el-dropdown-item>
            <div class="dropdown_menu_css" @click="modifyUserInfo">
              <i class="el-icon-edit" style="color: rgb(6, 153, 202);"></i>
              <span class="dropdown_menu_label_css">修改用户信息</span>
            </div>
          </el-dropdown-item>
          <el-dropdown-item divided>
            <div class="dropdown_menu_css" @click="userLogOut">
              <i
                class="el-icon-switch-button"
                style="color: rgb(6, 153, 202);"
              ></i>
              <span class="dropdown_menu_label_css">退出</span>
            </div>
          </el-dropdown-item>

          <!--el-dropdown-item disabled>双皮奶</el-dropdown-item>
          <el-dropdown-item divided>蚵仔煎</el-dropdown-item-->
        </el-dropdown-menu>
      </template>
    </el-dropdown>
  </div>
  <!--el-button type="primary" icon="el-icon-edit"> 修改账户</el-button>
    <el-button type="success" icon="el-icon-check">退出</el-button-->
</template>
<script>
import { store } from "@/store/store.js";
export default {
  methods: {
    /**
     * 用户登出
     */
    userLogOut() {
      store.setUserData("", "", "");
      localStorage.setItem("TOKEN", -1);
       this.$router.replace({
        name: "HomeMain",
        params: {},
      });
    },
    /**
     * 用户数据修改
     */
    modifyUserInfo() {
      this.$router.push({
        name: "ModifyUserInfoPage",
        params: {},
      });
    },
    handleChange() {
      console.log(document.querySelectorAll(`.el-dropdown__popper`));
      console.log(document.querySelectorAll(`.el-dropdown-menu`));
      console.log(this.$refs.dropDown);

      console.log(this.$refs.dropDown.$el);
      console.log(this.$refs.dropDownMenu.$el);
      console.log(this.$refs.dropDown.visible);
    },

    handleClick() {
      //alert("button click");
      console.log(this.$refs.dropDown.visible);
      this.$refs.dropDown;
      console.log(this.$refs.dropDown.visible);
    },
  },
  setup() {},
  mounted() {
    console.log(this.$refs.dropDown);
    console.log(this.$refs.dropDown.visible);
  },
};
</script>
<style scoped>
.dropdown_menu_css {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  margin-left: 4px;
  margin-right: 4px;
  margin-top: 2px;
  margin-bottom: 2px;
}
.dropdown_menu_label_css {
  display: flex;
  justify-content: flex-start;
  width: 150px;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  flex-grow: 1;
  font-size: 15px;
  margin-left: 7px;
  color: rgb(6, 153, 202);
}

.manager_button_css {
  display: flex;
  flex-grow: 2;
  justify-content: flex-start;
  margin-left: 20px;
} /*
.el-dropdown {
  vertical-align: top;
}
.el-dropdown + .el-dropdown {
  margin-left: 15px;
}
.el-icon-arrow-down {
  font-size: 12px;
}*/
</style>
