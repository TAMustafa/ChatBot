import { useState } from 'react'

export default function InputBox({ onSend, disabled }: { onSend: (text: string) => Promise<void> | void; disabled?: boolean }) {
  const [text, setText] = useState('')

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    const t = text.trim()
    if (!t) return
    setText('')
    await onSend(t)
  }

  return (
    <form onSubmit={submit} className="flex gap-2">
      <input
        className="flex-1 border rounded px-3 py-2 text-sm"
        placeholder="Type your message…"
        value={text}
        onChange={(e) => setText(e.target.value)}
        disabled={disabled}
      />
      <button className="px-3 py-2 bg-blue-600 text-white rounded disabled:opacity-50" disabled={disabled || !text.trim()}>
        Send
      </button>
    </form>
  )
}
