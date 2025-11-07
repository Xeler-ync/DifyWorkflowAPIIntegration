<template>
  <div class="main-layout">
    <aside class="sidebar">
      <div class="sidebar-header">
        <button class="new-chat-btn" @click="handleCreateChat" :disabled="loading">
          <i class="icon">➕</i>
          新建对话
        </button>
      </div>

      <div class="chat-history">
        <div class="history-section">
          <h3>历史会话</h3>
          <div v-for="chat in chatHistory.slice().reverse()" :key="chat.id" class="chat-item"
            :class="{ active: currentChatId === chat.id }" @click="switchChat(chat.id)">
            <div class="chat-title">{{ chat.title }}</div>
            <div class="chat-time">{{ formatTime(chat.updated_at) }}</div>
            <button class="delete-btn" @click.stop="handleDeleteChat(chat.id)">
              🗑️
            </button>
          </div>
        </div>
      </div>
    </aside>

    <main class="main-content">
      <chat-dialog ref="chatRef" :session-id="currentChatId" @session-created="handleSessionCreated" />
    </main>
  </div>
</template>


<script setup lang="ts">
import { ref, onMounted } from 'vue'
import ChatDialog from './ChatDialog.vue'
import { chatService } from '../api/chat'
import type { ChatSession } from '../api/types'

const chatRef = ref<InstanceType<typeof ChatDialog> | null>(null)
const currentChatId = ref<string>('')
const chatHistory = ref<ChatSession[]>([])
const loading = ref(false)

// 处理新会话创建
const handleSessionCreated = (sessionId: string) => {
  currentChatId.value = sessionId
  loadChatList() // 重新加载会话列表
}

// 创建新会话
const handleCreateChat = () => {
  if (loading.value) return
  // 不再立即创建会话，只是清空当前会话ID
  currentChatId.value = ''
}

// 加载会话列表
const loadChatList = async () => {
  try {
    const sessions = await chatService.getChatList()
    chatHistory.value = sessions
  } catch (error) {
    console.error('加载会话列表失败:', error)
  }
}

// 切换会话
const switchChat = (chatId: string) => {
  if (currentChatId.value === chatId) return
  currentChatId.value = chatId
}

// 删除会话
const handleDeleteChat = async (sessionId: string) => {
  if (loading.value) return

  try {
    loading.value = true
    await chatService.deleteChat(sessionId)

    // 如果删除的是当前会话，清空当前会话ID
    if (currentChatId.value === sessionId) {
      currentChatId.value = ''
    }

    // 重新加载会话列表
    await loadChatList()
  } catch (error) {
    console.error('删除会话失败:', error)
  } finally {
    loading.value = false
  }
}

// 格式化时间
const formatTime = (timestamp: number) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))

  if (days === 0) {
    return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  } else if (days === 1) {
    return '昨天'
  } else if (days < 7) {
    return `${days}天前`
  } else {
    return date.toLocaleDateString('zh-CN', { month: 'numeric', day: 'numeric' })
  }
}

// 初始化
onMounted(async () => {
  await loadChatList()
})
</script>

<style scoped>
.main-layout {
  display: flex;
  height: 100vh;
  background: #1a1a1a;
}

.sidebar {
  width: 260px;
  background: #242424;
  border-right: 1px solid #333;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  flex-shrink: 0;
  /* 防止侧边栏被压缩 */
}

.sidebar-header {
  padding: 16px;
  border-bottom: 1px solid #333;
}

.new-chat-btn {
  width: 100%;
  padding: 12px;
  background: #2d2d2d;
  border: 1px solid #333;
  border-radius: 8px;
  color: #e0e0e0;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s ease;
}

.new-chat-btn:hover {
  background: #333;
  border-color: #444;
}

.new-chat-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.icon {
  font-size: 16px;
}

.chat-history {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.history-section h3 {
  color: #999;
  font-size: 12px;
  text-transform: uppercase;
  margin-bottom: 12px;
  letter-spacing: 0.5px;
}

.chat-item {
  padding: 12px;
  margin-bottom: 8px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.chat-item:hover {
  background: #2d2d2d;
}

.chat-item.active {
  background: #333;
}

.chat-title {
  color: #e0e0e0;
  font-size: 14px;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.chat-time {
  color: #666;
  font-size: 12px;
}

.main-content {
  flex: 1;
  overflow: hidden;
  position: relative;
  min-width: 0;
  /* 防止flex子项溢出 */
}

.chat-history::-webkit-scrollbar {
  width: 6px;
}

.chat-history::-webkit-scrollbar-thumb {
  background: #333;
  border-radius: 3px;
}

.chat-history::-webkit-scrollbar-track {
  background: transparent;
}

.delete-btn {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #666;
  cursor: pointer;
  padding: 4px;
  opacity: 0;
  transition: opacity 0.2s;
}

.chat-item:hover .delete-btn {
  opacity: 1;
}

.delete-btn:hover {
  color: #ff4444;
}

.chat-item {
  position: relative;
  padding: 12px;
  margin-bottom: 8px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}
</style>
