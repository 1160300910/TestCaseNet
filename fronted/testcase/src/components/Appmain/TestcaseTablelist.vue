<template>
  <el-table
    border
    :data="tableData"
    style="width: 100%"
    :row-class-name="tableRowClassName"
    @cell-click="cellClick"
    highlight-current-row
  >
    <el-table-column prop="name" label="用例名" width="100"> </el-table-column>
    <el-table-column prop="level" label="用例等级" width="90">
      <template #default="scope">
        <el-select
          v-model="scope.row.choose_test_level"
          placeholder="P0"
          @blur="chooseTestLevel(scope.row, scope.column)"
        >
          <el-option
            v-for="item in options"
            :key="item.key"
            :label="item.label"
            :value="item.value"
          >
          </el-option>
        </el-select>
      </template>
    </el-table-column>
    <el-table-column
      prop="actionmethod"
      label="执行方案"
      show-overflow-tooltip
      width="180"
    >
      <template #default="scope">
        <el-input
          type="textarea"
          v-if="scope.row.isColumnEditing"
          :autosize="{ minRows: 2 }"
          :resize="both"
          @keyup.enter="blurClick(scope.$index, scope.row, scope.column)"
          @blur="blurClick(scope.$index, scope.row, scope.column)"
          v-model="scope.row.actionmethod"
          style="width:100%;hight:100%"
        ></el-input>
        <span v-else>{{ scope.row.actionmethod }}</span>
      </template>
    </el-table-column>
    <el-table-column prop="ps" label="备注"> </el-table-column>
    <el-table-column prop="actionResult" label="执行结果"> </el-table-column>
    <el-table-column prop="changePeo" label="修改人"> </el-table-column>
    <el-table-column prop="changeDate" label="修改日期"> </el-table-column>
  </el-table>
</template>

<style>
.el-table .warning-row {
  background: oldlace;
}

.el-table .success-row {
  background: #f0f9eb;
}
</style>

<script>
import { ref, onMounted } from "vue";

export default {
  /*
  setup() {
    var gain = ref(null);
    onMounted(()=>{
      console.log(gain)
    });
    return {
      gain,
    };
  },*/
  /*
  directives: {
    //注册一个局部的自定义指令 v-focus
    focus: {
      // 指令的定义
      inserted: function(el) {
        // 聚焦元素
        el.querySelector("input").focus();
      },
    },
  },
  */
  methods: {
    chooseTestLevel(row, column) {
      row.level = this.choose_test_level;
    },
    cellClick(row, column, cell, event) {
      console.log(row, column.label, cell);
      if (column.label === "执行方案") {
        row.isColumnEditing = true;
      } else if (column.label === "备注") {
        this.$set(row, "isColumnEditing2", true);
      } else if (column.label === "备注") {
        this.$set(row, "isColumnEditing2", true);
      }
      /*
      this.$nextTick(() => {
        console.log(this.gain);
        this.$refs.gain.focus();
      });*/
    },
    blurClick(index, row, column) {
      if (column.label === "执行方案") {
        row.isColumnEditing = false;

        //alert("ok!");
      }
    },
    tableRowClassName({ rowIndex }) {
      if (rowIndex === 1) {
        return "warning-row";
      } else if (rowIndex === 3) {
        return "success-row";
      }
      return "";
    },
  },
  data() {
    return {
      choose_test_level: "",
      options: [
        {
          value: "0",
          key: "P0",
        },
        {
          value: "1",
          key: "P1",
        },
        {
          value: "2",
          key: "P2",
        },
        {
          value: "3",
          key: "P3",
        },
        {
          value: "4",
          key: "P4",
        },
      ],
      tableData: [
        {
          name: "入口-1",
          actionmethod:
            "点击弹出对应GM命令或者执行方案,点击弹出对应GM命令或者执行方案,点击弹出对应GM命令或者执行方案",
          level: "P1",
          changeDate: "2021-5-23",
          ps: "备注巴啦啦把",
          actionResult: "成功",
          changePeo: "西子卡",
          isColumnEditing: false,
          choose_test_level: ref("P0"),
        },
        {
          name: "入口-2",
          actionmethod: "点击弹出对应GM命令或者执行方案",
          level: "P2",
          isColumnEditing: false,
          choose_test_level: ref(""),
        },
        {
          name: "入口-3",
          actionmethod: "点击弹出对应GM命令或者执行方案",
          level: "P1",
          isColumnEditing: false,
          choose_test_level: ref(""),
        },
        {
          name: "入口-4",
          actionmethod: "点击弹出对应GM命令或者执行方案",
          level: "P1",
          isColumnEditing: false,
          choose_test_level: ref(""),
        },
      ],
    };
  },
};
</script>
