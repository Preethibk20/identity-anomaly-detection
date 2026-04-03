import React, { useState } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Button,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  FormControl,
  InputLabel,
  Select,
  Tabs,
  Tab,
} from '@mui/material';
import {
  Visibility,
  Edit,
  CheckCircle,
  Warning,
  Error,
  Info,
  FilterList,
} from '@mui/icons-material';
import { formatDistanceToNow } from 'date-fns';

interface Alert {
  id: string;
  title: string;
  description: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  status: 'open' | 'investigating' | 'resolved' | 'false_positive';
  timestamp: string;
  user_id: string;
  risk_score: number;
  assigned_to?: string;
}

const AlertsPage: React.FC = () => {
  const [selectedAlert, setSelectedAlert] = useState<Alert | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [activeTab, setActiveTab] = useState(0);
  const [statusFilter, setStatusFilter] = useState('all');
  const [severityFilter, setSeverityFilter] = useState('all');

  // Mock data
  const alerts: Alert[] = [
    {
      id: 'alert-001',
      title: 'Suspicious Login from Moscow',
      description: 'User john.doe logged in from unusual location at 3 AM',
      severity: 'high',
      status: 'open',
      timestamp: new Date(Date.now() - 1800000).toISOString(),
      user_id: 'john.doe',
      risk_score: 85,
    },
    {
      id: 'alert-002',
      title: 'Multiple Failed Login Attempts',
      description: 'User jane.smith had 5 failed login attempts in 2 minutes',
      severity: 'medium',
      status: 'investigating',
      timestamp: new Date(Date.now() - 3600000).toISOString(),
      user_id: 'jane.smith',
      risk_score: 65,
      assigned_to: 'analyst1',
    },
    {
      id: 'alert-003',
      title: 'Impossible Travel Detected',
      description: 'User mike.wilson appeared in Tokyo 30 minutes after New York login',
      severity: 'critical',
      status: 'open',
      timestamp: new Date(Date.now() - 7200000).toISOString(),
      user_id: 'mike.wilson',
      risk_score: 95,
    },
    {
      id: 'alert-004',
      title: 'Off-hours Database Access',
      description: 'User sarah.connor accessed sensitive database at 2 AM',
      severity: 'medium',
      status: 'resolved',
      timestamp: new Date(Date.now() - 86400000).toISOString(),
      user_id: 'sarah.connor',
      risk_score: 55,
      assigned_to: 'analyst2',
    },
  ];

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
      case 'false_positive':
        return 'default';
      default:
        return 'default';
    }
  };

  const handleViewAlert = (alert: Alert) => {
    setSelectedAlert(alert);
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setSelectedAlert(null);
  };

  const filteredAlerts = alerts.filter(alert => {
    const statusMatch = statusFilter === 'all' || alert.status === statusFilter;
    const severityMatch = severityFilter === 'all' || alert.severity === severityFilter;
    return statusMatch && severityMatch;
  });

  const alertsByStatus = {
    open: alerts.filter(a => a.status === 'open').length,
    investigating: alerts.filter(a => a.status === 'investigating').length,
    resolved: alerts.filter(a => a.status === 'resolved').length,
    false_positive: alerts.filter(a => a.status === 'false_positive').length,
  };

  return (
    <Box>
      {/* Header */}
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h4" component="h1" sx={{ fontWeight: 600 }}>
          Security Alerts
        </Typography>
        <Button variant="contained" startIcon={<FilterList />}>
          Advanced Filters
        </Button>
      </Box>

      {/* Alert Summary Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ bgcolor: 'error.dark', color: 'error.contrastText' }}>
            <CardContent>
              <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
                {alertsByStatus.open}
              </Typography>
              <Typography variant="body2">Open Alerts</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ bgcolor: 'warning.dark', color: 'warning.contrastText' }}>
            <CardContent>
              <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
                {alertsByStatus.investigating}
              </Typography>
              <Typography variant="body2">Investigating</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ bgcolor: 'success.dark', color: 'success.contrastText' }}>
            <CardContent>
              <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
                {alertsByStatus.resolved}
              </Typography>
              <Typography variant="body2">Resolved</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ bgcolor: 'info.dark', color: 'info.contrastText' }}>
            <CardContent>
              <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
                {alerts.length}
              </Typography>
              <Typography variant="body2">Total Alerts</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Filters */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} sm={4}>
              <FormControl fullWidth size="small">
                <InputLabel>Status</InputLabel>
                <Select
                  value={statusFilter}
                  label="Status"
                  onChange={(e) => setStatusFilter(e.target.value)}
                >
                  <MenuItem value="all">All Statuses</MenuItem>
                  <MenuItem value="open">Open</MenuItem>
                  <MenuItem value="investigating">Investigating</MenuItem>
                  <MenuItem value="resolved">Resolved</MenuItem>
                  <MenuItem value="false_positive">False Positive</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={4}>
              <FormControl fullWidth size="small">
                <InputLabel>Severity</InputLabel>
                <Select
                  value={severityFilter}
                  label="Severity"
                  onChange={(e) => setSeverityFilter(e.target.value)}
                >
                  <MenuItem value="all">All Severities</MenuItem>
                  <MenuItem value="critical">Critical</MenuItem>
                  <MenuItem value="high">High</MenuItem>
                  <MenuItem value="medium">Medium</MenuItem>
                  <MenuItem value="low">Low</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={4}>
              <Button variant="outlined" fullWidth>
                Clear Filters
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Alerts Table */}
      <Card>
        <CardContent>
          <TableContainer component={Paper} elevation={0}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Alert</TableCell>
                  <TableCell>User</TableCell>
                  <TableCell>Severity</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Risk Score</TableCell>
                  <TableCell>Time</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {filteredAlerts.map((alert) => (
                  <TableRow key={alert.id} hover>
                    <TableCell>
                      <Box>
                        <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                          {alert.title}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          {alert.description}
                        </Typography>
                      </Box>
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2" sx={{ fontFamily: 'monospace' }}>
                        {alert.user_id}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Chip
                        icon={getSeverityIcon(alert.severity)}
                        label={alert.severity.toUpperCase()}
                        size="small"
                        color={getSeverityColor(alert.severity) as any}
                        variant="outlined"
                      />
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={alert.status.replace('_', ' ').toUpperCase()}
                        size="small"
                        color={getStatusColor(alert.status) as any}
                        variant="filled"
                      />
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2" sx={{ fontWeight: 600 }}>
                        {alert.risk_score}/100
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2">
                        {formatDistanceToNow(new Date(alert.timestamp), { addSuffix: true })}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <IconButton
                        size="small"
                        onClick={() => handleViewAlert(alert)}
                        color="primary"
                      >
                        <Visibility />
                      </IconButton>
                      <IconButton size="small" color="secondary">
                        <Edit />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>

      {/* Alert Detail Dialog */}
      <Dialog
        open={dialogOpen}
        onClose={handleCloseDialog}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          Alert Details: {selectedAlert?.title}
        </DialogTitle>
        <DialogContent>
          {selectedAlert && (
            <Box sx={{ mt: 2 }}>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <Typography variant="subtitle2" color="text.secondary">
                    Alert ID
                  </Typography>
                  <Typography variant="body1" sx={{ fontFamily: 'monospace', mb: 2 }}>
                    {selectedAlert.id}
                  </Typography>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Typography variant="subtitle2" color="text.secondary">
                    User ID
                  </Typography>
                  <Typography variant="body1" sx={{ fontFamily: 'monospace', mb: 2 }}>
                    {selectedAlert.user_id}
                  </Typography>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Typography variant="subtitle2" color="text.secondary">
                    Severity
                  </Typography>
                  <Chip
                    icon={getSeverityIcon(selectedAlert.severity)}
                    label={selectedAlert.severity.toUpperCase()}
                    color={getSeverityColor(selectedAlert.severity) as any}
                    variant="outlined"
                    sx={{ mb: 2 }}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Typography variant="subtitle2" color="text.secondary">
                    Risk Score
                  </Typography>
                  <Typography variant="h6" sx={{ mb: 2 }}>
                    {selectedAlert.risk_score}/100
                  </Typography>
                </Grid>
                <Grid item xs={12}>
                  <Typography variant="subtitle2" color="text.secondary">
                    Description
                  </Typography>
                  <Typography variant="body1" sx={{ mb: 2 }}>
                    {selectedAlert.description}
                  </Typography>
                </Grid>
                <Grid item xs={12}>
                  <Typography variant="subtitle2" color="text.secondary">
                    Timestamp
                  </Typography>
                  <Typography variant="body1">
                    {new Date(selectedAlert.timestamp).toLocaleString()}
                  </Typography>
                </Grid>
              </Grid>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Close</Button>
          <Button variant="contained" color="warning">
            Assign to Me
          </Button>
          <Button variant="contained" color="success">
            Mark Resolved
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default AlertsPage;