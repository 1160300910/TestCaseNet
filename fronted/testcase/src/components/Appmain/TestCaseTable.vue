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
          v-if="!scope.data.row.isRowOk"
          circle
          @click="
            ChangeTestCase(this.colConfigs, scope.data.row.id, this.tableData)
          "
        ></el-button>
        <el-button
          v-else
          size="mini"
          type="success"
          icon="el-icon-circle-check"
          circle
          @click="
            SaveChange(this.colConfigs, scope.data.row.id, this.tableData)
          "
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
      <el-select v-model="scope.data.row.test_level" placeholder="P0">
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
  props: ["row", "column_name", "isOk", "isRowOk"],
  template: `
      <el-input type="textarea" v-if="isOk || isRowOk" v-model="row[column_name]">
      </el-input>
      <span v-else><span> {{ row[column_name]}}</span></span>
    `,
};

import axios from "axios";
export default {
  inject: ["parentObj"],
  mounted() {
    //在组件B中监听动作的发生
    this.$bus.on("CHANGE_CHOOSE_TEST", () => {
      console.log("CHANGE_CHOOSE_TEST发生了");
      this.ChangeTestCase(
        this.colConfigs,
        this.parentObj.nowId,
        this.tableData
      );
    });
  },
  methods: {
    /**
     * 保存测试用例的修改到服务器
     *
     */
    SaveChange(colConfigs, id, tableData) {
      var that = this;
      //用例编号，父用例文件夹id，类型（文件夹or用例）
      //用例标题，用例等级,前置条件，执行条件，预期结果，备注，标签，修改人
      var fatherId, type, data, childId;
      data = this.FindNodeEdit(id, tableData);
      if (!this.parentObj.nowChild.data) {
        type = -1; //Child
        childId = -1;
      } else {
        childId = that.parentObj.nowChild.data.id;
        type = 1; //Parent
      }
      if (!that.parentObj.nowParent.data) {
        alert(that.parentObj.nowParent.data);
        fatherId = -1;
      } else {
        alert(that.parentObj.nowParent.data);
        alert(that.parentObj.nowParent.data.id);
        fatherId = that.parentObj.nowParent.data.id;
      }
      if (data) {
        axios
          .post("saveTestCase", {
            id: id,
            fatherId: fatherId,
            childId: childId,
            type: type,

            title: data.title,
            test_level: data.test_level,
            preCondition: data.preCondition,
            actionCondition: data.actionCondition,
            preResult: data.preResult,
            ps: data.ps,
            tag: data.tag,
            changer: data.changer,
          })
          .then((res) => {
            console.log(res);

            //是需要修改的行
            data.isRowOk = false;
          })
          .catch(function(error) {
            console.log(that.parentObj.nowParent.data);
            console.log(childId);
            console.log(type);
            console.log(data);
            alert("Error " + error);
          });
      }
    },
    /***
     * 从列表里找到对应的id的数据,修改其他id数据为不可编辑状态
     * id:对应的用例id
     * tableData:表格数据
     */
    FindNodeEdit(id, tableData) {
      var data;
      for (data in tableData) {
        data = tableData[data];
        if (id == data.id) {
          return data;
        } else {
          data.isRowOk = false;
        }
      }
      return false;
    },
    /**
     * 修改测试用例，将对应行全部可编辑区域变成可编辑状态
     * colConfigs ：
     * id ：需要修改表格的行id
     * tableData ：表格数据
     */
    ChangeTestCase(colConfigs, id, tableData) {
      console.log(id);
      var colConfig, data, title, propName;
      data = this.FindNodeEdit(id, tableData);
      if (data) {
        //是需要修改的行
        data.isRowOk = true;
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
      isEditing: false,
      tableData: [
        {
          id: 1,
          title: "2016-05-02",
          preCondition: "王小虎",
          actionCondition: "上海市普陀区金沙江路 1518 弄",
          type: 12312,
          preResult: 1212312312312312312312,
          ps: "123",
          isRowOk: false,
          test_level: "P1",
          changer: "西子卡",
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
          isRowOk: false,
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
