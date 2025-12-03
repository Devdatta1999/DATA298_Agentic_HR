import { create } from 'zustand';

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  metadata?: {
    sql_query?: string;
    tables?: string[];
    columns?: Record<string, string[]>;
    visualization?: any;
    results?: any[];
    insights?: string[];
    explanation?: string;
    error?: boolean;
  };
}

interface QueryHistory {
  question: string;
  sql_query?: string;
  tables?: string[];
  columns?: Record<string, string[]>;
  token_count?: number;
  response_time?: number;
}

interface ChatState {
  sessionId: string | null;
  messages: Message[];
  isLoading: boolean;
  tokenCount: number;
  queryHistory: QueryHistory[];
  lastQueryTokens: number;
  lastResponseTime: number;
  setSessionId: (id: string) => void;
  addMessage: (message: Omit<Message, 'id' | 'timestamp'>) => void;
  setLoading: (loading: boolean) => void;
  setTokenCount: (count: number) => void;
  addQueryHistory: (query: QueryHistory) => void;
  setLastQueryTokens: (tokens: number) => void;
  setLastResponseTime: (time: number) => void;
  clearMessages: () => void;
}

export const useChatStore = create<ChatState>((set) => ({
  sessionId: null,
  messages: [],
  isLoading: false,
  tokenCount: 0,
  queryHistory: [],
  lastQueryTokens: 0,
  lastResponseTime: 0,
  setSessionId: (id) => set({ sessionId: id }),
  addMessage: (message) =>
    set((state) => ({
      messages: [
        ...state.messages,
        {
          ...message,
          id: Date.now().toString(),
          timestamp: new Date(),
        },
      ],
    })),
  setLoading: (loading) => set({ isLoading: loading }),
  setTokenCount: (count) => set({ tokenCount: count }),
  addQueryHistory: (query) =>
    set((state) => ({
      queryHistory: [...state.queryHistory, query],
    })),
  setLastQueryTokens: (tokens) => set({ lastQueryTokens: tokens }),
  setLastResponseTime: (time) => set({ lastResponseTime: time }),
  clearMessages: () => set({ messages: [], queryHistory: [] }),
}));


