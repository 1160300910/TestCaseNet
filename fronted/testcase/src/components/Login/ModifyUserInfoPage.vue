<template>
  <div width="400px">
    <el-dialog
      title="修改用户信息"
      v-model="dialogFormVisible"
      width="400px"
      :before-close="handleClose"
    >
      <el-form
        :label-position="labelPosition"
        label-width="100px"
        :model="form"
      >
        <el-form-item
          label="原用户名："
          :rules="[{ required: true, message: '原名不能为空' }]"
        >
          <el-input
            v-model="form.old_name"
            placeholder="请输入需要修改的原名"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="新用户名："
          :rules="[{ required: true, message: '新用户名不能为空' }]"
        >
          <el-input
            v-model="form.new_name"
            placeholder="请输入修改后的名字"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="职能："
          :rules="[{ required: true, message: '职能不能为空' }]"
        >
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
          <el-button @click="handleClose">取消修改</el-button>
          <el-button type="primary" @click="modifyUserInfo">确定修改</el-button>
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
        old_name: "",
        new_name: "",
        work: "",
      },
      dialogFormVisible: true,
      filled: false,
    };
  },
  methods: {
    handleClose() {
      console.log(this.form.name);
      console.log(this.form.name != "");
      this.$router.back()
    },
    /**
     * 用户信息修改
     */
    modifyUserInfo() {
      var that = this;
      if (this.IsFilled()) {
        axios
          .post("/modifyUserInfo", {
            userOldName: that.form.old_name,
            userNewName: that.form.new_name,
            userWork: that.form.work,
          })
          .then((res) => {
            console.log(res.data);
            if (res.data.msg) {
              //修改成功，跳转到主界面
              that.dialogFormVisible = false; //隐藏登录弹窗
              //指定跳转回到Login页面，可带参数
              this.$router.replace({
                name: "Layout",
                params: {
                  userName: that.form.new_name,
                  userId: res.data.msg.peoId,
                  userWork: this.transWorkType(that.form.work),
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
      for(var w=0;w<  works.length;w++){
        if(workId==works[w].key){
          return works[w].value
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
