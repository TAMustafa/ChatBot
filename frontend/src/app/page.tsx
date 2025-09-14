import ChatWindow from '@/components/ChatWindow/ChatWindow'

export default function Home() {
  return (
    <main className="container mx-auto p-4">
      <h1 className="text-2xl font-semibold mb-4">Tarek's Chatbot</h1>
      <ChatWindow />
    </main>
  )
}
