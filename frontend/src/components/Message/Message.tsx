import clsx from 'clsx'

type Props = {
  role: 'user' | 'assistant'
  content: string
  structured?: { summary: string; bullets: string[] } | null
  sources?: string[]
  confidence?: number
}

export default function Message({ role, content, structured, sources, confidence }: Props) {
  const isUser = role === 'user'
  const bullets = !isUser && structured?.bullets && structured.bullets.length > 0 ? structured.bullets : []

  return (
    <div className={clsx('flex', isUser ? 'justify-end' : 'justify-start')}>
      <div className={clsx('max-w-[80%] rounded px-3 py-2 text-sm space-y-2', isUser ? 'bg-blue-600 text-white' : 'bg-slate-100 text-slate-900')}>
        <div className="whitespace-pre-wrap">{content}</div>
        {bullets.length > 0 && (
          <ul className={clsx('list-disc pl-5', isUser ? 'marker:text-white' : 'marker:text-slate-600')}>
            {bullets.map((b, i) => (
              <li key={i} className="mb-1">{b}</li>
            ))}
          </ul>
        )}
        {!isUser && sources && sources.length > 0 && (
          <div className="text-xs text-slate-600">
            Sources: {sources.join(', ')} {typeof confidence === 'number' && (
              <span className="ml-2 inline-block rounded bg-slate-200 px-1 py-0.5">conf {Math.round(confidence * 100)}%</span>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
