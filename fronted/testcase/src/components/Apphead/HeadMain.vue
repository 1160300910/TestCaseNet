<template>
  <div class="header">
    <img src="./heads/005-man.png" class="div1" />
    <div class="welcomeText">欢迎您! {{ work }} : [{{ userName }}]</div>
    <div class="TestCaseNameText">XX系统测试用例</div>
    <div class="editButton">
      <!--el-button size="small" type="primary" v-on:click="getData"
        >编辑用例</el-button
      -->
    </div>
  </div>
</template>

<script>
import axios from "axios";
const peoHeads = [
  {
    img: "./heads/048-woman.png",
    work: "QA",
    key: "1",
  },
  {
    img: "./heads/010-woman.png",
    work: "策划",
    key: "2",
  },
  {
    img: "./heads/005-man.png",
    work: "程序",
    key: "3",
  },
  {
    img: "./heads/016-woman.png",
    work: "PM",
    key: "4",
  },
];
export default {
  data: function() {
    return {
      headSrc: "",
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
     * 根据角色类型设定工作和头像图片
     */
    getHeadImgUrl(work) {
      console.log(
        "++++++++++++++++++++++++getWorkImg+++++++++++++++++++++++++++++"
      );
      console.log(this.$route.params);
      for (var t = 0; t < peoHeads.length; t++) {
        //console.log(work);
        //console.log(peoHeads[t]);
        if (peoHeads[t].work == work || peoHeads[t].key == work) {
          //this.headSrc =require(peoHeads[t].img)
          this.work = peoHeads[t].work;
          try {
            var img = peoHeads[t].img;
            console.log(img);
            return img;
          } catch (err) {
            alert(err);
          }
        }
      }
      console.log("+++++++++++++++++++啦啦啦啦++++++++++++++++++++++++++++++");
    },
  },
  mounted() {
    this.getHeadImgUrl(this.work);
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
