import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline, Box } from '@mui/material';
import { QueryClient, QueryClientProvider } from 'react-query';
import { SnackbarProvider } from 'notistack';

// Components
import Sidebar from './components/Layout/Sidebar';
import TopBar from './components/Layout/TopBar';
import Dashboard from './pages/Dashboard';
import AlertsPage from './pages/AlertsPage';
import ThreatHunting from './pages/ThreatHunting';
import UserAnalytics from './pages/UserAnalytics';
import Settings from './pages/Settings';
import Reports from './pages/Reports';

// Services
import { WebSocketService } from './services/WebSocketService';
import { AuthService } from './services/AuthService';

// Context
import { WebSocketProvider } from './contexts/WebSocketContext';
import { AuthProvider } from './contexts/AuthContext';

// Create theme
const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#667eea',
    },
    secondary: {
      main: '#764ba2',
    },
    background: {
      default: '#0f1419',
      paper: '#1a202c',
    },
    error: {
      main: '#e53e3e',
    },
    warning: {
      main: '#dd6b20',
    },
    success: {
      main: '#38a169',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h4: {
      fontWeight: 600,
    },
    h5: {
      fontWeight: 600,
    },
    h6: {
      fontWeight: 600,
    },
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
          backgroundColor: '#1a202c',
          border: '1px solid #2d3748',
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
        },
      },
    },
  },
});

// Create query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 30000,
    },
  },
});

const App: React.FC = () => {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check authentication status
    const checkAuth = async () => {
      try {
        const authStatus = await AuthService.checkAuthStatus();
        setIsAuthenticated(authStatus);
      } catch (error) {
        console.error('Auth check failed:', error);
        setIsAuthenticated(false);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  const handleSidebarToggle = () => {
    setSidebarOpen(!sidebarOpen);
  };

  if (loading) {
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Box
          display="flex"
          justifyContent="center"
          alignItems="center"
          minHeight="100vh"
          bgcolor="background.default"
        >
          <div>Loading...</div>
        </Box>
      </ThemeProvider>
    );
  }

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <QueryClientProvider client={queryClient}>
        <SnackbarProvider maxSnack={3}>
          <AuthProvider>
            <WebSocketProvider>
              <Router>
                <Box sx={{ display: 'flex', minHeight: '100vh' }}>
                  {isAuthenticated && (
                    <Sidebar open={sidebarOpen} onToggle={handleSidebarToggle} />
                  )}
                  
                  <Box sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
                    {isAuthenticated && (
                      <TopBar onSidebarToggle={handleSidebarToggle} />
                    )}
                    
                    <Box
                      component="main"
                      sx={{
                        flexGrow: 1,
                        p: isAuthenticated ? 3 : 0,
                        bgcolor: 'background.default',
                      }}
                    >
                      <Routes>
                        {isAuthenticated ? (
                          <>
                            <Route path="/" element={<Dashboard />} />
                            <Route path="/dashboard" element={<Dashboard />} />
                            <Route path="/alerts" element={<AlertsPage />} />
                            <Route path="/threat-hunting" element={<ThreatHunting />} />
                            <Route path="/user-analytics" element={<UserAnalytics />} />
                            <Route path="/reports" element={<Reports />} />
                            <Route path="/settings" element={<Settings />} />
                            <Route path="*" element={<Navigate to="/dashboard" replace />} />
                          </>
                        ) : (
                          <>
                            <Route path="/login" element={<div>Login Page</div>} />
                            <Route path="*" element={<Navigate to="/login" replace />} />
                          </>
                        )}
                      </Routes>
                    </Box>
                  </Box>
                </Box>
              </Router>
            </WebSocketProvider>
          </AuthProvider>
        </SnackbarProvider>
      </QueryClientProvider>
    </ThemeProvider>
  );
};

export default App;