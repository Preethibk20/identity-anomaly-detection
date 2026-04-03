import React, { useState } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
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
} from '@mui/material';
import {
  Assessment,
  Download,
  Visibility,
  Add,
  Schedule,
  PictureAsPdf,
  TableChart,
} from '@mui/icons-material';

const Reports: React.FC = () => {
  const [dialogOpen, setDialogOpen] = useState(false);
  const [reportType, setReportType] = useState('');
  const [timeRange, setTimeRange] = useState('');

  // Mock reports data
  const reports = [
    {
      id: 'report-001',
      name: 'Weekly Security Summary',
      type: 'Security Summary',
      status: 'Completed',
      createdAt: '2026-01-09T10:00:00Z',
      size: '2.3 MB',
      format: 'PDF',
      description: 'Comprehensive weekly security overview with key metrics and trends',
    },
    {
      id: 'report-002',
      name: 'User Risk Assessment',
      type: 'Risk Assessment',
      status: 'Completed',
      createdAt: '2026-01-08T15:30:00Z',
      size: '1.8 MB',
      format: 'Excel',
      description: 'Detailed analysis of user risk scores and behavioral patterns',
    },
    {
      id: 'report-003',
      name: 'Threat Intelligence Digest',
      type: 'Threat Intelligence',
      status: 'In Progress',
      createdAt: '2026-01-09T14:00:00Z',
      size: '-',
      format: 'PDF',
      description: 'Latest threat intelligence findings and IOCs',
    },
    {
      id: 'report-004',
      name: 'Compliance Audit Report',
      type: 'Compliance',
      status: 'Completed',
      createdAt: '2026-01-07T09:00:00Z',
      size: '4.1 MB',
      format: 'PDF',
      description: 'SOX compliance audit results and recommendations',
    },
  ];

  const reportTemplates = [
    {
      name: 'Security Summary',
      description: 'Overview of security metrics, alerts, and system health',
      icon: <Assessment />,
    },
    {
      name: 'Risk Assessment',
      description: 'User risk analysis and behavioral anomaly detection',
      icon: <Assessment />,
    },
    {
      name: 'Threat Intelligence',
      description: 'Latest threat indicators and security intelligence',
      icon: <Assessment />,
    },
    {
      name: 'Compliance Audit',
      description: 'Regulatory compliance status and audit findings',
      icon: <Assessment />,
    },
    {
      name: 'Incident Response',
      description: 'Security incident analysis and response metrics',
      icon: <Assessment />,
    },
    {
      name: 'Executive Dashboard',
      description: 'High-level security metrics for executive leadership',
      icon: <Assessment />,
    },
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Completed':
        return 'success';
      case 'In Progress':
        return 'warning';
      case 'Failed':
        return 'error';
      default:
        return 'default';
    }
  };

  const getFormatIcon = (format: string) => {
    switch (format) {
      case 'PDF':
        return <PictureAsPdf />;
      case 'Excel':
        return <TableChart />;
      default:
        return <Assessment />;
    }
  };

  const handleCreateReport = () => {
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setReportType('');
    setTimeRange('');
  };

  const handleGenerateReport = () => {
    // Mock report generation
    console.log('Generating report:', { reportType, timeRange });
    handleCloseDialog();
  };

  return (
    <Box>
      {/* Header */}
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Box>
          <Typography variant="h4" component="h1" sx={{ fontWeight: 600, mb: 1 }}>
            Security Reports
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Generate and manage security reports for compliance and analysis
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={handleCreateReport}
          size="large"
        >
          Create Report
        </Button>
      </Box>

      {/* Report Templates */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 2 }}>
            📊 Report Templates
          </Typography>
          <Grid container spacing={2}>
            {reportTemplates.map((template, index) => (
              <Grid item xs={12} sm={6} md={4} key={index}>
                <Card
                  sx={{
                    cursor: 'pointer',
                    transition: 'all 0.2s',
                    '&:hover': {
                      transform: 'translateY(-2px)',
                      boxShadow: 4,
                    },
                  }}
                  onClick={handleCreateReport}
                >
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                      {template.icon}
                      <Typography variant="subtitle1" sx={{ ml: 1, fontWeight: 600 }}>
                        {template.name}
                      </Typography>
                    </Box>
                    <Typography variant="body2" color="text.secondary">
                      {template.description}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </CardContent>
      </Card>

      {/* Recent Reports */}
      <Card>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 2 }}>
            📋 Recent Reports
          </Typography>
          <TableContainer component={Paper} elevation={0}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Report Name</TableCell>
                  <TableCell>Type</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Created</TableCell>
                  <TableCell>Size</TableCell>
                  <TableCell>Format</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {reports.map((report) => (
                  <TableRow key={report.id} hover>
                    <TableCell>
                      <Box>
                        <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                          {report.name}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          {report.description}
                        </Typography>
                      </Box>
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={report.type}
                        size="small"
                        variant="outlined"
                      />
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={report.status}
                        size="small"
                        color={getStatusColor(report.status) as any}
                        variant="filled"
                      />
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2">
                        {new Date(report.createdAt).toLocaleDateString()}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {new Date(report.createdAt).toLocaleTimeString()}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2">
                        {report.size}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        {getFormatIcon(report.format)}
                        <Typography variant="body2" sx={{ ml: 1 }}>
                          {report.format}
                        </Typography>
                      </Box>
                    </TableCell>
                    <TableCell>
                      <IconButton
                        size="small"
                        color="primary"
                        disabled={report.status !== 'Completed'}
                      >
                        <Visibility />
                      </IconButton>
                      <IconButton
                        size="small"
                        color="secondary"
                        disabled={report.status !== 'Completed'}
                      >
                        <Download />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>

      {/* Create Report Dialog */}
      <Dialog
        open={dialogOpen}
        onClose={handleCloseDialog}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>
          Create New Report
        </DialogTitle>
        <DialogContent>
          <Box sx={{ mt: 2 }}>
            <FormControl fullWidth sx={{ mb: 3 }}>
              <InputLabel>Report Type</InputLabel>
              <Select
                value={reportType}
                label="Report Type"
                onChange={(e) => setReportType(e.target.value)}
              >
                {reportTemplates.map((template, index) => (
                  <MenuItem key={index} value={template.name}>
                    {template.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <FormControl fullWidth sx={{ mb: 3 }}>
              <InputLabel>Time Range</InputLabel>
              <Select
                value={timeRange}
                label="Time Range"
                onChange={(e) => setTimeRange(e.target.value)}
              >
                <MenuItem value="last_24h">Last 24 Hours</MenuItem>
                <MenuItem value="last_7d">Last 7 Days</MenuItem>
                <MenuItem value="last_30d">Last 30 Days</MenuItem>
                <MenuItem value="last_90d">Last 90 Days</MenuItem>
                <MenuItem value="custom">Custom Range</MenuItem>
              </Select>
            </FormControl>

            <TextField
              fullWidth
              label="Report Name"
              placeholder="Enter custom report name (optional)"
              sx={{ mb: 2 }}
            />

            <TextField
              fullWidth
              label="Description"
              placeholder="Enter report description (optional)"
              multiline
              rows={3}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>
            Cancel
          </Button>
          <Button
            variant="contained"
            onClick={handleGenerateReport}
            disabled={!reportType || !timeRange}
            startIcon={<Assessment />}
          >
            Generate Report
          </Button>
        </DialogActions>
      </Dialog>

      {/* Scheduled Reports Section */}
      <Card sx={{ mt: 3 }}>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h6">
              ⏰ Scheduled Reports
            </Typography>
            <Button variant="outlined" startIcon={<Schedule />}>
              Manage Schedules
            </Button>
          </Box>
          
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6} md={4}>
              <Card variant="outlined">
                <CardContent>
                  <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 1 }}>
                    Weekly Security Summary
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    Every Monday at 9:00 AM
                  </Typography>
                  <Chip label="Active" size="small" color="success" variant="filled" />
                </CardContent>
              </Card>
            </Grid>
            
            <Grid item xs={12} sm={6} md={4}>
              <Card variant="outlined">
                <CardContent>
                  <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 1 }}>
                    Monthly Compliance Report
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    First day of each month
                  </Typography>
                  <Chip label="Active" size="small" color="success" variant="filled" />
                </CardContent>
              </Card>
            </Grid>
            
            <Grid item xs={12} sm={6} md={4}>
              <Card variant="outlined">
                <CardContent>
                  <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 1 }}>
                    Executive Dashboard
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    Daily at 8:00 AM
                  </Typography>
                  <Chip label="Paused" size="small" color="warning" variant="filled" />
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Reports;