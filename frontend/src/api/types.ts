// api/types.ts
export interface Message {
  id: string
  username: string
  content: string
  position: 'left' | 'right'
  timestamp: number
  avatar?: string
}

export interface ChatSession {
  id: string
  title: string
  messages: Message[]
  createdAt: number
  updatedAt: number
}

export interface CreateChatResponse {
  sessionId: string
  message: Message
}

export interface SendMessageRequest {
  sessionId: string
  content: string
}

export interface SendMessageResponse {
  message: Message
}
