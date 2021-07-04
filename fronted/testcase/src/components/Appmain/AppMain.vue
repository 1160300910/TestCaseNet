<template>
  <div class="main">
    <div class="testcase_table_main_css">
      <test-case-table></test-case-table>
    </div>
  </div>
</template>
<script>
import TestCaseTable from "./TestCaseTable";
export default {
  data() {
    return {};
  },
  mounted() {},

  components: { TestCaseTable },

  methods: {},
};
</script>
<style  scoped>
.testcase_table_main_css {
  flex-grow: 20;
  color: aliceblue;
}
</style>
