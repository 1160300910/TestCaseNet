<template>
  <div
    id="rightMenu"
    v-if="visible"
    class="tree_menu"
    :style="rightMenuStyle"
    :key="(currentNode && currentNode.id) || '0'"
  >
    <div class="menu_main_css">
      <a
        class="menu_row_css"
        v-if="data.type == 'folder'"
        @click="CreateNewTestCaseFolder(data, node)"
      >
        <img src="/icons/icon-menu-folder.png" />
        <span class="menu_label_css">添加新子suit文件夹</span>
      </a>
      <div
        class="menu_row_css"
        v-if="data.type == 'folder'"
        @click="changeTestCaseFolder(data, node)"
      >
        <i class="el-icon-edit" style="color: rgb(6, 153, 202);"></i>
        <span class="menu_label_css">更改suit文件夹名</span>
      </div>
      <div
        class="menu_row_css"
        v-if="data.type == 'file'"
        @click="ChangeTestCase(data, node)"
      >
        <i class="el-icon-edit" style="color: rgb(6, 153, 202);"></i>
        <span class="menu_label_css">更改用例名</span>
      </div>
      <div class="menu_row_css" @click="CreateNewTestCaseFile(data, node)">
        <img src="/icons/icon-menu-file.png" />
        <span class="menu_label_css">添加新测试用例</span>
      </div>
      <div
        class="menu_row_css"
        v-if="data.type == 'file'"
        @click="DeleteTestCase(data, node)"
      >
        <img src="/icons/icon-menu-delete-file.png" />
        <span class="menu_label_css">删除用例</span>
      </div>
      <div
        class="menu_row_css"
        v-if="data.type == 'folder'"
        @click="DeleteTestCase(data, node)"
      >
        <img src="/icons/icon-menu-delet-folder.png" />
        <span class="menu_label_css">删除文件夹</span>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  mounted() {
    /**
     * 展示popover
     */
    this.$bus.on("SHOW_POPOVER_MENU", (param) => {
      //console.log("————展示————  SHOW_POPOVER_MENU 发生了");
      this.visible = true;
      this.node = param.node;
      this.data = param.data;
      this.event = param.event;
      this.getContextmenu(this.event, this.data);
    });
  },
  data() {
    return {
      visible: false,
      node: {},
      data: {},
      event: {},
    };
  },

  setup() {},

  methods: {
    getContextmenu(e, data) {
      this.rightMenuStyle = "top:" + e.pageY + "px; left:" + e.pageX + "px";
      this.visible = true;
      this.currentNode = data;
      if (data.children && data.children.length > 0) {
        this.addTypeLi = true;
      } else {
        this.addTypeLi = false;
      }
      const self = this;
      document.onclick = function(ev) {
        if (ev.target !== document.getElementById("rightMenu")) {
          self.visible = false;
        }
      };
    },
    // 解决单击隐藏右键菜单的问题
    handleNodeClick(data, node) {
      if (this.visible) {
        this.visible = false;
      }
    },

    /***
     * 通知TreeNode创建新的子用例
     * 输入：
     * data : 当前节点的数据
     */
    CreateNewTestCaseFile(data, node) {
      console.log(
        "——————————————————————————CreateNewTestCaseFile————————————————————————————"
      );

      this.visible = false;
      var fileType = "file";
      this.$bus.emit("CREATE_NEW_TESTCASE_NODE_POP", {
        data: data,
        node: node,
        fileType: fileType, //需要创造的文件类型
      });
    },
    /***
     * 通知TreeNode创建新的测试用例文件夹
     */
    CreateNewTestCaseFolder(data, node) {
      this.visible = false;
      var fileType = "folder";
      this.$bus.emit("CREATE_NEW_TESTCASE_NODE_POP", {
        data: data,
        node: node,
        fileType: fileType, //需要创造的文件类型
      });
    },
    /**
     * 复制测试用例
     */
    CopyTestcasePopOver(node, data) {
      this.visible = false;
    },
    /***
     * 删除测试用例节点
     * 1.node节点中需要删除这个用例
     * 2.table里需要删除
     */
    DeleteTestCase(data, node) {
      this.visible = false;
      this.$bus.emit("DELETE_TESTCASE_NODE_BYPOP", { data: data, node: node });
    },
    UpdateFatherChooseNode(data, node, currentNodeKey) {
      this.$emit("updateCurrentNode", data, node, currentNodeKey);
    },
    /**
     *  @click="ParentOnAdditionChoice(node)"
     */
    ParentOnAdditionChoice(node) {
      console.log("ParentOnAdditionChoice");
      console.log(node);
      //console.log( this.OnAdditionChoice)
      if (this.OnAdditionChoice && node) {
        console.log("ParentOnAdditionChoice2");
        this.OnAdditionChoice(node);
      }
      //this.$emit('OnAdditionChoice="OnChooseNode"', data);
    },

    /***
     * 修改当前用例
     * 输入：
     * data : 当前节点的数据
     * nowChildren：当前节点的孩子
     */
    ChangeTestCase(data, node) {
      this.visible = false;
      this.$bus.emit("CHANGE_TESTCASE_BY_POP", { data: data, node: node });
    },
    /**
     * 修改当前测试用例文件夹
     */
    changeTestCaseFolder(data, node) {
      this.visible = false;
      this.$bus.emit("CHANGE_TESTCASE_FOLDER_BY_POP", {
        data: data,
        node: node,
      });
    },
  },
};
</script>

<style>
.menu_row_css img {
  width: 15px;
  height: 15px;
}

.menu_row_css:hover img {
  filter: brightness(100);
}

.menu_row_css i {
  width: 15px;
  height: 15px;
}

.menu_row_css:hover i {
  color: rgb(6, 153, 202);
  filter: brightness(100);
}

.menu_row_css {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  margin-left: 4px;
  margin-right: 4px;
  margin-top: 2px;
  margin-bottom: 2px;
}
.menu_label_css {
  display: flex;
  justify-content: flex-start;
  width: 150px;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  flex-grow: 1;
  font-size: 15px;
  margin-left: 7px;
  color: rgb(6, 153, 202);
}

.menu_main_css {
  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;
  justify-content: flex-start;
  align-items: flex-start;
  margin: 0;
  padding: 0;
}
.tree_menu {
  position: absolute;
  background-color: #fff;
  padding: 5px 0;
  border: 1px solid rgb(153, 151, 151);
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
.menu_main_css > .menu_row_css:hover {
  background-color: rgb(52, 188, 155);
  color: white;
  align-items: center;
  border-radius: 7px;
}
.menu_main_css > .menu_row_css > .menu_label_css:hover {
  color: white;
}
</style>
