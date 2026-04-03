import React from 'react';
import {
  Box,
  Typography,
  LinearProgress,
  Chip,
  Grid,
  Divider,
} from '@mui/material';
import {
  Memory,
  Storage,
  Speed,
  NetworkCheck,
  Security,
  CheckCircle,
  Warning,
  Error,
} from '@mui/icons-material';

interface SystemHealthProps {
  metrics?: {
    totalUsers?: number;
    eventsProcessed?: number;
    eventsPerSecond?: number;
    avgProcessingTime?: number;
    systemUptime?: number;
  };
}

const SystemHealth: React.FC<SystemHealthProps> = ({ metrics }) => {
  // Generate sample system health data
  const systemHealth = {
    cpu: 45,
    memory: 62,
    disk: 38,
    network: 85,
    database: 92,
    mlEngine: 88,
    alertEngine: 95,
    apiGateway: 90,
  };

  const getHealthColor = (value: number) => {
    if (value >= 90) return 'success';
    if (value >= 70) return 'warning';
    return 'error';
  };

  const getHealthIcon = (value: number) => {
    if (value >= 90) return <CheckCircle color="success" />;
    if (value >= 70) return <Warning color="warning" />;
    return <Error color="error" />;
  };

  const getHealthStatus = (value: number) => {
    if (value >= 90) return 'Healthy';
    if (value >= 70) return 'Warning';
    return 'Critical';
  };

  const HealthMetric: React.FC<{
    label: string;
    value: number;
    icon: React.ReactNode;
  }> = ({ label, value, icon }) => (
    <Box sx={{ mb: 2 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 1 }}>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          {icon}
          <Typography variant="body2" sx={{ ml: 1 }}>
            {label}
          </Typography>
        </Box>
        <Chip
          label={`${value}%`}
          size="small"
          color={getHealthColor(value) as any}
          variant="outlined"
        />
      </Box>
      <LinearProgress
        variant="determinate"
        value={value}
        sx={{
          height: 6,
          borderRadius: 3,
          bgcolor: 'action.hover',
          '& .MuiLinearProgress-bar': {
            borderRadius: 3,
            bgcolor: value >= 90 ? 'success.main' : value >= 70 ? 'warning.main' : 'error.main',
          },
        }}
      />
    </Box>
  );

  return (
    <Box sx={{ height: '100%' }}>
      {/* Overall System Status */}
      <Box sx={{ mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
          <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center' }}>
            <Security sx={{ mr: 1 }} />
            System Status
          </Typography>
          <Chip
            icon={<CheckCircle />}
            label="Operational"
            color="success"
            variant="filled"
          />
        </Box>
        
        <Grid container spacing={2} sx={{ mb: 2 }}>
          <Grid item xs={6}>
            <Typography variant="body2" color="text.secondary">
              Uptime
            </Typography>
            <Typography variant="h6">
              {metrics?.systemUptime ? `${Math.floor(metrics.systemUptime / 3600)}h ${Math.floor((metrics.systemUptime % 3600) / 60)}m` : '24h 15m'}
            </Typography>
          </Grid>
          <Grid item xs={6}>
            <Typography variant="body2" color="text.secondary">
              Events/sec
            </Typography>
            <Typography variant="h6">
              {metrics?.eventsPerSecond?.toFixed(1) || '125.3'}
            </Typography>
          </Grid>
        </Grid>
      </Box>

      <Divider sx={{ mb: 2 }} />

      {/* Infrastructure Health */}
      <Typography variant="subtitle2" sx={{ mb: 2, fontWeight: 600 }}>
        Infrastructure
      </Typography>
      
      <HealthMetric
        label="CPU Usage"
        value={systemHealth.cpu}
        icon={<Speed fontSize="small" />}
      />
      
      <HealthMetric
        label="Memory Usage"
        value={systemHealth.memory}
        icon={<Memory fontSize="small" />}
      />
      
      <HealthMetric
        label="Disk Usage"
        value={systemHealth.disk}
        icon={<Storage fontSize="small" />}
      />
      
      <HealthMetric
        label="Network"
        value={systemHealth.network}
        icon={<NetworkCheck fontSize="small" />}
      />

      <Divider sx={{ my: 2 }} />

      {/* Service Health */}
      <Typography variant="subtitle2" sx={{ mb: 2, fontWeight: 600 }}>
        Services
      </Typography>
      
      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
        {[
          { name: 'Database', health: systemHealth.database },
          { name: 'ML Engine', health: systemHealth.mlEngine },
          { name: 'Alert Engine', health: systemHealth.alertEngine },
          { name: 'API Gateway', health: systemHealth.apiGateway },
        ].map((service) => (
          <Box
            key={service.name}
            sx={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              p: 1,
              border: '1px solid',
              borderColor: 'divider',
              borderRadius: 1,
            }}
          >
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              {getHealthIcon(service.health)}
              <Typography variant="body2" sx={{ ml: 1 }}>
                {service.name}
              </Typography>
            </Box>
            <Typography variant="caption" color="text.secondary">
              {getHealthStatus(service.health)}
            </Typography>
          </Box>
        ))}
      </Box>

      {/* Performance Metrics */}
      <Divider sx={{ my: 2 }} />
      
      <Typography variant="subtitle2" sx={{ mb: 2, fontWeight: 600 }}>
        Performance
      </Typography>
      
      <Grid container spacing={2}>
        <Grid item xs={6}>
          <Typography variant="caption" color="text.secondary">
            Avg Response
          </Typography>
          <Typography variant="body2" sx={{ fontWeight: 600 }}>
            {metrics?.avgProcessingTime?.toFixed(1) || '85.2'}ms
          </Typography>
        </Grid>
        <Grid item xs={6}>
          <Typography variant="caption" color="text.secondary">
            Total Events
          </Typography>
          <Typography variant="body2" sx={{ fontWeight: 600 }}>
            {metrics?.eventsProcessed?.toLocaleString() || '1,245,678'}
          </Typography>
        </Grid>
      </Grid>
    </Box>
  );
};

export default SystemHealth;