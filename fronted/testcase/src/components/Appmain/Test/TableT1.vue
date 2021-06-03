<template>
  <my-table :data="tableData" :col-configs="colConfigs">
      <!--定义一个插槽（slot），列名为 :label="colConfig.data.label" ，列里的值的标记为 :prop="colConfig.data.prop"，列宽度被设置为：
        :width="colConfig.data.width" 并且这个插槽slot里放了一个按钮-->
    <template #opt="colConfig">
      <el-table-column
        :prop="colConfig.data.prop"
        :label="colConfig.data.label"
        :width="colConfig.data.width"
      >
        <el-button size="mini" @click="Test(colConfig)">
          {{ colConfig.data.label }}
        </el-button>
      </el-table-column>
    </template>
    <!--定义一个插槽（slot），列名为 :label="colConfig.data.label" ，列里的值的标记为 :prop="colConfig.data.prop"，列宽度被设置为：
        :width="colConfig.data.width" 并且这个插槽slot里放了一个输入框-->
    <template #input="colConfig"
      ><el-table-column
        :prop="colConfig.data.prop"
        :label="colConfig.data.label"
        :width="colConfig.data.width"
      >
        <el-input type="textarea" v-if="true" placeholder="colConfig.data.label">
          }</el-input
        >
        <span v-else>{{ scope.row.actionmethod }}</span>
      </el-table-column>
    </template>
  </my-table>
</template>

<script>
import myTable from "./table.vue";

export default {
  methods: {
    Test(data) {
      console.log(data);
    },
  },
  components: { myTable },
  data() {
    this.colConfigs = [
      {
        prop: "date",
        label: "日期",
        width: 160,
        editable: true,
      },
      { prop: "name", label: "姓名", width: 150, editable: true },
      { prop: "address", label: "地址", width: 180, editable: true },
      { prop: "info", label: "信息", width: 180, editable: true },
      {
        prop: "type",
        label: "类型",
        width: 270,
        editable: true,
        chooseble: false,
        slot: "input",
        resize: "both",
      },
      { prop: "test", label: "测试", width: 140, slot: "opt" },

      // 模版中的元素需要对应的有 slot="opt" 属性
    ];
    return {
      tableData: [
        {
          date: "2016-05-02",
          name: "王小虎",
          address: "上海市普陀区金沙江路 1518 弄",
          type: 12312,
          info: 1212312312312312312312,
          test: 123,
        },
        {
          date: "2016-05-04",
          name: "打磨",
          address: "西岸",
        },
      ],
    };
  },
};
</script>
