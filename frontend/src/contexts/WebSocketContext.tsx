import React, { createContext, useContext, useState, useRef, useEffect } from 'react';
import { useAuth } from './AuthContext';

interface WebSocketContextType {
  isConnected: boolean;
  messages: any[];
  sendMessage: (data: any) => void;
  addMessage: (msg: any) => void;
}

const WebSocketContext = createContext<WebSocketContextType | undefined>(undefined);

export const WebSocketProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user } = useAuth();
  const [isConnected, setIsConnected] = useState(false);
  const [messages, setMessages] = useState<any[]>([]);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (!user) return;
    const token = localStorage.getItem('access_token');
    if (!token) return;
    const ws = new WebSocket(`${import.meta.env.VITE_WS_URL}/chat/default?token=${token}`);
    ws.onopen = () => setIsConnected(true);
    ws.onmessage = (ev) => {
      const text = ev.data;
      setMessages(prev => [...prev, { role: 'assistant', content: text, timestamp: new Date().toISOString() }]);
    };
    ws.onclose = () => setIsConnected(false);
    wsRef.current = ws;
    return () => ws.close();
  }, [user]);

  const sendMessage = (data: any) => {
    if (wsRef.current && isConnected) {
      wsRef.current.send(JSON.stringify(data));
    }
  };

  const addMessage = (msg: any) => {
    setMessages(prev => [...prev, msg]);
  };

  return (
    <WebSocketContext.Provider value={{ isConnected, messages, sendMessage, addMessage }}>
      {children}
    </WebSocketContext.Provider>
  );
};

export const useWebSocket = () => {
  const ctx = useContext(WebSocketContext);
  if (!ctx) throw new Error('useWebSocket must be used within WebSocketProvider');
  return ctx;
};
