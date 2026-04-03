import React, { useState } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  TextField,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  Avatar,
  LinearProgress,
  Tabs,
  Tab,
} from '@mui/material';
import {
  Person,
  TrendingUp,
  LocationOn,
  Devices,
  Schedule,
  Security,
} from '@mui/icons-material';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
} from 'recharts';

const UserAnalytics: React.FC = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [selectedUser, setSelectedUser] = useState('john.doe');

  // Mock user data
  const users = [
    {
      id: 'john.doe',
      name: 'John Doe',
      email: 'john.doe@company.com',
      department: 'Engineering',
      riskScore: 85,
      lastActivity: '2026-01-09T16:30:00Z',
      totalActivities: 1250,
      alertCount: 8,
      status: 'High Risk',
    },
    {
      id: 'jane.smith',
      name: 'Jane Smith',
      email: 'jane.smith@company.com',
      department: 'Marketing',
      riskScore: 25,
      lastActivity: '2026-01-09T15:45:00Z',
      totalActivities: 890,
      alertCount: 2,
      status: 'Normal',
    },
    {
      id: 'mike.wilson',
      name: 'Mike Wilson',
      email: 'mike.wilson@company.com',
      department: 'Finance',
      riskScore: 65,
      lastActivity: '2026-01-09T14:20:00Z',
      totalActivities: 720,
      alertCount: 5,
      status: 'Medium Risk',
    },
  ];

  const selectedUserData = users.find(u => u.id === selectedUser) || users[0];

  // Mock analytics data
  const activityData = [
    { hour: '00', activities: 2 },
    { hour: '01', activities: 1 },
    { hour: '02', activities: 0 },
    { hour: '03', activities: 8 }, // Suspicious spike
    { hour: '04', activities: 1 },
    { hour: '05', activities: 3 },
    { hour: '06', activities: 15 },
    { hour: '07', activities: 25 },
    { hour: '08', activities: 45 },
    { hour: '09', activities: 65 },
    { hour: '10', activities: 55 },
    { hour: '11', activities: 48 },
    { hour: '12', activities: 35 },
    { hour: '13', activities: 42 },
    { hour: '14', activities: 58 },
    { hour: '15', activities: 52 },
    { hour: '16', activities: 38 },
    { hour: '17', activities: 28 },
    { hour: '18', activities: 15 },
    { hour: '19', activities: 8 },
    { hour: '20', activities: 5 },
    { hour: '21', activities: 3 },
    { hour: '22', activities: 2 },
    { hour: '23', activities: 1 },
  ];

  const locationData = [
    { name: 'New York', value: 65, color: '#8884d8' },
    { name: 'Moscow', value: 25, color: '#ff4444' }, // Suspicious
    { name: 'London', value: 8, color: '#82ca9d' },
    { name: 'Tokyo', value: 2, color: '#ffc658' },
  ];

  const deviceData = [
    { name: 'Laptop', value: 70, color: '#8884d8' },
    { name: 'Mobile', value: 20, color: '#82ca9d' },
    { name: 'Unknown', value: 10, color: '#ff4444' }, // Suspicious
  ];

  const riskTrendData = [
    { date: '2026-01-03', risk: 20 },
    { date: '2026-01-04', risk: 25 },
    { date: '2026-01-05', risk: 30 },
    { date: '2026-01-06', risk: 45 },
    { date: '2026-01-07', risk: 65 },
    { date: '2026-01-08', risk: 75 },
    { date: '2026-01-09', risk: 85 },
  ];

  const getRiskColor = (score: number) => {
    if (score >= 70) return 'error';
    if (score >= 40) return 'warning';
    return 'success';
  };

  const getRiskLevel = (score: number) => {
    if (score >= 70) return 'High Risk';
    if (score >= 40) return 'Medium Risk';
    return 'Low Risk';
  };

  return (
    <Box>
      {/* Header */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="h4" component="h1" sx={{ fontWeight: 600, mb: 1 }}>
          User Analytics
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Analyze user behavior patterns and identify potential security risks
        </Typography>
      </Box>

      {/* User Selection */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} md={6}>
              <TextField
                select
                fullWidth
                label="Select User"
                value={selectedUser}
                onChange={(e) => setSelectedUser(e.target.value)}
                SelectProps={{ native: true }}
              >
                {users.map((user) => (
                  <option key={user.id} value={user.id}>
                    {user.name} ({user.id})
                  </option>
                ))}
              </TextField>
            </Grid>
            <Grid item xs={12} md={6}>
              <Button variant="contained" fullWidth>
                Generate User Report
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* User Overview */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Avatar sx={{ width: 64, height: 64, mr: 2, bgcolor: 'primary.main' }}>
                  {selectedUserData.name.split(' ').map(n => n[0]).join('')}
                </Avatar>
                <Box>
                  <Typography variant="h5" sx={{ fontWeight: 600 }}>
                    {selectedUserData.name}
                  </Typography>
                  <Typography variant="body1" color="text.secondary">
                    {selectedUserData.email}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {selectedUserData.department} Department
                  </Typography>
                </Box>
              </Box>
              
              <Grid container spacing={2}>
                <Grid item xs={6} sm={3}>
                  <Typography variant="body2" color="text.secondary">
                    Risk Score
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                    <Typography variant="h6" sx={{ mr: 1 }}>
                      {selectedUserData.riskScore}/100
                    </Typography>
                    <Chip
                      label={getRiskLevel(selectedUserData.riskScore)}
                      size="small"
                      color={getRiskColor(selectedUserData.riskScore) as any}
                      variant="filled"
                    />
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={selectedUserData.riskScore}
                    color={getRiskColor(selectedUserData.riskScore) as any}
                    sx={{ mt: 1 }}
                  />
                </Grid>
                <Grid item xs={6} sm={3}>
                  <Typography variant="body2" color="text.secondary">
                    Total Activities
                  </Typography>
                  <Typography variant="h6" sx={{ mt: 1 }}>
                    {selectedUserData.totalActivities.toLocaleString()}
                  </Typography>
                </Grid>
                <Grid item xs={6} sm={3}>
                  <Typography variant="body2" color="text.secondary">
                    Active Alerts
                  </Typography>
                  <Typography variant="h6" sx={{ mt: 1, color: 'error.main' }}>
                    {selectedUserData.alertCount}
                  </Typography>
                </Grid>
                <Grid item xs={6} sm={3}>
                  <Typography variant="body2" color="text.secondary">
                    Last Activity
                  </Typography>
                  <Typography variant="body1" sx={{ mt: 1 }}>
                    {new Date(selectedUserData.lastActivity).toLocaleTimeString()}
                  </Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2 }}>
                🚨 Recent Alerts
              </Typography>
              
              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="error.main">
                  Suspicious Login from Moscow
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  2 hours ago
                </Typography>
              </Box>
              
              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="warning.main">
                  Off-hours Database Access
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  1 day ago
                </Typography>
              </Box>
              
              <Box>
                <Typography variant="subtitle2" color="info.main">
                  New Device Login
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  2 days ago
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Analytics Tabs */}
      <Card>
        <CardContent>
          <Tabs value={activeTab} onChange={(_, newValue) => setActiveTab(newValue)} sx={{ mb: 3 }}>
            <Tab label="Activity Patterns" icon={<Schedule />} />
            <Tab label="Location Analysis" icon={<LocationOn />} />
            <Tab label="Device Usage" icon={<Devices />} />
            <Tab label="Risk Trends" icon={<TrendingUp />} />
          </Tabs>

          {/* Activity Patterns Tab */}
          {activeTab === 0 && (
            <Box>
              <Typography variant="h6" sx={{ mb: 2 }}>
                📊 24-Hour Activity Pattern
              </Typography>
              <Box sx={{ height: 300 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={activityData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="hour" />
                    <YAxis />
                    <Tooltip />
                    <Bar
                      dataKey="activities"
                      fill="#8884d8"
                      radius={[4, 4, 0, 0]}
                    />
                  </BarChart>
                </ResponsiveContainer>
              </Box>
              <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
                ⚠️ Unusual activity spike detected at 3 AM - potential security concern
              </Typography>
            </Box>
          )}

          {/* Location Analysis Tab */}
          {activeTab === 1 && (
            <Box>
              <Typography variant="h6" sx={{ mb: 2 }}>
                🌍 Login Locations
              </Typography>
              <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                  <Box sx={{ height: 300 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={locationData}
                          cx="50%"
                          cy="50%"
                          outerRadius={80}
                          dataKey="value"
                          label={({ name, value }) => `${name}: ${value}%`}
                        >
                          {locationData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.color} />
                          ))}
                        </Pie>
                        <Tooltip />
                      </PieChart>
                    </ResponsiveContainer>
                  </Box>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" sx={{ mb: 2 }}>
                    Location Risk Assessment
                  </Typography>
                  {locationData.map((location) => (
                    <Box key={location.name} sx={{ mb: 2 }}>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                        <Typography variant="body2">{location.name}</Typography>
                        <Typography variant="body2">{location.value}%</Typography>
                      </Box>
                      <LinearProgress
                        variant="determinate"
                        value={location.value}
                        sx={{
                          '& .MuiLinearProgress-bar': {
                            bgcolor: location.color,
                          },
                        }}
                      />
                      {location.name === 'Moscow' && (
                        <Typography variant="caption" color="error.main">
                          ⚠️ High-risk location
                        </Typography>
                      )}
                    </Box>
                  ))}
                </Grid>
              </Grid>
            </Box>
          )}

          {/* Device Usage Tab */}
          {activeTab === 2 && (
            <Box>
              <Typography variant="h6" sx={{ mb: 2 }}>
                💻 Device Usage Distribution
              </Typography>
              <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                  <Box sx={{ height: 300 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={deviceData}
                          cx="50%"
                          cy="50%"
                          outerRadius={80}
                          dataKey="value"
                          label={({ name, value }) => `${name}: ${value}%`}
                        >
                          {deviceData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.color} />
                          ))}
                        </Pie>
                        <Tooltip />
                      </PieChart>
                    </ResponsiveContainer>
                  </Box>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" sx={{ mb: 2 }}>
                    Device Security Status
                  </Typography>
                  {deviceData.map((device) => (
                    <Box key={device.name} sx={{ mb: 2 }}>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                        <Typography variant="body2">{device.name}</Typography>
                        <Typography variant="body2">{device.value}%</Typography>
                      </Box>
                      <LinearProgress
                        variant="determinate"
                        value={device.value}
                        sx={{
                          '& .MuiLinearProgress-bar': {
                            bgcolor: device.color,
                          },
                        }}
                      />
                      {device.name === 'Unknown' && (
                        <Typography variant="caption" color="error.main">
                          ⚠️ Unrecognized devices detected
                        </Typography>
                      )}
                    </Box>
                  ))}
                </Grid>
              </Grid>
            </Box>
          )}

          {/* Risk Trends Tab */}
          {activeTab === 3 && (
            <Box>
              <Typography variant="h6" sx={{ mb: 2 }}>
                📈 Risk Score Trend (7 Days)
              </Typography>
              <Box sx={{ height: 300 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={riskTrendData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis domain={[0, 100]} />
                    <Tooltip />
                    <Line
                      type="monotone"
                      dataKey="risk"
                      stroke="#ff4444"
                      strokeWidth={3}
                      dot={{ fill: '#ff4444', strokeWidth: 2, r: 6 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </Box>
              <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
                📊 Risk score has increased significantly over the past week - requires immediate attention
              </Typography>
            </Box>
          )}
        </CardContent>
      </Card>
    </Box>
  );
};

export default UserAnalytics;