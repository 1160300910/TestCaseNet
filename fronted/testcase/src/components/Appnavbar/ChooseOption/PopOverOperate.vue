<template>
  <div>
    <el-popover
      placement="right-end"
      :width="50"
      trigger="click"
      v-model:visible="visible"
      @show="UpdateFatherChooseNode(data.caseId,node)"
    >
      <el-form ref="form" label-width="2px" size="mini">
        <el-form-item>
          <el-button type="text" icon="el-icon-folder-add"
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
            @click="CreateTestCase"
            type="text"
            >新建用例</el-button
          >
        </el-form-item>
        <el-form-item>
          <el-button icon="el-icon-document-copy" type="text" @click="DeleteTestcase"
            >复制用例</el-button
          >
        </el-form-item>
        <el-form-item>
          <el-button icon="el-icon-document-delete" type="danger"
            >删除该用例</el-button
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
     * 删除测试用例
     */
    DeleteTestcase(){

    },
    UpdateFatherChooseNode(currentNodeKey, node) {
      this.$emit("updateNode", currentNodeKey, node);
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
    CreateTestCase() {},
    /***
     * 修改当前用例
     * 输入：
     * data : 当前节点的数据
     * nowChildren：当前节点的孩子
     */
    ChangeTestCase(data, nowChildren, nowParent) {
      //console.log(data);
      //alert(data.label);
      this.visible = false;
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
    },
  },
};
</script>
