import { ChatMessage } from '../lib/types';

/**
 * Azure OpenAI Service
 * Handles all communication with Azure OpenAI API
 */
export class AzureOpenAIService {
  /**
   * Sends a chat completion request to Azure OpenAI via our API server
   * and returns a ReadableStream for real-time streaming
   */
  static async streamChatCompletion(
    messages: ChatMessage[]
  ): Promise<ReadableStream<Uint8Array>> {
    const response = await fetch('http://localhost:3001/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        messages: messages.map(msg => ({
          role: msg.role,
          content: msg.content,
        })),
        stream: true,
        max_tokens: 1000,
        temperature: 0.7,
      }),
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`API request failed: ${response.status} ${error}`);
    }

    return response.body!;
  }

  /**
   * Parses Server-Sent Events (SSE) stream from Azure OpenAI
   * and yields content deltas for real-time display
   */
  static async* parseSSEStream(
    stream: ReadableStream<Uint8Array>
  ): AsyncGenerator<string, void, unknown> {
    const reader = stream.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    try {
      while (true) {
        const { done, value } = await reader.read();
        
        if (done) break;
        
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        
        // Keep the last incomplete line in buffer
        buffer = lines.pop() || '';
        
        for (const line of lines) {
          const trimmed = line.trim();
          
          if (trimmed === 'data: [DONE]') {
            return; // Stream complete
          }
          
          if (trimmed.startsWith('data: ')) {
            try {
              const jsonStr = trimmed.slice(6); // Remove "data: " prefix
              const parsed = JSON.parse(jsonStr);
              
              const content = parsed.choices?.[0]?.delta?.content;
              if (content) {
                yield content;
              }
              
              const finishReason = parsed.choices?.[0]?.finish_reason;
              if (finishReason) {
                return; // Stream complete
              }
            } catch (parseError) {
              // Skip malformed JSON chunks
              console.warn('Failed to parse SSE chunk:', trimmed);
            }
          }
        }
      }
    } finally {
      reader.releaseLock();
    }
  }
}
