import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export class AuthService {
  static async login(username: string, password: string): Promise<boolean> {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/auth/login`, {
        username,
        password,
      });

      if (response.data.token) {
        localStorage.setItem('auth_token', response.data.token);
        localStorage.setItem('user_info', JSON.stringify(response.data.user));
        return true;
      }

      return false;
    } catch (error) {
      console.error('Login failed:', error);
      return false;
    }
  }

  static async logout(): Promise<void> {
    try {
      const token = localStorage.getItem('auth_token');
      if (token) {
        await axios.post(`${API_BASE_URL}/api/auth/logout`, {}, {
          headers: { Authorization: `Bearer ${token}` },
        });
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user_info');
    }
  }

  static async checkAuthStatus(): Promise<boolean> {
    try {
      const token = localStorage.getItem('auth_token');
      if (!token) {
        return false;
      }

      const response = await axios.get(`${API_BASE_URL}/api/auth/verify`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      return response.status === 200;
    } catch (error) {
      console.error('Auth check failed:', error);
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user_info');
      return false;
    }
  }

  static getCurrentUser(): any {
    try {
      const userInfo = localStorage.getItem('user_info');
      return userInfo ? JSON.parse(userInfo) : null;
    } catch (error) {
      console.error('Failed to parse user info:', error);
      return null;
    }
  }

  static getToken(): string | null {
    return localStorage.getItem('auth_token');
  }

  static isAuthenticated(): boolean {
    return !!localStorage.getItem('auth_token');
  }

  // For demo purposes, always return true
  static async demoLogin(): Promise<boolean> {
    const demoUser = {
      id: 'demo-user',
      username: 'security.analyst',
      email: 'analyst@company.com',
      role: 'Security Analyst',
      permissions: ['view_alerts', 'manage_alerts', 'view_analytics'],
    };

    localStorage.setItem('auth_token', 'demo-token-12345');
    localStorage.setItem('user_info', JSON.stringify(demoUser));
    return true;
  }
}