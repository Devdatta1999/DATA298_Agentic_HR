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
    <div className="flex h-screen bg-[#F8F9F5] text-[#222]">
      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className="bg-white border-b border-[#DFE4DD] px-8 py-6 flex items-center justify-between shadow-sm">
          <div className="flex items-center gap-6">
            <button
              onClick={() => setShowLanding(true)}
              className="flex items-center gap-2 px-4 py-2 rounded-lg bg-[#F8F9F5] hover:bg-[#DFE4DD]/30 border border-[#DFE4DD] transition-all duration-200 text-[#222] hover:text-[#344E41]"
              title="Back to Home"
            >
              <Home className="w-5 h-5" />
              <span className="text-sm font-medium">Home</span>
            </button>
            <div>
              <h1 className="text-3xl font-bold text-[#222] tracking-tight">
                HR Analytics Platform
              </h1>
              <p className="text-sm text-[#588157] mt-1.5 font-medium">RAG-Enhanced • Semantic Caching</p>
            </div>
          </div>
          <TokenCounter />
        </header>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto px-8 py-8 bg-[#F8F9F5]">
          {messages.length === 0 && (
            <div className="flex items-center justify-center h-full">
              <div className="text-center">
                <h2 className="text-3xl font-bold text-[#222] mb-3">
                  Welcome to HR Analytics Platform
                </h2>
                <p className="text-[#344E41] mb-8 text-lg">
                  Ask questions about your HR data - Powered by RAG & Semantic Caching
                </p>
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
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-[#588157] flex items-center justify-center">
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                </div>
                <div className="bg-white border border-[#DFE4DD] rounded-lg px-4 py-3 shadow-sm">
                  <div className="text-[#222]">Processing your query with AI...</div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Input Area */}
        <div className="bg-white border-t border-[#DFE4DD]">
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
        theme="light"
      />
    </div>
  );
}

export default App;

