<template>
  <div class="custom-tree-container">
    <div class="tree-condition-suffix">
      <!--el-select v-model="userName" @change="getNodeDataByUser(userName)">
        <el-option
          v-for="item in parentObj.options.QAs"
          :key="item.key"
          :label="item.label"
          :value="item.value"
        >
        </el-option>
      </el-select-->
      <el-input placeholder="关键字过滤查询" v-model="filterText"> </el-input>
    </div>
    <div class="navbar_tree_css">
      <p>
        新增用例系统集
        <i @click="CreateNewRoot()" class="el-icon-edit"></i>
      </p>
      <el-tree
        node-key="caseId"
        ref="tree"
        :data="node_data"
        :expand-on-click-node="false"
        :filter-node-method="filterNode"
        draggable
        accordion
        highlight-current
        @node-click="OnTreeClickChooseNode"
        @node-expand="OnTreeClickChooseNode"
        @node-contextmenu="OnActivatePopOver"
        @node-collapse="OnTreeClickChooseNode"
        ><template #default="{ node, data }">
          <span>
            <span v-if="testif" span="1">
              <!--i @click="remove(node, data)" 
              class="el-icon-delete"></i-->
              <el-checkbox> </el-checkbox
            ></span>
            <div class="node_row_no_editing_css" v-if="!data.isEditing">
              <i v-if="data.type == 'folder' && node.expanded">
                <img
                  src="/icons/icon-folder-opened.png"
                  style="width:20px; height: 20px"
                />
              </i>
              <i v-if="data.type == 'folder' && !node.expanded">
                <img
                  src="/icons/icon-folder.png"
                  style="width:20px; height: 20px"
                />
              </i>
              <i v-else-if="data.type == 'file'">
                <img
                  src="/icons/icon-file.png"
                  style="width:20px; height: 20px"
                />
              </i>
              <span class="node_row_label_css" v-if="data.type == 'folder'"
                >{{ node.label }} ({{ data.testCase_num }})
                {{ data.caseId }}
              </span>
              <span class="node_row_label_css" v-else-if="data.type == 'file'">
                {{ node.label }} {{ data.caseId }}
              </span>
              <!--pop-over-operate
                @updateCurrentNode="updateCurrentNode"
                :node="node"
                :data="data"
              ></pop-over-operate-->
            </div>

            <div class="node_row_editing_css" v-else>
              <i class="el-icon-folder-opened" v-if="data.type == 'folder'">
              </i>
              <i class="el-icon-star-off" v-else-if="data.type == 'file'"> </i>
              <!--
                -->
              <el-input
                v-focus-input="InputVFocus(node)"
                v-model="treeNodeInput"
                clearable
                ref="caseNodeNameInput"
                autofocus
              >
              </el-input
              ><i
                class="el-icon-circle-close"
                style="font-size: 25px; color: red"
                @click="cancelNodeEditing(data, node)"
              ></i>
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
            </span>
          </span>
        </template>
      </el-tree>
    </div>
  </div>
</template>

