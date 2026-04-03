import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { Socket } from 'socket.io-client';
import { WebSocketService } from '../services/WebSocketService';

interface WebSocketContextType {
  socket: Socket | null;
  isConnected: boolean;
  connectionStatus: 'connecting' | 'connected' | 'disconnected' | 'error';
}

const WebSocketContext = createContext<WebSocketContextType>({
  socket: null,
  isConnected: false,
  connectionStatus: 'disconnected',
});

interface WebSocketProviderProps {
  children: ReactNode;
}

export const WebSocketProvider: React.FC<WebSocketProviderProps> = ({ children }) => {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState<'connecting' | 'connected' | 'disconnected' | 'error'>('disconnected');

  useEffect(() => {
    const wsService = new WebSocketService();
    const wsUrl = process.env.REACT_APP_WS_URL || 'ws://localhost:8000';
    
    setConnectionStatus('connecting');
    
    try {
      const socketInstance = wsService.connect(wsUrl);
      setSocket(socketInstance);

      // Connection event handlers
      socketInstance.on('connect', () => {
        console.log('WebSocket connected successfully');
        setIsConnected(true);
        setConnectionStatus('connected');
      });

      socketInstance.on('disconnect', (reason) => {
        console.log('WebSocket disconnected:', reason);
        setIsConnected(false);
        setConnectionStatus('disconnected');
      });

      socketInstance.on('connect_error', (error) => {
        console.error('WebSocket connection error:', error);
        setIsConnected(false);
        setConnectionStatus('error');
      });

      // Application-specific event handlers
      socketInstance.on('metrics_update', (data) => {
        // Handle metrics updates
        console.log('Metrics update:', data);
      });

      socketInstance.on('new_alert', (alert) => {
        // Handle new alerts
        console.log('New alert:', alert);
        
        // Show notification if browser supports it
        if ('Notification' in window && Notification.permission === 'granted') {
          new Notification('Security Alert', {
            body: alert.title || 'New security alert detected',
            icon: '/favicon.ico',
          });
        }
      });

      socketInstance.on('system_status', (status) => {
        // Handle system status updates
        console.log('System status:', status);
      });

      // Request notification permission
      if ('Notification' in window && Notification.permission === 'default') {
        Notification.requestPermission();
      }

    } catch (error) {
      console.error('Failed to initialize WebSocket:', error);
      setConnectionStatus('error');
    }

    // Cleanup on unmount
    return () => {
      if (socket) {
        socket.disconnect();
      }
      wsService.disconnect();
    };
  }, []);

  const contextValue: WebSocketContextType = {
    socket,
    isConnected,
    connectionStatus,
  };

  return (
    <WebSocketContext.Provider value={contextValue}>
      {children}
    </WebSocketContext.Provider>
  );
};

export const useWebSocket = (): WebSocketContextType => {
  const context = useContext(WebSocketContext);
  if (!context) {
    throw new Error('useWebSocket must be used within a WebSocketProvider');
  }
  return context;
};