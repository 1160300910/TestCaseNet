// my-table.vue
<template>
  <el-table :data="data" :row-class-name="tableRowClassName">
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
        <component
          v-else-if="colConfig.component"
          :isOk="scope.row.isOk[colConfig.prop]"
          :row="scope.row"
          :column_name="colConfig.prop"
          v-focus="test"
          @focus="Test(scope.row)"
          :is="colConfig.component"
          @blur="blurClick(scope.row, scope.column, colConfig.prop)"
          @keyup.enter="blurClick(scope.row, colConfig.prop)"
        >
        </component>
        <span v-else> {{ scope.row[scope.column.property] }} </span>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
export default {
  /*
          
          @keyup.enter="blurClick(scope.row, colConfig.prop)"
          @blur="blurClick(scope.row, colConfig.prop)"*/
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
  props: ["colConfigs", "data"],
  mounted() {},
  methods: {
    Test(data) {
      console.log(data);
    },
    blurClick(row, column, column_name) {
      console.log(column_name);
        row.isOk[column.property] = false;
      /*if (column_name === "title") {
        row.isOk[column.property] = false;
        console.log(row);
      } else if (column_name === "preCondition") {
        row.isOk[column.property] = false;
        console.log(row);
      } else if (column_name === "actionCondition") {
        row.isOk[column.property] = false;
        console.log(row);
      } else if (column_name === "preResult") {
        row.isOk[column.property] = false;
        console.log(row);
      }*/
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
};
</script>
