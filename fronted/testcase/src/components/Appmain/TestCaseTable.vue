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
const EdibleInput = {
  props: ["row", "column_name", "isOk"],
  template: `
      <el-input type="textarea" v-if="isOk" v-model="row[column_name]">
      </el-input>
      <span v-else><span> {{ row[column_name]}}</span></span>
    `,
};
export default {
  inject: ["parentObj"],
  methods: {
    /**
     * 修改测试用例，将全部可编辑区域变成可编辑状态
     * colConfigs ：
     * row_index ：需要修改表格的行id
     * tableData ：表格数据
     */
    ChangeTestCase(colConfigs, row_index, tableData) {
      console.log(colConfig);
      var colConfig, data, propName;
      for (data in tableData) {
        if (data.id == row_index) { //是需要修改的行
          for (propName in data.isOk) { //对于需要修改的属性名
            data.isOk[propName] = true;
          }
        }
      }
    },
    Test(data) {
      console.log(data);
    },
    cellClick(row, column, cell, event) {
      row.isOk[column.property] = true;
      //console.log(column.prop);
      //console.log(row.isOk[column.prop]);
      //console.log(row.isOk[column.property]);
      //console.log(cell);
      /*if (column.label === "XX") {
        //console.log(row.isOk[column.property]);
      } else if (column.label === "XXX") {
        this.$set(row, "isOK2", true);
      }*/
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
        component: EdibleInput,
      },
      {
        prop: "test_level",
        label: "用例等级",
        width: 100,
        editable: true,
        chooseble: false,
        slot: "chooseLevel",
      },
      {
        prop: "preCondition",
        label: "前置条件",
        width: 140,
        editable: true,
        component: EdibleInput,
      },
      {
        prop: "actionCondition",
        label: "执行条件",
        width: 180,
        editable: true,
        component: EdibleInput,
      },
      {
        prop: "preResult",
        label: "预期结果",
        width: 180,
        editable: true,
        component: EdibleInput,
      },
      {
        prop: "ps",
        label: "备注",
        width: 180,
        editable: true,
        component: EdibleInput,
      },

      {
        prop: "tag",
        label: "标签",
        width: 80,
        editable: true,
        chooseble: false,
      },
      { prop: "operate", label: "操作", width: 140, slot: "opt" },
      { prop: "changer", label: "修改人", width: 140 },

      // 模版中的元素需要对应的有 slot="opt" 属性
    ];
    return {
      tableData: [
        {
          id: 1,
          title: "2016-05-02",
          preCondition: "王小虎",
          actionCondition: "上海市普陀区金沙江路 1518 弄",
          type: 12312,
          preResult: 1212312312312312312312,
          ps: "123",
          isOk: {
            title: false,
            preCondition: false,
            preResult: false,
            actionCondition: false,
            ps: false,
          },
        },
        {
          id: 4,
          title: "2016-05-04",
          preCondition: "打磨",
          actionCondition: "西岸",
          isOk: {
            title: false,
            preCondition: false,
            preResult: false,
            actionCondition: false,
            ps: false,
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
