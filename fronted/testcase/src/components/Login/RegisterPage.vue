<template>
  <div width="360px">
    <el-dialog
      title="注册信息"
      v-model="dialogFormVisible"
      width="360px"
      :before-close="handleClose"
    >
      <el-form :label-position="labelPosition" label-width="80px" :model="form">
        <el-form-item label="用户名：">
          <el-input v-model="form.name" placeholder="请输入注册名"></el-input>
        </el-form-item>
        <el-form-item label="密码：">
          <el-input v-model="form.password" placeholder="请输入登录密码"></el-input>
        </el-form-item>
        <el-form-item label="职能：">
          <el-select
            v-model="form.work"
            placeholder="请选择 职能"
            style="width: 100%"
          >
            <el-option label="策划" value="2"></el-option>
            <el-option label="PM" value="4"></el-option>
            <el-option label="QA" value="1"></el-option>
            <el-option label="程序" value="3"></el-option>
          </el-select>
        </el-form-item>
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="handleClose">返回</el-button>
          <el-button type="primary" @click="UserRegister">注册</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      labelPosition: "right",
      form: {
        name: "",
        work: "",
        password:""
      },
      dialogFormVisible: true,
      filled: false,
    };
  },
  methods: {
    handleClose() {
      console.log(this.form.name);
      console.log(this.form.name != "");

      console.log(this.form);
      alert("注册并登陆后才能使用噢！");
      //若尚未登录，跳转到登录界面
      this.$router.replace({
        name: "HomeMain",
        params: {},
      });
    },
    /**
     * 用户进行注册
     */
    UserRegister() {
      var that = this;
      if (this.IsFilled()) {
        axios
          .post("/userRegister", {
            userName: that.form.name,
            userWork: that.form.work,
            userPasswd:that.form.password,
          })
          .then((res) => {
            console.log(res.data.msg);
            if (res.data.msg) {
              //注册成功，跳转到主界面
              localStorage.setItem ("TOKEN", res.data.msg.token)
              that.dialogFormVisible = false; //隐藏登录弹窗
              //指定跳转回到Login页面，可带参数
              this.$router.replace({
                name: "Layout",
                params: {
                  userName: that.form.name,
                  userId: res.data.msg.userId,
                  userWork: that.transWorkType(that.form.work),
                },
              });
            } else {
              alert(res.data.error);
            }
          })
          .catch(function(error) {
            alert("Error " + error);
          });
      } else {
        alert("填写全部信息后才能使用噢！");
      }
    },
    /**
     * 获取角色类型，数字转换为具体类型
     */
    transWorkType(workId) {
      var works = [
        { key: "1", value: "QA" },
        { key: "2", value: "策划" },
        { key: "3", value: "程序" },
        { key: "4", value: "PM" },
      ];
      for (var w = 0; w < works.length; w++) {
        if (workId == works[w].key) {
          return works[w].value;
        }
      }
    },
    /**
     * 检查下空是不是都填写了
     */
    IsFilled() {
      if (this.form.name != "" && this.form.work != "") {
        return true;
      } else {
        return false;
      }
    },
  },
};
</script>

<style>
.user_change_button {
  font-size: 10px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
</style>
