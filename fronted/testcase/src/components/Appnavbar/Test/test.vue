<template>
  <div id="itany">
    <my-a @handleChange="changeName" :callback="callback" :myName="name"></my-a>
    <my-b :myName="name" @changeName="editName"></my-b>
    <my-c></my-c>
    {{ name }}
    <button @click="sendToChild">父组件改变name值</button>
  </div>
</template>
<script>
import A from "./A";
import B from "./B";
import C from "./C";
export default {
  provide() {
    return {
      parentObj: this,
    };
  },
  data() {
    return {
      name: "12314",
      test: "change",
    };
  },
  components: { "my-a": A, "my-b": B, "my-c": C },
  methods: {
    sendToChild() {
      this.name = "sendsendToChild";
    },
    changeName(name) {
      // name形参是子组件中传入的值Jack
      this.name = name;
    },
    callback(name) {
      this.name = name; //2.先在父组件中定义一个callback函数，并把 callback 函数传过去
    },
    editName(name) {
      //在父组件中给要传值的两个兄弟组件都绑定要传的变量，并定义事件
      this.name = name;
    },
  },
};
</script>
