import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Grid,
  Box,
  LinearProgress,
  Chip,
} from '@mui/material';
import {
  Speed,
  Timer,
  TrendingUp,
  Security,
} from '@mui/icons-material';

interface RealtimeMetricsProps {
  metrics: {
    events_processed: number;
    events_per_second: number;
    avg_processing_time: number;
    alerts_generated: number;
    uptime: number;
  };
}

const RealtimeMetrics: React.FC<RealtimeMetricsProps> = ({ metrics }) => {
  const formatUptime = (seconds: number): string => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    return `${hours}h ${minutes}m`;
  };

  const getPerformanceColor = (value: number, thresholds: { good: number; warning: number }) => {
    if (value >= thresholds.good) return 'success';
    if (value >= thresholds.warning) return 'warning';
    return 'error';
  };

  const getProcessingTimeColor = (ms: number) => {
    if (ms <= 100) return 'success';
    if (ms <= 500) return 'warning';
    return 'error';
  };

  return (
    <Card sx={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
      <CardContent>
        <Typography variant="h6" sx={{ color: 'white', mb: 2, display: 'flex', alignItems: 'center' }}>
          <Speed sx={{ mr: 1 }} />
          Real-time Performance Metrics
        </Typography>
        
        <Grid container spacing={3}>
          {/* Events Processed */}
          <Grid item xs={12} sm={6} md={3}>
            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="h4" sx={{ color: 'white', fontWeight: 'bold' }}>
                {metrics.events_processed.toLocaleString()}
              </Typography>
              <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.8)' }}>
                Events Processed
              </Typography>
            </Box>
          </Grid>

          {/* Events Per Second */}
          <Grid item xs={12} sm={6} md={3}>
            <Box sx={{ textAlign: 'center' }}>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', mb: 1 }}>
                <Typography variant="h4" sx={{ color: 'white', fontWeight: 'bold' }}>
                  {metrics.events_per_second.toFixed(1)}
                </Typography>
                <Chip
                  size="small"
                  label="EPS"
                  sx={{ ml: 1, bgcolor: 'rgba(255,255,255,0.2)', color: 'white' }}
                />
              </Box>
              <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.8)' }}>
                Events Per Second
              </Typography>
              <LinearProgress
                variant="determinate"
                value={Math.min((metrics.events_per_second / 1000) * 100, 100)}
                sx={{
                  mt: 1,
                  bgcolor: 'rgba(255,255,255,0.2)',
                  '& .MuiLinearProgress-bar': {
                    bgcolor: metrics.events_per_second > 500 ? '#4caf50' : '#ff9800',
                  },
                }}
              />
            </Box>
          </Grid>

          {/* Processing Time */}
          <Grid item xs={12} sm={6} md={3}>
            <Box sx={{ textAlign: 'center' }}>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', mb: 1 }}>
                <Timer sx={{ color: 'white', mr: 1 }} />
                <Typography variant="h4" sx={{ color: 'white', fontWeight: 'bold' }}>
                  {metrics.avg_processing_time.toFixed(1)}
                </Typography>
                <Typography variant="body1" sx={{ color: 'white', ml: 0.5 }}>
                  ms
                </Typography>
              </Box>
              <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.8)' }}>
                Avg Processing Time
              </Typography>
              <Chip
                size="small"
                label={
                  metrics.avg_processing_time <= 100 ? 'Excellent' :
                  metrics.avg_processing_time <= 500 ? 'Good' : 'Needs Attention'
                }
                color={getProcessingTimeColor(metrics.avg_processing_time)}
                sx={{ mt: 1 }}
              />
            </Box>
          </Grid>

          {/* System Uptime */}
          <Grid item xs={12} sm={6} md={3}>
            <Box sx={{ textAlign: 'center' }}>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', mb: 1 }}>
                <Security sx={{ color: 'white', mr: 1 }} />
                <Typography variant="h4" sx={{ color: 'white', fontWeight: 'bold' }}>
                  {formatUptime(metrics.uptime)}
                </Typography>
              </Box>
              <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.8)' }}>
                System Uptime
              </Typography>
              <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.6)', mt: 1 }}>
                {metrics.alerts_generated} alerts generated
              </Typography>
            </Box>
          </Grid>
        </Grid>

        {/* Performance Indicators */}
        <Box sx={{ mt: 3, display: 'flex', justifyContent: 'center', gap: 2 }}>
          <Chip
            icon={<TrendingUp />}
            label={`${metrics.events_per_second > 100 ? 'High' : 'Normal'} Throughput`}
            color={metrics.events_per_second > 100 ? 'success' : 'default'}
            sx={{ bgcolor: 'rgba(255,255,255,0.1)', color: 'white' }}
          />
          
          <Chip
            icon={<Timer />}
            label={`${metrics.avg_processing_time <= 100 ? 'Fast' : 'Slow'} Response`}
            color={metrics.avg_processing_time <= 100 ? 'success' : 'warning'}
            sx={{ bgcolor: 'rgba(255,255,255,0.1)', color: 'white' }}
          />
          
          <Chip
            icon={<Security />}
            label="System Healthy"
            color="success"
            sx={{ bgcolor: 'rgba(255,255,255,0.1)', color: 'white' }}
          />
        </Box>
      </CardContent>
    </Card>
  );
};

export default RealtimeMetrics;