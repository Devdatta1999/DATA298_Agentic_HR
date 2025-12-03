import React, { useState, useRef, useEffect } from 'react';
import { useChatStore } from './store/chatStore';
import { queryHR } from './services/api';
import ChatMessage from './components/ChatMessage';
import ChatInput from './components/ChatInput';
import DataVisualization from './components/DataVisualization';
import Sidebar from './components/Sidebar';
import TokenCounter from './components/TokenCounter';
import SingleValueCard from './components/SingleValueCard';
import { Message } from './store/chatStore';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function App() {
  const {
    sessionId,
    messages,
    isLoading,
    tokenCount,
    setSessionId,
    addMessage,
    setLoading,
    setTokenCount,
  } = useChatStore();

  const [selectedMessage, setSelectedMessage] = useState<Message | null>(null);
  const [showSidebar, setShowSidebar] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (question: string) => {
    // Add user message
    addMessage({
      role: 'user',
      content: question,
    });

    setLoading(true);
    const startTime = Date.now();

    try {
      const response = await queryHR({
        question,
        session_id: sessionId || undefined,
      });

      const responseTime = Date.now() - startTime;

      // Set session ID if new
      if (!sessionId && response.session_id) {
        setSessionId(response.session_id);
      }

      // Update token count
      if (response.token_count) {
        setTokenCount(response.token_count);
      }

      // Get tokens for this query (backend provides it directly)
      const queryTokens = response.query_tokens || 0;
      
      // Update state
      const store = useChatStore.getState();
      store.setLastQueryTokens(queryTokens);
      store.setLastResponseTime(responseTime);

      // Add to query history
      store.addQueryHistory({
        question,
        sql_query: response.sql_query,
        tables: response.tables,
        columns: response.columns,
        token_count: queryTokens,
        response_time: responseTime,
      });

      if (response.success) {
        // Add assistant message with metadata
        addMessage({
          role: 'assistant',
          content: response.answer,
          metadata: {
            sql_query: response.sql_query,
            tables: response.tables,
            columns: response.columns,
            visualization: response.visualization,
            results: response.results,
            insights: response.insights,
            explanation: response.explanation,
          },
        });

        // Auto-select this message for sidebar if it has visualization
        if (response.visualization && response.results) {
          // Create message object for sidebar
          const assistantMessage: Message = {
            id: Date.now().toString(),
            role: 'assistant',
            content: response.answer,
            timestamp: new Date(),
            metadata: {
              sql_query: response.sql_query,
              tables: response.tables,
              columns: response.columns,
              visualization: response.visualization,
              results: response.results,
              insights: response.insights,
              explanation: response.explanation,
            },
          };
          setSelectedMessage(assistantMessage);
          setShowSidebar(true);
        }
      } else {
        addMessage({
          role: 'assistant',
          content: response.error || 'An error occurred',
          metadata: { error: true },
        });
        toast.error(response.error || 'Failed to process query');
      }
    } catch (error: any) {
      addMessage({
        role: 'assistant',
        content: `Error: ${error.message || 'Failed to process query'}`,
        metadata: { error: true },
      });
      toast.error('Failed to process query. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getLastAssistantMessage = (): Message | null => {
    for (let i = messages.length - 1; i >= 0; i--) {
      if (messages[i].role === 'assistant' && messages[i].metadata?.visualization) {
        return messages[i];
      }
    }
    return null;
  };

  const lastVisualizationMessage = getLastAssistantMessage();

  return (
    <div className="flex h-screen bg-gradient-to-br from-slate-950 via-slate-900/95 to-slate-950 text-gray-100">
      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className="bg-gradient-to-r from-slate-900/95 via-slate-800/95 to-slate-900/95 border-b border-slate-700/50 backdrop-blur-sm px-8 py-6 flex items-center justify-between shadow-xl">
          <div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-400 via-blue-400 to-cyan-400 bg-clip-text text-transparent tracking-tight">
              HR Analytics Platform
            </h1>
            <p className="text-sm text-slate-400 mt-1.5 font-medium">Intelligent Data Analysis & Insights</p>
          </div>
          <TokenCounter />
        </header>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto px-8 py-8 bg-gradient-to-b from-slate-950/30 via-slate-900/20 to-slate-950/30">
          {messages.length === 0 && (
            <div className="flex items-center justify-center h-full">
              <div className="text-center">
                <h2 className="text-3xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent mb-3">
                  Welcome to HR Analytics
                </h2>
                <p className="text-slate-400 mb-8 text-lg">
                  Ask questions about your HR data in natural language
                </p>
                <div className="bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700 rounded-2xl p-8 max-w-2xl shadow-2xl">
                  <h3 className="text-xl font-semibold text-slate-200 mb-6 flex items-center gap-2">
                    <span className="w-1 h-6 bg-gradient-to-b from-purple-500 to-blue-500 rounded-full"></span>
                    Example Questions:
                  </h3>
                  <ul className="space-y-3 text-left text-slate-300">
                    <li className="flex items-center gap-3">
                      <span className="text-purple-400">•</span>
                      <span>Show me department wise headcount</span>
                    </li>
                    <li className="flex items-center gap-3">
                      <span className="text-purple-400">•</span>
                      <span>What is the average salary by department?</span>
                    </li>
                    <li className="flex items-center gap-3">
                      <span className="text-purple-400">•</span>
                      <span>Show employee turnover trends</span>
                    </li>
                    <li className="flex items-center gap-3">
                      <span className="text-purple-400">•</span>
                      <span>Which employees have the highest performance ratings?</span>
                    </li>
                    <li className="flex items-center gap-3">
                      <span className="text-purple-400">•</span>
                      <span>What is the attrition rate by department?</span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          )}

          <div className="max-w-4xl mx-auto">
            {messages.map((message) => (
              <div key={message.id}>
                <ChatMessage message={message} />
                {message.role === 'assistant' &&
                  message.metadata?.results && (
                    <div className="mb-6">
                      {message.metadata?.visualization?.visualization_type === 'none' ? (
                        <SingleValueCard 
                          data={message.metadata.results}
                          question={messages[messages.findIndex(m => m.id === message.id) - 1]?.content}
                        />
                      ) : message.metadata?.visualization ? (
                        <DataVisualization
                          data={message.metadata.results}
                          visualization={message.metadata.visualization}
                        />
                      ) : null}
                    </div>
                  )}
              </div>
            ))}
            {isLoading && (
              <div className="flex gap-4 mb-6">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-purple-600 flex items-center justify-center">
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                </div>
                <div className="bg-gray-800 border border-gray-700 rounded-lg px-4 py-3">
                  <div className="text-gray-400">Processing your query...</div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Input Area */}
        <div className="bg-gradient-to-r from-slate-900 to-slate-800 border-t border-slate-700">
          <ChatInput onSend={handleSendMessage} isLoading={isLoading} />
        </div>
      </div>

      {/* Sidebar */}
      {showSidebar && lastVisualizationMessage && (
        <Sidebar
          currentMessage={lastVisualizationMessage}
          onClose={() => setShowSidebar(false)}
        />
      )}

      <ToastContainer
        position="top-right"
        autoClose={3000}
        hideProgressBar={false}
        newestOnTop
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="dark"
      />
    </div>
  );
}

export default App;

