import React, { useState, useEffect } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Area,
  AreaChart,
} from 'recharts';
import { Box, Typography, ToggleButton, ToggleButtonGroup } from '@mui/material';
import { useQuery } from 'react-query';
import { ApiService } from '../../services/ApiService';

interface RiskDataPoint {
  timestamp: string;
  avgRiskScore: number;
  alertCount: number;
  criticalAlerts: number;
  highAlerts: number;
  mediumAlerts: number;
  lowAlerts: number;
}

const RiskTrendsChart: React.FC = () => {
  const [timeRange, setTimeRange] = useState<'1h' | '6h' | '24h' | '7d'>('24h');
  const [chartType, setChartType] = useState<'line' | 'area'>('area');

  const { data: riskData, isLoading } = useQuery<RiskDataPoint[]>(
    ['risk-trends', timeRange],
    () => ApiService.getRiskTrends(timeRange),
    {
      refetchInterval: 60000, // Refresh every minute
    }
  );

  // Generate sample data if API data is not available
  const generateSampleData = (): RiskDataPoint[] => {
    const now = new Date();
    const data: RiskDataPoint[] = [];
    const points = timeRange === '1h' ? 12 : timeRange === '6h' ? 24 : timeRange === '24h' ? 48 : 168;
    const interval = timeRange === '1h' ? 5 : timeRange === '6h' ? 15 : timeRange === '24h' ? 30 : 60;

    for (let i = points; i >= 0; i--) {
      const timestamp = new Date(now.getTime() - i * interval * 60000);
      const baseRisk = 30 + Math.sin(i * 0.1) * 20 + Math.random() * 15;
      
      data.push({
        timestamp: timestamp.toISOString(),
        avgRiskScore: Math.max(0, Math.min(100, baseRisk)),
        alertCount: Math.floor(Math.random() * 10) + 1,
        criticalAlerts: Math.floor(Math.random() * 3),
        highAlerts: Math.floor(Math.random() * 5) + 1,
        mediumAlerts: Math.floor(Math.random() * 8) + 2,
        lowAlerts: Math.floor(Math.random() * 12) + 3,
      });
    }

    return data;
  };

  const chartData = riskData || generateSampleData();

  const formatXAxisLabel = (tickItem: string) => {
    const date = new Date(tickItem);
    if (timeRange === '1h' || timeRange === '6h') {
      return date.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit' 
      });
    } else if (timeRange === '24h') {
      return date.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit' 
      });
    } else {
      return date.toLocaleDateString('en-US', { 
        month: 'short', 
        day: 'numeric' 
      });
    }
  };

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <Box
          sx={{
            bgcolor: 'background.paper',
            p: 2,
            border: '1px solid',
            borderColor: 'divider',
            borderRadius: 1,
            boxShadow: 2,
          }}
        >
          <Typography variant="subtitle2" sx={{ mb: 1 }}>
            {new Date(label).toLocaleString()}
          </Typography>
          <Typography variant="body2" color="primary">
            Avg Risk Score: {data.avgRiskScore.toFixed(1)}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Total Alerts: {data.alertCount}
          </Typography>
          <Box sx={{ mt: 1 }}>
            <Typography variant="caption" color="error.main">
              Critical: {data.criticalAlerts}
            </Typography>
            <Typography variant="caption" color="warning.main" sx={{ ml: 1 }}>
              High: {data.highAlerts}
            </Typography>
            <Typography variant="caption" color="info.main" sx={{ ml: 1 }}>
              Medium: {data.mediumAlerts}
            </Typography>
            <Typography variant="caption" color="success.main" sx={{ ml: 1 }}>
              Low: {data.lowAlerts}
            </Typography>
          </Box>
        </Box>
      );
    }
    return null;
  };

  return (
    <Box sx={{ height: '100%' }}>
      {/* Controls */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
        <ToggleButtonGroup
          value={timeRange}
          exclusive
          onChange={(_, newRange) => newRange && setTimeRange(newRange)}
          size="small"
        >
          <ToggleButton value="1h">1H</ToggleButton>
          <ToggleButton value="6h">6H</ToggleButton>
          <ToggleButton value="24h">24H</ToggleButton>
          <ToggleButton value="7d">7D</ToggleButton>
        </ToggleButtonGroup>

        <ToggleButtonGroup
          value={chartType}
          exclusive
          onChange={(_, newType) => newType && setChartType(newType)}
          size="small"
        >
          <ToggleButton value="line">Line</ToggleButton>
          <ToggleButton value="area">Area</ToggleButton>
        </ToggleButtonGroup>
      </Box>

      {/* Chart */}
      <Box sx={{ height: 280 }}>
        <ResponsiveContainer width="100%" height="100%">
          {chartType === 'area' ? (
            <AreaChart data={chartData}>
              <defs>
                <linearGradient id="riskGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#667eea" stopOpacity={0.8} />
                  <stop offset="95%" stopColor="#667eea" stopOpacity={0.1} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis
                dataKey="timestamp"
                tickFormatter={formatXAxisLabel}
                stroke="#9CA3AF"
                fontSize={12}
              />
              <YAxis
                domain={[0, 100]}
                stroke="#9CA3AF"
                fontSize={12}
              />
              <Tooltip content={<CustomTooltip />} />
              <Area
                type="monotone"
                dataKey="avgRiskScore"
                stroke="#667eea"
                strokeWidth={2}
                fill="url(#riskGradient)"
              />
            </AreaChart>
          ) : (
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis
                dataKey="timestamp"
                tickFormatter={formatXAxisLabel}
                stroke="#9CA3AF"
                fontSize={12}
              />
              <YAxis
                domain={[0, 100]}
                stroke="#9CA3AF"
                fontSize={12}
              />
              <Tooltip content={<CustomTooltip />} />
              <Line
                type="monotone"
                dataKey="avgRiskScore"
                stroke="#667eea"
                strokeWidth={2}
                dot={{ fill: '#667eea', strokeWidth: 2, r: 4 }}
                activeDot={{ r: 6, stroke: '#667eea', strokeWidth: 2 }}
              />
            </LineChart>
          )}
        </ResponsiveContainer>
      </Box>
    </Box>
  );
};

export default RiskTrendsChart;