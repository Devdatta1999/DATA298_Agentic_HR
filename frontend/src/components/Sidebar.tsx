import React, { useState } from 'react';
import { Message } from '../store/chatStore';
import { Database, Code, X } from 'lucide-react';

interface SidebarProps {
  currentMessage: Message | null;
  onClose: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ currentMessage, onClose }) => {
  const [activeTab, setActiveTab] = useState<'tables' | 'sql'>('tables');

  if (!currentMessage || !currentMessage.metadata) {
    return null;
  }

  const { sql_query, tables, columns } = currentMessage.metadata;

  return (
    <div className="w-96 bg-gray-900 border-l border-gray-700 flex flex-col h-full">
      {/* Header */}
      <div className="p-4 border-b border-gray-700 flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-200">Query Details</h3>
        <button
          onClick={onClose}
          className="text-gray-400 hover:text-gray-200 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-gray-700">
        <button
          onClick={() => setActiveTab('tables')}
          className={`flex-1 px-4 py-3 text-sm font-medium transition-colors ${
            activeTab === 'tables'
              ? 'text-purple-400 border-b-2 border-purple-400'
              : 'text-gray-400 hover:text-gray-200'
          }`}
        >
          <Database className="w-4 h-4 inline mr-2" />
          Tables & Columns
        </button>
        <button
          onClick={() => setActiveTab('sql')}
          className={`flex-1 px-4 py-3 text-sm font-medium transition-colors ${
            activeTab === 'sql'
              ? 'text-purple-400 border-b-2 border-purple-400'
              : 'text-gray-400 hover:text-gray-200'
          }`}
        >
          <Code className="w-4 h-4 inline mr-2" />
          SQL Query
        </button>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-4">
        {activeTab === 'tables' && (
          <div className="space-y-4">
            <div>
              <h4 className="text-sm font-semibold text-gray-300 mb-2">
                Relevant Tables
              </h4>
              {tables && tables.length > 0 ? (
                <div className="space-y-2">
                  {tables.map((table, idx) => (
                    <div
                      key={idx}
                      className="bg-gray-800 border border-gray-700 rounded-lg p-3"
                    >
                      <div className="text-sm font-medium text-purple-400 mb-2">
                        {table}
                      </div>
                      {columns && columns[table] && Array.isArray(columns[table]) && columns[table].length > 0 && (
                        <div className="flex flex-wrap gap-1 mt-2">
                          {columns[table].map((col: string, colIdx: number) => (
                            <span
                              key={colIdx}
                              className="px-2 py-1 bg-gray-700 text-gray-300 text-xs rounded"
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
                <p className="text-sm text-gray-400">No table information available</p>
              )}
            </div>
          </div>
        )}

        {activeTab === 'sql' && (
          <div>
            <h4 className="text-sm font-semibold text-gray-300 mb-2">Generated SQL</h4>
            {sql_query ? (
              <div className="bg-gray-950 rounded-lg overflow-hidden">
                <pre className="p-4 text-sm text-gray-300 overflow-x-auto">
                  <code>{sql_query}</code>
                </pre>
              </div>
            ) : (
              <p className="text-sm text-gray-400">No SQL query available</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Sidebar;

