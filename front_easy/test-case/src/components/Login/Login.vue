<template>

  <!--el-button type="text" @click="open">点击打开 Message Box</el-button-->
  <select-role></select-role>
</template>

<script>
import SelectRole from './SelectRole.vue';
export default {
  components: { SelectRole },
  methods: {
    open() {
      this.$prompt("请选择账号", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        inputPattern: /[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?/,
        inputErrorMessage: "邮箱格式不正确",
      })
        .then(({ value }) => {
          this.$message({
            type: "success",
            message: "你的邮箱是: " + value,
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "取消输入",
          });
        });
    },
  },
  create() {
    this.open();
  },
};
</script>

<style></style>
