<template>
  <div>
    <el-button type="primary" @click="handleExpandChildNodes"
      >点我手动【展开】当前选中节点的子节点</el-button
    ><el-button type="danger" @click="handleUnExpandChildNodes" width
      >点我手动【关闭】当前选中节点的子节点</el-button
    >
  </div>
  <el-tree
    ref="tree"
    :data="data"
    node-key="label"
    @node-click="handleNodeClick"
    highlight-current
  ></el-tree>
</template>

<script>
export default {
  mounted() {
    this.$refs["tree"].setCurrentKey("一级 2"); //默认打开的时候，选中一个根node
    this.handleExpandChildNodes(); //并且展开其子节点
  },
  methods: {
    handleNodeClick(data) {
      console.log(data);
    },
    /***
     * 手动展开当前选中节点的全部节点
     */
    handleExpandChildNodes() {
      /**
       * 错误的获取当前节点实例的做法（X）：
       *     var node = this.$refs["tree"].getCurrentNode();
       *     node.expanded =true
       *
       * 正确做法（ √ ）:
       */
      var node = this.$refs.tree.store.currentNode;
      node.expanded = true;
      var child_nodes = new Array();
      child_nodes.unshift(node);
      while (child_nodes.length != 0) {
        var nowNode = child_nodes.pop();
        if (nowNode.childNodes) { //如果有孩子节点才需要进一步遍历
          for (var i = 0; i < nowNode.childNodes.length; i++) {
            console.log(nowNode.childNodes[i].expanded);
            nowNode.childNodes[i].expanded = true;
            child_nodes.unshift(nowNode.childNodes[i]);
          }
        }
      }
      //展开全部节点，需要将全部有子节点的节点的expand改成true
    },
    /***
     * 手动关闭当前选中节点的全部节点
     */
    handleUnExpandChildNodes() {
      /**
       * 错误的获取当前节点实例的做法（X）：
       *     var node = this.$refs["tree"].getCurrentNode();
       *     node.expanded =true
       *
       * 正确做法（ √ ）:
       */
      var node = this.$refs.tree.store.currentNode;
      node.expanded = false;
      //关闭的话，只要关掉根节点的expand属性即可
    },
  },
  data() {
    return {
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
                  label: "三级 2-2-1", children: [
                    {
                      label: "四级 2-2-1-1",
                    },
                  ],
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
  color: #4d95fd;
  font-weight: bold;
  background-color: #dde9ff !important;
}
</style>
