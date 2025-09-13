"use client";
import { useChat } from '@/hooks/useChat';
import InputBox from '@/components/InputBox/InputBox';
import Message from '@/components/Message/Message';

export default function ChatWindow() {
  const { messages, loading, error, send } = useChat();

  return (
    <div className="flex flex-col h-[70vh] border rounded-lg bg-white shadow">
      <div className="flex-1 overflow-auto p-4 space-y-3">
        {messages.map((m, i) => (
          <Message key={i} role={m.role} content={m.content} />
        ))}
        {loading && <div className="text-sm text-slate-500">Thinking…</div>}
        {error && <div className="text-sm text-red-600">{error}</div>}
      </div>
      <div className="border-t p-3">
        <InputBox onSend={send} disabled={loading} />
      </div>
    </div>
  );
}
