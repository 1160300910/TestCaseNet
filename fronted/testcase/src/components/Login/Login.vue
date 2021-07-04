<template>
  <div width="360px">
    <el-dialog
      title="登录信息"
      v-model="dialogFormVisible"
      width="360px"
      :before-close="handleClose"
    >
      <el-form :label-position="labelPosition" label-width="80px" :model="form">
        <el-form-item label="用户名：">
          <el-input v-model="form.name" placeholder="请输入用户名"></el-input>
        </el-form-item>
        <el-form-item label="密码：">
          <el-input v-model="form.password" placeholder="请输入登录密码"></el-input>
        </el-form-item>
        <!--el-form-item label="职能：">
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
        </el-form-item-->
      </el-form>
      <div class="user_change_button">
        <el-button type="text" @click="registUser">注册用户</el-button>
        <!--el-button type="text" @click="modifyUserInfo"> 修改用户信息</el-button-->
      </div>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="handleClose">取 消</el-button>
          <el-button type="primary" @click="UserLogin">确 定</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";
import {store} from '@/store/store.js'
export default {
  data() {
    return {
      labelPosition: "right",
      form: {
        name: "",
        password:""
      },
      dialogFormVisible: true,
      filled: false,
    };
  },
  methods: {
    /**
     * 用户注册
     */
    registUser() {
      this.$router.replace({
        name: "RegisterPage",
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
    /**
     * 用户登录：
     * 需要输入用户名，用户职能
     * 不能使用重复的用户名
     */
    UserLogin() {
      var that = this;
      if (this.IsFilled()) {
        axios
          .post("/userLogin", {
            userName: that.form.name,
            userPasswd:that.form.password,
          })
          .then((res) => {
            console.log(res.data);
            if (res.data.msg) {
              localStorage.setItem ("TOKEN", res.data.msg.token)
              //在用户刷新的时候userLogin会回到默认值false，所以我们需要用到HTML5储存
              //我们设置一个名为Flag，值为isLogin的字段，作用是如果Flag有值且为isLogin的时候，证明用户已经登录了
              // sessionStorage.setItem("FLAG","isLogin") //关闭窗口之后将会删除这些数据
              //localStorage.setItem("FLAG","isLogin")//关闭窗口后不会删除这些数据
              this.$router.replace({
                name: "Layout",
                params: {
                  userName: that.form.name,
                  userId: res.data.msg.peoId,
                  userWork: this.transWorkType(res.data.msg.peoType),
                },
              });
              that.dialogFormVisible = false; //隐藏登录弹窗
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
    handleClose() {
      console.log(this.form.name);
      console.log(this.form.name != "");
      if (this.IsFilled()) {
        this.dialogFormVisible = false;
      } else {
        console.log(this.form);
        alert("登录后才能使用噢！");
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
      for(var w=0;w<  works.length;w++){
        if(workId==works[w].key){
          return works[w].value
        }
      }
    },
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
.el-form-item {
}
.user_change_button {
  font-size: 10px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
</style>
