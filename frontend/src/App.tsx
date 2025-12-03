import React, { useState, useRef, useEffect } from 'react';
import { useChatStore } from './store/chatStore';
import { queryHR } from './services/api';
import ChatMessage from './components/ChatMessage';
import ChatInput from './components/ChatInput';
import DataVisualization from './components/DataVisualization';
import Sidebar from './components/Sidebar';
import TokenCounter from './components/TokenCounter';
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

    try {
      const response = await queryHR({
        question,
        session_id: sessionId || undefined,
      });

      // Set session ID if new
      if (!sessionId && response.session_id) {
        setSessionId(response.session_id);
      }

      // Update token count
      if (response.token_count) {
        setTokenCount(response.token_count);
      }

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
    <div className="flex h-screen bg-gray-950 text-gray-100">
      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className="bg-gray-900 border-b border-gray-800 px-6 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-white">HR Analytics</h1>
            <p className="text-sm text-gray-400">AI-Powered Data Analysis</p>
          </div>
          <TokenCounter />
        </header>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto px-6 py-6">
          {messages.length === 0 && (
            <div className="flex items-center justify-center h-full">
              <div className="text-center">
                <h2 className="text-2xl font-semibold text-gray-300 mb-2">
                  Welcome to HR Analytics
                </h2>
                <p className="text-gray-400 mb-6">
                  Ask questions about your HR data in natural language
                </p>
                <div className="bg-gray-900 border border-gray-800 rounded-lg p-6 max-w-2xl">
                  <h3 className="text-lg font-semibold text-gray-200 mb-4">
                    Example Questions:
                  </h3>
                  <ul className="space-y-2 text-left text-gray-400">
                    <li>• Show me department wise headcount</li>
                    <li>• What is the average salary by department?</li>
                    <li>• Show employee turnover trends</li>
                    <li>• Which employees have the highest performance ratings?</li>
                    <li>• What is the attrition rate by department?</li>
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
                  message.metadata?.visualization &&
                  message.metadata?.results && (
                    <div className="mb-6">
                      <DataVisualization
                        data={message.metadata.results}
                        visualization={message.metadata.visualization}
                      />
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
        <ChatInput onSend={handleSendMessage} isLoading={isLoading} />
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

