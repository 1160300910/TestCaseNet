<template>
  <div class="header">
    <img src="../../source/048-woman.png" class="div1" />
    <div class="welcomeText">
      <div >{{ serverResponse }}</div>
      欢迎您[(QA,策划,程序PM)][角色名称XXX]
    </div>
    <div class="TestCaseNameText">XX系统测试用例</div>
    <div class="editButton">
      <el-button size="small" type="primary" v-on:click="getData"
        >编辑用例</el-button
      >
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data: function() {
    return {
      serverResponse: "resp",
      
    };
  },
  created() {
  },
  methods: {
    getData() {
      var that = this;
      const path = "http://127.0.0.1:5000/";
      axios
        .get(path)
        .then(function(response) {
          var msg = response.data.msg;
          that.serverResponse = msg;
        })
        .catch(function(error) {
          alert("Error " + error);
        });
    },
  },mounted() {
    this.getData()
  },
};
</script>

<style scoped>
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
