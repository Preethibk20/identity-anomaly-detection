import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
} from '@mui/icons-material';

interface MetricCardProps {
  title: string;
  value: number;
  icon: React.ReactNode;
  color: 'primary' | 'secondary' | 'success' | 'warning' | 'error';
  trend?: number;
  format?: 'number' | 'decimal' | 'percentage';
}

const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  icon,
  color,
  trend,
  format = 'number'
}) => {
  const formatValue = (val: number): string => {
    switch (format) {
      case 'decimal':
        return val.toFixed(1);
      case 'percentage':
        return `${val.toFixed(1)}%`;
      default:
        return val.toLocaleString();
    }
  };

  const getTrendColor = (trendValue: number) => {
    if (trendValue > 0) return 'success';
    if (trendValue < 0) return 'error';
    return 'default';
  };

  return (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
          <Box sx={{ color: `${color}.main` }}>
            {icon}
          </Box>
          {trend !== undefined && (
            <Chip
              icon={trend >= 0 ? <TrendingUp /> : <TrendingDown />}
              label={`${trend >= 0 ? '+' : ''}${trend.toFixed(1)}%`}
              size="small"
              color={getTrendColor(trend)}
              variant="outlined"
            />
          )}
        </Box>
        
        <Typography variant="h4" component="div" sx={{ fontWeight: 'bold', mb: 1 }}>
          {formatValue(value)}
        </Typography>
        
        <Typography variant="body2" color="text.secondary">
          {title}
        </Typography>
      </CardContent>
    </Card>
  );
};

export default MetricCard;