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

const COLORS = ['#588157', '#344E41', '#D4A373', '#6B9A7A', '#8FB88F', '#C5A882'];

const DataVisualization: React.FC<DataVisualizationProps> = ({ data, visualization }) => {
  if (!data || data.length === 0) {
    return (
      <div className="bg-white border border-[#DFE4DD] rounded-lg p-8 text-center text-[#344E41]">
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
      <div className="bg-white border border-[#DFE4DD] rounded-2xl p-6 shadow-sm">
        <ResponsiveContainer width="100%" height={450}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#DFE4DD" opacity={0.5} />
            <XAxis 
              dataKey={xKey} 
              stroke="#344E41" 
              tick={{ fill: '#344E41', fontSize: 12, fontWeight: 500 }}
              angle={-45}
              textAnchor="end"
              height={80}
            />
            <YAxis 
              stroke="#344E41" 
              tick={{ fill: '#344E41', fontSize: 12, fontWeight: 500 }}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#FFFFFF',
                border: '1px solid #DFE4DD',
                borderRadius: '8px',
                color: '#222',
                boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
              }}
              cursor={{ fill: 'rgba(88, 129, 87, 0.1)' }}
            />
            <Legend 
              wrapperStyle={{ color: '#222', fontSize: '13px' }}
            />
            <Bar 
              dataKey={yKey} 
              fill="url(#barGradient)"
              radius={[8, 8, 0, 0]}
            />
            <defs>
              <linearGradient id="barGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#588157" stopOpacity={1} />
                <stop offset="100%" stopColor="#344E41" stopOpacity={0.8} />
              </linearGradient>
            </defs>
          </BarChart>
        </ResponsiveContainer>
      </div>
    );
  }

  if (visualization_type === 'line') {
    return (
      <div className="bg-white border border-[#DFE4DD] rounded-2xl p-6 shadow-sm">
        <ResponsiveContainer width="100%" height={450}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#DFE4DD" opacity={0.5} />
            <XAxis 
              dataKey={xKey} 
              stroke="#344E41" 
              tick={{ fill: '#344E41', fontSize: 12, fontWeight: 500 }}
            />
            <YAxis 
              stroke="#344E41" 
              tick={{ fill: '#344E41', fontSize: 12, fontWeight: 500 }}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#FFFFFF',
                border: '1px solid #DFE4DD',
                borderRadius: '8px',
                color: '#222',
                boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
              }}
              cursor={{ stroke: '#588157', strokeWidth: 1 }}
            />
            <Legend 
              wrapperStyle={{ color: '#222', fontSize: '13px' }}
            />
            <Line 
              type="monotone" 
              dataKey={yKey} 
              stroke="#588157" 
              strokeWidth={3}
              dot={{ fill: '#588157', r: 4 }}
              activeDot={{ r: 6, fill: '#D4A373' }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    );
  }

  if (visualization_type === 'pie') {
    return (
      <div className="bg-white border border-[#DFE4DD] rounded-2xl p-6 shadow-sm">
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
                backgroundColor: '#FFFFFF',
                border: '1px solid #DFE4DD',
                borderRadius: '8px',
                color: '#222',
                boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
              }}
            />
            <Legend 
              wrapperStyle={{ color: '#222', fontSize: '13px' }}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>
    );
  }

  if (visualization_type === 'scatter') {
    return (
      <div className="bg-white border border-[#DFE4DD] rounded-2xl p-6 shadow-sm">
        <ResponsiveContainer width="100%" height={450}>
          <ScatterChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#DFE4DD" opacity={0.5} />
            <XAxis 
              dataKey={xKey} 
              stroke="#344E41" 
              tick={{ fill: '#344E41', fontSize: 12, fontWeight: 500 }}
              name={xKey}
              type="number"
            />
            <YAxis 
              stroke="#344E41" 
              tick={{ fill: '#344E41', fontSize: 12, fontWeight: 500 }}
              name={yKey}
              type="number"
            />
            <Tooltip
              cursor={{ stroke: '#588157', strokeWidth: 1 }}
              contentStyle={{
                backgroundColor: '#FFFFFF',
                border: '1px solid #DFE4DD',
                borderRadius: '8px',
                color: '#222',
                boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
              }}
            />
            <Legend 
              wrapperStyle={{ color: '#222', fontSize: '13px' }}
            />
            <Scatter 
              dataKey={yKey} 
              fill="#588157" 
              shape="circle"
            />
          </ScatterChart>
        </ResponsiveContainer>
      </div>
    );
  }

  if (visualization_type === 'area') {
    return (
      <div className="bg-white border border-[#DFE4DD] rounded-2xl p-6 shadow-sm">
        <ResponsiveContainer width="100%" height={450}>
          <AreaChart data={chartData}>
            <defs>
              <linearGradient id="areaGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#588157" stopOpacity={0.8} />
                <stop offset="95%" stopColor="#588157" stopOpacity={0.1} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#DFE4DD" opacity={0.5} />
            <XAxis 
              dataKey={xKey} 
              stroke="#344E41" 
              tick={{ fill: '#344E41', fontSize: 12, fontWeight: 500 }}
            />
            <YAxis 
              stroke="#344E41" 
              tick={{ fill: '#344E41', fontSize: 12, fontWeight: 500 }}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#FFFFFF',
                border: '1px solid #DFE4DD',
                borderRadius: '8px',
                color: '#222',
                boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
              }}
              cursor={{ stroke: '#588157', strokeWidth: 1 }}
            />
            <Legend 
              wrapperStyle={{ color: '#222', fontSize: '13px' }}
            />
            <Area 
              type="monotone" 
              dataKey={yKey} 
              stroke="#588157" 
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
    <div className="bg-white border border-[#DFE4DD] rounded-2xl overflow-hidden shadow-sm">
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-[#F8F9F5]">
            <tr>
              {Object.keys(data[0]).map((key) => (
                <th key={key} className="px-6 py-4 text-left text-sm font-semibold text-[#222] uppercase tracking-wide">
                  {key.replace(/_/g, ' ')}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.slice(0, 100).map((row, idx) => (
              <tr 
                key={idx} 
                className="border-t border-[#DFE4DD] hover:bg-[#F8F9F5] transition-colors"
              >
                {Object.values(row).map((value: any, colIdx) => (
                  <td key={colIdx} className="px-6 py-4 text-sm text-[#222]">
                    {value}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
        {data.length > 100 && (
          <div className="px-6 py-3 text-sm text-[#344E41] bg-[#F8F9F5] border-t border-[#DFE4DD]">
            Showing first 100 of {data.length} rows
          </div>
        )}
      </div>
    </div>
  );
};

export default DataVisualization;


