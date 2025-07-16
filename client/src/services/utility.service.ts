/**
 * Utility Service
 * Contains common utility functions used across the app
 */
export class UtilityService {
  /**
   * Generates a unique ID for chat messages
   */
  static generateMessageId(): string {
    return `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}
