<template>
  <div class="main">
    <div class="selector_css3">
      <test-case-table></test-case-table>
    </div>
    <!--div class="table_head_floating">
      <table ref="middle-table">
        <thead class="thead-middle" :style="theadStyle">
          <tr>
            <th
              v-for="colConfig in colConfigs"
              :key="colConfig.prop"
              :property="colConfig.prop"
              :label="colConfig.label"
              :width="colConfig.width"
            >
              {{ colConfig.label }}
            </th>
          </tr>
        </thead>
      </table>
    </div-->
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
.selector_css3 {
  flex-grow: 20;
  color: aliceblue;
}
</style>
