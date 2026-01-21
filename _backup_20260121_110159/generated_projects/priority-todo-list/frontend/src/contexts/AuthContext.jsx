import React, { createContext, useContext, useState, useEffect } from 'react';

// Create the AuthContext
const AuthContext = createContext();

/**
 * AuthProvider component that wraps the application and provides authentication context
 * @param {Object} props - Component props
 * @param {React.ReactNode} props.children - Child components that will have access to auth context
 */
export const AuthProvider = ({ children }) => {
  // State management
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  /**
   * Load user data from localStorage on component mount
   */
  useEffect(() => {
    const loadUserFromStorage = () => {
      try {
        const storedToken = localStorage.getItem('authToken');
        const storedUser = localStorage.getItem('userData');
        
        if (storedToken && storedUser) {
          setToken(storedToken);
          setUser(JSON.parse(storedUser));
        }
      } catch (err) {
        console.error('Failed to load user data from storage:', err);
        setError('Failed to initialize authentication state');
      } finally {
        setLoading(false);
      }
    };

    loadUserFromStorage();
  }, []);

  /**
   * Login function that calls API and stores token/user data
   * @async
   * @param {string} email - User's email
   * @param {string} password - User's password
   * @returns {Promise<Object>} Login response
   */
  const login = async (email, password) => {
    try {
      setLoading(true);
      setError(null);
      
      // Simulate API call - replace with actual API endpoint
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        throw new Error(`Login failed: ${response.status}`);
      }

      const data = await response.json();
      
      // Store token and user data
      setToken(data.token);
      setUser(data.user);
      
      // Save to localStorage
      localStorage.setItem('authToken', data.token);
      localStorage.setItem('userData', JSON.stringify(data.user));
      
      return data;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  /**
   * Logout function that clears token and user data
   */
  const logout = () => {
    try {
      setToken(null);
      setUser(null);
      setError(null);
      
      // Remove from localStorage
      localStorage.removeItem('authToken');
      localStorage.removeItem('userData');
    } catch (err) {
      console.error('Logout error:', err);
      setError('Failed to logout');
    }
  };

  /**
   * Register function that calls API to create new user
   * @async
   * @param {Object} userData - User registration data
   * @returns {Promise<Object>} Registration response
   */
  const register = async (userData) => {
    try {
      setLoading(true);
      setError(null);
      
      // Simulate API call - replace with actual API endpoint
      const response = await fetch('/api/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      if (!response.ok) {
        throw new Error(`Registration failed: ${response.status}`);
      }

      const data = await response.json();
      
      // Store token and user data
      setToken(data.token);
      setUser(data.user);
      
      // Save to localStorage
      localStorage.setItem('authToken', data.token);
      localStorage.setItem('userData', JSON.stringify(data.user));
      
      return data;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Value provided to consumers of the context
  const value = {
    user,
    token,
    loading,
    error,
    isAuthenticated: !!token,
    login,
    logout,
    register,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

/**
 * Custom hook to use authentication context
 * @returns {Object} Authentication context values
 * @throws {Error} If used outside of AuthProvider
 */
export const useAuth = () => {
  const context = useContext(AuthContext);
  
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  
  return context;
};