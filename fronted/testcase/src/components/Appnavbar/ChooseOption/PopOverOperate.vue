<template>
  <div>
    <el-popover
      placement="right-end"
      :width="50"
      trigger="click"
      v-model:visible="visible"
      @hide="UpdateFatherChooseNode(data, node, data.caseId)"
    >
      <el-form ref="form" label-width="2px" size="mini">
        <el-form-item v-if="data.type == 'folder'">
          <el-button
            type="text"
            icon="el-icon-folder-add"
            @click="CreateNewTestCaseFolder(data, node)"
            >新建子文件夹</el-button
          >
        </el-form-item>
        <el-form-item>
          <el-button
            icon="el-icon-edit-outline"
            type="text"
            @click="ChangeTestCase(data, nowChildren, nowParent)"
            >更改用例</el-button
          >
        </el-form-item>
        <el-form-item>
          <el-button
            icon="el-icon-magic-stick"
            @click="CreateNewTestCaseFile(data, node)"
            type="text"
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
          <el-button
            icon="el-icon-document-delete"
            type="danger"
            @click="DeleteTestCase(node, data)"
            >删除用例</el-button
          >
        </el-form-item>
        <el-form-item v-if="data.type == 'folder'">
          <el-button
            icon="el-icon-document-delete"
            type="danger"
            @click="DeleteTestCase(node, data)"
            >删除文件夹</el-button
          >
        </el-form-item>
      </el-form>

      <template #reference>
        <i class="el-icon-circle-plus-outline"></i>
      </template>
    </el-popover>
  </div>
</template>
<script>
import { getCurrentInstance } from "vue";
export default {
  props: {
    //nowId: { type: Number, requires: true },
    //nowLable: { type: String, requires: true },
    node: { requirs: true },
    nowChildren: {},
    nowParent: {},
    data: { requires: true },
    OnAdditionChoice: {
      type: Function,
      required: false,
    },
  },
  data() {
    return {
      visible: false,
    };
  },
  inject: ["parentObj"],
  //向layout里修改当前选中行的信息

  methods: {
    /***
     * 通知TreeNode创建新的子用例
     * 输入：
     * data : 当前节点的数据
     */
    CreateNewTestCaseFile(data, node) {
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
     * 删除测试用例
     * 1.node节点中需要删除这个用例
     * 2.table里需要删除
     */
    DeleteTestCase(node, data) {
      this.visible = false;
      this.$bus.emit("DELETE_TESTCASE_NODE_BYPOP", { data: data, node: node });
      //this.$bus.emit("DELETE_TESTCASE_TABLE_BYPOP", { node: node, data: data });
    },
    UpdateFatherChooseNode(data, node, currentNodeKey) {
      this.$emit("updateNode", data, node, currentNodeKey);
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
    ChangeTestCase(data, nowChildren, nowParent) {
      //console.log(data);
      //alert(data.label);
      /*console.log(
        this.parentObj.nowId,
        this.parentObj.nowLabel,
        this.parentObj.choice,
        this.parentObj.nowChildren,
        this.parentObj.nowParent
      );*/
      //console.log(nowId, nowLabel);
      this.parentObj.node_data = data;
      this.parentObj.choice = "change";
      this.parentObj.nowChildren = nowChildren;
      this.parentObj.nowParent = nowParent;
      /*
      console.log(
        this.parentObj.nowId,
        this.parentObj.nowLabel,
        this.parentObj.choice
      );*/

      this.$bus.emit("CHANGE_CHOOSE_TEST");
      this.visible = false;
    },
  },
};
</script>
