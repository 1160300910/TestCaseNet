<template>
  <div>
    <el-dropdown split-button type="primary" @click="handleClick">
      更多菜单
      <template v-slot:dropdown>
        <el-dropdown-menu>
          <el-dropdown-item
            ><el-button type="primary" icon="el-icon-check"
              >修改账户</el-button
            ></el-dropdown-item
          >
          <el-dropdown-item
            ><el-button type="success" icon="el-icon-check"
              >退出</el-button
            ></el-dropdown-item
          >
          <el-dropdown-item>双皮奶</el-dropdown-item>
          <el-dropdown-item>蚵仔煎</el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
  </div>
  <!--el-button type="primary" icon="el-icon-edit"> 修改账户</el-button>
    <el-button type="success" icon="el-icon-check">退出</el-button-->
</template>
<script>
export default {
  methods: {
    handleClick() {
      alert("button click");
    },
  },
  setup() {},
};
</script>
<style scoped>
.manager_button_css {
  width: 280px;
  margin-right: 20px;
  display: flex;
  flex-direction: row;
}
.el-dropdown {
  vertical-align: top;
}
.el-dropdown + .el-dropdown {
  margin-left: 15px;
}
.el-icon-arrow-down {
  font-size: 12px;
}
</style>
