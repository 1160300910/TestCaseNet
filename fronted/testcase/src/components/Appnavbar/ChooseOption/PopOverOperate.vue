<template>
  <div>
    <el-popover
      placement="right-end"
      :width="100"
      trigger="click" v-model:visible="visible"
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
            @click="ChangeTestCase"
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
        <i class="el-icon-circle-plus-outline"></i>
      </template>
    </el-popover>
  </div>
</template>
<script>
export default {
  props: {
    nowId: { type: String, requires: true },
    nowLable: { type: String, requires: true },
  },
  data() {
    return {
      visible: false,
    };
  },
  methods: {
    CreateTestCase() {},
    ChangeTestCase() {
      alert(this.nowLable);
      this.visible = false
      console.log(this.nowId, this.nowLable);
    },
  },
};
</script>
