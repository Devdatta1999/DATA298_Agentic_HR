import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface QueryRequest {
  question: string;
  session_id?: string;
}

export interface QueryResponse {
  success: boolean;
  session_id: string;
  answer: string;
  sql_query?: string;
  results?: any[];
  tables?: string[];
  columns?: Record<string, string[]>;
  visualization?: {
    visualization_type: string;
    x_axis?: string;
    y_axis?: string;
    explanation?: string;
  };
  insights?: string[];
  explanation?: string;
  token_count?: number;
  error?: string;
}

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const queryHR = async (request: QueryRequest): Promise<QueryResponse> => {
  const response = await api.post<QueryResponse>('/api/query', request);
  return response.data;
};

export const getConversation = async (sessionId: string) => {
  const response = await api.get(`/api/conversation/${sessionId}`);
  return response.data;
};


