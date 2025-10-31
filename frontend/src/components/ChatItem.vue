<template>
  <div class="message-item" :class="message.position">
    <div class="message-content">
      <div class="avatar">
        <img :src="message.avatar" :alt="message.username">
      </div>
      <div class="message-bubble">
        <div class="username">{{ message.username }}</div>
        <div class="text">{{ message.content }}</div>
        <div class="timestamp" :class="message.position">
          {{ formatTime(message.timestamp) }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Message } from '../api/types'

defineProps<{
  message: Message
}>()

const formatTime = (timestamp: number) => {
  const date = new Date(timestamp)
  return date.toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<style scoped>
.message-item {
  display: flex;
  margin-bottom: 16px;
}

.message-item.left {
  justify-content: flex-start;
}

.message-item.right {
  justify-content: flex-end;
}

.message-content {
  display: flex;
  gap: 8px;
  max-width: 70%;
}

.message-item.right .message-content {
  flex-direction: row-reverse;
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  overflow: hidden;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.message-bubble {
  background: #2a2a2a;
  padding: 12px;
  border-radius: 12px;
  position: relative;
}

.message-item.right .message-bubble {
  background: #3a3a3a;
}

.username {
  font-size: 12px;
  color: #666;
  margin-bottom: 4px;
}

.text {
  color: #fff;
  word-wrap: break-word;
}

.timestamp {
  font-size: 11px;
  color: #666;
  margin-top: 4px;
}

.timestamp.left {
  text-align: left;
}

.timestamp.right {
  text-align: right;
}
</style>
