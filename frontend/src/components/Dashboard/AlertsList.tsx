import React from 'react';
import {
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Chip,
  Typography,
  Box,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  Warning,
  Error,
  Info,
  CheckCircle,
} from '@mui/icons-material';
import { formatDistanceToNow } from 'date-fns';

interface AlertItem {
  id: string;
  title: string;
  description: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  timestamp: string;
  user_id: string;
  risk_score: number;
  status: 'open' | 'investigating' | 'resolved';
}

interface AlertsListProps {
  alerts: AlertItem[];
  loading?: boolean;
}

const AlertsList: React.FC<AlertsListProps> = ({ alerts, loading }) => {
  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'critical':
        return <Error color="error" />;
      case 'high':
        return <Warning color="warning" />;
      case 'medium':
        return <Info color="info" />;
      case 'low':
        return <CheckCircle color="success" />;
      default:
        return <Info />;
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'error';
      case 'high':
        return 'warning';
      case 'medium':
        return 'info';
      case 'low':
        return 'success';
      default:
        return 'default';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'resolved':
        return 'success';
      case 'investigating':
        return 'warning';
      case 'open':
        return 'error';
      default:
        return 'default';
    }
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (!alerts || alerts.length === 0) {
    return (
      <Alert severity="info">
        No recent alerts found. System is operating normally.
      </Alert>
    );
  }

  return (
    <List sx={{ maxHeight: 300, overflow: 'auto' }}>
      {alerts.map((alert) => (
        <ListItem
          key={alert.id}
          sx={{
            border: '1px solid',
            borderColor: 'divider',
            borderRadius: 1,
            mb: 1,
            '&:hover': {
              bgcolor: 'action.hover',
            },
          }}
        >
          <ListItemIcon>
            {getSeverityIcon(alert.severity)}
          </ListItemIcon>
          
          <ListItemText
            primary={
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 0.5 }}>
                <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                  {alert.title}
                </Typography>
                <Chip
                  label={alert.severity.toUpperCase()}
                  size="small"
                  color={getSeverityColor(alert.severity) as any}
                  variant="outlined"
                />
                <Chip
                  label={alert.status.toUpperCase()}
                  size="small"
                  color={getStatusColor(alert.status) as any}
                  variant="filled"
                />
              </Box>
            }
            secondary={
              <Box>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 0.5 }}>
                  {alert.description}
                </Typography>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Typography variant="caption" color="text.secondary">
                    User: {alert.user_id} • Risk: {alert.risk_score}/100
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {formatDistanceToNow(new Date(alert.timestamp), { addSuffix: true })}
                  </Typography>
                </Box>
              </Box>
            }
          />
        </ListItem>
      ))}
    </List>
  );
};

export default AlertsList;