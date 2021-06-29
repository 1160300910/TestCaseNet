// my-table.vue
<template>
  <el-table :data="data" :row-class-name="tableRowClassName" ref="my-table"
  >
    <el-table-column
      v-for="colConfig in colConfigs"
      :key="colConfig.prop"
      :property="colConfig.prop"
      :label="colConfig.label"
      :width="colConfig.width"
    >
      <template #default="scope">
        <slot v-if="colConfig.slot" :name="colConfig.slot" :data="scope">
        </slot>
        <!--当不处于整行编辑模式的时候-->
        <component
          v-else-if="colConfig.component && !scope.row.isRowEditing"
          :isColumnEditing="scope.row.isColumnEditing[colConfig.prop]"
          :row="scope.row"
          :column_name="colConfig.prop"
          v-focus-table
          :isRowEditing="scope.row.isRowEditing"
          :is="colConfig.component"
          :options="options"
        >
        </component>
        <component
          v-else-if="colConfig.component"
          :isColumnEditing="scope.row.isColumnEditing[colConfig.prop]"
          :row="scope.row"
          :column_name="colConfig.prop"
          :isRowEditing="scope.row.isRowEditing"
          :is="colConfig.component"
          :options="options"
        >
        </component>
        <span v-else> {{ scope.row[scope.column.property] }} </span>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
import axios from "axios";
export default {
  directives: {
    //注册一个局部的自定义指令 v-focus
    focusTable: {
      mounted(el) {
        //console.log(el);
        el.children[0].focus();
        //因为el-input这是个组件，input外面被一层 div 包裹着,
        ///el打印出来是外面这个 div，需要找到内层的input
      },
    },
  },
  props: ["colConfigs", "data"],
  created() {
    this.getChangers();
  },
  mounted() {
    /***
     * 从节点位置修改列表title
     */
    this.$bus.on("CASE_NAME_TREENODE_CHANGE", (param) => {
      //console.log(param);
      //console.log("CASE_NAME_TREENODE_CHANGE发生了");
      if (param.node.type == "file") {
        //设置当前选中行的caseName为对应的value
        var currentRow = this.FindCurrentTableRow(param.node.caseId);
        //console.log(currentRow);
        //console.log(this.data);
        currentRow.caseName = param.value;
      }
    });
  },
  methods: {
    /**
     * 获取修改人（只能是QA）
     */
    getChangers() {
      axios
        .get("getQAPeoData")
        .then((res) => {
          //console.log(res.data.msg);
          var changer = [];
          for (var p = 0; p < res.data.msg.length; p++) {
            changer.unshift({
              value: res.data.msg[p].peoName,
              key: res.data.msg[p].peoId,
            });
          }
          this.options.changer = changer;
          //console.log("this.options.changer");
          //console.log(this.options.changer);
        })
        .catch(function(error) {
          alert(error);
        });
    },
    /**
     * ——————————————————————————————————————————————————————————————————————
     */
    /**
     * 获取标签
     */
    getTags() {},
    /***
     * 查找当前的选中行
     */
    FindCurrentTableRow(rowId) {
      var d;
      for (d = 0; d < this.data.length; d++) {
        console.log(this.data[d]);
        if (this.data[d].caseId == rowId) {
          return this.data[d];
        }
      }
    },
    /**
     * 设置当前的选中行
     * 在父组件里调用 this.$refs.['子组件名'].ChangeCurrentRow(row)
     * 能通过调用子组件，设置当前选中行
     *
     */
    ChangeCurrentRow(row) {
      this.$refs["my-table"].setCurrentRow(row);
    },

    tableRowClassName({ row, rowIndex }) {
      if (rowIndex === 1) {
        return "warning-row";
      } else if (rowIndex === 0) {
        return "success-row";
      }
      return "";
    },
  },
  data() {
    return {
      options: {
        test_level: [
          {
            value: "P0",
            key: "P0",
          },
          {
            value: "P1",
            key: "P1",
          },
          {
            value: "P2",
            key: "P2",
          },
          {
            value: "P3",
            key: "P3",
          },
          {
            value: "P4",
            key: "P4",
          },
        ],
        changer: [],
        tag: [],
      },
    };
  },
};
</script>
