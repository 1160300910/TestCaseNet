<template>
  <div class="navbar">
    <el-tabs
      type="border-card"
      v-model="activeName"
      @tab-click="handleClick"
      strech="true"
    >
      <el-tab-pane  name ="first">
        <template #label>
          <span><i class="el-icon-date"></i> 系统tab</span>
        </template>

        <tree-node></tree-node>
      </el-tab-pane>
      <el-tab-pane name ="second">
        <template #label>
          <span><i class="el-icon-edit"></i> 待执行</span>
        </template>

        当前待执行tab
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import TreeNode from "./TreeNode/TreeFile";
export default {
  components: { TreeNode },
  data() {
    return {
      activeName: "first",
    };
  },
  methods: {
    handleClick(tab, event) {
      console.log(tab, event);
    },
  },
};
</script>
