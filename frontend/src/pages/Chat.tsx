import React, { useState, useRef, useEffect } from 'react';
import { useWebSocket } from '../contexts/WebSocketContext';
import MessageList from '../components/chat/MessageList';
import ChatInput from '../components/chat/ChatInput';

const Chat: React.FC = () => {
  const { sendMessage, messages, isConnected, addMessage } = useWebSocket();
  const [input, setInput] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || !isConnected || isStreaming) return;
    const userMessage = {
      id: crypto.randomUUID(),
      role: 'user',
      content: input,
      timestamp: new Date().toISOString()
    };
    addMessage(userMessage);
    setInput('');
    setIsStreaming(true);
    try {
      await sendMessage({
        conversation_id: 'default',
        message: input,
        model: 'llama3.2',
        use_rag: true,
        use_memory: true
      });
    } catch (error) {
      console.error('Send error:', error);
    } finally {
      setIsStreaming(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-twilight-bg text-twilight-text">
      <div className="flex items-center justify-between px-6 py-3 border-b border-twilight-border">
        <span className="text-sm font-medium">Twilight AI Chat</span>
        <span className={`text-xs px-2 py-0.5 rounded-full ${isConnected ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'}`}>
          {isConnected ? '● Live' : '● Getrennt'}
        </span>
      </div>
      <div className="flex-1 overflow-y-auto px-4 py-4">
        <MessageList messages={messages} isStreaming={isStreaming} />
        <div ref={messagesEndRef} />
      </div>
      <div className="border-t border-twilight-border px-4 py-3">
        <ChatInput
          value={input}
          onChange={setInput}
          onSend={handleSend}
          disabled={!isConnected || isStreaming}
          placeholder="Nachricht an Twilight AI …"
        />
      </div>
    </div>
  );
};

export default Chat;
