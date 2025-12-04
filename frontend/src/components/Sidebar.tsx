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
    <div className="w-[420px] bg-gradient-to-b from-emerald-950 to-slate-950 border-l border-emerald-800/50 flex flex-col h-full shadow-2xl">
      {/* Header */}
      <div className="p-5 border-b border-emerald-800/50 bg-gradient-to-r from-emerald-900 to-teal-900 flex items-center justify-between">
        <h3 className="text-lg font-semibold text-emerald-200">Query Details</h3>
        <button
          onClick={onClose}
          className="text-emerald-300/70 hover:text-emerald-200 transition-colors p-1 hover:bg-emerald-800/50 rounded"
        >
          <X className="w-5 h-5" />
        </button>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-emerald-800/50 bg-emerald-900/30">
        <button
          onClick={() => setActiveTab('tables')}
          className={`flex-1 px-3 py-3 text-xs font-medium transition-all ${
            activeTab === 'tables'
              ? 'text-emerald-400 border-b-2 border-emerald-400 bg-emerald-900/50'
              : 'text-emerald-300/70 hover:text-emerald-200'
          }`}
        >
          <Database className="w-3 h-3 inline mr-1" />
          Current
        </button>
        <button
          onClick={() => setActiveTab('sql')}
          className={`flex-1 px-3 py-3 text-xs font-medium transition-all ${
            activeTab === 'sql'
              ? 'text-emerald-400 border-b-2 border-emerald-400 bg-emerald-900/50'
              : 'text-emerald-300/70 hover:text-emerald-200'
          }`}
        >
          <Code className="w-3 h-3 inline mr-1" />
          SQL
        </button>
        <button
          onClick={() => setActiveTab('history')}
          className={`flex-1 px-3 py-3 text-xs font-medium transition-all ${
            activeTab === 'history'
              ? 'text-emerald-400 border-b-2 border-emerald-400 bg-emerald-900/50'
              : 'text-emerald-300/70 hover:text-emerald-200'
          }`}
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
              <h4 className="text-sm font-semibold text-emerald-200 mb-3 uppercase tracking-wide">
                Relevant Tables
              </h4>
              {tables && tables.length > 0 ? (
                <div className="space-y-3">
                  {tables.map((table, idx) => (
                    <div
                      key={idx}
                      className="bg-gradient-to-br from-emerald-900/50 to-teal-900/50 border border-emerald-700/50 rounded-xl p-4 shadow-lg"
                    >
                      <div className="text-sm font-semibold text-emerald-400 mb-3">
                        {table}
                      </div>
                      {columns && columns[table] && Array.isArray(columns[table]) && columns[table].length > 0 && (
                        <div className="flex flex-wrap gap-2 mt-2">
                          {columns[table].map((col: string, colIdx: number) => (
                            <span
                              key={colIdx}
                              className="px-3 py-1 bg-emerald-800/50 text-emerald-100 text-xs rounded-lg border border-emerald-600/50"
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
                <p className="text-sm text-emerald-300/70">No table information available</p>
              )}
            </div>
          </div>
        )}

        {activeTab === 'sql' && (
          <div>
            <h4 className="text-sm font-semibold text-emerald-200 mb-3 uppercase tracking-wide">Generated SQL</h4>
            {sql_query ? (
              <div className="bg-emerald-950 rounded-xl overflow-hidden border border-emerald-800/50 shadow-lg">
                <pre className="p-5 text-sm text-emerald-100 overflow-x-auto font-mono">
                  <code>{sql_query}</code>
                </pre>
              </div>
            ) : (
              <p className="text-sm text-emerald-300/70">No SQL query available</p>
            )}
          </div>
        )}

        {activeTab === 'history' && (
          <div className="space-y-3">
            <h4 className="text-sm font-semibold text-emerald-200 mb-3 uppercase tracking-wide">
              Query History
            </h4>
            {queryHistory.length > 0 ? (
              <div className="space-y-2">
                {queryHistory.map((query, idx) => (
                  <div
                    key={idx}
                    className="bg-gradient-to-br from-emerald-900/30 to-teal-900/30 border border-emerald-700/50 rounded-lg overflow-hidden"
                  >
                    <button
                      onClick={() => toggleQuery(idx)}
                      className="w-full p-3 flex items-center justify-between hover:bg-emerald-800/30 transition-colors"
                    >
                      <div className="flex items-center gap-2 flex-1 text-left">
                        {expandedQueries.has(idx) ? (
                          <ChevronDown className="w-4 h-4 text-emerald-300/70 flex-shrink-0" />
                        ) : (
                          <ChevronRight className="w-4 h-4 text-emerald-300/70 flex-shrink-0" />
                        )}
                        <span className="text-xs font-medium text-emerald-400">Q{idx + 1}:</span>
                        <span className="text-sm text-emerald-100 truncate flex-1">{query.question}</span>
                      </div>
                    </button>
                    {expandedQueries.has(idx) && (
                      <div className="px-3 pb-3 space-y-3 border-t border-emerald-700/50">
                        {/* Tables & Columns */}
                        {query.tables && query.tables.length > 0 && (
                          <div>
                            <h5 className="text-xs font-semibold text-emerald-300/70 mb-2 uppercase">Tables & Columns</h5>
                            <div className="space-y-2">
                              {query.tables.map((table, tIdx) => (
                                <div key={tIdx} className="bg-emerald-900/40 rounded p-2">
                                  <div className="text-xs font-medium text-emerald-400 mb-1">{table}</div>
                                  {query.columns && query.columns[table] && (
                                    <div className="flex flex-wrap gap-1">
                                      {query.columns[table].map((col: string, cIdx: number) => (
                                        <span
                                          key={cIdx}
                                          className="px-2 py-0.5 bg-emerald-800/50 text-emerald-100 text-xs rounded"
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
                            <h5 className="text-xs font-semibold text-emerald-300/70 mb-2 uppercase">SQL Query</h5>
                            <div className="bg-emerald-950 rounded p-2 border border-emerald-800/50">
                              <pre className="text-xs text-emerald-100 font-mono overflow-x-auto">
                                <code>{query.sql_query}</code>
                              </pre>
                            </div>
                          </div>
                        )}
                        {/* Stats */}
                        <div className="flex gap-3 text-xs text-emerald-300/70">
                          {query.token_count && (
                            <span>Tokens: <span className="text-emerald-400">{query.token_count.toLocaleString()}</span></span>
                          )}
                          {query.response_time && (
                            <span>Time: <span className="text-teal-400">{(query.response_time / 1000).toFixed(1)}s</span></span>
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-sm text-emerald-300/70">No query history yet</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Sidebar;

