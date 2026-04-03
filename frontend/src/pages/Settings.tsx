import React, { useState } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Switch,
  FormControlLabel,
  TextField,
  Button,
  Divider,
  Tabs,
  Tab,
  Slider,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
} from '@mui/material';
import {
  Settings as SettingsIcon,
  Security,
  Notifications,
  Integration,
  Tune,
  Delete,
  Add,
} from '@mui/icons-material';

const Settings: React.FC = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [settings, setSettings] = useState({
    // General Settings
    realTimeUpdates: true,
    autoRefresh: true,
    refreshInterval: 30,
    darkMode: true,
    
    // Security Settings
    riskThreshold: 70,
    alertThreshold: 60,
    autoLockout: true,
    sessionTimeout: 480,
    
    // Notification Settings
    emailNotifications: true,
    slackNotifications: false,
    pushNotifications: true,
    criticalAlertsOnly: false,
    
    // ML Settings
    modelSensitivity: 75,
    autoRetrain: true,
    retrainInterval: 7,
    falsePositiveThreshold: 5,
  });

  const handleSettingChange = (setting: string, value: any) => {
    setSettings(prev => ({
      ...prev,
      [setting]: value,
    }));
  };

  const integrations = [
    {
      name: 'Splunk SIEM',
      type: 'SIEM',
      status: 'Connected',
      lastSync: '2026-01-09T16:30:00Z',
    },
    {
      name: 'Microsoft Sentinel',
      type: 'SIEM',
      status: 'Disconnected',
      lastSync: null,
    },
    {
      name: 'ServiceNow',
      type: 'ITSM',
      status: 'Connected',
      lastSync: '2026-01-09T15:45:00Z',
    },
    {
      name: 'Slack Workspace',
      type: 'Communication',
      status: 'Connected',
      lastSync: '2026-01-09T16:25:00Z',
    },
  ];

  const getStatusColor = (status: string) => {
    return status === 'Connected' ? 'success' : 'error';
  };

  return (
    <Box>
      {/* Header */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="h4" component="h1" sx={{ fontWeight: 600, mb: 1 }}>
          System Settings
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Configure system behavior, security parameters, and integrations
        </Typography>
      </Box>

      {/* Settings Tabs */}
      <Card>
        <CardContent>
          <Tabs value={activeTab} onChange={(_, newValue) => setActiveTab(newValue)} sx={{ mb: 3 }}>
            <Tab label="General" icon={<SettingsIcon />} />
            <Tab label="Security" icon={<Security />} />
            <Tab label="Notifications" icon={<Notifications />} />
            <Tab label="ML Engine" icon={<Tune />} />
            <Tab label="Integrations" icon={<Integration />} />
          </Tabs>

          {/* General Settings Tab */}
          {activeTab === 0 && (
            <Box>
              <Typography variant="h6" sx={{ mb: 3 }}>
                ⚙️ General Settings
              </Typography>
              
              <Grid container spacing={3}>
                <Grid item xs={12} sm={6}>
                  <Card variant="outlined">
                    <CardContent>
                      <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 2 }}>
                        Dashboard Settings
                      </Typography>
                      
                      <FormControlLabel
                        control={
                          <Switch
                            checked={settings.realTimeUpdates}
                            onChange={(e) => handleSettingChange('realTimeUpdates', e.target.checked)}
                          />
                        }
                        label="Real-time Updates"
                        sx={{ mb: 2, display: 'block' }}
                      />
                      
                      <FormControlLabel
                        control={
                          <Switch
                            checked={settings.autoRefresh}
                            onChange={(e) => handleSettingChange('autoRefresh', e.target.checked)}
                          />
                        }
                        label="Auto Refresh"
                        sx={{ mb: 2, display: 'block' }}
                      />
                      
                      <Typography variant="body2" sx={{ mb: 1 }}>
                        Refresh Interval (seconds)
                      </Typography>
                      <Slider
                        value={settings.refreshInterval}
                        onChange={(_, value) => handleSettingChange('refreshInterval', value)}
                        min={10}
                        max={300}
                        step={10}
                        marks={[
                          { value: 10, label: '10s' },
                          { value: 60, label: '1m' },
                          { value: 300, label: '5m' },
                        ]}
                        valueLabelDisplay="auto"
                        disabled={!settings.autoRefresh}
                      />
                    </CardContent>
                  </Card>
                </Grid>
                
                <Grid item xs={12} sm={6}>
                  <Card variant="outlined">
                    <CardContent>
                      <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 2 }}>
                        Appearance
                      </Typography>
                      
                      <FormControlLabel
                        control={
                          <Switch
                            checked={settings.darkMode}
                            onChange={(e) => handleSettingChange('darkMode', e.target.checked)}
                          />
                        }
                        label="Dark Mode"
                        sx={{ mb: 2, display: 'block' }}
                      />
                      
                      <TextField
                        fullWidth
                        label="Time Zone"
                        value="UTC-5 (Eastern Time)"
                        disabled
                        sx={{ mb: 2 }}
                      />
                      
                      <TextField
                        fullWidth
                        label="Date Format"
                        value="MM/DD/YYYY"
                        disabled
                      />
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>
            </Box>
          )}

          {/* Security Settings Tab */}
          {activeTab === 1 && (
            <Box>
              <Typography variant="h6" sx={{ mb: 3 }}>
                🔒 Security Settings
              </Typography>
              
              <Grid container spacing={3}>
                <Grid item xs={12} sm={6}>
                  <Card variant="outlined">
                    <CardContent>
                      <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 2 }}>
                        Risk Thresholds
                      </Typography>
                      
                      <Typography variant="body2" sx={{ mb: 1 }}>
                        High Risk Threshold: {settings.riskThreshold}
                      </Typography>
                      <Slider
                        value={settings.riskThreshold}
                        onChange={(_, value) => handleSettingChange('riskThreshold', value)}
                        min={50}
                        max={100}
                        step={5}
                        marks={[
                          { value: 50, label: '50' },
                          { value: 70, label: '70' },
                          { value: 90, label: '90' },
                        ]}
                        valueLabelDisplay="auto"
                        sx={{ mb: 3 }}
                      />
                      
                      <Typography variant="body2" sx={{ mb: 1 }}>
                        Alert Threshold: {settings.alertThreshold}
                      </Typography>
                      <Slider
                        value={settings.alertThreshold}
                        onChange={(_, value) => handleSettingChange('alertThreshold', value)}
                        min={30}
                        max={90}
                        step={5}
                        marks={[
                          { value: 30, label: '30' },
                          { value: 60, label: '60' },
                          { value: 90, label: '90' },
                        ]}
                        valueLabelDisplay="auto"
                      />
                    </CardContent>
                  </Card>
                </Grid>
                
                <Grid item xs={12} sm={6}>
                  <Card variant="outlined">
                    <CardContent>
                      <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 2 }}>
                        Security Policies
                      </Typography>
                      
                      <FormControlLabel
                        control={
                          <Switch
                            checked={settings.autoLockout}
                            onChange={(e) => handleSettingChange('autoLockout', e.target.checked)}
                          />
                        }
                        label="Automatic Account Lockout"
                        sx={{ mb: 2, display: 'block' }}
                      />
                      
                      <TextField
                        fullWidth
                        label="Session Timeout (minutes)"
                        type="number"
                        value={settings.sessionTimeout}
                        onChange={(e) => handleSettingChange('sessionTimeout', parseInt(e.target.value))}
                        sx={{ mb: 2 }}
                      />
                      
                      <TextField
                        fullWidth
                        label="Max Failed Attempts"
                        type="number"
                        value={5}
                        disabled
                      />
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>
            </Box>
          )}

          {/* Notifications Settings Tab */}
          {activeTab === 2 && (
            <Box>
              <Typography variant="h6" sx={{ mb: 3 }}>
                🔔 Notification Settings
              </Typography>
              
              <Grid container spacing={3}>
                <Grid item xs={12} sm={6}>
                  <Card variant="outlined">
                    <CardContent>
                      <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 2 }}>
                        Notification Channels
                      </Typography>
                      
                      <FormControlLabel
                        control={
                          <Switch
                            checked={settings.emailNotifications}
                            onChange={(e) => handleSettingChange('emailNotifications', e.target.checked)}
                          />
                        }
                        label="Email Notifications"
                        sx={{ mb: 2, display: 'block' }}
                      />
                      
                      <FormControlLabel
                        control={
                          <Switch
                            checked={settings.slackNotifications}
                            onChange={(e) => handleSettingChange('slackNotifications', e.target.checked)}
                          />
                        }
                        label="Slack Notifications"
                        sx={{ mb: 2, display: 'block' }}
                      />
                      
                      <FormControlLabel
                        control={
                          <Switch
                            checked={settings.pushNotifications}
                            onChange={(e) => handleSettingChange('pushNotifications', e.target.checked)}
                          />
                        }
                        label="Browser Push Notifications"
                        sx={{ mb: 2, display: 'block' }}
                      />
                    </CardContent>
                  </Card>
                </Grid>
                
                <Grid item xs={12} sm={6}>
                  <Card variant="outlined">
                    <CardContent>
                      <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 2 }}>
                        Notification Preferences
                      </Typography>
                      
                      <FormControlLabel
                        control={
                          <Switch
                            checked={settings.criticalAlertsOnly}
                            onChange={(e) => handleSettingChange('criticalAlertsOnly', e.target.checked)}
                          />
                        }
                        label="Critical Alerts Only"
                        sx={{ mb: 2, display: 'block' }}
                      />
                      
                      <TextField
                        fullWidth
                        label="Email Address"
                        value="security@company.com"
                        sx={{ mb: 2 }}
                      />
                      
                      <TextField
                        fullWidth
                        label="Slack Channel"
                        value="#security-alerts"
                      />
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>
            </Box>
          )}

          {/* ML Engine Settings Tab */}
          {activeTab === 3 && (
            <Box>
              <Typography variant="h6" sx={{ mb: 3 }}>
                🧠 Machine Learning Settings
              </Typography>
              
              <Grid container spacing={3}>
                <Grid item xs={12} sm={6}>
                  <Card variant="outlined">
                    <CardContent>
                      <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 2 }}>
                        Model Configuration
                      </Typography>
                      
                      <Typography variant="body2" sx={{ mb: 1 }}>
                        Model Sensitivity: {settings.modelSensitivity}%
                      </Typography>
                      <Slider
                        value={settings.modelSensitivity}
                        onChange={(_, value) => handleSettingChange('modelSensitivity', value)}
                        min={50}
                        max={100}
                        step={5}
                        marks={[
                          { value: 50, label: 'Low' },
                          { value: 75, label: 'Medium' },
                          { value: 100, label: 'High' },
                        ]}
                        valueLabelDisplay="auto"
                        sx={{ mb: 3 }}
                      />
                      
                      <Typography variant="body2" sx={{ mb: 1 }}>
                        False Positive Threshold: {settings.falsePositiveThreshold}%
                      </Typography>
                      <Slider
                        value={settings.falsePositiveThreshold}
                        onChange={(_, value) => handleSettingChange('falsePositiveThreshold', value)}
                        min={1}
                        max={20}
                        step={1}
                        marks={[
                          { value: 1, label: '1%' },
                          { value: 10, label: '10%' },
                          { value: 20, label: '20%' },
                        ]}
                        valueLabelDisplay="auto"
                      />
                    </CardContent>
                  </Card>
                </Grid>
                
                <Grid item xs={12} sm={6}>
                  <Card variant="outlined">
                    <CardContent>
                      <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 2 }}>
                        Training Settings
                      </Typography>
                      
                      <FormControlLabel
                        control={
                          <Switch
                            checked={settings.autoRetrain}
                            onChange={(e) => handleSettingChange('autoRetrain', e.target.checked)}
                          />
                        }
                        label="Automatic Retraining"
                        sx={{ mb: 2, display: 'block' }}
                      />
                      
                      <TextField
                        fullWidth
                        label="Retrain Interval (days)"
                        type="number"
                        value={settings.retrainInterval}
                        onChange={(e) => handleSettingChange('retrainInterval', parseInt(e.target.value))}
                        disabled={!settings.autoRetrain}
                        sx={{ mb: 2 }}
                      />
                      
                      <Button variant="outlined" fullWidth>
                        Retrain Model Now
                      </Button>
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>
            </Box>
          )}

          {/* Integrations Settings Tab */}
          {activeTab === 4 && (
            <Box>
              <Typography variant="h6" sx={{ mb: 3 }}>
                🔌 System Integrations
              </Typography>
              
              <Card variant="outlined" sx={{ mb: 3 }}>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                    <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                      Active Integrations
                    </Typography>
                    <Button variant="outlined" startIcon={<Add />}>
                      Add Integration
                    </Button>
                  </Box>
                  
                  <List>
                    {integrations.map((integration, index) => (
                      <ListItem key={index} divider={index < integrations.length - 1}>
                        <ListItemText
                          primary={
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                              <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                                {integration.name}
                              </Typography>
                              <Chip
                                label={integration.type}
                                size="small"
                                variant="outlined"
                              />
                              <Chip
                                label={integration.status}
                                size="small"
                                color={getStatusColor(integration.status) as any}
                                variant="filled"
                              />
                            </Box>
                          }
                          secondary={
                            integration.lastSync
                              ? `Last sync: ${new Date(integration.lastSync).toLocaleString()}`
                              : 'Never synced'
                          }
                        />
                        <ListItemSecondaryAction>
                          <IconButton edge="end" color="error">
                            <Delete />
                          </IconButton>
                        </ListItemSecondaryAction>
                      </ListItem>
                    ))}
                  </List>
                </CardContent>
              </Card>
              
              <Grid container spacing={3}>
                <Grid item xs={12} sm={6}>
                  <Card variant="outlined">
                    <CardContent>
                      <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 2 }}>
                        API Configuration
                      </Typography>
                      
                      <TextField
                        fullWidth
                        label="API Rate Limit (requests/minute)"
                        type="number"
                        value={1000}
                        sx={{ mb: 2 }}
                      />
                      
                      <TextField
                        fullWidth
                        label="API Timeout (seconds)"
                        type="number"
                        value={30}
                        sx={{ mb: 2 }}
                      />
                      
                      <Button variant="outlined" fullWidth>
                        Test API Connection
                      </Button>
                    </CardContent>
                  </Card>
                </Grid>
                
                <Grid item xs={12} sm={6}>
                  <Card variant="outlined">
                    <CardContent>
                      <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 2 }}>
                        Webhook Settings
                      </Typography>
                      
                      <TextField
                        fullWidth
                        label="Webhook URL"
                        value="https://api.company.com/webhooks/security"
                        sx={{ mb: 2 }}
                      />
                      
                      <TextField
                        fullWidth
                        label="Secret Key"
                        type="password"
                        value="••••••••••••••••"
                        sx={{ mb: 2 }}
                      />
                      
                      <Button variant="outlined" fullWidth>
                        Test Webhook
                      </Button>
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>
            </Box>
          )}

          <Divider sx={{ my: 3 }} />

          {/* Save Button */}
          <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
            <Button variant="outlined">
              Reset to Defaults
            </Button>
            <Button variant="contained">
              Save Settings
            </Button>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Settings;