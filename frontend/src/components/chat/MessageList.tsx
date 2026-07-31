import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { materialDark } from 'react-syntax-highlighter/dist/esm/styles/prism';

interface Message {
  id?: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
}

const MessageList: React.FC<{ messages: Message[]; isStreaming: boolean }> = ({ messages, isStreaming }) => {
  return (
    <div className="space-y-4">
      {messages.map((msg, idx) => (
        <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
          <div className={`max-w-3/4 p-3 rounded-lg ${msg.role === 'user' ? 'bg-twilight-accent text-white' : 'bg-twilight-surface border border-twilight-border'}`}>
            <ReactMarkdown
              components={{
                code({ node, inline, className, children, ...props }) {
                  const match = /language-(\w+)/.exec(className || '');
                  return !inline && match ? (
                    <SyntaxHighlighter style={materialDark} language={match[1]} PreTag="div" {...props}>
                      {String(children).replace(/\n$/, '')}
                    </SyntaxHighlighter>
                  ) : (
                    <code className={className} {...props}>{children}</code>
                  );
                }
              }}
            >
              {msg.content}
            </ReactMarkdown>
            {msg.timestamp && <div className="text-xs text-twilight-muted mt-1">{new Date(msg.timestamp).toLocaleTimeString()}</div>}
          </div>
        </div>
      ))}
      {isStreaming && <div className="text-twilight-muted text-sm">Twilight AI schreibt …</div>}
    </div>
  );
};

export default MessageList;
