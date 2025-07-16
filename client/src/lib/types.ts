export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
  id: string;
  timestamp: number;
}
