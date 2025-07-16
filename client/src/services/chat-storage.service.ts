import { ChatMessage } from '../lib/types';

/**
 * Chat Storage Service
 * Handles saving and loading chat history from localStorage
 */
export class ChatStorageService {
  private static readonly STORAGE_KEY = 'azure-chat-history';

  /**
   * Saves chat history to localStorage
   */
  static saveChatHistory(messages: ChatMessage[]): void {
    try {
      localStorage.setItem(this.STORAGE_KEY, JSON.stringify(messages));
    } catch (error) {
      console.warn('Failed to save chat history:', error);
    }
  }

  /**
   * Loads chat history from localStorage
   */
  static loadChatHistory(): ChatMessage[] {
    try {
      const stored = localStorage.getItem(this.STORAGE_KEY);
      return stored ? JSON.parse(stored) : [];
    } catch (error) {
      console.warn('Failed to load chat history:', error);
      return [];
    }
  }

  /**
   * Clears chat history from localStorage
   */
  static clearChatHistory(): void {
    try {
      localStorage.removeItem(this.STORAGE_KEY);
    } catch (error) {
      console.warn('Failed to clear chat history:', error);
    }
  }
}
