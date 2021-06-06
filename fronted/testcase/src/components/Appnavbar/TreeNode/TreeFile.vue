<template>
  <div class="custom-tree-container">
    <!--div class="tree-condition-suffix">
      <span>创建人：</span>
      <span>筛选器:</span>
    </div-->
    <div class="tree-condition-suffix">
      <el-select v-model="userName">
        <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        >
        </el-option>
      </el-select>

      <el-input placeholder="输入关键字进行过滤" v-model="filterText">
      </el-input>
    </div>
    <div class="block">
      <p>
        测试用例集
        <span>
          <i @click="edit(data)" class="el-icon-edit"></i>
        </span>
      </p>
      <el-tree
        ref="tree"
        :data="data"
        node-key="id"
        :expand-on-click-node="true"
        :filter-node-method="filterNode"
        draggable
        accordion
        highlight-current
        @node-click="OnChooseNode"
        ><template #default="{ node, data }">
          <span class="custom-tree-node">
            <span v-if="testif" span="100">
              <!--i @click="remove(node, data)" 
              class="el-icon-delete"></i-->
              <el-checkbox> </el-checkbox
            ></span>
            <span>{{ node.label }} {{ data.id }}</span>
            <span>
              <!--i @click="edit(data)" class="el-icon-edit">
              :OnAdditionChoice="OnChooseNode(data, node)"
              
              </i-->

              <!--v-bind:nodeInfo="nodeInfo"-->
              <pop-over-operate
                :data="data"
                :nowChild="nowChild"
                :nowParent="nowParent"
              ></pop-over-operate>
              <!--i
                @click="addTestcase(node, data)"
                class="el-icon-circle-plus-outline"
              ></i-->
            </span>
          </span>
        </template>
      </el-tree>
    </div>
  </div>
</template>

<script>
import PopOverOperate from "../ChooseOption/PopOverOperate.vue";
let id = 1000;
export default {
  created() {
    this.userName = this.$route.params.userName;
    this.userWork = this.$route.params.userWork;
  },
  components: { PopOverOperate },
  watch: {
    filterText(val) {
      this.$refs.tree.filter(val);
    },
  },
  methods: {
    /**
     * 展开一级node下的全部子node
     */
    handleExpandChildNodes(data, node) {
      //const len = nodeList.length;
      for (
        var i = 0;
        i < this.$refs.tree.store.currentNode.childNodes.length;
        i++
      ) {
        this.$refs.tree.store.currentNode.childNodes[i].expanded = true;
      }
      //console.log(this.$refs.tree.store.currentNode.childNodes)
      //console.log("---------")
      //console.log(this.$refs.tree.getCheckedKeys())
      //node.expanded = node.expanded; //在组件点击事件 中使用
    },

    filterNode(value, data) {
      //显示过滤节点
      if (!value) return true;
      return data.label.indexOf(value) !== -1;
    },
    OnChooseNode(data, node) {
      console.log(node.store.currentNode.parent.data);
      console.log(node.store.currentNode.childNodes);
      // 保存并传递当前选中节点的数据
      this.nowid = data.id;
      this.nowLabel = data.label;
      this.nowParent = node.store.currentNode.parent;

      console.log(node.store.currentNode.parent);
      this.nowChild = node.store.currentNode.childNodes;
      console.log(data.id + " " + data.label);
      this.handleExpandChildNodes(data, node);
      // console.log(data.label);
    },
    /*
            <el-button size="mini" on-click={() => this.append(store, data)}>
              Append
            </el-button>
            <el-button size="mini" on-click={() => this.remove(store, data)}>
              Delete
            </el-button>
    */
    renderContent(h, { node, data, store }) {
      return (
        <span>
          <span>
            <el-checkbox> </el-checkbox>
            <span>{node.label}</span>
          </span>
          <span style="float: right; margin-right: 20px"></span>
        </span>
      );
    },
    append(data) {
      const newChild = { id: id++, label: "testtest", children: [] };
      if (!data.children) {
        data.children = [];
      }
      data.children.push(newChild);
      this.data = [...this.data];
    },

    remove(node, data) {
      const parent = node.parent;
      const children = parent.data.children || parent.data;
      const index = children.findIndex((d) => d.id === data.id);
      children.splice(index, 1);
      this.data = [...this.data];
    },
    addTestcase() {},
  },
  data() {
    const options = [
      {
        value: "西紫卡",
        label: "11",
      },
    ];

    const data = [
      {
        id: 10,
        label: "人脉",
        children: [
          {
            id: 4,
            label: "入口-1",
            children: [
              {
                id: 9,
                label: "功能-0",
              },
              {
                id: 1,
                label: "功能-1",
              },
            ],
          },
        ],
      },
      {
        id: 2,
        label: "形象",
        children: [
          {
            id: 5,
            label: "形象-入口1",
          },
          {
            id: 6,
            label: "形象-入口2",
            children: [
              {
                id: 9,
                label: "形象功能1",
              },
              {
                id: 10,
                label: "形象功能2",
              },
            ],
          },
        ],
      },
    ];
    return {
      options: options,
      userName: "",
      userWork: "",
      nowid: "",
      nowLabel: "",
      nowParent: "",
      nowChild: "",
      filterText: "",
      data: JSON.parse(JSON.stringify(data)),
      testif: true,
      nodeInfo: {
        nowid: this.nowid,
        nowLabel: this.nowLabel,
      },
    };
  },
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
.tree-condition-suffix {
  flex: 1;
  display: flex;

  justify-content: space-between;
}
</style>
