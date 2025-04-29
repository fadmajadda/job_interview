<template>
  <div class="a">
    <QuizzView/>
  </div>
</template>
<script setup lang="ts">
import QuizzView from "@/views/QuizzView.vue";
</script>


<style scoped>

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  line-height: 1.6;
  color: var(--text-color);
  background-color: #f5f5f5;
}
</style>