<template>
  <my-table
    :data="tableData"
    :col-configs="colConfigs"
    highlight-current-row
    border
    @cell-click="cellClick"
  >
    <template #opt="scope">
      <el-row>
        <el-button
          size="mini"
          type="primary"
          icon="el-icon-edit"
          circle
          @click="Test(scope.data.row)"
        ></el-button>
        <el-button
          type="info"
          icon="el-icon-picture-outline"
          circle
          size="mini"
        ></el-button>
        <el-button
          type="danger"
          size="mini"
          icon="el-icon-delete"
          circle
        ></el-button>
      </el-row>
    </template>
    <template #input="scope" :resize="both" :autosize="{ minRows: 2 }">
      <el-input
        v-focus
        type="textarea"
        v-if="scope.data.row.isOk.title"
        v-model="scope.data.row.title"
        @focus="Test(scope.data.row.title)"
        @keyup.enter="blurClick(scope.data.row, scope.data.column)"
        @blur="blurClick(scope.data.row, scope.data.column)"
      >
      </el-input>
      <span v-else>{{ scope.data.row.title }}</span>
    </template>
    <template #chooseLevel="scope">
      <el-select v-model="scope.data.row.choose_test_level" placeholder="P0">
        <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        >
        </el-option>
      </el-select>
    </template>
  </my-table>
</template>

<script>
import myTable from "./my-table.vue";

export default {
  directives: {
    //注册一个局部的自定义指令 v-focus
    focus: {
      mounted(el) {
        console.log(el);
        el.children[0].focus();
        //因为el-input这是个组件，input外面被一层 div 包裹着,
        ///el打印出来是外面这个 div，需要找到内层的input
      },
    },
  },
  methods: {
    Test(data) {
      console.log(data);
    },
    blurClick(row, column) {
      if (column.label === "用例标题") {
        row.isOk.title = false;
      }
    },
    cellClick(row, column, cell, event) {
      console.log(row, column.label, cell);
      if (column.label === "用例标题") {
        row.isOk.title = true;
      } else if (column.label === "备注") {
        this.$set(row, "isOK2", true);
      } else if (column.label === "备注") {
        this.$set(row, "isOK2", true);
      }
    },
  },
  components: { myTable },
  data() {
    this.colConfigs = [
      {
        prop: "title",
        label: "用例标题",
        width: 95,
        editable: true,
        slot: "input",
      },
      {
        prop: "test_level",
        label: "用例等级",
        width: 100,
        editable: true,
        chooseble: false,
        slot: "chooseLevel",
      },
      { prop: "preCondition", label: "前置条件", width: 140, editable: true },
      {
        prop: "actionCondition",
        label: "执行条件",
        width: 180,
        editable: true,
      },
      { prop: "preResult", label: "预期结果", width: 180, editable: true },
      { prop: "ps", label: "备注", width: 180, editable: true },

      {
        prop: "tag",
        label: "标签",
        width: 80,
        editable: true,
        chooseble: false,
      },
      { prop: "operate", label: "操作", width: 140, slot: "opt" },

      // 模版中的元素需要对应的有 slot="opt" 属性
    ];
    return {
      tableData: [
        {
          title: "2016-05-02",
          preCondition: "王小虎",
          actionCondition: "上海市普陀区金沙江路 1518 弄",
          type: 12312,
          preResult: 1212312312312312312312,
          ps: "123",
          isOk: {
            title: false,
          },
        },
        {
          title: "2016-05-04",
          preCondition: "打磨",
          actionCondition: "西岸",
          isOk: {
            title: false,
          },
        },
      ],
      options: [
        {
          value: "0",
          label: "P0",
        },
        {
          value: "1",
          label: "P1",
        },
        {
          value: "2",
          label: "P2",
        },
        {
          value: "3",
          label: "P3",
        },
        {
          value: "4",
          label: "P4",
        },
      ],
    };
  },
};
</script>
