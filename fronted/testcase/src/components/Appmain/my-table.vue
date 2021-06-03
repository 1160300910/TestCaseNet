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
        <span v-else> {{ scope.row[scope.column.property] }} </span>
        <!-- 渲染对应表格里面的内容 -->
      </template>
    </el-table-column>
    <!--template v-for="colConfig in colConfigs" :key="colConfig.prop"-->
    <!--slot v-if="colConfig.slot" > </slot-->
    <!--slot v-if="colConfig.slot" :name="colConfig.slot" :data="colConfig"-->
    <!--component
          v-if="colConfig.component"
          :is="config.componet"
          :col-config="colConfig"
        ></component-->
    <!--/slot>
      <el-table-column
        v-if="!colConfig.slot"
        :prop="colConfig.prop"
        :label="colConfig.label"
        :width="colConfig.width"
      ></el-table-column>
    </template-->
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
