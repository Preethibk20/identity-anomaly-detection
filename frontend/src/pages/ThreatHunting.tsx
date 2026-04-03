import React, { useState } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  TextField,
  Button,
  Grid,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Tabs,
  Tab,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from '@mui/material';
import {
  Search,
  Security,
  Timeline,
  AccountTree,
  ExpandMore,
  Visibility,
  Download,
  Share,
} from '@mui/icons-material';

const ThreatHunting: React.FC = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<any[]>([]);

  const handleSearch = () => {
    // Mock search results
    const mockResults = [
      {
        id: 'result-1',
        type: 'User Activity',
        title: 'Suspicious login pattern for john.doe',
        description: 'Multiple logins from different countries within 1 hour',
        timestamp: '2026-01-09T15:30:00Z',
        riskScore: 85,
        entities: ['john.doe', '185.220.101.42', 'Moscow'],
      },
      {
        id: 'result-2',
        type: 'Network Activity',
        title: 'Unusual data transfer volume',
        description: 'Large file downloads during off-hours',
        timestamp: '2026-01-09T14:45:00Z',
        riskScore: 65,
        entities: ['jane.smith', '192.168.1.100', 'file-server'],
      },
    ];
    setSearchResults(mockResults);
  };

  const savedQueries = [
    'user_id:"john.doe" AND location:"Moscow"',
    'failed_login:true AND count:>5',
    'time_range:"off_hours" AND resource:"admin_panel"',
    'impossible_travel:true',
  ];

  const threatHuntingTemplates = [
    {
      name: 'Credential Stuffing Detection',
      description: 'Detect multiple failed login attempts across different users',
      query: 'failed_login:true AND unique_users:>10 AND time_window:"5m"',
    },
    {
      name: 'Insider Threat - Data Exfiltration',
      description: 'Identify unusual data access patterns by internal users',
      query: 'data_access:true AND volume:>1GB AND time:"off_hours"',
    },
    {
      name: 'Account Takeover',
      description: 'Find signs of compromised user accounts',
      query: 'location_change:true AND device_change:true AND time_diff:<30m',
    },
  ];

  return (
    <Box>
      {/* Header */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="h4" component="h1" sx={{ fontWeight: 600, mb: 1 }}>
          Threat Hunting
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Proactively search for threats and suspicious activities in your environment
        </Typography>
      </Box>

      {/* Search Interface */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center' }}>
            <Search sx={{ mr: 1 }} />
            Threat Hunting Query
          </Typography>
          
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} md={8}>
              <TextField
                fullWidth
                placeholder="Enter your hunting query (e.g., user_id:john.doe AND location:Moscow)"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                variant="outlined"
                sx={{
                  '& .MuiOutlinedInput-root': {
                    fontFamily: 'monospace',
                  },
                }}
              />
            </Grid>
            <Grid item xs={12} md={4}>
              <Button
                variant="contained"
                fullWidth
                startIcon={<Search />}
                onClick={handleSearch}
                size="large"
              >
                Hunt Threats
              </Button>
            </Grid>
          </Grid>

          {/* Saved Queries */}
          <Box sx={{ mt: 2 }}>
            <Typography variant="subtitle2" sx={{ mb: 1 }}>
              Saved Queries:
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {savedQueries.map((query, index) => (
                <Chip
                  key={index}
                  label={query}
                  variant="outlined"
                  size="small"
                  onClick={() => setSearchQuery(query)}
                  sx={{ fontFamily: 'monospace', fontSize: '0.75rem' }}
                />
              ))}
            </Box>
          </Box>
        </CardContent>
      </Card>

      <Grid container spacing={3}>
        {/* Left Panel - Templates and Tools */}
        <Grid item xs={12} md={4}>
          {/* Hunting Templates */}
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2 }}>
                🎯 Hunting Templates
              </Typography>
              
              {threatHuntingTemplates.map((template, index) => (
                <Accordion key={index} sx={{ mb: 1 }}>
                  <AccordionSummary expandIcon={<ExpandMore />}>
                    <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                      {template.name}
                    </Typography>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                      {template.description}
                    </Typography>
                    <TextField
                      fullWidth
                      multiline
                      rows={2}
                      value={template.query}
                      variant="outlined"
                      size="small"
                      sx={{
                        '& .MuiOutlinedInput-root': {
                          fontFamily: 'monospace',
                          fontSize: '0.8rem',
                        },
                        mb: 1,
                      }}
                    />
                    <Button
                      size="small"
                      variant="outlined"
                      onClick={() => setSearchQuery(template.query)}
                    >
                      Use Template
                    </Button>
                  </AccordionDetails>
                </Accordion>
              ))}
            </CardContent>
          </Card>

          {/* Quick Stats */}
          <Card>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2 }}>
                📊 Hunting Statistics
              </Typography>
              
              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" color="text.secondary">
                  Total Hunts Today
                </Typography>
                <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
                  23
                </Typography>
              </Box>
              
              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" color="text.secondary">
                  Threats Discovered
                </Typography>
                <Typography variant="h4" sx={{ fontWeight: 'bold', color: 'error.main' }}>
                  7
                </Typography>
              </Box>
              
              <Box>
                <Typography variant="body2" color="text.secondary">
                  False Positives
                </Typography>
                <Typography variant="h4" sx={{ fontWeight: 'bold', color: 'success.main' }}>
                  2
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Right Panel - Results */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Tabs value={activeTab} onChange={(_, newValue) => setActiveTab(newValue)} sx={{ mb: 2 }}>
                <Tab label="Search Results" icon={<Search />} />
                <Tab label="Timeline View" icon={<Timeline />} />
                <Tab label="Entity Graph" icon={<AccountTree />} />
              </Tabs>

              {/* Search Results Tab */}
              {activeTab === 0 && (
                <Box>
                  {searchResults.length === 0 ? (
                    <Box sx={{ textAlign: 'center', py: 4 }}>
                      <Security sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
                      <Typography variant="h6" color="text.secondary">
                        No search results yet
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Enter a hunting query above to start searching for threats
                      </Typography>
                    </Box>
                  ) : (
                    <TableContainer component={Paper} elevation={0}>
                      <Table>
                        <TableHead>
                          <TableRow>
                            <TableCell>Finding</TableCell>
                            <TableCell>Type</TableCell>
                            <TableCell>Risk Score</TableCell>
                            <TableCell>Entities</TableCell>
                            <TableCell>Actions</TableCell>
                          </TableRow>
                        </TableHead>
                        <TableBody>
                          {searchResults.map((result) => (
                            <TableRow key={result.id} hover>
                              <TableCell>
                                <Box>
                                  <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                                    {result.title}
                                  </Typography>
                                  <Typography variant="body2" color="text.secondary">
                                    {result.description}
                                  </Typography>
                                  <Typography variant="caption" color="text.secondary">
                                    {new Date(result.timestamp).toLocaleString()}
                                  </Typography>
                                </Box>
                              </TableCell>
                              <TableCell>
                                <Chip
                                  label={result.type}
                                  size="small"
                                  variant="outlined"
                                />
                              </TableCell>
                              <TableCell>
                                <Chip
                                  label={`${result.riskScore}/100`}
                                  size="small"
                                  color={result.riskScore >= 70 ? 'error' : result.riskScore >= 40 ? 'warning' : 'success'}
                                  variant="filled"
                                />
                              </TableCell>
                              <TableCell>
                                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                                  {result.entities.map((entity: string, index: number) => (
                                    <Chip
                                      key={index}
                                      label={entity}
                                      size="small"
                                      variant="outlined"
                                      sx={{ fontSize: '0.7rem' }}
                                    />
                                  ))}
                                </Box>
                              </TableCell>
                              <TableCell>
                                <IconButton size="small" color="primary">
                                  <Visibility />
                                </IconButton>
                                <IconButton size="small" color="secondary">
                                  <Download />
                                </IconButton>
                                <IconButton size="small">
                                  <Share />
                                </IconButton>
                              </TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    </TableContainer>
                  )}
                </Box>
              )}

              {/* Timeline View Tab */}
              {activeTab === 1 && (
                <Box sx={{ textAlign: 'center', py: 4 }}>
                  <Timeline sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
                  <Typography variant="h6" color="text.secondary">
                    Timeline View
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Visual timeline of threat hunting results will be displayed here
                  </Typography>
                </Box>
              )}

              {/* Entity Graph Tab */}
              {activeTab === 2 && (
                <Box sx={{ textAlign: 'center', py: 4 }}>
                  <AccountTree sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
                  <Typography variant="h6" color="text.secondary">
                    Entity Relationship Graph
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Interactive graph showing relationships between entities will be displayed here
                  </Typography>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default ThreatHunting;