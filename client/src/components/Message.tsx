import { motion } from 'framer-motion';
import { ChatMessage } from '../lib/types';
import { User, Bot } from 'lucide-react';

interface MessageProps {
  message: ChatMessage;
  isStreaming?: boolean;
}

export default function Message({ message, isStreaming = false }: MessageProps) {
  const isUser = message.role === 'user';
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`flex gap-3 mb-4 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}
    >
      {/* Avatar */}
      <div
        className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
          isUser
            ? 'bg-gradient-to-br from-neon-pink to-neon-blue'
            : 'bg-gradient-to-br from-neon-blue to-neon-green'
        }`}
      >
        {isUser ? (
          <User className="w-4 h-4 text-white" />
        ) : (
          <Bot className="w-4 h-4 text-white" />
        )}
      </div>

      {/* Message bubble */}
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-3 shadow-lg ${
          isUser
            ? 'bg-gradient-to-br from-neon-pink/80 to-neon-blue/80 text-white'
            : 'bg-light-card dark:bg-dark-card text-light-text dark:text-gray-100 border border-light-border/50 dark:border-dark-border/50'
        } backdrop-blur-sm`}
      >
        <div className="text-sm leading-relaxed whitespace-pre-wrap">
          {message.content}
          {isStreaming && (
            <motion.span
              className="inline-block w-2 h-4 bg-current ml-1"
              animate={{ opacity: [0, 1, 0] }}
              transition={{ duration: 0.8, repeat: Infinity }}
            />
          )}
        </div>
        
        {/* Timestamp */}
        <div
          className={`text-xs mt-2 opacity-70 ${
            isUser ? 'text-white/80' : 'text-light-text-muted dark:text-gray-400'
          }`}
        >
          {new Date(message.timestamp).toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit',
          })}
        </div>
      </div>
    </motion.div>
  );
}
