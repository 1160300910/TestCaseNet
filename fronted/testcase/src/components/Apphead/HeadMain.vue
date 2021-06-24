<template>
  <div class="header">
    <img :src="headSrc" class="div1" />
    <div class="welcomeText">欢迎您! {{ work }} : [{{ userName }}]</div>
    <div class="TestCaseNameText">
      L30测试用例
    </div>
    <div class="editButton">
      <!--el-button size="small" type="primary" v-on:click="getData"
        >编辑用例</el-button
      -->
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  props: ["headSrc"],
  data: function() {
    return {
      serverResponse: "resp",
      userName: "",
      work: "",
      userId: "",
    };
  },
  created() {
    //require('@/assets/icons/048-woman.png')
    //require('@/assets/icons/005-man.png')
    // require('@/assets/icons/016-woman.png')
    // require('@/assets/icons/010-woman.png')
    this.userName = this.$route.params.userName;
    this.work = this.$route.params.userWork;
    this.userId = this.$route.params.userId;
  },
  methods: {},
  mounted() {},
};
</script>

<style scoped>
.header {
}
.div1 {
  width: 50px;
  height: 50px;
  background-color: 1px solid rgb(118, 60, 211);
}
.welcomeText {
  display: flex;
  flex-grow: 20;
  justify-content: flex-start;
  margin-left: 20px;
}
.TestCaseNameText {
  display: flex;
  flex-grow: 20;
  justify-content: flex-start;
}
.editButton {
  display: flex;
  flex-grow: 1;
  justify-content: left;
  width: 5%;
  height: 10%;
}
</style>
