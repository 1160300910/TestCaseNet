<template>
  <div class="table_head_floating" v-pin="200">
    <table ref="middle-table">
      <thead class="thead-middle">
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
  </div>
</template>
<script>
export default {
  directives: {
    //注册一个局部的自定义指令 v-pin
    pin: {
      bind(el, binding, vnode) {
        el.style.position = "fixed";
        el.style.top = binding.value + "px";
      },
    },
  },
  setup() {},
};
</script>
