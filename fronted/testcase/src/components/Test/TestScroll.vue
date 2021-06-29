<template>
  <div>
    <!-- 内容区域 -->
    <div class="content">
      <div>
        content-0
      </div>
      <div>
        content-1
      </div>
      <div>
        content-2
      </div>
      <div>
        content-3
      </div>
      <div>
        content-4
      </div>
    </div>
  </div>
</template>
<script>
export default {
  props: {},
  data() {
    return {
      active: 0 // 当前激活的导航索引
    }
  },
  mounted() {
    // 监听滚动事件
  },
  destroy() {
  },
  methods: {
  
  }
}
</script>