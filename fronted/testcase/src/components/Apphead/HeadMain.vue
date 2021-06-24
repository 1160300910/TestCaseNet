<template>
  <div class="header">
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
          console.log(response.data);
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
