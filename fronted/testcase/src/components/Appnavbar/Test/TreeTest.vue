<template>
  <el-button @click="CreateNode(data)">点击新建节点</el-button>

  <el-tree
    ref="tree"
    :data="data"
    :props="defaultProps"
    node-key="label"
    @node-click="handleNodeClick"
    highlight-current
  ></el-tree>
</template>

<script>
export default {
  watch: {
    currertKey(label) {
      if (label) {
        this.$refs["tree"].setCurrentKey(label);
        //或者this.$refs.tree.setCurrentKey(label);
      } else {
        this.$refs["tree"].setCurrentKey(null);
      }
    },
  },
  methods: {
    CreateNode(data) {
      var newChild = this.createNodeData();
      data.unshift(newChild);
      this.currertKey = newChild.label;
      //this.refreshNode(newChild.label);
    },
    createNodeData() {
      var myDate = new Date();
      const node = {
        caseId: this.caseId++,
        label: myDate.toLocaleString(),
        type: "folder",
        children: [],
      };
      return node;
    },
    handleNodeClick(data) {
      console.log(data);
    },
  },
  data() {
    return {
      currertKey: "",
      data: [
        {
          label: "一级 1",
          children: [
            {
              label: "二级 1-1",
              children: [
                {
                  label: "三级 1-1-1",
                },
              ],
            },
          ],
        },
        {
          label: "一级 2",
          children: [
            {
              label: "二级 2-1",
              children: [
                {
                  label: "三级 2-1-1",
                },
              ],
            },
            {
              label: "二级 2-2",
              children: [
                {
                  label: "三级 2-2-1",
                },
              ],
            },
          ],
        },
        {
          label: "一级 3",
          children: [
            {
              label: "二级 3-1",
              children: [
                {
                  label: "三级 3-1-1",
                },
              ],
            },
            {
              label: "二级 3-2",
              children: [
                {
                  label: "三级 3-2-1",
                },
              ],
            },
          ],
        },
      ],
      defaultProps: {
        children: "children",
        label: "label",
      },
    };
  },
};
</script>

<style>
.el-tree-node:focus > .el-tree-node__content {
  /*设置选中的样式 */
  background-color: #dde9ff !important;
}
.el-tree-node__content:hover {
  /*设置鼠标飘过的颜色 */
  background: #eaf9ff !important;
  color: #007bff;
}

.el-tree--highlight-current .el-tree-node.is-current > .el-tree-node__content {
  /*current选中的样式 */
  color: white;
  font-weight: bold;
  background-color: rgb(3, 155, 191) !important;
}
/*
* 行样式
*/
.node_row_css{
  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;
  justify-content: flex-start;
  align-items: center;
}

/*
 * 行内元素样式
 */
 .node_row_label_css{
   margin-left: 5px;
   margin-right: 5px;
 }
 
</style>
