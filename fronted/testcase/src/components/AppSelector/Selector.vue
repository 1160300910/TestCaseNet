<template>
  <el-select
    v-model="value"
    filterable
    placeholder="请选择"
    size="small"
    class="select_css"
    @visible-change="changeOption($event, value)"
    ref="selector_ref"
  >
    <el-option
      v-for="item in data"
      :key="item.key"
      :label="item.label"
      :value="item.value"
    >
    </el-option>
  </el-select>
</template>

<script>
import axios from "axios";
export default {
  props: ["optionInfo"],
  data() {
    return {
      value: "",
      data: [],
    };
  },
  created() {
    //console.log(this.optionInfo);
  },
  mounted() {
    /**
     * 重置筛选框内容
     */
    this.$bus.on("RESET_SELECT_CONDITIONS", () => {
      this.value = "";
    });
  },
  methods: {
    /***
     * 根据当前的筛选条件，修改删选条件
     * 当隐藏下拉框时触发
     */
    changeOption(callback, val) {
      
      console.log(this.$refs.selector_ref.popper);
     
      console.log(this.$refs.selector_ref.popper.popperRef);
      console.log(this.$refs.selector_ref.$el);
      console.log(this.$refs.selector_ref.visible);
      if (!callback) {
       // console.log("______________changeOption_____________")
        //console.log(val)
        //当隐藏下拉框时触发
        //alert(val)
        //alert(val)

        let obj = this.data.find((item) => {
          //model就是上面的数据源
          return item.value === val; //筛选出匹配数据
        });
        //alert(val)
        if (!val) {
          this.$emit("changeSelectorCondition", {
            name: this.optionInfo.name,
            val: '',
          });
        } else {
        //console.log(obj)
          this.$emit("changeSelectorCondition", {
            name: this.optionInfo.name,
            val: obj.key,
          });
        }
      } else {
        this.getOptionData();
      }
    },
    /**
     * 根据optionName获取对应option数据 */
    getOptionData() {
      var optionInfo = this.optionInfo;
      //console.log("===================== getOptionData =====================");
      if (optionInfo.data && optionInfo.name == "test_level") {
        this.data = optionInfo.data;
      } else if (optionInfo.name == "caseSystems") {
        this.getProjectSystemsData();
      } else if (optionInfo.name == "QAs") {
        this.getQAPeoData();
      } else if (optionInfo.name == "peos") {
        this.getProjectPeoData();
      } else if (optionInfo.name == "tag") {
        this.getProjectTestCaseTagData();
      }
    },
    /**
     * 初始化项目测试用例系统选项
     * fatherId =-1,且类型是fileType的即为系统名节点
     */
    getProjectSystemsData() {
      axios.get("getProjectSystemsData").then((res) => {
        var option = this.initOptionArray(res.data.msg, "caseId", "caseName");
        this.data = option;
      });
    },
    /**
     * 初始化QA组数据（只有QA可以修改和创建测试用例）
     */
    getQAPeoData() {
      axios.get("getQAPeoData").then((res) => {
        var option = this.initOptionArray(res.data.msg, "peoId", "peoName");
        this.data = option;
      });
    },
    /**
     * 初始化项目组人员数据（QA,策划和程序,PM）
     */
    getProjectPeoData() {
      axios.get("getProjectPeos").then((res) => {
        //console.log(res.data.msg);
        var option = this.initOptionArray(res.data.msg, "peoId", "peoName");
        this.data = option;
      });
    },
    /**
     * 初始化项目测试用例标签数据
     */
    getProjectTestCaseTagData() {
      axios.get("get").then((res) => {
        //console.log(res.data.msg);
        this.options.peos = res.data.msg;
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
      options.unshift({
        key: "",
        value: "全部",
      });
      return options;
    },
  },
};
</script>
<style scoped>
.select_css {
  width: 120px;
}
</style>
