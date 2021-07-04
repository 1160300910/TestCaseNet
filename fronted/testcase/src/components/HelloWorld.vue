<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <div id="counter">Counter: {{ counter }}</div>
    <div id="bind-attribute">
      <span v-bind:title="message">
        鼠标悬停几秒钟查看此处动态绑定的提示信息！
      </span>
    </div>
    
    <div id="event-handling">
      <p>{{ hello }}</p>
      <button v-on:click="StopCounting">停止计数</button>
    </div>
    <div id="two-way-binding">
      <p>{{ hello }}</p>
      <input v-model="helloInput" />
    </div>
    <div id="conditional-rendering">
      <span v-if="seen">现在你看到我了</span>
    </div>
    <h3>Installed CLI Plugins</h3>
    <ul></ul>
    <h3>Essential Links</h3>
    <ul></ul>
    <h3>Ecosystem</h3>
    <ul></ul>
  </div>
</template>

<script>
var timer;
export default {
  name: "HelloWorld",
  props: {
    msg: String,
  },
  data() {
    return {
      seen:false,
      helloInput: "helloInput",
      hello: "hello",
      counter: 0,
      message: "You loaded this page on " + new Date().toLocaleString(),
    };
  },
  mounted() {
    timer = setInterval(() => {
      this.counter++;
    }, 1000);
  },
  methods: {
    StopCounting() {
      clearInterval(timer);
      this.seen = true;
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
