<template>
  <div class="main">
    <div class="selector_css">
      <div>类型:</div>
      <selector></selector>
      <div>修改人:</div>
      <selector></selector>
      <div>用例等级:</div>
      <selector></selector>
      <div>执行人:</div>
      <selector></selector>
      <div>tag:</div>
      <selector></selector>
    </div>
    <div class="selector_css3">
      <test-case-table ></test-case-table>
    </div>
  </div>
</template>
<script>
import TestCaseTable from "./TestCaseTable";
import Selector from "./Selector";
export default {
  components: { TestCaseTable, Selector },

  methods: {},
};
</script>
<style scoped>
.selector_css {
  display: flex;
  flex-grow: 1;
  justify-content: space-around;
  flex-direction: row;
  color: rgb(2, 24, 44);
  line-height: 20px;
  top: 0px;
  left: 0px;
  right: 0px;
  font-size: 10px;
  align-items: center;
}
.selector_css3 {
  flex-grow: 20;
  color: aliceblue;
}
</style>
