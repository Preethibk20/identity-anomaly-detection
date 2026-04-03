import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Chip,
  Grid,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
} from '@mui/material';
import {
  LocationOn,
  Person,
  Warning,
  TrendingUp,
} from '@mui/icons-material';
import { useQuery } from 'react-query';
import { ApiService } from '../../services/ApiService';

interface LocationActivity {
  location: string;
  userCount: number;
  activityCount: number;
  riskScore: number;
  coordinates: [number, number];
  topUsers: string[];
  alertCount: number;
}

const UserActivityMap: React.FC = () => {
  const { data: locationData, isLoading } = useQuery<LocationActivity[]>(
    'location-activity',
    ApiService.getLocationActivity,
    {
      refetchInterval: 30000, // Refresh every 30 seconds
    }
  );

  // Generate sample data if API data is not available
  const generateSampleData = (): LocationActivity[] => {
    return [
      {
        location: 'New York',
        userCount: 45,
        activityCount: 1250,
        riskScore: 25,
        coordinates: [40.7128, -74.0060],
        topUsers: ['john.doe', 'jane.smith', 'mike.wilson'],
        alertCount: 2,
      },
      {
        location: 'London',
        userCount: 32,
        activityCount: 890,
        riskScore: 35,
        coordinates: [51.5074, -0.1278],
        topUsers: ['alice.brown', 'bob.jones'],
        alertCount: 4,
      },
      {
        location: 'Tokyo',
        userCount: 28,
        activityCount: 720,
        riskScore: 15,
        coordinates: [35.6762, 139.6503],
        topUsers: ['yuki.tanaka', 'hiroshi.sato'],
        alertCount: 1,
      },
      {
        location: 'Moscow',
        userCount: 3,
        activityCount: 45,
        riskScore: 85,
        coordinates: [55.7558, 37.6176],
        topUsers: ['unknown.user'],
        alertCount: 8,
      },
      {
        location: 'Sydney',
        userCount: 18,
        activityCount: 420,
        riskScore: 20,
        coordinates: [-33.8688, 151.2093],
        topUsers: ['emma.davis', 'liam.taylor'],
        alertCount: 1,
      },
      {
        location: 'Toronto',
        userCount: 22,
        activityCount: 580,
        riskScore: 30,
        coordinates: [43.6532, -79.3832],
        topUsers: ['sarah.wilson', 'david.lee'],
        alertCount: 3,
      },
    ];
  };

  const locations = locationData || generateSampleData();

  const getRiskColor = (riskScore: number) => {
    if (riskScore >= 70) return 'error';
    if (riskScore >= 40) return 'warning';
    if (riskScore >= 20) return 'info';
    return 'success';
  };

  const getRiskLevel = (riskScore: number) => {
    if (riskScore >= 70) return 'High Risk';
    if (riskScore >= 40) return 'Medium Risk';
    if (riskScore >= 20) return 'Low Risk';
    return 'Normal';
  };

  // Sort locations by risk score (highest first)
  const sortedLocations = [...locations].sort((a, b) => b.riskScore - a.riskScore);

  return (
    <Box sx={{ height: '100%' }}>
      {/* World Map Placeholder */}
      <Box
        sx={{
          height: 200,
          bgcolor: 'background.default',
          border: '1px solid',
          borderColor: 'divider',
          borderRadius: 1,
          mb: 2,
          position: 'relative',
          overflow: 'hidden',
          background: 'linear-gradient(135deg, #1a202c 0%, #2d3748 100%)',
        }}
      >
        {/* Map Background */}
        <Box
          sx={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23374151' fill-opacity='0.1'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
            opacity: 0.3,
          }}
        />
        
        {/* Location Markers */}
        {locations.map((location, index) => (
          <Box
            key={location.location}
            sx={{
              position: 'absolute',
              left: `${20 + (index * 15) % 60}%`,
              top: `${30 + (index * 10) % 40}%`,
              transform: 'translate(-50%, -50%)',
            }}
          >
            <Box
              sx={{
                width: Math.max(8, location.riskScore / 5),
                height: Math.max(8, location.riskScore / 5),
                borderRadius: '50%',
                bgcolor: location.riskScore >= 70 ? 'error.main' : 
                        location.riskScore >= 40 ? 'warning.main' : 
                        location.riskScore >= 20 ? 'info.main' : 'success.main',
                boxShadow: `0 0 ${location.riskScore / 10}px currentColor`,
                animation: location.riskScore >= 70 ? 'pulse 2s infinite' : 'none',
                '@keyframes pulse': {
                  '0%': { opacity: 1 },
                  '50%': { opacity: 0.5 },
                  '100%': { opacity: 1 },
                },
              }}
            />
          </Box>
        ))}
        
        {/* Legend */}
        <Box
          sx={{
            position: 'absolute',
            bottom: 8,
            right: 8,
            display: 'flex',
            gap: 1,
          }}
        >
          <Chip size="small" label="Low Risk" color="success" variant="outlined" />
          <Chip size="small" label="Medium Risk" color="warning" variant="outlined" />
          <Chip size="small" label="High Risk" color="error" variant="outlined" />
        </Box>
      </Box>

      {/* Location Details */}
      <Grid container spacing={2}>
        {sortedLocations.slice(0, 6).map((location) => (
          <Grid item xs={12} sm={6} key={location.location}>
            <Card
              sx={{
                height: '100%',
                border: location.riskScore >= 70 ? '1px solid' : 'none',
                borderColor: 'error.main',
              }}
            >
              <CardContent sx={{ p: 2 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 1 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <LocationOn sx={{ mr: 1, color: 'text.secondary' }} />
                    <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                      {location.location}
                    </Typography>
                  </Box>
                  <Chip
                    label={getRiskLevel(location.riskScore)}
                    size="small"
                    color={getRiskColor(location.riskScore) as any}
                    variant="outlined"
                  />
                </Box>
                
                <Grid container spacing={1} sx={{ mb: 1 }}>
                  <Grid item xs={6}>
                    <Typography variant="caption" color="text.secondary">
                      Users: {location.userCount}
                    </Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography variant="caption" color="text.secondary">
                      Activities: {location.activityCount}
                    </Typography>
                  </Grid>
                </Grid>
                
                {location.alertCount > 0 && (
                  <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                    <Warning sx={{ fontSize: 16, color: 'warning.main', mr: 0.5 }} />
                    <Typography variant="caption" color="warning.main">
                      {location.alertCount} active alerts
                    </Typography>
                  </Box>
                )}
                
                {location.topUsers.length > 0 && (
                  <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                    Top users: {location.topUsers.slice(0, 2).join(', ')}
                    {location.topUsers.length > 2 && ` +${location.topUsers.length - 2} more`}
                  </Typography>
                )}
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default UserActivityMap;