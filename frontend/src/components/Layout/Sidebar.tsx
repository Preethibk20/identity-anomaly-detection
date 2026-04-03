import React from 'react';
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Typography,
  Box,
  Divider,
  Chip,
} from '@mui/material';
import {
  Dashboard,
  Security,
  Search,
  People,
  Assessment,
  Settings,
  Notifications,
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';

interface SidebarProps {
  open: boolean;
  onToggle: () => void;
}

const DRAWER_WIDTH = 280;

const menuItems = [
  {
    text: 'Dashboard',
    icon: <Dashboard />,
    path: '/dashboard',
    badge: null,
  },
  {
    text: 'Security Alerts',
    icon: <Notifications />,
    path: '/alerts',
    badge: '23',
  },
  {
    text: 'Threat Hunting',
    icon: <Search />,
    path: '/threat-hunting',
    badge: null,
  },
  {
    text: 'User Analytics',
    icon: <People />,
    path: '/user-analytics',
    badge: null,
  },
  {
    text: 'Reports',
    icon: <Assessment />,
    path: '/reports',
    badge: null,
  },
  {
    text: 'Settings',
    icon: <Settings />,
    path: '/settings',
    badge: null,
  },
];

const Sidebar: React.FC<SidebarProps> = ({ open, onToggle }) => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleNavigation = (path: string) => {
    navigate(path);
  };

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  return (
    <Drawer
      variant="persistent"
      anchor="left"
      open={open}
      sx={{
        width: DRAWER_WIDTH,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: DRAWER_WIDTH,
          boxSizing: 'border-box',
          bgcolor: 'background.paper',
          borderRight: '1px solid',
          borderColor: 'divider',
        },
      }}
    >
      {/* Header */}
      <Box sx={{ p: 3, textAlign: 'center' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', mb: 1 }}>
          <Security sx={{ fontSize: 32, color: 'primary.main', mr: 1 }} />
          <Typography variant="h6" sx={{ fontWeight: 'bold', color: 'primary.main' }}>
            SecureWatch
          </Typography>
        </Box>
        <Typography variant="body2" color="text.secondary">
          Identity Anomaly Detection
        </Typography>
      </Box>

      <Divider />

      {/* Navigation Menu */}
      <List sx={{ px: 2, py: 1 }}>
        {menuItems.map((item) => (
          <ListItem key={item.text} disablePadding sx={{ mb: 0.5 }}>
            <ListItemButton
              onClick={() => handleNavigation(item.path)}
              selected={isActive(item.path)}
              sx={{
                borderRadius: 2,
                '&.Mui-selected': {
                  bgcolor: 'primary.main',
                  color: 'primary.contrastText',
                  '&:hover': {
                    bgcolor: 'primary.dark',
                  },
                  '& .MuiListItemIcon-root': {
                    color: 'primary.contrastText',
                  },
                },
                '&:hover': {
                  bgcolor: 'action.hover',
                },
              }}
            >
              <ListItemIcon
                sx={{
                  color: isActive(item.path) ? 'primary.contrastText' : 'text.secondary',
                }}
              >
                {item.icon}
              </ListItemIcon>
              <ListItemText
                primary={item.text}
                primaryTypographyProps={{
                  fontSize: '0.9rem',
                  fontWeight: isActive(item.path) ? 600 : 400,
                }}
              />
              {item.badge && (
                <Chip
                  label={item.badge}
                  size="small"
                  color={isActive(item.path) ? 'secondary' : 'error'}
                  sx={{
                    height: 20,
                    fontSize: '0.75rem',
                    fontWeight: 600,
                  }}
                />
              )}
            </ListItemButton>
          </ListItem>
        ))}
      </List>

      <Box sx={{ flexGrow: 1 }} />

      {/* Footer */}
      <Box sx={{ p: 2 }}>
        <Divider sx={{ mb: 2 }} />
        <Box
          sx={{
            p: 2,
            bgcolor: 'action.hover',
            borderRadius: 2,
            textAlign: 'center',
          }}
        >
          <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mb: 1 }}>
            System Status
          </Typography>
          <Chip
            label="Operational"
            size="small"
            color="success"
            variant="filled"
            sx={{ fontSize: '0.7rem' }}
          />
        </Box>
      </Box>
    </Drawer>
  );
};

export default Sidebar;