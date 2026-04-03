import React, { useState } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Tab,
  Tabs,
  Alert,
  LinearProgress,
} from '@mui/material';
import {
  Security,
  Warning,
  Block,
  Public,
  VpnKey,
  BugReport,
  TrendingUp,
  Shield,
} from '@mui/icons-material';
import { useQuery } from 'react-query';
import { ApiService } from '../../services/ApiService';

interface ThreatIntelData {
  ipThreats: Array<{
    ip: string;
    threatType: string;
    severity: 'low' | 'medium' | 'high' | 'critical';
    lastSeen: string;
    description: string;
  }>;
  malwareDomains: Array<{
    domain: string;
    malwareFamily: string;
    firstSeen: string;
    confidence: number;
  }>;
  threatActors: Array<{
    name: string;
    techniques: string[];
    lastActivity: string;
    targetSectors: string[];
  }>;
  vulnerabilities: Array<{
    cve: string;
    severity: string;
    description: string;
    exploitAvailable: boolean;
  }>;
}

const ThreatIntelligence: React.FC = () => {
  const [activeTab, setActiveTab] = useState(0);

  const { data: threatData, isLoading } = useQuery<ThreatIntelData>(
    'threat-intelligence',
    ApiService.getThreatIntelligence,
    {
      refetchInterval: 300000, // Refresh every 5 minutes
    }
  );

  // Generate sample data if API data is not available
  const generateSampleData = (): ThreatIntelData => {
    return {
      ipThreats: [
        {
          ip: '185.220.101.42',
          threatType: 'Tor Exit Node',
          severity: 'high',
          lastSeen: '2026-01-09T15:30:00Z',
          description: 'Known Tor exit node used for anonymization',
        },
        {
          ip: '45.142.214.123',
          threatType: 'Botnet C2',
          severity: 'critical',
          lastSeen: '2026-01-09T14:45:00Z',
          description: 'Command and control server for Emotet botnet',
        },
        {
          ip: '192.168.1.100',
          threatType: 'Suspicious Activity',
          severity: 'medium',
          lastSeen: '2026-01-09T16:00:00Z',
          description: 'Multiple failed authentication attempts',
        },
      ],
      malwareDomains: [
        {
          domain: 'malicious-site.com',
          malwareFamily: 'TrickBot',
          firstSeen: '2026-01-08T10:00:00Z',
          confidence: 95,
        },
        {
          domain: 'phishing-bank.net',
          malwareFamily: 'Phishing',
          firstSeen: '2026-01-09T08:30:00Z',
          confidence: 88,
        },
      ],
      threatActors: [
        {
          name: 'APT29 (Cozy Bear)',
          techniques: ['Spear Phishing', 'Credential Dumping', 'Lateral Movement'],
          lastActivity: '2026-01-05T00:00:00Z',
          targetSectors: ['Government', 'Healthcare', 'Technology'],
        },
        {
          name: 'Lazarus Group',
          techniques: ['Supply Chain Attack', 'Cryptocurrency Theft'],
          lastActivity: '2026-01-07T00:00:00Z',
          targetSectors: ['Financial', 'Cryptocurrency'],
        },
      ],
      vulnerabilities: [
        {
          cve: 'CVE-2024-1234',
          severity: 'Critical',
          description: 'Remote code execution in authentication service',
          exploitAvailable: true,
        },
        {
          cve: 'CVE-2024-5678',
          severity: 'High',
          description: 'Privilege escalation vulnerability',
          exploitAvailable: false,
        },
      ],
    };
  };

  const data = threatData || generateSampleData();

  const getSeverityColor = (severity: string) => {
    switch (severity.toLowerCase()) {
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

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
  };

  if (isLoading) {
    return (
      <Box sx={{ width: '100%' }}>
        <LinearProgress />
        <Typography variant="body2" sx={{ mt: 1, textAlign: 'center' }}>
          Loading threat intelligence...
        </Typography>
      </Box>
    );
  }

  return (
    <Box>
      {/* Threat Intelligence Summary */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ bgcolor: 'error.dark', color: 'error.contrastText' }}>
            <CardContent sx={{ p: 2 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box>
                  <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
                    {data.ipThreats.filter(t => t.severity === 'critical').length}
                  </Typography>
                  <Typography variant="body2">
                    Critical IPs
                  </Typography>
                </Box>
                <Block sx={{ fontSize: 40, opacity: 0.7 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ bgcolor: 'warning.dark', color: 'warning.contrastText' }}>
            <CardContent sx={{ p: 2 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box>
                  <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
                    {data.malwareDomains.length}
                  </Typography>
                  <Typography variant="body2">
                    Malware Domains
                  </Typography>
                </Box>
                <Public sx={{ fontSize: 40, opacity: 0.7 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ bgcolor: 'info.dark', color: 'info.contrastText' }}>
            <CardContent sx={{ p: 2 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box>
                  <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
                    {data.threatActors.length}
                  </Typography>
                  <Typography variant="body2">
                    Threat Actors
                  </Typography>
                </Box>
                <Shield sx={{ fontSize: 40, opacity: 0.7 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ bgcolor: 'success.dark', color: 'success.contrastText' }}>
            <CardContent sx={{ p: 2 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box>
                  <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
                    {data.vulnerabilities.filter(v => v.exploitAvailable).length}
                  </Typography>
                  <Typography variant="body2">
                    Active Exploits
                  </Typography>
                </Box>
                <BugReport sx={{ fontSize: 40, opacity: 0.7 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Detailed Threat Intelligence */}
      <Card>
        <CardContent>
          <Tabs value={activeTab} onChange={handleTabChange} sx={{ mb: 2 }}>
            <Tab label="IP Threats" icon={<Block />} />
            <Tab label="Malware Domains" icon={<Public />} />
            <Tab label="Threat Actors" icon={<Shield />} />
            <Tab label="Vulnerabilities" icon={<BugReport />} />
          </Tabs>

          {/* IP Threats Tab */}
          {activeTab === 0 && (
            <Box>
              <Typography variant="h6" sx={{ mb: 2 }}>
                🚫 Malicious IP Addresses
              </Typography>
              <List>
                {data.ipThreats.map((threat, index) => (
                  <ListItem
                    key={index}
                    sx={{
                      border: '1px solid',
                      borderColor: 'divider',
                      borderRadius: 1,
                      mb: 1,
                    }}
                  >
                    <ListItemIcon>
                      <Warning color={getSeverityColor(threat.severity) as any} />
                    </ListItemIcon>
                    <ListItemText
                      primary={
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Typography variant="subtitle2" sx={{ fontFamily: 'monospace' }}>
                            {threat.ip}
                          </Typography>
                          <Chip
                            label={threat.severity.toUpperCase()}
                            size="small"
                            color={getSeverityColor(threat.severity) as any}
                            variant="outlined"
                          />
                          <Chip
                            label={threat.threatType}
                            size="small"
                            variant="filled"
                          />
                        </Box>
                      }
                      secondary={
                        <Box>
                          <Typography variant="body2" color="text.secondary">
                            {threat.description}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            Last seen: {new Date(threat.lastSeen).toLocaleString()}
                          </Typography>
                        </Box>
                      }
                    />
                  </ListItem>
                ))}
              </List>
            </Box>
          )}

          {/* Malware Domains Tab */}
          {activeTab === 1 && (
            <Box>
              <Typography variant="h6" sx={{ mb: 2 }}>
                🌐 Malicious Domains
              </Typography>
              <List>
                {data.malwareDomains.map((domain, index) => (
                  <ListItem
                    key={index}
                    sx={{
                      border: '1px solid',
                      borderColor: 'divider',
                      borderRadius: 1,
                      mb: 1,
                    }}
                  >
                    <ListItemIcon>
                      <Public color="warning" />
                    </ListItemIcon>
                    <ListItemText
                      primary={
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Typography variant="subtitle2" sx={{ fontFamily: 'monospace' }}>
                            {domain.domain}
                          </Typography>
                          <Chip
                            label={domain.malwareFamily}
                            size="small"
                            color="error"
                            variant="outlined"
                          />
                          <Chip
                            label={`${domain.confidence}% confidence`}
                            size="small"
                            color={domain.confidence >= 90 ? 'error' : 'warning'}
                            variant="filled"
                          />
                        </Box>
                      }
                      secondary={
                        <Typography variant="caption" color="text.secondary">
                          First seen: {new Date(domain.firstSeen).toLocaleString()}
                        </Typography>
                      }
                    />
                  </ListItem>
                ))}
              </List>
            </Box>
          )}

          {/* Threat Actors Tab */}
          {activeTab === 2 && (
            <Box>
              <Typography variant="h6" sx={{ mb: 2 }}>
                🎭 Known Threat Actors
              </Typography>
              <List>
                {data.threatActors.map((actor, index) => (
                  <ListItem
                    key={index}
                    sx={{
                      border: '1px solid',
                      borderColor: 'divider',
                      borderRadius: 1,
                      mb: 1,
                    }}
                  >
                    <ListItemIcon>
                      <Shield color="error" />
                    </ListItemIcon>
                    <ListItemText
                      primary={
                        <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                          {actor.name}
                        </Typography>
                      }
                      secondary={
                        <Box>
                          <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                            Techniques: {actor.techniques.join(', ')}
                          </Typography>
                          <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                            Target Sectors: {actor.targetSectors.join(', ')}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            Last Activity: {new Date(actor.lastActivity).toLocaleDateString()}
                          </Typography>
                        </Box>
                      }
                    />
                  </ListItem>
                ))}
              </List>
            </Box>
          )}

          {/* Vulnerabilities Tab */}
          {activeTab === 3 && (
            <Box>
              <Typography variant="h6" sx={{ mb: 2 }}>
                🐛 Critical Vulnerabilities
              </Typography>
              <List>
                {data.vulnerabilities.map((vuln, index) => (
                  <ListItem
                    key={index}
                    sx={{
                      border: '1px solid',
                      borderColor: 'divider',
                      borderRadius: 1,
                      mb: 1,
                    }}
                  >
                    <ListItemIcon>
                      <BugReport color={getSeverityColor(vuln.severity) as any} />
                    </ListItemIcon>
                    <ListItemText
                      primary={
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Typography variant="subtitle2" sx={{ fontFamily: 'monospace' }}>
                            {vuln.cve}
                          </Typography>
                          <Chip
                            label={vuln.severity}
                            size="small"
                            color={getSeverityColor(vuln.severity) as any}
                            variant="outlined"
                          />
                          {vuln.exploitAvailable && (
                            <Chip
                              label="Exploit Available"
                              size="small"
                              color="error"
                              variant="filled"
                            />
                          )}
                        </Box>
                      }
                      secondary={
                        <Typography variant="body2" color="text.secondary">
                          {vuln.description}
                        </Typography>
                      }
                    />
                  </ListItem>
                ))}
              </List>
            </Box>
          )}
        </CardContent>
      </Card>
    </Box>
  );
};

export default ThreatIntelligence;