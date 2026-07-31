import React, { KeyboardEvent } from 'react';

interface ChatInputProps {
  value: string;
  onChange: (v: string) => void;
  onSend: () => void;
  disabled: boolean;
  placeholder: string;
}

const ChatInput: React.FC<ChatInputProps> = ({ value, onChange, onSend, disabled, placeholder }) => {
  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      onSend();
    }
  };

  return (
    <div className="flex gap-2">
      <textarea
        className="flex-1 bg-twilight-surface border border-twilight-border rounded-lg p-2 resize-none text-twilight-text focus:outline-none focus:ring-1 focus:ring-twilight-accent"
        rows={2}
        value={value}
        onChange={e => onChange(e.target.value)}
        onKeyDown={handleKeyDown}
        disabled={disabled}
        placeholder={placeholder}
      />
      <button
        className="px-4 py-2 bg-twilight-accent text-white rounded-lg hover:bg-purple-600 transition disabled:opacity-50 disabled:cursor-not-allowed"
        onClick={onSend}
        disabled={disabled || !value.trim()}
      >
        Senden
      </button>
    </div>
  );
};

export default ChatInput;