<script>
import { store } from '@/store/store.js'
import axios from "axios";
let caseId = 11112;
export default {
  directives: {
    //注册一个局部的自定义指令 v-focus-Input
    focusInput: {
      mounted(el) {
        console.log(
          "el.querySelector()==========================================="
        );
        console.log(el.children[0]);
        el.querySelector("input").focus();
        console.log(el.querySelector("input"));
        //因为el-input这是个组件，input外面被一层 div 包裹着,
        ///el打印出来是外面这个 div，需要找到内层的input
      },
    },
  },
  beforeUnmount() {},
  inject: ["parentObj"],
  created() {
    var userData = store.getUserData()
    if (
      userData.userName &&
      userData.work &&
      userData.userId
    ) {
        this.userName = userData.userName;
      this.userWork = userData.work;
      this.userId = userData.userId;
      this.initTreeNodeData(this.userName, this.userId);
    }
  },
  components: {},
  watch: {
    /**
     * 实时根据输入的过滤内容输出过滤结果
     */
    filterText(val) {
      this.$refs.tree.filter(val);
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
        node: node,
      }); //告诉table，发生了用例标题修改事件
    },
  },

  destroy() {
    // 必须移除监听器，不然当该vue组件被销毁了，监听器还在就会出错
    /*window.removeEventListener("scroll", this.onTreeNodeScroll);
  
  */
  },
  mounted() {
    /***
     * 监听全部的滑动事件，限制监听的修改对象为树
     * 
      window.addEventListener("scroll", this.onTreeNodeScroll, true);
    */

    /***
     * 发起修改当前文件夹名
     */
    this.$bus.on("SET_SYSTEM_CURRENT_NODE_NULL", () => {
      this.$refs["tree"].setCurrentKey(null);
      //console.log(param.node.data)
    });
    /***
     * 发起修改当前文件夹名
     */
    this.$bus.on("CHANGE_TESTCASE_FOLDER_BY_POP", (param) => {
      this.$refs["tree"].setCurrentKey(param.data.caseId);
      //console.log(param.node.data)
      param.data.isEditing = true;
    });
    /***
     * 从table设置当前选中的节点node
     */
    this.$bus.on("CHANGE_CURRENT_TREENODE_FROM_TABLE", (data) => {
      console.log("CHANGE_CURRENT_TREENODE_FROM_TABLE==============================")
      this.$refs["tree"].setCurrentKey(data.caseId);
      //输入跳转节点名，跳转到对应节点
      var index = this.FindNodeIndexByCaseId(data.caseId, data.caseName);
      console.log("index--------------------------------");
      console.log(index);
      if (index != -1) {
        this.scrollTreeTo(index);
      } else {
        /**
         * 如果没有这个数据，则等待树节点加载这个数据，再进行跳转
         */
        this.waitForTreeNodeData(
          () => {
            //函数触发回调，表明table的数据已经更新且载入，可以被读取到
            console.log("action___result");
            index = this.FindNodeIndexByCaseId(data.caseId, data.caseName);
            this.$refs["tree"].setCurrentKey(data.caseId);
            this.scrollTreeTo( index); //设置滑动的滚轮，滚动到对应的treeNode 位置
          },
          500, //设置等待时间间隔为0.5秒
          data.caseId,
          data.caseName
        );
      }
    });
    /***
     * 获取父节点下的测试用例列表
     */
    this.$bus.on("UPDATE_FATHER_TABLE_DATAS", (data) => {
      this.getFolderNodeDatas(data.fatherId, data.caseId);
    });
    /**
     * 当从table发起了修改caseName时
     * treeNode节点的值和 caseName的一起进行变化
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
      if (node.isEditing == true) {
        node.isEditing = false;
        this.saveNodePathData(param.caseId);
      }
    });
    /**
     * 创建新用例
     * 1.如果是文件夹类型，创建子用例，
     * 2.如果是文件类型，创建兄弟用例
     */
    this.$bus.on("CREATE_NEW_TESTCASE_FILE_POP", (node) => {
      console.log("CREATE_NEW_TESTCASE_FILE_POP  发生了");
      if (node.type == "file") {
        this.CreateNewTestCase(node);
      } else if (node.type == "folder") {
        this.CreateNewTestCase(node);
      }
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
    /***
     * 通过popOver通知testCaseNode删除对应节点
     * 1.删除服务器节点
     * 2.删除客户端数据中的节点
     * 3.刷新当前选中为被删除节点曾经的父亲节点，并且通知table更新选中数据
     */
    this.$bus.on("DELETE_TESTCASE_NODE_BYPOP", (param) => {
      console.log("————删除————  DELETE_TESTCASE_NODE_BYPOP 发生了");
      this.updateNodePathCaseNum(param.data, param.node, -1);
      if (param.data.type == "file") {
        this.deleteTestCaseNode(param.data, param.node);
      } else if (param.data.type == "folder") {
        this.deleteTestCaseFolder(param.data, param.node);
      } else {
        alert("出现了不能存在的类型");
      }
    });
    /***
     * 通过Table通知testCaseNode删除对应节点
     * 1.删除服务器节点
     * 2.删除客户端数据中的节点
     * 3.刷新当前选中为被删除节点曾经的父亲节点，并且通知table更新选中数据
     */
    this.$bus.on("DELETE_TESTCASE_NODE_BYTABLE", (param) => {
      console.log("————删除————  DELETE_TESTCASE_NODE_BYTABLE 发生了");
      this.deleteTestCaseNodeByTable(param.data.caseId);
    });
  },
  methods: {
    /**
     * 等待树的数据
     */
    waitForTreeNodeData(callback, interval, caseId, caseName) {
      let handle = setInterval(() => {
        var index = this.FindNodeIndexByCaseId(caseId, caseName);
        if (index >= 0) {
          // index>0 说明对应的文件已经在文件集合里面了，表明已经载入了需要的数据
          clearInterval(handle);
          // 此时可以清除间隔且返回到调用函数（俗称回调函数）
          callback();
        } else {
          console.log("waiting!!!!!!!!!!!!!");
          //否则，一直处于等待数据状态
        }
      }, interval);
    },
    /**
     * 激活popover
     */
    OnActivatePopOver(event, data, node, node_obj) {
      this.OnTreeClickChooseNode(data, node);
      //console.log("OnActivatePopOver=====================");
      //console.log(event);
      //console.log(data);
      //console.log(node);
      //console.log(node_obj);
      this.$bus.emit("SHOW_POPOVER_MENU", {
        node: node,
        data: data,
        event: event,
      });
    },
    /***
     * 获取当前选中节点的index
     */
    FindNodeIndexByCaseId(caseId, caseName) {
      var navContents = document.querySelectorAll(".node_row_label_css");
      // 所有锚点元素的 offsetTop
      var index = 0;
      var save = 0;
      for (var i = 0; i < navContents.length; i++) {
        if (
          caseName.trim() !=
          navContents[i].textContent
            .trim()
            .split(" ")[0]
            .trim()
        ) {
          index += 1;
          console.log("不相等");
        } else {
          return index;
        }
      }
      return -1;
    },
    /***
     * 跳转到指定索引的元素
     */
    scrollTreeTo(index) {
      // 获取目标的 offsetTop
      // css选择器是从 1 开始计数，我们是从 0 开始，所以要 +1
      const targetOffsetTop = document.querySelectorAll(`.node_row_label_css`)[
        index
      ].offsetTop;
      // 获取当前 offsetTop
      console.log(targetOffsetTop);
      let scrollTop = document.querySelector(".navbar").scrollTop;
      // 定义一次跳 50 个像素，数字越大跳得越快，但是会有掉帧得感觉，步子迈大了会扯到蛋
      const STEP = 150;
      // 判断是往下滑还是往上滑
      if (scrollTop > targetOffsetTop) {
        // 往上滑
        smoothUp();
      } else {
        // 往下滑
        smoothDown();
      }
      // 定义往下滑函数
      function smoothDown() {
        console.log("smoothDown");
        // 如果当前 scrollTop 小于 targetOffsetTop 说明视口还没滑到指定位置
        if (scrollTop < targetOffsetTop) {
          // 如果和目标相差距离大于等于 STEP 就跳 STEP
          // 否则直接跳到目标点，目标是为了防止跳过了。
          if (targetOffsetTop - scrollTop >= STEP) {
            scrollTop += STEP;
          } else {
            scrollTop = targetOffsetTop;
          }
          document.querySelector(".navbar").scrollTop = scrollTop;
          // 关于 requestAnimationFrame 可以自己查一下，在这种场景下，相比 setInterval 性价比更高
          requestAnimationFrame(smoothDown);
        }
      }
      // 定义往上滑函数
      function smoothUp() {
        if (scrollTop > targetOffsetTop) {
          if (scrollTop - targetOffsetTop >= STEP) {
            scrollTop -= STEP;
          } else {
            scrollTop = targetOffsetTop;
          }
          document.querySelector(".navbar").scrollTop = scrollTop;
          requestAnimationFrame(smoothUp);
        }
      }
    },
    /**
     * 实时根据选中的修改人Id输出过滤结果
     *
     */
    getNodeDataByUser(val) {
      console.log(val);
      let obj = {};
      obj = this.parentObj.options.QAs.find((item) => {
        //model就是上面的数据源
        return item.value === val; //筛选出匹配数据
      });
      console.log(obj);
      var userId = obj.key;
      axios
        .get("getUserTestCaseNodesArray", {
          params: { userId: userId },
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
     * 利用关键字过滤节点的过滤函数
     */
    filterNode(value, data) {
      //显示过滤节点
      console.log(data.label + "  " + data.label.indexOf(value));
      if (!value) return true;
      return data.label.indexOf(value) !== -1;
    },
    /***
     * 删除测试用例节点
     * 1.删除服务器节点
     * 2.删除客户端数据中的节点
     * 3.刷新当前选中为被删除节点曾经的父亲节点，并且通知table更新选中数据
     */ deleteTestCaseNodeByTable(caseId) {
      axios
        .post("deleteTestCase", {
          caseId: caseId,
        })
        .then((res) => {
          console.log(caseId);
          console.log(res.data);
          var node = this.$refs["tree"].getNode(caseId);
          var parentNode = node.parent;
          this.$refs["tree"].setCurrentNode(parentNode.data);
          this.$refs["tree"].remove(node);
          this.getFolderNodeDatas(parentNode.data.caseId, null);
        });
    },
    /***
     * 删除测试用例节点
     */
    deleteTestCaseNode(data, node) {
      axios
        .post("deleteTestCase", {
          caseId: data.caseId,
        })
        .then((res) => {
          console.log(res);
          var parentNode = node.parent;
          console.log(parentNode.data);
          this.$refs["tree"].setCurrentNode(parentNode.data);
          this.$refs["tree"].remove(node);
          this.getFolderNodeDatas(parentNode.data.caseId, null);
        });
    },
    /**
     * 删除测试用例文件夹
     * 1.包括其子文件夹,子用例里面的全部内容
     * 2.删除当前显示的节点
     */
    deleteTestCaseFolder(data, node) {
      axios
        .post("deleteTestCaseFolder", {
          caseId: data.caseId,
        })
        .then((res) => {
          console.log(res.data);
          var parentNode = node.parent;
          if (parentNode.parent) {
            console.log(parentNode);
            this.$refs["tree"].setCurrentNode(parentNode.data);
          }
          console.log(node);
          this.$refs["tree"].remove(node);
        });
    },
    /***
     * 保存节点的路径关系到服务器
     */
    saveNodePathData(caseId) {
      var path_node = this.$refs["tree"].store.currentNode;
      console.log("———————————————————savePath————————————————");
      var level = 0;
      while (path_node.parent) {
        /*console.log(
          "savePathInside:level: " +
            level +
            " path_node: " +
            path_node.data.caseId
        );*/
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
        //console.log(path_node);
      }
    },
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
          console.log(
            "________________________Create_New_Root________________________________"
          );
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
      if (data.type == "file") {
        this.changeTreeNodeData(data, node); //保存树数据
        //保存table数据CREATE_NEW_TESTCASE_NOTIFY_TABLE
        this.$bus.emit("SAVE_TESTCASE_TABLE_DATA", {
          data: data,
          fatherId: node.parent.data.caseId,
        }); //告诉table，发生了保存事件*/
      } else if (data.type == "folder") {
        this.changeTreeNodeData(data, node);
      }
      this.saveNodePathData(data.caseId);
    },
    /**
     * 修改文件夹类型的测试用例节点数据
     * 保存到服务器
     */
    changeTreeNodeData(data, node) {
      var fatherId;
      console.log("changeTreeNodeData");
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
        .post("changeTreeNodeData", {
          caseId: data.caseId,
          caseName: data.label,
          fileType: data.type,
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
      var node = {};
      if (type == "file") {
        node = {
          caseId: newCaseId,
          label: "",
          type: type,
          children: [],
          isEditing: true,
        };
      } else if (type == "folder") {
        node = {
          caseId: newCaseId,
          label: "",
          type: type,
          children: [],
          isEditing: true,
          testCase_num: 0,
        };
      }
      return node;
    },
    /***
     * 创造兄弟新节点类型
     * 在节点的后面增加一个新节点
     * fileType：需要创建的节点类型
     */
    createBrotherNewNode(node, fileType, newCaseId) {
      var newChild = this.CreateNodeData(newCaseId, fileType);
      this.$refs["tree"].insertAfter(newChild, node); //为节点的后面增加一个节点
      this.$refs["tree"].setCurrentNode(newChild); //设置当前节点为新增节点
      return newChild;
    },
    /***
     * 创建子文件新节点类型，
     * 节点增加一个新子节点
     * fileType：需要创建的节点类型
     */
    createChildNewNode(node, fileType, newCaseId) {
      var newChild = this.CreateNodeData(newCaseId, fileType);
      this.$refs["tree"].append(newChild, node); //新增node
      this.$refs["tree"].setCurrentNode(newChild); //设置当前节点为新增节点
      return newChild;
    },
    /**
     * 新建树节点
     * data：当前节点
     * node：当前节点data
     * fileType：需要创建的文件夹类型
     * creatorType：发起创造的文件类型
     * aimFileType：需要创造的文件类型
     * 文件夹创造文件或者文件夹，只能创造子节点
     * 文件创建文件，只能创造兄弟节点
     */
    CreateNewTreeNode(data, node, aimFileType) {
      //从服务器获取新caseId
      axios
        .get("getNewCaseId")
        .then((res) => {
          var newCaseId = res.data.msg;
          //console.log(node.childNodes);
          let creatorFileType = data.type;
          //console.log(data.type);
          //console.log(aimFileType);
          var newChild;
          if (aimFileType == "file" && creatorFileType == "file") {
            //文件创建文件，只能创造兄弟节点
            newChild = this.createBrotherNewNode(node, aimFileType, newCaseId);
          } else if (aimFileType == "folder" && creatorFileType == "folder") {
            // 文件夹创造文件夹,只能创造子节点
            newChild = this.createChildNewNode(node, aimFileType, newCaseId);
          } else if (aimFileType == "file" && creatorFileType == "folder") {
            // 文件夹创造文件,只能创造子节点
            newChild = this.createChildNewNode(node, aimFileType, newCaseId);
          } else {
            alert("出现了异常创造情况！！！");
          }
          //console.log(node.childNodes);
          if (aimFileType == "file" && creatorFileType == "file") {
            this.$bus.emit("CREATE_NEW_TESTCASE_NOTIFY_TABLE", {
              data: newChild,
              fatherId: data.caseId,
              broId: data.caseId,
            }); //告诉table，发生了创造事件*/
          } else if (aimFileType == "file" && creatorFileType == "folder") {
            this.$bus.emit("CREATE_NEW_TESTCASE_NOTIFY_TABLE", {
              data: newChild,
              fatherId: data.caseId,
              broId: null,
            }); //告诉table，发生了创造事件*/
          }
          //给路径上的所有节点的用例数目+1
          this.updateNodePathCaseNum(data, node, 1);
        })
        .catch(function(error) {
          alert(error);
        });
    },
    /**
     * 给路径上的所有节点的用例数目进行修改
     * @param data,node
     * @param num 需要修改的数目，-1或1用于增加或者删除
     */
    updateNodePathCaseNum(data, node, num) {
      console.log("updateNodePathCaseNum==========================");
      var parent = node;
      console.log(parent);
      var folder_children = 0;
      if (parent && node.data.type == "folder" && num == -1) {
        folder_children = parent.data.testCase_num;
      }
      while (parent != null) {
        if (parent.data.type == "folder" && num == -1) {
          parent.data.testCase_num += num * folder_children;
          parent.data.testCase_num += num;
        } else {
          parent.data.testCase_num += num;
        }
        parent = parent.parent;
      }
    },
    /**
     * 初始化数据，获取测试用例目录数组
     * 传入用户名和用户Id进行校验
     */
    initTreeNodeData(userName, userId) {
      axios
        .get("getUserTestCaseNodesArray", {
          params: { userId: userId, userName: userName },
        })
        .then((res) => {
          var NodeRoots = res.data.msg;
          if (res.data.msg) {
            this.node_data = JSON.parse(JSON.stringify(NodeRoots));
            console.log(this.node_data);
          } else {
            alert("用户信息错误！");
            //用户信息有问题，跳转到重新登录界面
            this.$router.replace({
              name: "HomeMain",
              params: {},
            });
          }
        })
        .catch(function(error) {
          alert(error);
        });
    },
    /***
     * 初始化文件节点的孩子数量
     */
    initFolderChildrenNum(node_datas) {
      console.log(node_datas);
      for (var t = 0; t < node_datas.length; t++) {
        if (node_datas[t].type == "folder") {
          node_datas[t].testCase_num = node_datas[t].children.length - 1;
        }
      }
      console.log(node_datas);
    },
    /**
     * 1.对于文件夹，点击节点，选中该节点,自动展开该节点下面的子节点；
     *   右侧显示子一级的全部用例
     * 2.对于不可展开的用例，自动选中table中对应的caseId的行
     * 3.右侧筛选框自动变为空
     */
    OnTreeClickChooseNode(data, node) {
      if(node && !node.expanded){
        node.expanded=true
      }
      this.$refs["tree"].setCurrentNode(data); //设置当前节点为选中节点

      //this.currentNodeKey = node.data.caseId;
      //console.log(node);
      if (data.type == "folder") {
        this.getFolderNodeDatas(data.caseId, null);
      } else if (data.type === "file") {
        var fatherId = node.parent.data.caseId;
        //console.log(data)
        this.getFileNodeDataChoosed(data.caseId, fatherId, data.label);
      } else {
        alert("节点只能是文件或者文件夹类型！！！");
      }
      this.$bus.emit("RESET_SELECT_CONDITIONS", {});
    },
    /***
     * 获取文件夹类型节点下的直接子用例节点
     */
    getFolderNodeDatas(fatherId, caseId) {
      axios
        .get("getFolderTableTestCases", {
          params: {
            caseId: fatherId,
          },
        })
        .then((res) => {
          console.log(res.data.msg);
          this.$bus.emit("UPDATE_CURRENT_FOLDER_TABLEDATAS", {
            data: res.data.msg,
            caseId: caseId,
            fatherId: fatherId,
          });
        })
        .catch(function(error) {
          alert("Error " + error);
        });
    },
    /***
     * 获取文件类型节点下的直接子用例节点
     * 自动选中table中，对应的caseId
     */
    getFileNodeDataChoosed(caseId, fatherId, caseName) {
      this.$bus.emit("UPDATE_CURRENT_NODE_DATA_CHOOSE", {
        caseId: caseId,
        fatherId: fatherId,
        caseName: caseName,
      });
    },

    /**
     * 通过popover
     * 设置当前选中的node的值,并展开子node
     */
    updateCurrentNode(data, node, caseId) {
      console.log("---------updateCurrrentNode------------");
      //this.currentNodeKey = currentNodeKey;
      this.$refs["tree"].setCurrentNode(data); //设置当前节点为选中节点
      //console.log("===========");
    },

    /***
     * 触发了输入聚焦函数
     *
     */
    InputVFocus(node) {
      this.treeNodeInput = node.label;
      console.log("FOCUS FOCUS");
      console.log(this.$refs["caseNodeNameInput"]);
      //this.$refs.caseNodeNameInput.$refs.input.focus()
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
  },
  data() {
    this.scrollTreeDom = null;
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
      userId: 1,
      filterText: "",
      node_data: JSON.parse(JSON.stringify(node_data)),
      testif: false,
    };
  },
};
</script>

 <style scoped>
.node_editing > .el-input > .el-input__inner {
  height: 20px;
  width: 120px;
}
.node_editing {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  padding-right: 8px;
}
/* 
.node_label {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  font-size: 10px;
  padding-right: 2px;
}

.custom-tree-node {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  padding-right: 8px;
}*/
.tree-condition-suffix {
  flex: 1;
  display: flex;
  justify-content: space-between;
}
.el-tree-node > .el-tree-node__content {
  /*设置树节点的样式 */
  height: 22px;
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
  color: white;
  font-weight: bold;
  background-color: rgb(3, 155, 191) !important;
}

/*
* 行样式
*/
.node_row_css {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  justify-content: flex-start;
  align-items: center;
  font-size: 14px;
  flex-grow: 1;
  background: #007bff;
}
/*
 * 编辑中样式
 */
.node_row_editing_css {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  justify-content: flex-start;
  align-items: center;
  font-size: 14px;
  flex-grow: 1;
}

/*
 * not编辑中样式
 */
.node_row_no_editing_css {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  justify-content: flex-start;
  align-items: center;
  font-size: 14px;
  flex-grow: 1;
}

/*
 * 行内元素样式
 */
.node_row_label_css {
  /* 设置node节点的label */
  display: flex;
  margin-left: 2px;
  margin-right: 2px;
  justify-content: flex-start;
  width: 180px;
  white-space: nowrap;
  text-overflow: ellipsis;
  flex-grow: 1;
  font-size: 15px;
}
</style>
