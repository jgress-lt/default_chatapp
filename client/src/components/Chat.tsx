import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Loader2, Trash2 } from 'lucide-react';
import Message from './Message';
import Spinner from './Spinner';
import { ChatMessage } from '../lib/types';
import {
  AzureOpenAIService,
  ChatStorageService,
  UtilityService,
} from '../services';

export default function Chat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [streamingMessage, setStreamingMessage] = useState<ChatMessage | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [lastFunctionCalls, setLastFunctionCalls] = useState<any>(null);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Load chat history on mount
  useEffect(() => {
    const history = ChatStorageService.loadChatHistory();
    setMessages(history);
  }, []);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, streamingMessage]);

  // Save messages to localStorage whenever they change
  useEffect(() => {
    if (messages.length > 0) {
      ChatStorageService.saveChatHistory(messages);
    }
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    const trimmedInput = input.trim();
    if (!trimmedInput || isLoading) return;

    const userMessage: ChatMessage = {
      id: UtilityService.generateMessageId(),
      role: 'user',
      content: trimmedInput,
      timestamp: Date.now(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    setError(null);
    setLastFunctionCalls(null);

    try {
      // Start streaming response
      const stream = await AzureOpenAIService.streamChatCompletion([...messages, userMessage]);
      
      // Create assistant message that will be updated during streaming
      const assistantMessage: ChatMessage = {
        id: UtilityService.generateMessageId(),
        role: 'assistant',
        content: '',
        timestamp: Date.now(),
      };
      
      setStreamingMessage(assistantMessage);
      
      let fullContent = '';
      let functionCallData = null;
      
      // Process the stream
      for await (const chunk of AzureOpenAIService.parseSSEStream(stream)) {
        if (chunk.content) {
          fullContent += chunk.content;
          setStreamingMessage(prev => 
            prev ? { ...prev, content: fullContent } : null
          );
        }
        
        if (chunk.functionCalls) {
          functionCallData = chunk.functionCalls;
          setLastFunctionCalls(functionCallData);
        }
      }
      
      // Finalize the message
      const finalMessage = { 
        ...assistantMessage, 
        content: fullContent,
        // Add function calls as metadata if needed
        metadata: functionCallData ? { functionCalls: functionCallData } : undefined
      };
      setMessages(prev => [...prev, finalMessage]);
      setStreamingMessage(null);
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An unexpected error occurred';
      setError(errorMessage);
      console.error('Chat error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      if (e.shiftKey) {
        // Shift+Enter: Allow default behavior (new line)
        return;
      } else {
        // Enter: Send message
        e.preventDefault();
        handleSubmit(e);
      }
    }
  };

  const clearChatHistory = () => {
    setMessages([]);
    setStreamingMessage(null);
    setLastFunctionCalls(null);
    ChatStorageService.clearChatHistory();
  };

  return (
    <div className="flex flex-col h-full max-w-4xl mx-auto">
      {/* Messages area */}
      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-4">
        <AnimatePresence>
          {messages.map((message) => (
            <Message key={message.id} message={message} />
          ))}
          
          {streamingMessage && (
            <Message 
              key={streamingMessage.id} 
              message={streamingMessage} 
              isStreaming={true}
            />
          )}
        </AnimatePresence>
        
        {/* Function calls display */}
        {lastFunctionCalls && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-700 rounded-lg p-3 text-sm"
          >
            <div className="font-medium text-blue-800 dark:text-blue-200 mb-2">
              🔧 Functions Called ({lastFunctionCalls.total_function_calls})
            </div>
            <div className="space-y-1">
              {lastFunctionCalls.function_calls?.map((call: any, index: number) => (
                <div key={index} className="text-blue-700 dark:text-blue-300">
                  <span className="font-mono">
                    {call.plugin_name}.{call.function_name}()
                  </span>
                  {call.execution_time && (
                    <span className="text-xs text-blue-500 ml-2">
                      ({(call.execution_time * 1000).toFixed(1)}ms)
                    </span>
                  )}
                </div>
              ))}
            </div>
          </motion.div>
        )}
        
        {/* Typing indicator */}
        {isLoading && !streamingMessage && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex items-center gap-3 mb-4"
          >
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-neon-blue to-neon-green flex items-center justify-center">
              <Spinner size="sm" color="text-white" />
            </div>
            <div className="bg-light-card dark:bg-dark-card backdrop-blur-sm rounded-2xl px-4 py-3">
              <div className="flex items-center gap-1">
                <span className="text-sm text-light-text-muted dark:text-gray-400">Assistant is thinking</span>
                <Spinner size="sm" />
              </div>
            </div>
          </motion.div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Error display */}
      <AnimatePresence>
        {error && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="mx-4 mb-4 p-3 bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-700 rounded-lg"
          >
            <div className="flex justify-between items-start">
              <p className="text-red-600 dark:text-red-300 text-sm">{error}</p>
              <button
                onClick={() => setError(null)}
                className="text-red-400 hover:text-red-600 dark:text-red-400 dark:hover:text-red-300"
              >
                ×
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Input area */}
      <div className="border-t border-light-border dark:border-dark-border bg-light-card/50 dark:bg-dark-card/50 backdrop-blur-sm p-4">
        <form onSubmit={handleSubmit} className="flex gap-3">
          <div className="flex-1 relative">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Type your message... (Enter to send, Shift+Enter for new line)"
              className="w-full px-4 py-3 pr-12 bg-light-card dark:bg-dark-card backdrop-blur-sm border border-light-border dark:border-dark-border rounded-2xl resize-none focus:outline-none focus:ring-2 focus:ring-neon-blue/30 text-light-text dark:text-gray-100"
              rows={1}
              style={{ minHeight: '48px', maxHeight: '120px' }}
              disabled={isLoading}
            />
          </div>
          
          {/* Clear chat button */}
          {messages.length > 0 && (
            <motion.button
              type="button"
              onClick={clearChatHistory}
              className="px-3 py-3 bg-red-500/10 hover:bg-red-500/20 text-red-600 dark:text-red-400 rounded-2xl transition-all duration-200 flex items-center justify-center"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              title="Clear chat history"
            >
              <Trash2 className="w-5 h-5" />
            </motion.button>
          )}
          
          <motion.button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="px-6 py-3 bg-gradient-to-r from-neon-blue to-neon-green text-white rounded-2xl font-medium disabled:opacity-50 disabled:cursor-not-allowed hover:from-neon-blue/90 hover:to-neon-green/90 transition-all duration-200 flex items-center gap-2"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            {isLoading ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <Send className="w-5 h-5" />
            )}
            <span className="hidden sm:inline">Send</span>
          </motion.button>
        </form>
        
        <p className="text-xs text-light-text-muted dark:text-gray-400 mt-2 text-center">
          Press Enter to send • Shift+Enter for new line • Messages are saved locally
        </p>
      </div>
    </div>
  );
}
