import React, { useState } from 'react';
import { Message } from '../store/chatStore';
import { useChatStore } from '../store/chatStore';
import { Database, Code, X, ChevronDown, ChevronRight } from 'lucide-react';

interface SidebarProps {
  currentMessage: Message | null;
  onClose: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ currentMessage, onClose }) => {
  const [activeTab, setActiveTab] = useState<'tables' | 'sql' | 'history'>('tables');
  const [expandedQueries, setExpandedQueries] = useState<Set<number>>(new Set());
  const queryHistory = useChatStore((state) => state.queryHistory);

  const toggleQuery = (index: number) => {
    const newExpanded = new Set(expandedQueries);
    if (newExpanded.has(index)) {
      newExpanded.delete(index);
    } else {
      newExpanded.add(index);
    }
    setExpandedQueries(newExpanded);
  };

  // Show current message if available, otherwise show history
  const showCurrent = currentMessage && currentMessage.metadata;
  const { sql_query, tables, columns } = showCurrent ? currentMessage.metadata! : { sql_query: undefined, tables: undefined, columns: undefined };

  return (
    <div className="w-[420px] border-l flex flex-col h-full shadow-2xl" style={{ 
      backgroundColor: '#11182A',
      borderColor: 'rgba(30, 42, 64, 0.5)'
    }}>
      {/* Header */}
      <div className="p-5 border-b flex items-center justify-between" style={{ 
        backgroundColor: '#1E2A40',
        borderColor: 'rgba(30, 42, 64, 0.5)'
      }}>
        <h3 className="text-lg font-semibold" style={{ color: '#FFFFFF' }}>Query Details</h3>
        <button
          onClick={onClose}
          className="transition-colors p-1 rounded"
          style={{ color: '#B6C2CC' }}
          onMouseEnter={(e) => {
            e.currentTarget.style.color = '#FFFFFF';
            e.currentTarget.style.backgroundColor = '#1E2A40';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.color = '#B6C2CC';
            e.currentTarget.style.backgroundColor = 'transparent';
          }}
        >
          <X className="w-5 h-5" />
        </button>
      </div>

      {/* Tabs */}
      <div className="flex border-b" style={{ 
        borderColor: 'rgba(30, 42, 64, 0.5)',
        backgroundColor: '#1E2A40'
      }}>
        <button
          onClick={() => setActiveTab('tables')}
          className={`flex-1 px-3 py-3 text-xs font-medium transition-all ${
            activeTab === 'tables' ? '' : ''
          }`}
          style={activeTab === 'tables' ? {
            color: '#F9A23F',
            borderBottom: '2px solid #F9A23F',
            backgroundColor: '#1E2A40'
          } : {
            color: '#B6C2CC'
          }}
          onMouseEnter={(e) => {
            if (activeTab !== 'tables') {
              e.currentTarget.style.color = '#FFFFFF';
            }
          }}
          onMouseLeave={(e) => {
            if (activeTab !== 'tables') {
              e.currentTarget.style.color = '#B6C2CC';
            }
          }}
        >
          <Database className="w-3 h-3 inline mr-1" />
          Current
        </button>
        <button
          onClick={() => setActiveTab('sql')}
          className={`flex-1 px-3 py-3 text-xs font-medium transition-all ${
            activeTab === 'sql' ? '' : ''
          }`}
          style={activeTab === 'sql' ? {
            color: '#F9A23F',
            borderBottom: '2px solid #F9A23F',
            backgroundColor: '#1E2A40'
          } : {
            color: '#B6C2CC'
          }}
          onMouseEnter={(e) => {
            if (activeTab !== 'sql') {
              e.currentTarget.style.color = '#FFFFFF';
            }
          }}
          onMouseLeave={(e) => {
            if (activeTab !== 'sql') {
              e.currentTarget.style.color = '#B6C2CC';
            }
          }}
        >
          <Code className="w-3 h-3 inline mr-1" />
          SQL
        </button>
        <button
          onClick={() => setActiveTab('history')}
          className={`flex-1 px-3 py-3 text-xs font-medium transition-all ${
            activeTab === 'history' ? '' : ''
          }`}
          style={activeTab === 'history' ? {
            color: '#F9A23F',
            borderBottom: '2px solid #F9A23F',
            backgroundColor: '#1E2A40'
          } : {
            color: '#B6C2CC'
          }}
          onMouseEnter={(e) => {
            if (activeTab !== 'history') {
              e.currentTarget.style.color = '#FFFFFF';
            }
          }}
          onMouseLeave={(e) => {
            if (activeTab !== 'history') {
              e.currentTarget.style.color = '#B6C2CC';
            }
          }}
        >
          <Database className="w-3 h-3 inline mr-1" />
          History
        </button>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-5">
        {activeTab === 'tables' && (
          <div className="space-y-4">
            <div>
              <h4 className="text-sm font-semibold mb-3 uppercase tracking-wide" style={{ color: '#B6C2CC' }}>
                Relevant Tables
              </h4>
              {tables && tables.length > 0 ? (
                <div className="space-y-3">
                  {tables.map((table, idx) => (
                    <div
                      key={idx}
                      className="rounded-xl p-4 shadow-lg"
                      style={{
                        background: 'linear-gradient(135deg, #11182A 0%, #1E2A40 100%)',
                        border: '1px solid rgba(30, 42, 64, 0.6)'
                      }}
                    >
                      <div className="text-sm font-semibold mb-3" style={{ color: '#F9A23F' }}>
                        {table}
                      </div>
                      {columns && columns[table] && Array.isArray(columns[table]) && columns[table].length > 0 && (
                        <div className="flex flex-wrap gap-2 mt-2">
                          {columns[table].map((col: string, colIdx: number) => (
                            <span
                              key={colIdx}
                              className="px-3 py-1 text-xs rounded-lg"
                              style={{
                                backgroundColor: '#1E2A40',
                                color: '#FFFFFF',
                                border: '1px solid rgba(30, 42, 64, 0.6)'
                              }}
                            >
                              {col}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm" style={{ color: '#B6C2CC' }}>No table information available</p>
              )}
            </div>
          </div>
        )}

        {activeTab === 'sql' && (
          <div>
            <h4 className="text-sm font-semibold mb-3 uppercase tracking-wide" style={{ color: '#B6C2CC' }}>Generated SQL</h4>
            {sql_query ? (
              <div className="rounded-xl overflow-hidden shadow-lg" style={{
                backgroundColor: '#0A0F1F',
                border: '1px solid rgba(30, 42, 64, 0.6)'
              }}>
                <pre className="p-5 text-sm overflow-x-auto font-mono" style={{ color: '#FFFFFF' }}>
                  <code>{sql_query}</code>
                </pre>
              </div>
            ) : (
              <p className="text-sm" style={{ color: '#B6C2CC' }}>No SQL query available</p>
            )}
          </div>
        )}

        {activeTab === 'history' && (
          <div className="space-y-3">
            <h4 className="text-sm font-semibold text-slate-300 mb-3 uppercase tracking-wide">
              Query History
            </h4>
            {queryHistory.length > 0 ? (
              <div className="space-y-2">
                {queryHistory.map((query, idx) => (
                  <div
                    key={idx}
                    className="bg-gradient-to-br from-slate-800/50 to-slate-900/50 border border-slate-700 rounded-lg overflow-hidden"
                  >
                    <button
                      onClick={() => toggleQuery(idx)}
                      className="w-full p-3 flex items-center justify-between hover:bg-slate-800/50 transition-colors"
                    >
                      <div className="flex items-center gap-2 flex-1 text-left">
                        {expandedQueries.has(idx) ? (
                          <ChevronDown className="w-4 h-4 text-slate-400 flex-shrink-0" />
                        ) : (
                          <ChevronRight className="w-4 h-4 text-slate-400 flex-shrink-0" />
                        )}
                        <span className="text-xs font-medium" style={{ color: '#F9A23F' }}>Q{idx + 1}:</span>
                        <span className="text-sm text-slate-300 truncate flex-1">{query.question}</span>
                      </div>
                    </button>
                    {expandedQueries.has(idx) && (
                      <div className="px-3 pb-3 space-y-3 border-t border-slate-700">
                        {/* Tables & Columns */}
                        {query.tables && query.tables.length > 0 && (
                          <div>
                            <h5 className="text-xs font-semibold text-slate-400 mb-2 uppercase">Tables & Columns</h5>
                            <div className="space-y-2">
                              {query.tables.map((table, tIdx) => (
                                <div key={tIdx} className="bg-slate-900/50 rounded p-2">
                                  <div className="text-xs font-medium mb-1" style={{ color: '#F9A23F' }}>{table}</div>
                                  {query.columns && query.columns[table] && (
                                    <div className="flex flex-wrap gap-1">
                                      {query.columns[table].map((col: string, cIdx: number) => (
                                        <span
                                          key={cIdx}
                                          className="px-2 py-0.5 bg-slate-800 text-slate-300 text-xs rounded"
                                        >
                                          {col}
                                        </span>
                                      ))}
                                    </div>
                                  )}
                                </div>
                              ))}
                            </div>
                          </div>
                        )}
                        {/* SQL Query */}
                        {query.sql_query && (
                          <div>
                            <h5 className="text-xs font-semibold text-slate-400 mb-2 uppercase">SQL Query</h5>
                            <div className="bg-slate-950 rounded p-2 border border-slate-700">
                              <pre className="text-xs text-slate-300 font-mono overflow-x-auto">
                                <code>{query.sql_query}</code>
                              </pre>
                            </div>
                          </div>
                        )}
                        {/* Stats */}
                        <div className="flex gap-3 text-xs text-slate-400">
                          {query.token_count && (
                            <span>Tokens: <span className="text-blue-400">{query.token_count.toLocaleString()}</span></span>
                          )}
                          {query.response_time && (
                            <span>Time: <span className="text-green-400">{(query.response_time / 1000).toFixed(1)}s</span></span>
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-sm text-slate-400">No query history yet</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Sidebar;

