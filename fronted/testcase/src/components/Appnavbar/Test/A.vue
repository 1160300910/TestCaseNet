<template id="a">
  <div>
    <h3>A组件：{{ name }}</h3>
    <button @click="sendToFather">将数据发送给父组件</button>
    <button @click="callback('name')">2.将数据发送给父组件</button>
  </div>
</template>
<script>
export default {
  props: {
    callback: Function,
    myName: { type: String, requires: true }, //是必填的参数
  },
  setup() {},
  data() {
    return {
      name: this.myName, // 把传过来的值赋值给新的变量
    };
  },
  watch: {
    myName(newVal) {
      this.name = newVal; //对父组件传过来的值进行监听，如果改变也对子组件内部的值进行改变
    },
  },
  methods: {
    sendToFather: function() {
      this.$emit("handleChange", "Jack"); // 触发父组件中handleChange事件并传参Jack
      // 注：此处事件名称与父组件中绑定的事件名称要一致
    },
    changeName() {
      this.name = "Lily"; // 这里修改的只是自己内部的值，就不会报错了
    },
  },
};
</script>
