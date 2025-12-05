import React from 'react';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  AreaChart,
  Area,
  PieChart,
  Pie,
  ScatterChart,
  Scatter,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import SingleValueCard from './SingleValueCard';

interface DataVisualizationProps {
  data: any[];
  visualization: {
    visualization_type: string;
    x_axis?: string;
    y_axis?: string;
    explanation?: string;
  };
}

const COLORS = ['#8b5cf6', '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#06b6d4'];

const DataVisualization: React.FC<DataVisualizationProps> = ({ data, visualization }) => {
  if (!data || data.length === 0) {
    return (
      <div className="bg-gray-800 border border-gray-700 rounded-lg p-8 text-center text-gray-400">
        No data available for visualization
      </div>
    );
  }

  const { visualization_type, x_axis, y_axis } = visualization;

  if (visualization_type === 'none') {
    return (
      <SingleValueCard data={data} />
    );
  }

  // Prepare data for charts
  const chartData = data.map((row) => {
    const entry: any = {};
    Object.keys(row).forEach((key) => {
      const value = row[key];
      // Convert numeric strings to numbers
      entry[key] = isNaN(Number(value)) ? value : Number(value);
    });
    return entry;
  });

  // Auto-detect axes if not specified
  const xKey = x_axis || Object.keys(data[0])[0];
  const yKey = y_axis || Object.keys(data[0])[1] || Object.keys(data[0])[0];

  if (visualization_type === 'bar') {
    return (
      <div className="bg-gradient-to-br from-slate-800/95 to-slate-900/95 border border-slate-700/50 rounded-2xl p-6 shadow-2xl backdrop-blur-sm">
        <ResponsiveContainer width="100%" height={450}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#475569" opacity={0.2} />
            <XAxis 
              dataKey={xKey} 
              stroke="#94a3b8" 
              tick={{ fill: '#cbd5e1', fontSize: 12, fontWeight: 500 }}
              angle={-45}
              textAnchor="end"
              height={80}
            />
            <YAxis 
              stroke="#94a3b8" 
              tick={{ fill: '#cbd5e1', fontSize: 12, fontWeight: 500 }}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#1e293b',
                border: '1px solid #475569',
                borderRadius: '8px',
                color: '#e2e8f0',
                boxShadow: '0 4px 6px rgba(0, 0, 0, 0.3)',
              }}
              cursor={{ fill: 'rgba(139, 92, 246, 0.1)' }}
            />
            <Legend 
              wrapperStyle={{ color: '#cbd5e1', fontSize: '13px' }}
            />
            <Bar 
              dataKey={yKey} 
              fill="url(#barGradient)"
              radius={[8, 8, 0, 0]}
            />
            <defs>
              <linearGradient id="barGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#8b5cf6" stopOpacity={1} />
                <stop offset="100%" stopColor="#6366f1" stopOpacity={0.8} />
              </linearGradient>
            </defs>
          </BarChart>
        </ResponsiveContainer>
      </div>
    );
  }

  if (visualization_type === 'line') {
    return (
      <div className="bg-gradient-to-br from-slate-800/95 to-slate-900/95 border border-slate-700/50 rounded-2xl p-6 shadow-2xl backdrop-blur-sm">
        <ResponsiveContainer width="100%" height={450}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#475569" opacity={0.2} />
            <XAxis 
              dataKey={xKey} 
              stroke="#94a3b8" 
              tick={{ fill: '#cbd5e1', fontSize: 12, fontWeight: 500 }}
            />
            <YAxis 
              stroke="#94a3b8" 
              tick={{ fill: '#cbd5e1', fontSize: 12, fontWeight: 500 }}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#1e293b',
                border: '1px solid #475569',
                borderRadius: '8px',
                color: '#e2e8f0',
                boxShadow: '0 4px 6px rgba(0, 0, 0, 0.3)',
              }}
              cursor={{ stroke: '#8b5cf6', strokeWidth: 1 }}
            />
            <Legend 
              wrapperStyle={{ color: '#cbd5e1', fontSize: '13px' }}
            />
            <Line 
              type="monotone" 
              dataKey={yKey} 
              stroke="#8b5cf6" 
              strokeWidth={3}
              dot={{ fill: '#8b5cf6', r: 4 }}
              activeDot={{ r: 6, fill: '#8b5cf6' }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    );
  }

  if (visualization_type === 'pie') {
    return (
      <div className="bg-gradient-to-br from-slate-800/95 to-slate-900/95 border border-slate-700/50 rounded-2xl p-6 shadow-2xl backdrop-blur-sm">
        <ResponsiveContainer width="100%" height={450}>
          <PieChart>
            <Pie
              data={chartData}
              dataKey={yKey}
              nameKey={xKey}
              cx="50%"
              cy="50%"
              outerRadius={140}
              label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
              labelLine={false}
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip
              contentStyle={{
                backgroundColor: '#1e293b',
                border: '1px solid #475569',
                borderRadius: '8px',
                color: '#e2e8f0',
                boxShadow: '0 4px 6px rgba(0, 0, 0, 0.3)',
              }}
            />
            <Legend 
              wrapperStyle={{ color: '#cbd5e1', fontSize: '13px' }}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>
    );
  }

  if (visualization_type === 'scatter') {
    return (
      <div className="bg-gradient-to-br from-slate-800/95 to-slate-900/95 border border-slate-700/50 rounded-2xl p-6 shadow-2xl backdrop-blur-sm">
        <ResponsiveContainer width="100%" height={450}>
          <ScatterChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#475569" opacity={0.2} />
            <XAxis 
              dataKey={xKey} 
              stroke="#94a3b8" 
              tick={{ fill: '#cbd5e1', fontSize: 12, fontWeight: 500 }}
              name={xKey}
              type="number"
            />
            <YAxis 
              stroke="#94a3b8" 
              tick={{ fill: '#cbd5e1', fontSize: 12, fontWeight: 500 }}
              name={yKey}
              type="number"
            />
            <Tooltip
              cursor={{ stroke: '#8b5cf6', strokeWidth: 1 }}
              contentStyle={{
                backgroundColor: '#1e293b',
                border: '1px solid #475569',
                borderRadius: '8px',
                color: '#e2e8f0',
                boxShadow: '0 4px 6px rgba(0, 0, 0, 0.3)',
              }}
            />
            <Legend 
              wrapperStyle={{ color: '#cbd5e1', fontSize: '13px' }}
            />
            <Scatter 
              dataKey={yKey} 
              fill="#8b5cf6" 
              shape="circle"
            />
          </ScatterChart>
        </ResponsiveContainer>
      </div>
    );
  }

  if (visualization_type === 'area') {
    return (
      <div className="bg-gradient-to-br from-slate-800/95 to-slate-900/95 border border-slate-700/50 rounded-2xl p-6 shadow-2xl backdrop-blur-sm">
        <ResponsiveContainer width="100%" height={450}>
          <AreaChart data={chartData}>
            <defs>
              <linearGradient id="areaGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.8} />
                <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0.1} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#475569" opacity={0.2} />
            <XAxis 
              dataKey={xKey} 
              stroke="#94a3b8" 
              tick={{ fill: '#cbd5e1', fontSize: 12, fontWeight: 500 }}
            />
            <YAxis 
              stroke="#94a3b8" 
              tick={{ fill: '#cbd5e1', fontSize: 12, fontWeight: 500 }}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#1e293b',
                border: '1px solid #475569',
                borderRadius: '8px',
                color: '#e2e8f0',
                boxShadow: '0 4px 6px rgba(0, 0, 0, 0.3)',
              }}
              cursor={{ stroke: '#8b5cf6', strokeWidth: 1 }}
            />
            <Legend 
              wrapperStyle={{ color: '#cbd5e1', fontSize: '13px' }}
            />
            <Area 
              type="monotone" 
              dataKey={yKey} 
              stroke="#8b5cf6" 
              strokeWidth={3}
              fill="url(#areaGradient)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    );
  }

  // Default: Table view
  return (
    <div className="bg-gradient-to-br from-slate-800/95 to-slate-900/95 border border-slate-700/50 rounded-2xl overflow-hidden shadow-2xl backdrop-blur-sm">
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gradient-to-r from-slate-700/80 to-slate-800/80">
            <tr>
              {Object.keys(data[0]).map((key) => (
                <th key={key} className="px-6 py-4 text-left text-sm font-semibold text-slate-200 uppercase tracking-wide">
                  {key.replace(/_/g, ' ')}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.slice(0, 100).map((row, idx) => (
              <tr 
                key={idx} 
                className="border-t border-slate-700/50 hover:bg-slate-700/30 transition-colors"
              >
                {Object.values(row).map((value: any, colIdx) => (
                  <td key={colIdx} className="px-6 py-4 text-sm text-slate-200">
                    {value}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
        {data.length > 100 && (
          <div className="px-6 py-3 text-sm text-slate-400 bg-slate-800/30 border-t border-slate-700/50">
            Showing first 100 of {data.length} rows
          </div>
        )}
      </div>
    </div>
  );
};

export default DataVisualization;


