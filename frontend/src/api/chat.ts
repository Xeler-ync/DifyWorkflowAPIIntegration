// api/chat.ts
import type { Message, ChatSession, CreateChatResponse, SendMessageRequest, SendMessageResponse } from './types'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

class ChatService {
  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    })

    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`)
    }

    // 对于 204 状态码，返回空对象
    if (response.status === 204) {
      return {} as T
    }

    return response.json()
  }

  // 创建新的聊天会话
  async createChat(): Promise<CreateChatResponse> {
    return this.request<CreateChatResponse>('/chats', {
      method: 'POST',
    })
  }

  // 获取所有聊天会话列表
  async getChatList(): Promise<ChatSession[]> {
    return this.request<ChatSession[]>('/chats')
  }

  // 获取特定会话的消息历史
  async getChatMessages(sessionId: string): Promise<Message[]> {
    return this.request<Message[]>(`/chats/${sessionId}/messages`)
  }

  // 发送消息
  async sendMessage(params: SendMessageRequest): Promise<SendMessageResponse> {
    return this.request<SendMessageResponse>('/messages', {
      method: 'POST',
      body: JSON.stringify(params),
    })
  }

  // 删除聊天会话
  async deleteChat(sessionId: string): Promise<{ success: boolean }> {
    return this.request<{ success: boolean }>(`/chats/${sessionId}`, {
      method: 'DELETE',
    })
  }
}

export const chatService = new ChatService()
