<template>
  <div class="main">
    <div class="selector_css">
      <div class="title_css">系统名:</div>
      <selector
        :optionInfo="optionInfo.caseSystems"
        @changeSelectorCondition="changeSelectorCondition"
      ></selector>
      <div class="title_css">修改人:</div>
      <selector
        :optionInfo="optionInfo.QAs"
        @changeSelectorCondition="changeSelectorCondition"
      ></selector>
      <div class="title_css">用例等级:</div>
      <selector
        :optionInfo="optionInfo.test_level"
        @changeSelectorCondition="changeSelectorCondition"
      ></selector>
      <div class="title_css">执行人:</div>
      <selector
        :optionInfo="optionInfo.peos"
        @changeSelectorCondition="changeSelectorCondition"
      ></selector>
      <div class="title_css">tag:</div>
      <selector
        :optionInfo="optionInfo.tags"
        @changeSelectorCondition="changeSelectorCondition"
      ></selector>
    </div>
    <div class="selector_css3">
      <test-case-table></test-case-table>
    </div>
  </div>
</template>
<script>
import TestCaseTable from "./TestCaseTable";
import Selector from "./Selector";
import axios from "axios";
export default {
  data() {
    return {
      options: {
        QAs: [],
        caseTypes: [],
        caseSystems: [],
        peos: [], //策划，qa，和程序,PM
        tags: [],
        test_level: [],
      },
      optionInfo: {
        caseSystems: {
          name: "caseSystems",
          key: "caseId",
          val: "caseName",
          data: [],
          select_val: "",
        },
        QAs: {
          name: "QAs",
          key: "peoId",
          val: "peoName",
          data: [],
          select_val: "",
        },
        test_level: {
          name: "test_level",
          key: "",
          val: "",
          data: [],
          select_val: "",
        },
        peos: {
          name: "peos",
          key: "peoId",
          val: "peoName",
          data: [],
          select_val: "",
        },
        tags: {
          name: "tags",
          key: "",
          val: "",
          data: [],
          select_val: "",
        },
      },
    };
  },
  mounted() {
    /**
     * 主组件更新全局数据，子 main界面的筛选组件同步更新数据
     */
    this.$bus.on("UPDATE_SELETOR_DATA", (param) => {
      this.options = param.options;
      this.optionInfo.test_level.data = param.options.test_level;
    });
  },

  components: { TestCaseTable, Selector },

  methods: {
    /**
     * 修改当前筛选条件
     */
    changeSelectorCondition(data) {
      this.optionInfo[data.name].select_val = data.val;
      axios
        .post("getSelectedTableDatas", {
          caseSystem: this.optionInfo["caseSystems"].select_val,
          QA: this.optionInfo["QAs"].select_val,
          test_level: this.optionInfo["test_level"].select_val,
          peo: this.optionInfo["peos"].select_val,
          tag: this.optionInfo["tags"].select_val,
        })
        .then((res) => {
          console.log(
            "________________________res.data.msg________________________"
          );
          console.log(res.data.msg);
          if (res.data.msg) {
            // 刷新table的展示数据
            this.$bus.emit("UPDATE_CURRENT_FOLDER_TABLEDATAS", {
              data: res.data.msg,
              caseId: null,
              fatherId: null,
            });
          } else {
            this.$bus.emit("UPDATE_CURRENT_FOLDER_TABLEDATAS", {
              data: [],
              caseId: null,
              fatherId: null,
            });
          }
           this.$bus.emit("SET_SYSTEM_CURRENT_NODE_NULL", {
            });
        });
    },
  },
};
</script>
<style scoped>
.title_css {
  margin-right: 15px;
  margin-left: 7px;
}
.selector_css {
  display: flex;
  flex-grow: 1;
  justify-content: left;
  flex-direction: row;
  color: rgb(2, 24, 44);
  line-height: 20px;
  top: 0px;
  left: 0px;
  right: 0px;
  font-size: 18px;
  align-items: center;
}
.selector_css3 {
  flex-grow: 20;
  color: aliceblue;
}
</style>
