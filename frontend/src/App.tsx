import React, { useState, useRef, useEffect } from 'react';
import { useChatStore, Message } from './store/chatStore';
import { queryHR } from './services/api';
import ChatMessage from './components/ChatMessage';
import ChatInput from './components/ChatInput';
import DataVisualization from './components/DataVisualization';
import Sidebar from './components/Sidebar';
import TokenCounter from './components/TokenCounter';
import SingleValueCard from './components/SingleValueCard';
import LandingPage from './components/LandingPage';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { Home } from 'lucide-react';

function App() {
  const [showLanding, setShowLanding] = useState(true);
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
            cache_hit: response.cache_hit,
            rag_used: response.rag_used,
            cache_similarity: response.cache_similarity,
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
              cache_hit: response.cache_hit,
              rag_used: response.rag_used,
              cache_similarity: response.cache_similarity,
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

  const handleEnterChat = () => {
    setShowLanding(false);
  };

  const lastVisualizationMessage = getLastAssistantMessage();

  if (showLanding) {
    return <LandingPage onEnterChat={handleEnterChat} />;
  }

  return (
    <div className="flex h-screen bg-gradient-to-br from-emerald-950 via-teal-950/95 to-slate-950 text-gray-100">
      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className="bg-gradient-to-r from-emerald-900/95 via-teal-900/95 to-emerald-900/95 border-b border-emerald-700/50 backdrop-blur-sm px-8 py-6 flex items-center justify-between shadow-xl">
          <div className="flex items-center gap-6">
            <button
              onClick={() => setShowLanding(true)}
              className="flex items-center gap-2 px-4 py-2 rounded-lg bg-emerald-800/50 hover:bg-emerald-700/50 border border-emerald-700/50 hover:border-emerald-600/50 transition-all duration-200 text-emerald-300 hover:text-emerald-200"
              title="Back to Home"
            >
              <Home className="w-5 h-5" />
              <span className="text-sm font-medium">Home</span>
            </button>
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-emerald-400 via-teal-400 to-cyan-400 bg-clip-text text-transparent tracking-tight">
                HR Analytics AI
              </h1>
              <p className="text-sm text-emerald-300/70 mt-1.5 font-medium">RAG-Enhanced • Semantic Caching</p>
            </div>
          </div>
          <TokenCounter />
        </header>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto px-8 py-8 bg-gradient-to-b from-emerald-950/30 via-teal-950/20 to-emerald-950/30">
          {messages.length === 0 && (
            <div className="flex items-center justify-center h-full">
              <div className="text-center">
                <h2 className="text-3xl font-bold bg-gradient-to-r from-emerald-400 to-teal-400 bg-clip-text text-transparent mb-3">
                  Welcome to HR Analytics AI
                </h2>
                <p className="text-emerald-200/80 mb-8 text-lg">
                  Ask questions about your HR data - Powered by RAG & Semantic Caching
                </p>
                <div className="bg-gradient-to-br from-emerald-900/40 to-teal-900/40 border border-emerald-700/50 rounded-2xl p-8 max-w-2xl shadow-2xl backdrop-blur-sm">
                  <h3 className="text-xl font-semibold text-emerald-200 mb-6 flex items-center gap-2">
                    <span className="w-1 h-6 bg-gradient-to-b from-emerald-500 to-teal-500 rounded-full"></span>
                    Try These Questions:
                  </h3>
                  <ul className="space-y-3 text-left text-emerald-100/90">
                    <li className="flex items-center gap-3">
                      <span className="text-emerald-400">•</span>
                      <span>Calculate Internal Mobility Rate by department</span>
                    </li>
                    <li className="flex items-center gap-3">
                      <span className="text-emerald-400">•</span>
                      <span>Show me Flight Risk employees</span>
                    </li>
                    <li className="flex items-center gap-3">
                      <span className="text-emerald-400">•</span>
                      <span>What is the Employee Net Promoter Score?</span>
                    </li>
                    <li className="flex items-center gap-3">
                      <span className="text-emerald-400">•</span>
                      <span>Show me department wise headcount</span>
                    </li>
                    <li className="flex items-center gap-3">
                      <span className="text-emerald-400">•</span>
                      <span>What is the average salary by department?</span>
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
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-emerald-600 to-teal-600 flex items-center justify-center">
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                </div>
                <div className="bg-emerald-900/40 border border-emerald-700/50 rounded-lg px-4 py-3 backdrop-blur-sm">
                  <div className="text-emerald-200">Processing your query with AI...</div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Input Area */}
        <div className="bg-gradient-to-r from-emerald-900 to-teal-900 border-t border-emerald-700/50">
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

