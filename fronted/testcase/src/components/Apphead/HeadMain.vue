<template>
  <div class="header">
    <img src="/icons/048-woman.png" class="div1" />
    <div class="welcomeText">欢迎您! {{ work }} : [{{ name }}]</div>
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
      name: "",
      work: "",
    };
  },
  created() {
    this.name = this.$route.params.userName;
    this.work = this.$route.params.userWork;
  },
  methods: {
    getWorkType() {
      if (this.work == "1") {
        this.work = "QA";
      } else if (this.work == "2") {
        this.work = "策划";
      } else if (this.work == "3") {
        this.work = "程序";
      } else if (this.work == "4") {
        this.work = "PM";
      } else {
        //alert("ERROR!!!");
      }
    },
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
  },
  mounted() {
    //this.getData();

    this.getWorkType();
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
