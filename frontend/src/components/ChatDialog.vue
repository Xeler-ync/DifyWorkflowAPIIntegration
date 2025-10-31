<template>
  <div class="chat-dialog">
    <div class="chat-container" ref="chatContainer">
      <chat-item v-for="(message, index) in messages" :key="index" :message="message" />
    </div>
    <div class="input-area">
      <input v-model="inputMessage" @keyup.enter="sendMessage" placeholder="输入消息..." class="message-input" />
      <button @click="sendMessage" class="send-button">发送</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'
import { chatService } from '../api/chat'
import ChatItem from './ChatItem.vue'
import type { Message } from '../api/types'

const props = defineProps<{
  sessionId?: string
}>()

const emit = defineEmits<{
  (e: 'session-created', sessionId: string): void
}>()

const messages = ref<Message[]>([])
const chatContainer = ref<HTMLElement | null>(null)
const inputMessage = ref('')
const isTemporarySession = ref(false) // 标记是否为临时会话

// 创建新会话
const createNewSession = async () => {
  try {
    const response = await chatService.createChat()
    messages.value = [response.message]
    emit('session-created', response.sessionId)
  } catch (error) {
    console.error('创建会话失败:', error)
  }
}

// 初始化会话
const initSession = async () => {
  if (props.sessionId) {
    // 加载历史会话
    messages.value = await chatService.getChatMessages(props.sessionId)
  } else {
    // 创建临时会话，不立即创建服务器会话
    isTemporarySession.value = true
    messages.value = [{
      id: window.crypto.randomUUID(),  // 添加唯一ID
      username: "AI助手",
      content: "你好！我是AI助手，有什么可以帮助你的吗？",
      position: "left",
      avatar: "/nwlt.jpg",
      timestamp: Date.now(),  // 添加时间戳
    }]
  }
}

// 发送消息
const sendMessage = async () => {
  if (!inputMessage.value.trim()) return

  let currentSessionId = props.sessionId

  // 如果没有会话ID，创建新会话
  if (!currentSessionId && isTemporarySession.value) {
    const response = await chatService.createChat()
    currentSessionId = response.sessionId
    emit('session-created', currentSessionId)
    isTemporarySession.value = false
  }

  if (!currentSessionId) return

  try {
    messages.value.push({
      username: "用户",
      content: inputMessage.value,
      position: "right",
      avatar: "https://avatars.githubusercontent.com/u/2?v=4",
      timestamp: Date.now(),  // 添加时间戳
    } as Message);

    const response = await chatService.sendMessage({
      sessionId: currentSessionId,
      content: inputMessage.value,
    })
    messages.value.push({
      ...response.message,
      timestamp: Date.now(), // 确保添加时间戳
    });
    inputMessage.value = ''
    scrollToBottom()
  } catch (error) {
    console.error('发送消息失败:', error)
  }
}

// 滚动到底部
const scrollToBottom = () => {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight
    }
  })
}

// 暴露方法给父组件
defineExpose({
  createNewSession
})

// 监听 sessionId 变化
watch(() => props.sessionId, initSession, { immediate: true })

// 监听消息变化
watch(messages, scrollToBottom, { deep: true })
</script>

<style scoped>
.chat-dialog {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: #1a1a1a;
}

.chat-container {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  background: #1a1a1a;
}

.input-area {
  padding: 16px;
  display: flex;
  gap: 12px;
  background: #2a2a2a;
  border-top: 1px solid #333;
}

.message-input {
  flex: 1;
  padding: 8px 12px;
  background: #333;
  border: 1px solid #444;
  border-radius: 4px;
  color: #fff;
  font-size: 14px;
}

.message-input:focus {
  outline: none;
  border-color: #666;
}

.send-button {
  padding: 8px 16px;
  background: #4a4a4a;
  border: none;
  border-radius: 4px;
  color: #fff;
  cursor: pointer;
  transition: background 0.2s;
}

.send-button:hover {
  background: #5a5a5a;
}

.chat-container::-webkit-scrollbar {
  width: 6px;
}

.chat-container::-webkit-scrollbar-thumb {
  background: #333;
  border-radius: 3px;
}

.chat-container::-webkit-scrollbar-track {
  background: transparent;
}

.chat-container {
  scroll-behavior: smooth;
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
