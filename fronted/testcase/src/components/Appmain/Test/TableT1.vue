<template>
  <table-son :data="tableData" :col-configs="colConfigs"> </table-son>
</template>
<script>
import tableSon from "./tableSon.vue";
import SetInput from "./SetInput.vue";
const PrefixPlusText = {
  props: ["colConfig","data","label"],
  template: `
      <el-input v-model="data[label]" type="textarea">
      </el-input> 
    `,
};

export default {
  components: { tableSon },
  data() {
    this.colConfigs = [
      { prop: "change", label: "变化" ,
        component: PrefixPlusText,},
      {
        prop: "trend",
        label: "趋势",
        component: PrefixPlusText,
      },
    ];
    return {
      tableData: [
        {
          change: "59%",
          trend: "34%",
        },
        {
          change: "-25%",
          trend: "-10%",
        },
      ],
    };
  },
};
</script>
