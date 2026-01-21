// api.test.js
import { beforeEach, describe, it, expect, jest } from '@jest/globals';
import ApiService from './api'; // Adjust import path as needed
import axios from 'axios';

// Mock axios
jest.mock('axios');

describe('ApiService', () => {
  let apiService;
  const mockAxios = axios;

  beforeEach(() => {
    // Reset mocks before each test
    jest.clearAllMocks();
    
    // Create a new instance of ApiService for each test
    apiService = new ApiService();
  });

  describe('Initialization', () => {
    it('should initialize API client with correct base URL and default headers', () => {
      expect(apiService.client).toBeDefined();
      expect(mockAxios.create).toHaveBeenCalledWith({
        baseURL: process.env.REACT_APP_API_BASE_URL || 'http://localhost:3001/api',
        headers: {
          'Content-Type': 'application/json'
        }
      });
    });

    it('should set up request and response interceptors', () => {
      expect(mockAxios.interceptors.request.use).toHaveBeenCalled();
      expect(mockAxios.interceptors.response.use).toHaveBeenCalled();
    });
  });

  describe('Request Interceptor', () => {
    it('should add authorization token to requests when available', async () => {
      // Mock localStorage.getItem to return a token
      Storage.prototype.getItem = jest.fn().mockReturnValue('mock-token');
      
      const mockConfig = { headers: {} };
      const expectedConfig = {
        ...mockConfig,
        headers: {
          ...mockConfig.headers,
          Authorization: 'Bearer mock-token'
        }
      };

      // Mock the interceptor function
      const requestInterceptor = mockAxios.interceptors.request.use.mock.calls[0][0];
      
      const result = await requestInterceptor(mockConfig);
      
      expect(result).toEqual(expectedConfig);
    });

    it('should not add authorization token when none is available', async () => {
      // Mock localStorage.getItem to return null
      Storage.prototype.getItem = jest.fn().mockReturnValue(null);
      
      const mockConfig = { headers: {} };
      
      // Mock the interceptor function
      const requestInterceptor = mockAxios.interceptors.request.use.mock.calls[0][0];
      
      const result = await requestInterceptor(mockConfig);
      
      expect(result).toEqual(mockConfig);
    });
  });

  describe('Response Interceptor', () => {
    it('should handle 401 errors by clearing auth and redirecting', async () => {
      // Mock localStorage.setItem and removeItem
      Storage.prototype.setItem = jest.fn();
      Storage.prototype.removeItem = jest.fn();
      
      // Mock window.location.assign
      Object.defineProperty(window, 'location', {
        value: { assign: jest.fn() },
        writable: true
      });

      const mockError = {
        response: {
          status: 401
        }
      };

      // Mock the response interceptor function
      const responseInterceptor = mockAxios.interceptors.response.use.mock.calls[0][1];
      
      try {
        await responseInterceptor(mockError);
      } catch (error) {
        // Expected to throw due to 401
        expect(Storage.prototype.removeItem).toHaveBeenCalledWith('authToken');
        expect(window.location.assign).toHaveBeenCalledWith('/login');
      }
    });

    it('should rethrow other errors', async () => {
      const mockError = {
        response: {
          status: 500,
          data: { message: 'Server Error' }
        }
      };

      // Mock the response interceptor function
      const responseInterceptor = mockAxios.interceptors.response.use.mock.calls[0][1];
      
      try {
        await responseInterceptor(mockError);
      } catch (error) {
        expect(error.response.status).toBe(500);
        expect(error.response.data.message).toBe('Server Error');
      }
    });
  });

  describe('Auth Methods', () => {
    describe('login', () => {
      it('should call POST /auth/login with correct data', async () => {
        const mockResponse = { data: { token: 'mock-token' } };
        mockAxios.post.mockResolvedValue(mockResponse);
        
        const loginData = { email: 'test@example.com', password: 'password' };
        const result = await apiService.login(loginData);
        
        expect(mockAxios.post).toHaveBeenCalledWith('/auth/login', loginData);
        expect(result).toEqual(mockResponse.data);
      });

      it('should handle login errors', async () => {
        const mockError = new Error('Login failed');
        mockAxios.post.mockRejectedValue(mockError);
        
        await expect(apiService.login({})).rejects.toThrow('Login failed');
      });
    });

    describe('register', () => {
      it('should call POST /auth/register with correct data', async () => {
        const mockResponse = { data: { user: { id: 1, name: 'Test User' } } };
        mockAxios.post.mockResolvedValue(mockResponse);
        
        const registerData = { 
          name: 'Test User', 
          email: 'test@example.com', 
          password: 'password' 
        };
        const result = await apiService.register(registerData);
        
        expect(mockAxios.post).toHaveBeenCalledWith('/auth/register', registerData);
        expect(result).toEqual(mockResponse.data);
      });

      it('should handle registration errors', async () => {
        const mockError = new Error('Registration failed');
        mockAxios.post.mockRejectedValue(mockError);
        
        await expect(apiService.register({})).rejects.toThrow('Registration failed');
      });
    });

    describe('logout', () => {
      it('should clear authentication token and remove from storage', () => {
        Storage.prototype.removeItem = jest.fn();
        
        apiService.logout();
        
        expect(Storage.prototype.removeItem).toHaveBeenCalledWith('authToken');
      });
    });
  });

  describe('CRUD Methods', () => {
    beforeEach(() => {
      // Mock localStorage to return a token for all CRUD tests
      Storage.prototype.getItem = jest.fn().mockReturnValue('mock-token');
    });

    describe('get', () => {
      it('should call GET with correct endpoint', async () => {
        const mockResponse = { data: [{ id: 1, name: 'Test Item' }] };
        mockAxios.get.mockResolvedValue(mockResponse);
        
        const result = await apiService.get('/users');
        
        expect(mockAxios.get).toHaveBeenCalledWith('/users');
        expect(result).toEqual(mockResponse.data);
      });

      it('should handle get errors', async () => {
        const mockError = new Error('Get failed');
        mockAxios.get.mockRejectedValue(mockError);
        
        await expect(apiService.get('/users')).rejects.toThrow('Get failed');
      });
    });

    describe('post', () => {
      it('should call POST with correct endpoint and data', async () => {
        const mockResponse = { data: { id: 1, name: 'New Item' } };
        mockAxios.post.mockResolvedValue(mockResponse);
        
        const postData = { name: 'New Item' };
        const result = await apiService.post('/users', postData);
        
        expect(mockAxios.post).toHaveBeenCalledWith('/users', postData);
        expect(result).toEqual(mockResponse.data);
      });

      it('should handle post errors', async () => {
        const mockError = new Error('Post failed');
        mockAxios.post.mockRejectedValue(mockError);
        
        await expect(apiService.post('/users', {})).rejects.toThrow('Post failed');
      });
    });

    describe('put', () => {
      it('should call PUT with correct endpoint and data', async () => {
        const mockResponse = { data: { id: 1, name: 'Updated Item' } };
        mockAxios.put.mockResolvedValue(mockResponse);
        
        const putData = { name: 'Updated Item' };
        const result = await apiService.put('/users/1', putData);
        
        expect(mockAxios.put).toHaveBeenCalledWith('/users/1', putData);
        expect(result).toEqual(mockResponse.data);
      });

      it('should handle put errors', async () => {
        const mockError = new Error('Put failed');
        mockAxios.put.mockRejectedValue(mockError);
        
        await expect(apiService.put('/users/1', {})).rejects.toThrow('Put failed');
      });
    });

    describe('delete', () => {
      it('should call DELETE with correct endpoint', async () => {
        const mockResponse = { data: { message: 'Deleted successfully' } };
        mockAxios.delete.mockResolvedValue(mockResponse);
        
        const result = await apiService.delete('/users/1');
        
        expect(mockAxios.delete).toHaveBeenCalledWith('/users/1');
        expect(result).toEqual(mockResponse.data);
      });

      it('should handle delete errors', async () => {
        const mockError = new Error('Delete failed');
        mockAxios.delete.mockRejectedValue(mockError);
        
        await expect(apiService.delete('/users/1')).rejects.toThrow('Delete failed');
      });
    });
  });

  describe('Error Handling', () => {
    beforeEach(() => {
      // Mock localStorage to return a token
      Storage.prototype.getItem = jest.fn().mockReturnValue('mock-token');
    });

    it('should properly handle network errors', async () => {
      const mockError = new Error('Network Error');
      mockError.code = 'ECONNABORTED';
      mockAxios.get.mockRejectedValue(mockError);
      
      await expect(apiService.get('/users')).rejects.toThrow('Network Error');
    });

    it('should handle HTTP errors with proper error messages', async () => {
      const mockError = {
        response: {
          status: 404,
          data: { message: 'Resource not found' }
        }
      };
      mockAxios.get.mockRejectedValue(mockError);
      
      try {
        await apiService.get('/nonexistent');
      } catch (error) {
        expect(error.response.status).toBe(404);
        expect(error.response.data.message).toBe('Resource not found');
      }
    });

    it('should handle unexpected errors gracefully', async () => {
      const mockError = new Error('Unexpected error');
      mockAxios.get.mockRejectedValue(mockError);
      
      await expect(apiService.get('/users')).rejects.toThrow('Unexpected error');
    });
  });
});