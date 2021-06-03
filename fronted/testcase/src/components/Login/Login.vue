<template>
  <div class="dialog_register">
    <el-dialog
      title="登录信息"
      v-model="dialogFormVisible"
      width="400px"
      :before-close="handleClose"
    >
      <el-form :model="form" class="form_register" label-width="80px">
        <el-form-item label="用户名：">
          <el-col class="line" :span="100"
            ><el-input v-model="form.name"></el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="职能：">
          <el-col :span="100">
            <el-select v-model="form.work" placeholder="请选择 职能">
              <el-option label="策划" value="2"></el-option>
              <el-option label="PM" value="4"></el-option>
              <el-option label="QA" value="1"></el-option>
              <el-option label="程序" value="3"></el-option>
            </el-select>
          </el-col>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="handleClose">取 消</el-button>
          <el-button type="primary" @click="UserLogin">确 定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      form: {
        name: "",
        work: "",
      },
      dialogFormVisible: true,
      filled: false,
    };
  },
  methods: {
    UserLogin() {
      var that = this;
      if (this.IsFilled()) {
        axios
          .post("/register", {
            name: that.form.name,
            work: that.form.work,
          })
          .then((res) => {
            console.log(res.data);
            that.dialogFormVisible = false;
            this.$router.push({
              name: "Layout",
              params: {
                name: that.form.name,
                work: that.form.work,
              },
            });
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
.dialog_register {
  width: 300px;
  height: 200px;
}
.form_register {
  width: 350px;
  flex-wrap: nowrap;
}
.label {
  width: 800px;
}
</style>
