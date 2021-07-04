<template>
  <div class="header_left">
    <img :src="headSrc" class="div1" />
    <div class="welcomeText">欢迎您! {{ work }} : [{{ userName }}]</div>
    <div class="TestCaseNameText">
      L30测试用例
    </div>
    <div class="editButton">
      <input
        type="file"
        id="file"
        ref="pathClear"
        @change="uploadTestCasesExcel"
      />
      <!--el-button size="small" type="success" v-on:click="uploadTestCasesExcel"
        >导入用例</el-button
      -->
    </div>

    <user-data-manager></user-data-manager>
  </div>
</template>

<script>
import { store } from "@/store/store.js";
import axios from "axios";
import UserDataManager from "@/components/AppUserManager/UserDataManager";

export default {
  components: { UserDataManager },
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
    var userData = store.getUserData();
    this.userName = userData.userName;
    this.userWork = userData.work;
    this.userId = userData.userId;
  },
  methods: {
    /**
     * 上传且导入用例
     */
    uploadTestCasesExcel(e) {
      let formData = new FormData();
      let data = JSON.stringify({
        user: this.userName,
      });
      formData.append("file", e.target.files[0]);
      formData.append("data", data); // 上传文件的同时， 也可以上传其他数据
      let url = "uploadExcelFile";
      let config = {
        headers: { "Content-Type": "multipart/form-data" },
      };
      axios
        .post(url, formData, config)
        .then(function(response) {
          //console.log(response.data);
        })
        .then((res) => {
          this.$refs.pathClear.value = "";
        })
        .catch((this.$refs.pathClear.value = ""));
    },
  },
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
  width: 25%;
  height: 10%;
}
</style>
