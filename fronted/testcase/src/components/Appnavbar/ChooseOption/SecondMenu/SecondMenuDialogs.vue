<template>
  <el-dialog
    title="指派用例集给...执行"
    v-model="setActionPeo_dialogFormVisible"
    width="520px"
    :before-close="openCancelSetActionPeo"
  >
    <el-form>
      <el-form-item label="执行人员" label-width="120px">
        <el-select
          v-model="setActionPeo_peo"
          placeholder="请选择执行人员"
          filterable
          @visible-change="changeActionPeoOption($event, setActionPeo_peo)"
        >
          <el-option
            v-for="item in project_peos"
            :key="item.key"
            :value="item.value"
          >
          </el-option>
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="openCancelSetActionPeo">取 消</el-button>
        <el-button
          type="primary"
          @click="handleSetActionPeoRequest(setActionPeo_peo, data)"
          >确 定</el-button
        >
      </span>
    </template>
  </el-dialog>
</template>
<script>
import axios from "axios";
export default {
  mounted() {
    /**
     * 展示弹窗
     */
    this.$bus.on("SHOW_SET_ACTION_PEO_DIALOG", (param) => {
      console.log("————展示———— SHOW_SET_ACTION_PEO_DIALOG 发生了");
      this.getProjectPeoData(); //等待数据
      this.setActionPeo_dialogFormVisible = true;
      this.node = param.node;
      this.data = param.data;
      this.setActionPeo_peo = "";
    });
  },
  setup() {},
  data() {
    return {
      project_peos: [],
      setActionPeo_peo: "",
      setActionPeo_dialogFormVisible: false,
      node: {},
      data: {},
    };
  },
  methods: {
    /**
     * 发送取消设置执行人员的消息
     */
    openCancelSetActionPeo() {
      this.$notify.info({
        title: "取消",
        message: "已取消设置执行人员和执行用例集",
        position: "top-left",
      });
      this.setActionPeo_dialogFormVisible = false;
    },
    /***
     * 点击确定按钮，发送确认执行人员消息
     */
    handleSetActionPeoRequest(peoName, data) {
      if (peoName) {
        let obj = this.project_peos.find((item) => {
          //model就是上面的数据源
          return item.value === peoName; //筛选出匹配数据
        });
        console.log(obj);
        console.log(data.caseId);
        axios
          .post("setActionPeoTreeNodeFolder", {
            peoName: obj.value,
            peoId: obj.key,
            caseId: data.caseId,
          })
          .then((res) => {
            console.log(res.data);
            this.setActionPeo_dialogFormVisible = false;
          });
      } else {
        alert("当前选择执行人员信息为空！！请选择人员！！！");
      }
    },
    /**
     * 修改执行人员
     */
    changeActionPeoOption(callback, val) {
      //当隐藏下拉框时触发
      if (!callback) {
        if (val) {
          console.log(val);
        }
      }
    },
    /**
     * 初始化项目组人员数据（QA,策划和程序,PM）
     */
    getProjectPeoData() {
      axios.get("getProjectPeos").then((res) => {
        //console.log(res.data.msg);
        var option = this.initOptionArray(res.data.msg, "peoId", "peoName");
        this.project_peos = option;
      });
    },
    /**
     * 输入数组，选项名，
     * keyName ，valueName
     * 输出option数组(直接引用修改了)
     */
    initOptionArray(data, keyName, valName) {
      var options = [];
      for (var d = 0; d < data.length; d++) {
        options.unshift({
          key: data[d][keyName],
          value: data[d][valName],
        });
      }
      return options;
    },
  },
};
</script>
