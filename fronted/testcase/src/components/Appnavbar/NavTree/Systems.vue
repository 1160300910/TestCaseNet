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
            <span v-else>
              <el-input v-focus="Test(node)" v-model="treeNodeInput" clearable>
              </el-input>
            </span>
            <!--span><i class="el-icon-check">
              </i> </span-->
            <span>
              <!--i @click="edit(data)" class="el-icon-edit">
              :OnAdditionChoice="OnChooseNode(data, node)"
              
              </i-->

              <!--
                :nowChildren="this.parentObj.nowChildren"
                :nowParent="nowParent"-->

              <pop-over-operate
                @updateNode="UpdateChooseNode"
                :node="node"
                :data="data"
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
import axios from "axios";
let caseId = 11112;
export default {
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
      console.log("currentNodeKey");
      // Tree 内部使用了 Node 类型的对象来包装用户传入的数据，用来保存目前节点的状态。可以用 $refs 获取 Tree 实例
      if (caseId.toString()) {
        this.$refs["tree"].setCurrentKey(caseId);
        console.log(caseId);
        //console.log(this.$refs["tree"].getCurrentNode());
        //var nowNode = this.$refs["tree"].getNode(caseId);
        //console.log()
        //this.$refs["tree"].setCurrentNode(nowNode.data);
        // console.log(this.$refs["tree"].store.currentNode.data);
        //this.setCurrentTreePosGlobal();
      } else {
        this.$refs["tree"].setCurrentKey(null);
        alert("ERROR!!!没有找到当前节点的caseId值");
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
      console.log(this.node_data)
      this.node_data = JSON.parse(JSON.stringify(this.parentObj.nodes_data));
      console.log(this.node_data)
      console.log(typeof (this.node_data))
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
    /**
     * 创建新用例
     */
    this.$bus.on("CREATE_NEW_TREENODE_POP", (node) => {
      console.log("CREATE_NEW_TREENODE_POP  发生了");
      this.CreateNewTestCase(node);
    });
  },
  methods: {
    /***
     * 建立某个系统文件夹下的测试用例
     */
    CreateNewTestCase(node) {
      var fileType = "file";
      //从服务器获取新caseId
      axios
        .get("getNewCaseId")
        .then((res) => {
          console.log("异步返回");
          var newCaseId = res.data.msg;
          var newChild = this.createNodeData(newCaseId, fileType);
          console.log(node.childNodes)
          if (!node.data.children) {
            node.data.children = [];
          }
          this.$refs['tree'].append(newChild,node) //新增node
          this.$refs['tree'].setCurrentNode(newChild) //设置当前节点为新增节点
          this.setCurrentTreePosGlobal() //设置孩子节点
          //node.data.children.push(newChild);
          console.log(node.childNodes)
          /*
          new Promise((resolve, reject) => {
            //todo ：等待这步完成
            console.log("finish");
            resolve("success");
          });
          console.log("end");*/
          console.log("????????????????");
          console.log(this.$refs["tree"].getCurrentNode());
          //this.UpdateChooseNode(newCaseId)
          //this.currentNodeKey = newCaseId;

          console.log("????????????????!!!!!");
          this.parentObj.node_data = newChild;

          this.$bus.emit("CREATE_CHOOSE_TEST", {
            caseId: newCaseId,
            type: fileType,
          }); //告诉table，发生了创造事件
         
        })
        .catch(function(error) {
          alert(error);
        });
    },
    Test(node) {
      //this.treeNodeInput = node.label;
      console.log("FOCUS FOCUS");
      console.log(node);
    },
    /***
     * 创建新的系统
     * 1.设置当前选中节点为新建节点，并focus到输入框中
     * 2.右侧的table里新增默认行,设置为待输入模式，且这一行被选中
     * 3.输入当前输入框的标题，table的标题也会一起改变；table输入，这里也一起输入，保持同步
     */
    CreateNewRoot(data) {
      var fileType = "folder";
      //从服务器获取新caseId
      axios
        .get("getNewCaseId")
        .then((res) => {
          var newCaseId = res.data.msg;
          var newChild = this.createNodeData(newCaseId, fileType);
          data.unshift(newChild);
          this.currentNodeKey = newCaseId;
          this.parentObj.node_data = newChild;

          this.$bus.emit("CREATE_CHOOSE_TEST", {
            caseId: newCaseId,
            type: fileType,
          }); //告诉table，发生了创造事件
        })
        .catch(function(error) {
          alert(error);
        });
    },
    /**
     * 设置当前选中的node的值,并展开子node
     */
    async UpdateChooseNode(currentNodeKey, node) {
      console.log("---------------------");
      this.currentNodeKey = currentNodeKey;
      console.log("===========");
    },
    /**
     * 调用函数，展开一级node下的全部子node
     */
    handleExpandChildNodes() {
      var node = this.$refs.tree.store.currentNode;
      node.expanded = true;
      for (var i = 0; i < node.childNodes.length; i++) {
        node.childNodes[i].expanded = true;
      }
      console.log("handleExpandChildNodes");
    },

    filterNode(value, data) {
      //显示过滤节点
      if (!value) return true;
      return data.label.indexOf(value) !== -1;
    },
    /***
     * 用node获取对应的树数据中的当前节点的父节点和儿子节点
     */
    setCurrentTreePosGlobal() {
      var node = this.$refs["tree"].store.currentNode;
      //console.log("setCurrentTreePosGlobal");
      //console.log(node);
      // 获取孩子节点
      var children = node.childNodes;
      /*console.log(children);
      for (var i = 0; i < children.length; i++) {
        console.log("孩子节点:" + i + " ");
        console.log(children[i].data);
      }*/
      //获取父节点
      var parent = node.parent;
      //console.log("父节点:");
      //console.log(parent.data);
      // 保存并传递当前选中节点的数据
      this.parentObj.nowParent = node.parent;
      this.parentObj.nowChildren = node.childNodes;
      //console.log(this.parentObj.nowChildren)
      //console.log(this.parentObj.nowParent)
    },
    /**
     * 1.点击节点，选中该节点,自动展开该节点下面的子节点
     * 2.自动选中table中，对应的caseId
     */
    OnChooseNode(data, node) {
      this.currentNodeKey = node.data.caseId;
      this.$bus.emit("UPDATE_CURRENT_DATA_NODE", node.data.caseId);
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
    /***
     * 新建一个树节点数据
     */
    createNodeData(newCaseId, type) {
      var myDate = new Date();
      myDate.toLocaleString();
      const node = {
        caseId: newCaseId,
        label: "",
        type: type,
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
      filterText: "",
      node_data: JSON.parse(JSON.stringify(node_data)),
      testif: false,
    };
  },
};
</script>

<style>
span > .el-input > .el-input__inner {
  height: 30px;
  width: 100px;
}
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
span {
  display: block;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
.el-tree-node > .el-tree-node__content {
  /*设置选中的样式 */
  height: 40px;
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
