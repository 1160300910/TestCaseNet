<template>
  <my-table :data="tableData" :col-configs="colConfigs">
    <!-- slot="opt" 不能省略，需要与下面配置项中的对应 -->
    <template #opt="scope">
        <el-button size="mini" @click="Test(scope.data.row)">
          
            {{ scope.data.row.name }}
          
        </el-button>
        <!--el-button size="mini" #default="{row}">查看{{ row }}</el-button-->
    </template>
    <template #input="scope">
        <el-input type="textarea" v-if="true" @focus="Test(scope.data.row)">
              {{ scope.data.row.name }}
        </el-input>
        <span v-else>{{ scope.data.row.name }}</span>
      
    </template>
  </my-table>
</template>

<script>
import myTable from "./my-table.vue";

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
        width: 60,
        editable: true,
      },
      { prop: "name", label: "姓名", width: 50, editable: true },
      { prop: "address", label: "地址", width: 180, editable: true },
      { prop: "info", label: "信息", width: 180, editable: true },
      {
        prop: "type",
        label: "类型",
        width: 70,
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
