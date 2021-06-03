<template>
  <el-table :data="rightsDate" border stripe height="713">
    <el-table-column
      v-for="info in rightHeader"
      :key="info.key"
      :property="info.key"
      :label="info.label"
    >
      <template #default="scope">
        {{ scope.row[scope.column.property] }}
        <!-- 渲染对应表格里面的内容 -->
      </template>
    </el-table-column>
    <!-- 自定义列的遍历-->
    <el-table-column label="启用状态">
      <!-- 数据的遍历  scope.row就代表数据的每一个对象-->
      <template #default="scope">
        <el-switch v-model="scope.row.ifUse"> </el-switch>
      </template>
    </el-table-column>
  </el-table>
</template>
<script>
export default {
  setup() {},
  data() {
    this.rightHeader = [
      {
        label: "编码",
        key: "code",
      },
      {
        label: "姓名",
        key: "name",
      },
      {
        label: "权限描述",
        key: "description",
      },
    ];
    this.rightsDate = [
      {
        id: 221,
        code: "01",
        name: "西药开立权限",
        description: "医生对西药处方权限",
        ifUse: "0",
      },
      {
        id: 222,
        code: "02",
        name: "草药开立权限",
        description: "医生对草药处方权限",
        ifUse: "0",
      },
      {
        id: 223,
        code: "03",
        name: "成药开立权限",
        description: "医生对成药处方权限",
        ifUse: "0",
      },
      {
        id: 224,
        code: "04",
        name: "麻醉开立权限",
        description: "医生对麻醉处方权限",
        ifUse: "0",
      },
      {
        id: 225,
        code: "05",
        name: "精一开立权限",
        description: "医生对精一处方权限",
        ifUse: "0",
      },
    ];
    return {};
  },
};
</script>
