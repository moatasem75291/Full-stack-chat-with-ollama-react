import ReactMarkdown from 'react-markdown'
import { useEffect, useState } from 'preact/hooks'

export default function ChatMessage({ message, isStreaming = false }) {
  const [displayContent, setDisplayContent] = useState('')

  useEffect(() => {
    if (isStreaming) {
      setDisplayContent(message.content)
    } else {
      
      let currentIndex = 0
      const text = message.content

      const typeWriter = () => {
        if (currentIndex < text.length) {
          setDisplayContent(text.substring(0, currentIndex + 1))
          currentIndex++
          setTimeout(typeWriter, 15)
        }
      }

      typeWriter()
    }
  }, [message.content, isStreaming])

  return (
    <div className={`message ${message.role} ${isStreaming ? 'streaming' : ''}`}>
      <div className="message-content">
        <span className="role">
          {message.role === 'user' ? 'You' : 'AI' }
        </span>
        <div className={`markdown-content ${isStreaming ? 'streaming-content' : ''}`}>
          <ReactMarkdown>{displayContent}</ReactMarkdown>
        </div>
      </div>
    </div>
  )
}
