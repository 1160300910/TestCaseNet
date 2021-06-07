
<template>
<div class="custom-tree-container">
  <div class="block">
    <p>测试用例集</p>
    <el-tree
      :data="data"
      show-checkbox
      node-key="caseId"
      default-expand-all
      :expand-on-click-node="false"
      :render-content="renderContent">
    </el-tree>
  </div>
  
</div>
</template>

<script>
  let caseId = 1000;

  export default {
    data() {
      const data = [{
        caseId: 1,
        label: '一级 1',
        children: [{
          caseId: 4,
          label: '二级 1-1',
          children: [{
            caseId: 9,
            label: '三级 1-1-1'
          }, {
            caseId: 10,
            label: '三级 1-1-2'
          }]
        }]
      }, {
        caseId: 2,
        label: '一级 2',
        children: [{
          caseId: 5,
          label: '二级 2-1'
        }, {
          caseId: 6,
          label: '二级 2-2'
        }]
      }, {
        caseId: 3,
        label: '一级 3',
        children: [{
          caseId: 7,
          label: '二级 3-1'
        }, {
          caseId: 8,
          label: '二级 3-2'
        }]
      }];
      return {
        data: JSON.parse(JSON.stringify(data)),
      }
    },

    methods: {
      append(data) {
        const newChild = { caseId: caseId++, label: 'testtest', children: [] };
        if (!data.children) {
          data.children = []
        }
        data.children.push(newChild);
        this.data = [...this.data]
      },

      remove(node, data) {
        const parent = node.parent;
        const children = parent.data.children || parent.data;
        const index = children.findIndex(d => d.caseId === data.caseId);
        children.splice(index, 1);
        this.data = [...this.data]
      },

      
    }
  };
</script>

<style>
.custom-tree-node {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 14px;
    padding-right: 8px;
  }
</style>
