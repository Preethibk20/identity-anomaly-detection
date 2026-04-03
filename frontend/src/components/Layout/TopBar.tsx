import React, { useState } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Badge,
  Menu,
  MenuItem,
  Avatar,
  Box,
  Chip,
  Divider,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Notifications,
  AccountCircle,
  Logout,
  Settings,
  Security,
} from '@mui/icons-material';
import { useAuth } from '../../contexts/AuthContext';
import { useWebSocket } from '../../contexts/WebSocketContext';

interface TopBarProps {
  onSidebarToggle: () => void;
}

const TopBar: React.FC<TopBarProps> = ({ onSidebarToggle }) => {
  const { user, logout } = useAuth();
  const { isConnected, connectionStatus } = useWebSocket();
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [notificationAnchor, setNotificationAnchor] = useState<null | HTMLElement>(null);

  const handleProfileMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleProfileMenuClose = () => {
    setAnchorEl(null);
  };

  const handleNotificationMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setNotificationAnchor(event.currentTarget);
  };

  const handleNotificationMenuClose = () => {
    setNotificationAnchor(null);
  };

  const handleLogout = async () => {
    handleProfileMenuClose();
    await logout();
  };

  const getConnectionStatusColor = () => {
    switch (connectionStatus) {
      case 'connected':
        return 'success';
      case 'connecting':
        return 'warning';
      case 'error':
        return 'error';
      default:
        return 'default';
    }
  };

  const getConnectionStatusText = () => {
    switch (connectionStatus) {
      case 'connected':
        return 'Connected';
      case 'connecting':
        return 'Connecting...';
      case 'error':
        return 'Connection Error';
      default:
        return 'Disconnected';
    }
  };

  return (
    <AppBar
      position="sticky"
      elevation={0}
      sx={{
        bgcolor: 'background.paper',
        borderBottom: '1px solid',
        borderColor: 'divider',
        color: 'text.primary',
      }}
    >
      <Toolbar>
        {/* Menu Button */}
        <IconButton
          edge="start"
          color="inherit"
          aria-label="menu"
          onClick={onSidebarToggle}
          sx={{ mr: 2 }}
        >
          <MenuIcon />
        </IconButton>

        {/* Title */}
        <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 600 }}>
          Security Operations Center
        </Typography>

        {/* Connection Status */}
        <Box sx={{ mr: 2 }}>
          <Chip
            icon={<Security />}
            label={getConnectionStatusText()}
            size="small"
            color={getConnectionStatusColor() as any}
            variant="outlined"
          />
        </Box>

        {/* Notifications */}
        <IconButton
          color="inherit"
          onClick={handleNotificationMenuOpen}
          sx={{ mr: 1 }}
        >
          <Badge badgeContent={3} color="error">
            <Notifications />
          </Badge>
        </IconButton>

        {/* Profile Menu */}
        <IconButton
          edge="end"
          color="inherit"
          onClick={handleProfileMenuOpen}
        >
          <Avatar sx={{ width: 32, height: 32, bgcolor: 'primary.main' }}>
            {user?.username?.charAt(0).toUpperCase() || 'U'}
          </Avatar>
        </IconButton>

        {/* Profile Menu Dropdown */}
        <Menu
          anchorEl={anchorEl}
          open={Boolean(anchorEl)}
          onClose={handleProfileMenuClose}
          anchorOrigin={{
            vertical: 'bottom',
            horizontal: 'right',
          }}
          transformOrigin={{
            vertical: 'top',
            horizontal: 'right',
          }}
        >
          <Box sx={{ px: 2, py: 1 }}>
            <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
              {user?.username || 'User'}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {user?.email || 'user@company.com'}
            </Typography>
            <Chip
              label={user?.role || 'Security Analyst'}
              size="small"
              color="primary"
              variant="outlined"
              sx={{ mt: 1 }}
            />
          </Box>
          <Divider />
          <MenuItem onClick={handleProfileMenuClose}>
            <AccountCircle sx={{ mr: 2 }} />
            Profile
          </MenuItem>
          <MenuItem onClick={handleProfileMenuClose}>
            <Settings sx={{ mr: 2 }} />
            Settings
          </MenuItem>
          <Divider />
          <MenuItem onClick={handleLogout}>
            <Logout sx={{ mr: 2 }} />
            Logout
          </MenuItem>
        </Menu>

        {/* Notifications Menu Dropdown */}
        <Menu
          anchorEl={notificationAnchor}
          open={Boolean(notificationAnchor)}
          onClose={handleNotificationMenuClose}
          anchorOrigin={{
            vertical: 'bottom',
            horizontal: 'right',
          }}
          transformOrigin={{
            vertical: 'top',
            horizontal: 'right',
          }}
          PaperProps={{
            sx: { width: 320, maxHeight: 400 },
          }}
        >
          <Box sx={{ px: 2, py: 1 }}>
            <Typography variant="h6" sx={{ fontWeight: 600 }}>
              Notifications
            </Typography>
          </Box>
          <Divider />
          
          <MenuItem onClick={handleNotificationMenuClose}>
            <Box>
              <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                High Risk Alert
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Suspicious login from Moscow detected
              </Typography>
              <Typography variant="caption" color="text.secondary">
                2 minutes ago
              </Typography>
            </Box>
          </MenuItem>
          
          <MenuItem onClick={handleNotificationMenuClose}>
            <Box>
              <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                System Update
              </Typography>
              <Typography variant="body2" color="text.secondary">
                ML model retrained with new data
              </Typography>
              <Typography variant="caption" color="text.secondary">
                15 minutes ago
              </Typography>
            </Box>
          </MenuItem>
          
          <MenuItem onClick={handleNotificationMenuClose}>
            <Box>
              <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                Threat Intelligence
              </Typography>
              <Typography variant="body2" color="text.secondary">
                New IOCs added to threat feed
              </Typography>
              <Typography variant="caption" color="text.secondary">
                1 hour ago
              </Typography>
            </Box>
          </MenuItem>
          
          <Divider />
          <MenuItem onClick={handleNotificationMenuClose} sx={{ justifyContent: 'center' }}>
            <Typography variant="body2" color="primary">
              View All Notifications
            </Typography>
          </MenuItem>
        </Menu>
      </Toolbar>
    </AppBar>
  );
};

export default TopBar;