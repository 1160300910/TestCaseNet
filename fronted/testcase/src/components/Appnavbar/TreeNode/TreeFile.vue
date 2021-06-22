<template>
  <div class="custom-tree-container">
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
        <i @click="CreateNewRoot(node_data)" class="el-icon-edit"></i>
      </p>
      <el-tree
        node-key="caseId"
        ref="tree"
        :data="node_data"
        :expand-on-click-node="true"
        :filter-node-method="filterNode"
        draggable
        accordion
        highlight-current
        @node-click="OnChooseNode"
        ><template #default="{ node, data }">
          <span class="custom-tree-node">
            <span v-if="testif" span="1">
              <!--i @click="remove(node, data)" 
              class="el-icon-delete"></i-->
              <el-checkbox> </el-checkbox
            ></span>
            <i class="el-icon-folder-opened" v-if="data.type == 'folder'"> </i>
            <i class="el-icon-star-off" v-else-if="data.type == 'file'"> </i>
            <span v-if="!data.isEditing"
              >{{ node.label }} {{ data.caseId }}</span
            >
            <span v-else
              ><el-input
                v-focus
                @focus="Test(node)"
                v-model="treeNodeInput"
                clearable
                size="mini"
              ></el-input
            ></span>
            <!--span><i class="el-icon-check">
              </i> </span-->
            <span>
              <!--i @click="edit(data)" class="el-icon-edit">
              :OnAdditionChoice="OnChooseNode(data, node)"
              
              </i-->

              <!--v-bind:nodeInfo="nodeInfo"-->

              <pop-over-operate
                @updateNode="UpdateChooseNode"
                :node="node"
                :data="data"
                :nowChildren="nowChildren"
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
let caseId = 11112;
export default {
  directives: {
    //注册一个局部的自定义指令 v-focus
    focus: {
      mounted(el) {
        console.log(el.children[0]);
        el.children[0].focus();
        //因为el-input这是个组件，input外面被一层 div 包裹着,
        ///el打印出来是外面这个 div，需要找到内层的input
      },
    },
  },
  inject: ["parentObj"],
  created() {
    if (this.$route.params.userName && this.$route.params.userWork)
      this.userName = this.$route.params.userName;
    this.userWork = this.$route.params.userWork;
  },
  components: { PopOverOperate },
  watch: {
    /***
     * 当前节点的caseId值
     */
    currentNodeKey(caseId) {
      // Tree 内部使用了 Node 类型的对象来包装用户传入的数据，用来保存目前节点的状态。可以用 $refs 获取 Tree 实例
      if (caseId.toString()) {
        this.$refs["tree"].setCurrentKey(caseId);
        console.log(this.$refs["tree"]);
      } else {
        this.$refs["tree"].setCurrentKey(null);
      }
    },
    /***
     * 当前节点的节点输入值
     */
    treeNodeInput(value) {
      var node = this.$refs["tree"].getCurrentNode();
      console.log(node);
      node.label = value;

      this.$bus.emit("CASE_NAME_TREENODE_CHANGE", {
        value: value,
        rowId: node.caseId,
      }); //告诉table，发生了用例标题修改事件
    },
  },
  mounted() {
    this.$bus.on("UPDATE_TABLE_AND_TREE", () => {
      console.log("UPDATE_TABLE_AND_TREE发生了");
      this.node_data = JSON.parse(JSON.stringify(this.parentObj.nodes_data));
    });
    /**
     * 从table发起了修改caseName
     */
    this.$bus.on("CASE_NAME_TABLE_CHANGE", (param) => {
      console.log(param);
      console.log("CASE_NAME_TABLE_CHANGE发生了");
      //设置当前选中行的caseName为对应的value
      var currentNode = this.$refs["tree"].getCurrentNode();
      currentNode.label = param.value;
      this.treeNodeInput = param.value;
    });
    /**
     * 保存了testCase
     */
    this.$bus.on("SAVE_TABLE_ROW", (param) => {
      var node = this.$refs["tree"].getCurrentNode();
      node.isEditing = false;
    });
  },
  methods: {
    Test(node) {
      this.treeNodeInput = node.label;
    },
    /***
     * 创建新的系统
     * 1.设置当前选中节点为新建节点，并focus
     * 2.右侧的table里新增默认行
     * 3.
     */
    CreateNewRoot(data) {
      console.log(data);
      var newChild = this.createNodeData();
      data.unshift(newChild);
      console.log(newChild.caseId);
      this.currentNodeKey = newChild.caseId;
      this.parentObj.node_data = newChild;
      this.$bus.emit("CREATE_CHOOSE_TEST"); //告诉table，发生了创造事件
    },
    /**
     * 设置当前选中的node的值,并展开子node
     */
    UpdateChooseNode(currentNodeKey, node) {
      console.log("---------------------");
      this.currentNodeKey = currentNodeKey;
      //this.handleExpandChildNodes(node);
    },
    /**
     * 调用函数，展开一级node下的全部子node
     */
    handleExpandChildNodes(node) {
      console.log("handleExpandChildNodes");
      //const len = nodeList.length;
      for (
        var i = 0;
        i < node.childNodes.length;
        //this.$refs.tree.store.currentNode.childNodes.length;
        i++
      ) {
        node.childNodes[i].expanded = true;
        console.log(node.childNodes[i].data);
        console.log(node.childNodes[i].expanded);
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
    /**
     * 点击节点，选中该节点
     */
    OnChooseNode(data, node) {
      console.log(node);
      //console.log(node.store.currentNode.childNodes);
      // 获取孩子节点
      var children = node.childNodes;
      for (var i = 0; i < children.length; i++) {
        console.log("孩子节点:" + i + " ");
        console.log(children[i].data);
      }
      //获取父节点
      var parent = node.parent;
      console.log("父节点:");
      console.log(parent.parent);
      // 保存并传递当前选中节点的数据
      this.data = data;
      this.nowParent = node.parent;
      this.nowChildren = node.childNodes;
      console.log(data.caseId + " " + data.label);
      //自动展开所有的孩子节点
      this.handleExpandChildNodes(node);
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
    /**
     * 增加一个根节点
     */
    appendRoot(data) {
      console.log(data);
      var newChild = this.createNodeData();
      data.unshift(newChild);
      console.log(newChild.caseId);
      this.currentNodeKey = newChild.caseId; //更新当前选中节点
    },
    createNodeData() {
      var myDate = new Date();
      myDate.toLocaleString();
      const node = {
        caseId: caseId++,
        label: "",
        type: "folder",
        children: [],
        isEditing: true,
      };
      return node;
    },
    append(data) {
      const newChild = { caseId: caseId++, label: "testtest", children: [] };
      if (!data.children) {
        data.children = [];
      }
      data.children.push(newChild);
      this.data = [...this.data];
    },

    remove(node, data) {
      const parent = node.parent;
      const children = parent.data.children || parent.data;
      const index = children.findIndex((d) => d.caseId === data.caseId);
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

    const node_data = [
      {
        caseId: 1,
        label: "人脉",
        type: "folder",
        children: [
          {
            caseId: 4,
            label: "入口-1",
            children: [
              {
                caseId: 9,
                label: "功能-0",
              },
              {
                caseId: 10,
                label: "功能-1",
              },
            ],
          },
        ],
      },
      {
        caseId: 2,
        label: "形象",
        type: "file",
        children: [
          {
            caseId: 5,
            label: "形象-入口1",
          },
          {
            caseId: 6,
            label: "形象-入口2",
            children: [
              {
                caseId: 19,
                label: "形象功能1",
              },
              {
                caseId: 110,
                label: "形象功能2",
              },
            ],
          },
        ],
      },
    ];
    return {
      treeNodeInput: "",
      currentNodeKey: "", //保存了当前选中节点的caseId信息，用于更新选中状态
      options: options,
      userName: "西子卡",
      userWork: "QA",
      nowParent: "",
      nowChildren: "",
      filterText: "",
      node_data: JSON.parse(JSON.stringify(node_data)),
      testif: false,
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
