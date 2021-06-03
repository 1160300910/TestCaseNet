// my-table.vue
<template>
  <el-table :data="data">
    <template v-for="colConfig in colConfigs" :key="colConfig.prop" >
        <!--插槽类型，读取colConfig作为插槽名，用:data来将列名colConfig.data.label传到外面-->
      <slot v-if="colConfig.slot" :name="colConfig.slot" :data="colConfig">
      </slot>
      <!--当不是插槽类型的列时，直接使用 label作为列名，读取data的每一个prop作为列的内容-->
      <el-table-column
        v-if="!colConfig.slot"
        :prop="colConfig.prop"
        :label="colConfig.label"
        :width="colConfig.width"
      ></el-table-column>
    </template>
  </el-table>
</template>

<script>
export default {
  props: ["colConfigs", "data"],
  mounted() {},
  methods: {
    test() {},
  },
};
</script>