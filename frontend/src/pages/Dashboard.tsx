import React, { useState, useEffect } from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  Button,
  Chip,
  LinearProgress,
  Alert,
} from '@mui/material';
import {
  Security,
  Warning,
  TrendingUp,
  Speed,
  People,
  Notifications,
} from '@mui/icons-material';

// Components
import MetricCard from '../components/Dashboard/MetricCard';
import AlertsList from '../components/Dashboard/AlertsList';
import RiskTrendsChart from '../components/Dashboard/RiskTrendsChart';
import UserActivityMap from '../components/Dashboard/UserActivityMap';
import ThreatIntelligence from '../components/Dashboard/ThreatIntelligence';
import SystemHealth from '../components/Dashboard/SystemHealth';
import RealtimeMetrics from '../components/Dashboard/RealtimeMetrics';

// Hooks
import { useWebSocket } from '../contexts/WebSocketContext';
import { useQuery } from 'react-query';

// Services
import { ApiService } from '../services/ApiService';

interface DashboardMetrics {
  totalUsers: number;
  activeAlerts: number;
  highRiskAlerts: number;
  criticalAlerts: number;
  eventsProcessed: number;
  eventsPerSecond: number;
  avgProcessingTime: number;
  systemUptime: number;
  threatScore: number;
  falsePositiveRate: number;
}

const Dashboard: React.FC = () => {
  const { socket, isConnected } = useWebSocket();
  const [realtimeMetrics, setRealtimeMetrics] = useState<any>(null);
  const [recentAlerts, setRecentAlerts] = useState<any[]>([]);

  // Fetch dashboard data
  const { data: metrics, isLoading: metricsLoading } = useQuery<DashboardMetrics>(
    'dashboard-metrics',
    ApiService.getDashboardMetrics,
    {
      refetchInterval: 30000, // Refresh every 30 seconds
    }
  );

  const { data: alerts, isLoading: alertsLoading } = useQuery(
    'recent-alerts',
    () => ApiService.getRecentAlerts(10),
    {
      refetchInterval: 10000, // Refresh every 10 seconds
    }
  );

  // WebSocket event handlers
  useEffect(() => {
    if (!socket) return;

    const handleMetricsUpdate = (data: any) => {
      setRealtimeMetrics(data.metrics);
    };

    const handleNewAlert = (alert: any) => {
      setRecentAlerts(prev => [alert, ...prev.slice(0, 9)]);
    };

    socket.on('metrics_update', handleMetricsUpdate);
    socket.on('new_alert', handleNewAlert);

    return () => {
      socket.off('metrics_update', handleMetricsUpdate);
      socket.off('new_alert', handleNewAlert);
    };
  }, [socket]);

  const handleSimulateAttack = async () => {
    try {
      await ApiService.simulateAttack();
    } catch (error) {
      console.error('Failed to simulate attack:', error);
    }
  };

  const handleRefreshData = async () => {
    try {
      // Trigger manual refresh of all queries
      window.location.reload();
    } catch (error) {
      console.error('Failed to refresh data:', error);
    }
  };

  if (metricsLoading) {
    return (
      <Box sx={{ width: '100%', mt: 2 }}>
        <LinearProgress />
        <Typography variant="h6" sx={{ mt: 2, textAlign: 'center' }}>
          Loading dashboard...
        </Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ flexGrow: 1 }}>
      {/* Header */}
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h4" component="h1" sx={{ fontWeight: 600 }}>
          Security Operations Center
        </Typography>
        
        <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
          <Chip
            icon={<Security />}
            label={isConnected ? 'Connected' : 'Disconnected'}
            color={isConnected ? 'success' : 'error'}
            variant="outlined"
          />
          
          <Button
            variant="contained"
            color="warning"
            onClick={handleSimulateAttack}
            startIcon={<Warning />}
          >
            Simulate Attack
          </Button>
          
          <Button
            variant="outlined"
            onClick={handleRefreshData}
            startIcon={<TrendingUp />}
          >
            Refresh Data
          </Button>
        </Box>
      </Box>

      {/* Connection Status Alert */}
      {!isConnected && (
        <Alert severity="warning" sx={{ mb: 3 }}>
          Real-time connection lost. Some features may not work properly.
        </Alert>
      )}

      {/* Key Metrics Row */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Users Monitored"
            value={metrics?.totalUsers || 0}
            icon={<People />}
            color="primary"
            trend={+2.5}
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Active Alerts"
            value={metrics?.activeAlerts || 0}
            icon={<Notifications />}
            color="warning"
            trend={-1.2}
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Critical Alerts"
            value={metrics?.criticalAlerts || 0}
            icon={<Warning />}
            color="error"
            trend={+0.8}
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Events/Second"
            value={realtimeMetrics?.events_per_second || metrics?.eventsPerSecond || 0}
            icon={<Speed />}
            color="success"
            trend={+5.3}
            format="decimal"
          />
        </Grid>
      </Grid>

      {/* Real-time Metrics */}
      {realtimeMetrics && (
        <Grid container spacing={3} sx={{ mb: 3 }}>
          <Grid item xs={12}>
            <RealtimeMetrics metrics={realtimeMetrics} />
          </Grid>
        </Grid>
      )}

      {/* Main Content Row */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        {/* Recent Alerts */}
        <Grid item xs={12} lg={6}>
          <Card sx={{ height: 400 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                🚨 Recent Security Alerts
              </Typography>
              <AlertsList 
                alerts={recentAlerts.length > 0 ? recentAlerts : alerts || []} 
                loading={alertsLoading}
              />
            </CardContent>
          </Card>
        </Grid>

        {/* Risk Trends */}
        <Grid item xs={12} lg={6}>
          <Card sx={{ height: 400 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                📊 Risk Trends
              </Typography>
              <RiskTrendsChart />
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Secondary Content Row */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        {/* User Activity Map */}
        <Grid item xs={12} lg={8}>
          <Card sx={{ height: 350 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                🌍 Global User Activity
              </Typography>
              <UserActivityMap />
            </CardContent>
          </Card>
        </Grid>

        {/* System Health */}
        <Grid item xs={12} lg={4}>
          <Card sx={{ height: 350 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                ⚡ System Health
              </Typography>
              <SystemHealth metrics={metrics} />
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Threat Intelligence Row */}
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                🔍 Threat Intelligence
              </Typography>
              <ThreatIntelligence />
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;