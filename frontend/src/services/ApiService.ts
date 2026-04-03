import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for auth
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export class ApiService {
  // Dashboard APIs
  static async getDashboardMetrics() {
    try {
      const response = await apiClient.get('/api/dashboard/metrics');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch dashboard metrics:', error);
      // Return mock data for demo
      return {
        totalUsers: 156,
        activeAlerts: 23,
        highRiskAlerts: 8,
        criticalAlerts: 3,
        eventsProcessed: 1245678,
        eventsPerSecond: 125.3,
        avgProcessingTime: 85.2,
        systemUptime: 87300,
        threatScore: 65,
        falsePositiveRate: 2.1,
      };
    }
  }

  static async getRecentAlerts(limit: number = 10) {
    try {
      const response = await apiClient.get(`/api/alerts/recent?limit=${limit}`);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch recent alerts:', error);
      // Return mock data for demo
      return [
        {
          id: 'alert-001',
          title: 'Suspicious Login from Moscow',
          description: 'User john.doe logged in from unusual location at 3 AM',
          severity: 'high',
          timestamp: new Date(Date.now() - 1800000).toISOString(),
          user_id: 'john.doe',
          risk_score: 85,
          status: 'open',
        },
        {
          id: 'alert-002',
          title: 'Multiple Failed Login Attempts',
          description: 'User jane.smith had 5 failed login attempts in 2 minutes',
          severity: 'medium',
          timestamp: new Date(Date.now() - 3600000).toISOString(),
          user_id: 'jane.smith',
          risk_score: 65,
          status: 'investigating',
        },
        {
          id: 'alert-003',
          title: 'Impossible Travel Detected',
          description: 'User mike.wilson appeared in Tokyo 30 minutes after New York login',
          severity: 'critical',
          timestamp: new Date(Date.now() - 7200000).toISOString(),
          user_id: 'mike.wilson',
          risk_score: 95,
          status: 'open',
        },
      ];
    }
  }

  static async getRiskTrends(timeRange: string) {
    try {
      const response = await apiClient.get(`/api/analytics/risk-trends?range=${timeRange}`);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch risk trends:', error);
      // Return mock data for demo
      const now = new Date();
      const data = [];
      const points = timeRange === '1h' ? 12 : timeRange === '6h' ? 24 : timeRange === '24h' ? 48 : 168;
      const interval = timeRange === '1h' ? 5 : timeRange === '6h' ? 15 : timeRange === '24h' ? 30 : 60;

      for (let i = points; i >= 0; i--) {
        const timestamp = new Date(now.getTime() - i * interval * 60000);
        const baseRisk = 30 + Math.sin(i * 0.1) * 20 + Math.random() * 15;
        
        data.push({
          timestamp: timestamp.toISOString(),
          avgRiskScore: Math.max(0, Math.min(100, baseRisk)),
          alertCount: Math.floor(Math.random() * 10) + 1,
          criticalAlerts: Math.floor(Math.random() * 3),
          highAlerts: Math.floor(Math.random() * 5) + 1,
          mediumAlerts: Math.floor(Math.random() * 8) + 2,
          lowAlerts: Math.floor(Math.random() * 12) + 3,
        });
      }

      return data;
    }
  }

  static async getLocationActivity() {
    try {
      const response = await apiClient.get('/api/analytics/location-activity');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch location activity:', error);
      // Return mock data for demo
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
          location: 'Moscow',
          userCount: 3,
          activityCount: 45,
          riskScore: 85,
          coordinates: [55.7558, 37.6176],
          topUsers: ['unknown.user'],
          alertCount: 8,
        },
      ];
    }
  }

  static async getThreatIntelligence() {
    try {
      const response = await apiClient.get('/api/threat-intel');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch threat intelligence:', error);
      // Return mock data for demo
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
        ],
        malwareDomains: [
          {
            domain: 'malicious-site.com',
            malwareFamily: 'TrickBot',
            firstSeen: '2026-01-08T10:00:00Z',
            confidence: 95,
          },
        ],
        threatActors: [
          {
            name: 'APT29 (Cozy Bear)',
            techniques: ['Spear Phishing', 'Credential Dumping', 'Lateral Movement'],
            lastActivity: '2026-01-05T00:00:00Z',
            targetSectors: ['Government', 'Healthcare', 'Technology'],
          },
        ],
        vulnerabilities: [
          {
            cve: 'CVE-2024-1234',
            severity: 'Critical',
            description: 'Remote code execution in authentication service',
            exploitAvailable: true,
          },
        ],
      };
    }
  }

  // Alert Management APIs
  static async getAlerts(filters?: any) {
    try {
      const response = await apiClient.get('/api/alerts', { params: filters });
      return response.data;
    } catch (error) {
      console.error('Failed to fetch alerts:', error);
      throw error;
    }
  }

  static async updateAlertStatus(alertId: string, status: string, notes?: string) {
    try {
      const response = await apiClient.patch(`/api/alerts/${alertId}`, {
        status,
        notes,
      });
      return response.data;
    } catch (error) {
      console.error('Failed to update alert status:', error);
      throw error;
    }
  }

  // User Analytics APIs
  static async getUserAnalytics(userId?: string) {
    try {
      const response = await apiClient.get('/api/analytics/users', {
        params: { userId },
      });
      return response.data;
    } catch (error) {
      console.error('Failed to fetch user analytics:', error);
      throw error;
    }
  }

  // System APIs
  static async simulateAttack() {
    try {
      const response = await apiClient.post('/api/system/simulate-attack');
      return response.data;
    } catch (error) {
      console.error('Failed to simulate attack:', error);
      throw error;
    }
  }

  static async getSystemHealth() {
    try {
      const response = await apiClient.get('/api/system/health');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch system health:', error);
      throw error;
    }
  }

  // Threat Hunting APIs
  static async searchThreats(query: string, filters?: any) {
    try {
      const response = await apiClient.post('/api/threat-hunting/search', {
        query,
        filters,
      });
      return response.data;
    } catch (error) {
      console.error('Failed to search threats:', error);
      throw error;
    }
  }

  // Reports APIs
  static async generateReport(type: string, parameters: any) {
    try {
      const response = await apiClient.post('/api/reports/generate', {
        type,
        parameters,
      });
      return response.data;
    } catch (error) {
      console.error('Failed to generate report:', error);
      throw error;
    }
  }

  static async getReports() {
    try {
      const response = await apiClient.get('/api/reports');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch reports:', error);
      throw error;
    }
  }
}