import { useState } from 'react'
import { chat, ChatResponse, StructuredAnswer } from '@/services/apiClient'

export type Message = {
  role: 'user' | 'assistant'
  content: string
  structured?: StructuredAnswer | null
  sources?: string[]
  confidence?: number
}

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const send = async (text: string) => {
    setError(null)
    setMessages((prev) => [...prev, { role: 'user', content: text }])
    setLoading(true)
    try {
      const res: ChatResponse = await chat(text)
      // Always keep the full answer as content so nothing is lost
      const content = res.answer
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content,
          // Attach structured if present for enhanced rendering
          structured: res.structured ?? undefined,
          sources: res.sources,
          confidence: res.confidence,
        },
      ])
    } catch (e: unknown) {
      if (e instanceof Error) {
        setError(e.message)
      } else if (typeof e === 'object' && e !== null && 'message' in e) {
        // handle Axios-like error shape
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        setError((e as any).message ?? 'Request failed')
      } else {
        setError('Request failed')
      }
    } finally {
      setLoading(false)
    }
  }

  return { messages, loading, error, send }
}
