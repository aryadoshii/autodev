import axios from 'axios';

// Create axios instance with base URL
const api = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL || 'http://localhost:3001/api',
  timeout: 10000,
});

// Request interceptor to attach JWT token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle 401 errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Clear token on 401 error
      localStorage.removeItem('token');
      // Optionally redirect to login page
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth service
const auth = {
  /**
   * Login user with email and password
   * @param {string} email - User email
   * @param {string} password - User password
   * @returns {Promise<Object>} Login response
   */
  async login(email, password) {
    try {
      const response = await api.post('/auth/login', { email, password });
      const { token, user } = response.data;
      
      // Store token in localStorage
      localStorage.setItem('token', token);
      
      return { token, user };
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Login failed');
    }
  },

  /**
   * Register new user
   * @param {Object} userData - User registration data
   * @returns {Promise<Object>} Registration response
   */
  async register(userData) {
    try {
      const response = await api.post('/auth/register', userData);
      const { token, user } = response.data;
      
      // Store token in localStorage
      localStorage.setItem('token', token);
      
      return { token, user };
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Registration failed');
    }
  },

  /**
   * Logout user
   * @returns {void}
   */
  logout() {
    localStorage.removeItem('token');
  }
};

// Users service
const users = {
  /**
   * Get all users
   * @returns {Promise<Array>} List of users
   */
  async getAll() {
    try {
      const response = await api.get('/users');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch users');
    }
  },

  /**
   * Get user by ID
   * @param {number|string} id - User ID
   * @returns {Promise<Object>} User object
   */
  async getById(id) {
    try {
      const response = await api.get(`/users/${id}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch user');
    }
  },

  /**
   * Create new user
   * @param {Object} data - User data
   * @returns {Promise<Object>} Created user
   */
  async create(data) {
    try {
      const response = await api.post('/users', data);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to create user');
    }
  },

  /**
   * Update user
   * @param {number|string} id - User ID
   * @param {Object} data - User data to update
   * @returns {Promise<Object>} Updated user
   */
  async update(id, data) {
    try {
      const response = await api.put(`/users/${id}`, data);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to update user');
    }
  },

  /**
   * Delete user
   * @param {number|string} id - User ID
   * @returns {Promise<void>}
   */
  async delete(id) {
    try {
      await api.delete(`/users/${id}`);
      return true;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to delete user');
    }
  }
};

// Export the API services
export { api, auth, users };

// Default export for convenience
export default { api, auth, users };