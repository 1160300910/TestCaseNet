<template>
  <div>
    <el-popover
      placement="right-end"
      trigger="manual"
      v-model:visible="visible"
      @hide="UpdateFatherChooseNode(data, node, data.caseId)"
    >
      <el-form ref="form" class="elform_popover">
        <el-form-item v-if="data.type == 'folder'"
          ><i class="el-icon-folder-add" style="font-size: 20px; "></i>
          <el-button
            type="text"
            style="font-size: 16px; "
            @click="CreateNewTestCaseFolder(data, node)"
            >新建子文件夹</el-button
          >
        </el-form-item>
        <el-form-item v-if="data.type == 'folder'"
          ><i class="el-icon-edit-outline" style="font-size: 20px; "></i>
          <el-button
            type="text"
            style="font-size: 16px; "
            @click="changeTestCaseFolder(data, node)"
            >更改文件夹名</el-button
          >
        </el-form-item>
        <el-form-item v-if="data.type == 'file'"
          ><i class="el-icon-edit-outline" style="font-size: 20px; "></i>
          <el-button
            type="text"
            style="font-size: 16px; "
            @click="ChangeTestCase(data, node)"
            >更改用例</el-button
          >
        </el-form-item>
        <el-form-item>
          <i class="el-icon-magic-stick" style="font-size: 20px; "></i>
          <el-button
            type="text"
            style="font-size: 16px; "
            @click="CreateNewTestCaseFile(data, node)"
            >新建用例</el-button
          >
        </el-form-item>
        <!--el-form-item>
          <el-button
            icon="el-icon-document-copy"
            type="text"
            @click="CopyTestcasePopOver(node, data)"
            >复制用例</el-button
          >
        </el-form-item-->
        <el-form-item v-if="data.type == 'file'">
          <i
            class="el-icon-document-delete"
            style="font-size: 20px; color: red;"
          ></i>
          <el-button
            type="text"
            style="font-size: 16px; color: red;"
            @click="DeleteTestCase(data, node)"
            >删除用例</el-button
          >
        </el-form-item>
        <el-form-item v-if="data.type == 'folder'">
          <i
            class="el-icon-folder-delete"
            style="font-size: 20px; color: red;"
          ></i>
          <el-button
            type="danger"
            style="font-size: 16px; color: white;"
            @click="DeleteTestCase(data, node)"
            >删除文件夹</el-button
          >
        </el-form-item>
      </el-form>
      <template #reference>
        <i
          class="el-icon-circle-plus-outline"
          style="font-size: 20px; color: grey"
          @click="Test"
        ></i>
      </template>
    </el-popover>
  </div>
</template>
<script>
export default {
  props: {
    //nowId: { type: Number, requires: true },
    //nowLable: { type: String, requires: true },
    node: { requirs: true },
    data: { requires: true },
    text: { requires: true },
    /*
    OnActivatePopOver: {
      type: Function,
      required: false,
    },*/
  },
  mounted() {},
  created() {
    console.log(
      "——————————————————————————PopoverOperator created————————————————————————————"
    );
  },
  data() {
    return {
      visible: false,
    };
  },
  //向layout里修改当前选中行的信息

  methods: {
    Test() {
      this.visible = true;
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

<style >
.elform_popover > .el-form-item {
  flex: 1;
  display: flex;
  flex-direction: row;
  justify-content: start;
  height: 10px;
}
.elform_popover {
  display: flex;
  flex-direction: column;
  justify-content: start;
  align-content: center;
  font-size: 14px;
}
</style>
