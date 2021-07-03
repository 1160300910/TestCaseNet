<template>
  <div>
    <img src="/background/DesignGraph.png" class="div_back" alt="" />
    <login></login>
  </div>
</template>
<script>
import Login from "@/components/Login/Login";
export default {
  components: { Login },
  data(){
      return{
        
      }
  },
};
</script>

<style >
.div_back {
  position: absolute;
  top: 0px;
  left: 0px;
  width: 100%;
  height: 100%;
}
</style>
