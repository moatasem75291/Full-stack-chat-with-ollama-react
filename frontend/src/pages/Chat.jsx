import { useState, useEffect, useRef } from 'preact/hooks';
import ChatMessage from '../components/ChatMessage.jsx';
import ChatInput from '../components/ChatInput.jsx';
import '../style/Chat.css';

function StatusPopup({ message, isVisible, onClose }) {
  if (!isVisible) return null;
  return (
    <div className="status-popup">
      <div className="popup-content">
        <p>{message}</p>
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  );
}

export default function Chat() {
  const baseUrl = import.meta.env.VITE_API_BASE_URL;
  const healthEndpoint = import.meta.env.VITE_HEALTH_ENDPOINT;
  const historyEndpoint = import.meta.env.VITE_HISTORY_ENDPOINT;
  const chatEndpoint = import.meta.env.VITE_CHAT_ENDPOINT;
  const deleteHistoryEndpoint = import.meta.env.VITE_DELETE_HISTORY_ENDPOINT;

  const [statusMessage, setStatusMessage] = useState('');
  const [showPopup, setShowPopup] = useState(false);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [currentStreamingMessage, setCurrentStreamingMessage] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const response = await fetch("http://localhost:8000/");
        console.log(response);
        const data = await response.json();
        setStatusMessage(data.message);
        setShowPopup(true);
      } catch (error) {
        setStatusMessage('Error: Could not connect to service');
        setShowPopup(true);
      }
    };
    checkHealth();
  }, []);

  useEffect(() => {
    fetchChatHistory();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, currentStreamingMessage]);

  const fetchChatHistory = async () => {
    try {
      const response = await fetch("http://localhost:8000/get_history");
      const data = await response.json();
      if (data.history) {
        setMessages(data.history);
      }
    } catch (error) {
      console.error('Error fetching chat history:', error);
    }
  };

  const sendMessage = async (message) => {
    if (!message.trim()) return;

    setLoading(true);
    setIsStreaming(true);
    const newMessage = { role: 'user', content: message };
    setMessages((prev) => [...prev, newMessage]);
    setCurrentStreamingMessage('');

    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message }),
      });

      if (!response.ok) throw new Error('Network response was not ok');

      const reader = response.body.getReader();
      let streamedText = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) {
          setMessages((prev) => [
            ...prev,
            { role: 'assistant', content: streamedText },
          ]);
          break;
        }

        const chunk = new TextDecoder().decode(value);
        streamedText += chunk;

        setCurrentStreamingMessage(streamedText);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: 'Sorry, an error occurred. Please try again.' },
      ]);
    } finally {
      setLoading(false);
      setIsStreaming(false);
      setCurrentStreamingMessage('');
    }
  };

  const clearHistory = async () => {
    try {
      await fetch("http://localhost:8000/delete_history", { method: 'DELETE' });
      setMessages([]);
    } catch (error) {
      console.error('Error clearing history:', error);
    }
  };

  return (
    <>
      <StatusPopup
        message={statusMessage}
        isVisible={showPopup}
        onClose={() => setShowPopup(false)}
      />
      <div className="chat-container">
        <div className="chat-header">
          <h1>Ollama Chat</h1>
          <button onClick={clearHistory} className="clear-button">
            Clear History
          </button>
        </div>
        <div className="messages-container">
          {messages.map((message, index) => (
            <ChatMessage key={index} message={message} />
          ))}
          {isStreaming && currentStreamingMessage && (
            <ChatMessage
              message={{ role: 'assistant', content: currentStreamingMessage }}
              isStreaming={true}
            />
          )}
          {loading && !currentStreamingMessage && (
            <div className="loading">AI is thinking...</div>
          )}
          <div ref={chatEndRef} />
        </div>
        <ChatInput onSend={sendMessage} disabled={loading} />
      </div>
    </>
  );
}
