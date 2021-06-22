<template>
  <el-select v-model="value" filterable placeholder="请选择" size="small">
    <el-option
      v-for="item in data"
      :key="item.value"
      :label="item.label"
      :value="item.value"
    >
    </el-option>
  </el-select>
</template>

<script>
export default {
  props: ["data"],
  created() {},
  mounted() {},
  data() {
    return {
      value: "",
    };
  },
};
</script>
