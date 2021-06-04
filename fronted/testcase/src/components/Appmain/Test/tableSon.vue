// my-table.vue
<template>
  <el-table :data="data">
    <el-table-column
      v-for="colConfig in colConfigs"
      :key="colConfig.prop"
      :property="colConfig.prop"
      :label="colConfig.label"
    >
      <template #default="scope">
        <slot v-if="colConfig.slot" :name="colConfig.slot" :data="scope">
        </slot>
        <component
          @click="componentTest(scope, colConfig.prop)"
          :data="scope.row"
          :label="colConfig.prop"
          v-else-if="colConfig.component"
          :is="colConfig.component"
        >
        </component>
        <span v-else> {{ scope.row[scope.column.property] }} </span>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
export default {
  props: ["colConfigs", "data"],
  date() {
    return {
      componentInfo: "",
    };
  },
  mounted() {
  },
  methods: {
    componentTest(scope, colConfigName) {
      console.log(scope["row"][colConfigName]);
      this.componentInfo = scope["row"][colConfigName];
    },
  },
};
</script>
