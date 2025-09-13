import axios from 'axios'

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000',
  timeout: 20000,
})

export type StructuredAnswer = { summary: string; bullets: string[] }
export type ChatResponse = { answer: string; structured?: StructuredAnswer | null; sources: string[]; confidence: number }

export async function chat(query: string): Promise<ChatResponse> {
  const r = await api.post('/api/chat', { query })
  return r.data
}
