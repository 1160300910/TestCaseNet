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
        <i @click="CreateNewRoot()" class="el-icon-edit"></i>
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
        @node-click="OnTreeClickChooseNode"
        ><template #default="{ node, data }">
          <span class="custom-tree-node">
            <span v-if="testif" span="1">
              <!--i @click="remove(node, data)" 
              class="el-icon-delete"></i-->
              <el-checkbox> </el-checkbox
            ></span>
            <div class="node_label" v-if="!data.isEditing">
              <i class="el-icon-folder-opened" v-if="data.type == 'folder'">
              </i>
              <i class="el-icon-star-off" v-else-if="data.type == 'file'"> </i>
              <span>{{ node.label }} {{ data.caseId }}</span>
              <pop-over-operate
                @updateNode="UpdateChooseNode"
                :node="node"
                :data="data"
              ></pop-over-operate>
            </div>
            <div class="node_editing" v-else>
              <i class="el-icon-folder-opened" v-if="data.type == 'folder'">
              </i>
              <i class="el-icon-star-off" v-else-if="data.type == 'file'"> </i>
              <el-input v-focus="Test(node)" v-model="treeNodeInput" clearable>
              </el-input>
              <i
                class="el-icon-circle-check"
                style="font-size: 25px; color: green"
                @click="saveNewTreeNodeFolder(data, node)"
              >
              </i>
            </div>
            <!--span><i class="el-icon-check">
              </i> </span-->
            <span>
              <!--i @click="edit(data)" class="el-icon-edit">
              :OnAdditionChoice="OnChooseNode(data, node)"
              
              </i-->

              <!--
                :nowChildren="this.parentObj.nowChildren"
                :nowParent="nowParent"-->

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
    this.initTreeNodeData();
    if (this.$route.params.userName && this.$route.params.userWork)
      this.userName = this.$route.params.userName;
    this.userWork = this.$route.params.userWork;
  },
  components: { PopOverOperate },
  watch: {
    /***
     * 当前节点的caseId值
     */
    /*
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
    },*/
    /***
     * 当前节点的节点输入值
     */
    treeNodeInput(value) {
      var node = this.$refs["tree"].getCurrentNode();
      console.log(node);
      node.label = value;

      this.$bus.emit("CASE_NAME_TREENODE_CHANGE", {
        value: value,
        node: node,
      }); //告诉table，发生了用例标题修改事件
    },
  },
  mounted() {
    this.$bus.on("UPDATE_TABLE_AND_TREE", (NodeRoots) => {
      console.log("UPDATE_TABLE_AND_TREE发生了");
      //console.log(this.node_data);
      this.node_data = JSON.parse(JSON.stringify(NodeRoots));
      //console.log(this.node_data);
      //console.log(typeof this.node_data);
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
    /***
     * 创建新TreeNode节点
     */
    this.$bus.on("CREATE_NEW_TESTCASE_NODE_POP", (param) => {
      console.log(
        "CREATE_NEW_TESTCASE_NODE_POP 发生了————节点类型： " + param.fileType
      );
      this.CreateNewTreeNode(param.data, param.node, param.fileType);
    });
  },
  methods: {
    /***
     * 创建新的系统文件夹
     * 1.设置当前选中节点为新建节点，并focus到输入框中
     * 2.右侧的table里新增默认行,设置为待输入模式，且这一行被选中
     * 3.输入当前输入框的标题，table的标题也会一起改变；table输入，这里也一起输入，保持同步
     */
    CreateNewRoot() {
      var fileType = "folder";
      //从服务器获取新caseId
      axios
        .get("getNewCaseId")
        .then((res) => {
          var newCaseId = res.data.msg;
          var newChild = this.CreateNodeData(newCaseId, fileType);
          console.log(this.$refs["tree"]);
          this.$refs["tree"].append(newChild, null); //新增node
          this.$refs["tree"].setCurrentNode(newChild);
          //this.parentObj.node_data = newChild;
        })
        .catch(function(error) {
          alert(error);
        });
    },

    /***
     * 保存新建节点文件夹
     * 1.保存节点之间的关系
     * 2.保存节点本身到testCase表
     */
    saveNewTreeNodeFolder(data, node) {
      console.log("---saveNewTreeNodeFolder---");
      console.log(data);
      data.isEditing = false;
      data.label = this.treeNodeInput;
      this.changeFolderNodeData(data, node);
      this.saveNodePath(data.caseId);
    },
    /**
     * 修改文件夹类型的测试用例节点数据
     * 保存到服务器
     */
    changeFolderNodeData(data, node) {
      var fatherId;
      console.log("changeFolderNodeData");
      console.log(this.$refs["tree"].store.currentNode.parent.data);
      console.log(node.data);
      console.log(node.parent.data);
      if (node.parent.parent == null) {
        //如果父节点的父节点没有数据
        fatherId = -1;
      } else {
        fatherId = node.parent.data.caseId;
      }

      axios
        .post("changeFolderNodeData", {
          caseId: data.caseId,
          caseName: data.label,
          fileType: "folder",
          changer: this.parentObj.userId,
          fatherId: fatherId,
        })
        .then((res) => {
          console.log(res);
        })
        .catch(function(error) {
          alert(error);
        });
    },
    /***
     * 新建一个树节点数据
     */
    CreateNodeData(newCaseId, type) {
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
    /***
     * 创造文件新节点类型
     * 在节点的后面增加一个新节点
     */
    createFileNewNode(data, node, fileType, newCaseId) {
      var newChild = this.CreateNodeData(newCaseId, fileType);
      this.$refs["tree"].insertAfter(newChild, node); //为节点的后面增加一个节点
      this.$refs["tree"].setCurrentNode(newChild); //设置当前节点为新增节点
      this.$bus.emit("CREATE_NEW_TESTCASE_NOTIFY_TABLE", {
        caseId: newCaseId,
        type: fileType,
      }); //告诉table，发生了创造事件*/
    },
    /***
     * 创建子文件夹新节点类型，
     */
    createFolderNewNode(data, node, fileType, newCaseId) {
      var newChild = this.CreateNodeData(newCaseId, fileType);
      this.$refs["tree"].append(newChild, node); //新增node
      this.$refs["tree"].setCurrentNode(newChild); //设置当前节点为新增节点
    },
    /**
     * 新建树节点
     */
    CreateNewTreeNode(data, node, fileType) {
      //从服务器获取新caseId
      axios
        .get("getNewCaseId")
        .then((res) => {
          var newCaseId = res.data.msg;
          console.log(node.childNodes);
          if (fileType == "file") {
            this.createFileNewNode(data, node, fileType, newCaseId);
          } else if (fileType == "folder") {
            this.createFolderNewNode(data, node, fileType, newCaseId);
          } else {
            alert("只能是文件夹或者文件类型！");
          }
          /*
          if (!node.data.children) {
            node.data.children = [];
          }
          this.$refs["tree"].append(newChild, node); //新增node
          this.$refs["tree"].setCurrentNode(newChild); //设置当前节点为新增节点
          //this.setCurrentTreePosGlobal(); //设置全局孩子节点
          //this.saveNodePath(newCaseId); //保存节点路径

          console.log(node.childNodes); */

          //console.log("????????????????");
          //console.log(this.$refs["tree"].getCurrentNode());

          //console.log("????????????????!!!!!");
          //this.parentObj.node_data = newChild;
          /*
          this.$bus.emit("CREATE_CHOOSE_TEST", {
            caseId: newCaseId,
            type: fileType,
          }); //告诉table，发生了创造事件*/
        })
        .catch(function(error) {
          alert(error);
        });
    },
    /**
     * 初始化数据，获取测试用例目录数组
     */
    initTreeNodeData() {
      axios
        .get("getUserTestCaseNodesArray", {
          params: { userId: this.parentObj.userId },
        })
        .then((res) => {
          var NodeRoots = res.data.msg;
          this.node_data = JSON.parse(JSON.stringify(NodeRoots));
        })
        .catch(function(error) {
          alert(error);
        });
    },
    /**
     * 1.对于文件夹，点击节点，选中该节点,自动展开该节点下面的子节点；
     *   右侧显示子一级的全部用例
     * 2.对于不可展开的用例，自动选中table中对应的caseId的行
     */
    OnTreeClickChooseNode(data, node) {
      //this.currentNodeKey = node.data.caseId;
      console.log(node);
      this.$refs["tree"].setCurrentNode(data); //设置当前节点为选中节点
      //this.$bus.emit("UPDATE_CURRENT_DATA_NODE", node.data);
      if (data.type == "folder") {
        this.getFolderNodeDatas(data.caseId);
      } else if (data.type === "file") {
        this.getFileNodeDataChoosed(data.caseId);
      } else {
        alert("节点只能是文件或者文件夹类型！！！");
      }
    },
    /***
     * 获取文件夹类型节点下的直接子用例节点
     */
    getFolderNodeDatas(caseId) {
      axios
        .get("getFolderTableTestCases", {
          params: {
            caseId: caseId,
          },
        })
        .then((res) => {
          console.log(res.data.msg);
          this.$bus.emit("UPDATE_CURRENT_FOLDER_TABLEDATAS", res.data.msg);
        })
        .catch(function(error) {
          alert("Error " + error);
        });
    },
    /***
     * 获取文件类型节点下的直接子用例节点
     * 自动选中table中，对应的caseId
     */
    getFileNodeDataChoosed(caseId) {},

    /**
     * 设置当前选中的node的值,并展开子node
     */
    UpdateChooseNode(data, node, caseId) {
      //console.log("---------------------");
      //this.currentNodeKey = currentNodeKey;
      this.$refs["tree"].setCurrentNode(data); //设置当前节点为选中节点
      //console.log("===========");
    },
    //————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
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
          var newChild = this.CreateNodeData(newCaseId, fileType);
          console.log(node.childNodes);
          if (!node.data.children) {
            node.data.children = [];
          }
          this.$refs["tree"].append(newChild, node); //新增node
          this.$refs["tree"].setCurrentNode(newChild); //设置当前节点为新增节点
          this.setCurrentTreePosGlobal(); //设置全局孩子节点
          this.saveNodePath(newCaseId); //保存节点路径

          console.log(node.childNodes);

          console.log("????????????????");
          console.log(this.$refs["tree"].getCurrentNode());

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
    /***
     * 保存节点路径
     */
    saveNodePath(caseId) {
      var path_node = this.$refs["tree"].store.currentNode; // this.$refs["tree"].getCurrentNode();

      console.log("savePath");
      console.log(path_node);
      //console.log(this.$refs["tree"].store.currentNode.parent);
      var level = 0;
      while (path_node.parent) {
        console.log(
          "savePathInside:level: " +
            level +
            " path_node: " +
            path_node.data.caseId
        );
        axios
          .post("saveTestCasePath", {
            caseId: caseId,
            ancestorId: path_node.data.caseId,
            level: level,
          })
          .then((res) => {
            console.log(res);
          })
          .catch(function(error) {
            alert("Error " + error);
          });
        level += 1;
        path_node = path_node.parent;
        console.log(path_node);
      }
    },
    Test(node) {
      //this.treeNodeInput = node.label;
      console.log("FOCUS FOCUS");
      console.log(node);
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
      //this.currentNodeKey = newChild.caseId; //更新当前选中节点
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
.node_editing > .el-input > .el-input__inner {
  height: 30px;
  width: 120px;
}
.node_editing {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  padding-right: 8px;
}
.node_label {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  padding-right: 8px;
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
