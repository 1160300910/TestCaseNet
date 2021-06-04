<template>
  <el-input v-model="testrt" type="textarea"> </el-input>
  <button @click="$emit('enlargeText')">
    Enlarge text
  </button>
</template>
