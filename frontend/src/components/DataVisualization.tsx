import React from 'react';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

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
      <div className="bg-gray-800 border border-gray-700 rounded-lg p-4 text-gray-300">
        {visualization.explanation || 'Single value result - no visualization needed'}
      </div>
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
      <div className="bg-gray-800 border border-gray-700 rounded-lg p-4">
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis dataKey={xKey} stroke="#9ca3af" />
            <YAxis stroke="#9ca3af" />
            <Tooltip
              contentStyle={{
                backgroundColor: '#1f2937',
                border: '1px solid #374151',
                borderRadius: '6px',
              }}
            />
            <Legend />
            <Bar dataKey={yKey} fill="#8b5cf6" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    );
  }

  if (visualization_type === 'line') {
    return (
      <div className="bg-gray-800 border border-gray-700 rounded-lg p-4">
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis dataKey={xKey} stroke="#9ca3af" />
            <YAxis stroke="#9ca3af" />
            <Tooltip
              contentStyle={{
                backgroundColor: '#1f2937',
                border: '1px solid #374151',
                borderRadius: '6px',
              }}
            />
            <Legend />
            <Line type="monotone" dataKey={yKey} stroke="#8b5cf6" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    );
  }

  if (visualization_type === 'pie') {
    return (
      <div className="bg-gray-800 border border-gray-700 rounded-lg p-4">
        <ResponsiveContainer width="100%" height={400}>
          <PieChart>
            <Pie
              data={chartData}
              dataKey={yKey}
              nameKey={xKey}
              cx="50%"
              cy="50%"
              outerRadius={120}
              label
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip
              contentStyle={{
                backgroundColor: '#1f2937',
                border: '1px solid #374151',
                borderRadius: '6px',
              }}
            />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </div>
    );
  }

  // Default: Table view
  return (
    <div className="bg-gray-800 border border-gray-700 rounded-lg overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-700">
            <tr>
              {Object.keys(data[0]).map((key) => (
                <th key={key} className="px-4 py-3 text-left text-sm font-semibold text-gray-200">
                  {key}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.slice(0, 100).map((row, idx) => (
              <tr key={idx} className="border-t border-gray-700 hover:bg-gray-750">
                {Object.values(row).map((value: any, colIdx) => (
                  <td key={colIdx} className="px-4 py-3 text-sm text-gray-300">
                    {value}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
        {data.length > 100 && (
          <div className="px-4 py-2 text-sm text-gray-400 bg-gray-750">
            Showing first 100 of {data.length} rows
          </div>
        )}
      </div>
    </div>
  );
};

export default DataVisualization;


