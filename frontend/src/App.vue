<template>
  <div class="app">
    <main-layout />
  </div>
</template>

<script setup lang="ts">
import MainLayout from './components/MainLayout.vue'
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
  background: #1a1a1a;
}

.app {
  width: 100vw;
  height: 100vh;
  background: #1a1a1a;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
    Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  overflow: hidden;
}
</style>
