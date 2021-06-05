<template>
  <div>
    <el-popover
      placement="right-end"
      :width="50"
      trigger="click"
      v-model:visible="visible"
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
            @click="ChangeTestCase(data)"
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
          <el-button icon="el-icon-document-copy" type="text"
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
        <i
          class="el-icon-circle-plus-outline"
          @click="ParentOnAdditionChoice(data)"
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
    ParentOnAdditionChoice(data) {
      //console.log(data)
      //console.log( this.OnAdditionChoice)
      if (this.OnAdditionChoice && this.data) {
        this.OnAdditionChoice(data);
      }
      //this.$emit('OnAdditionChoice="OnChooseNode"', data);
    },
    CreateTestCase() {},
    ChangeTestCase(data) {
      //console.log(data);
      //alert(data.label);
      this.visible = false;
      console.log(
        this.parentObj.nowId,
        this.parentObj.nowLabel,
        this.parentObj.choice
      );
      //console.log(nowId, nowLabel);
      this.parentObj.nowId = data.id;
      this.parentObj.nowLabel = data.label;
      this.parentObj.choice = "change";
      console.log(
        this.parentObj.nowId,
        this.parentObj.nowLabel,
        this.parentObj.choice
      );
      
      this.$bus.emit("CHANGE_CHOOSE_TEST");
    },
  },
};
</script>
