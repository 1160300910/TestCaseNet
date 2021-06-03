<template>
  <div>
    <router-view></router-view>
  </div>
</template>

<script>
//import HomeMain from "./components/HomeMain";
//<HomeMain id="app" msg="XX系统测试用例" />
export default {
  name: "App",
  components: {
    // /HomeMain,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
