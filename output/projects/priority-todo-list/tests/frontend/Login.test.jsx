jsx
// Login.test.jsx
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter as Router } from 'react-router-dom';
import { act } from 'react-dom/test-utils';
import Login from './Login'; // Adjust import path as needed

// Mock the API service
jest.mock('../services/api', () => ({
  login: jest.fn()
}));

// Mock react-router-dom's useNavigate
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => jest.fn()
}));

describe('Login Component', () => {
  const mockNavigate = jest.fn();
  const mockLoginService = require('../services/api').login;

  beforeEach(() => {
    jest.clearAllMocks();
    // Mock useNavigate to return our mock function
    jest.mock('react-router-dom', () => ({
      ...jest.requireActual('react-router-dom'),
      useNavigate: () => mockNavigate
    }));
  });

  test('renders login form with email and password fields', () => {
    render(
      <Router>
        <Login />
      </Router>
    );

    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
  });

  test('form validation shows errors for empty fields', async () => {
    render(
      <Router>
        <Login />
      </Router>
    );

    const submitButton = screen.getByRole('button', { name: /login/i });
    
    // Submit without filling any fields
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/email is required/i)).toBeInTheDocument();
      expect(screen.getByText(/password is required/i)).toBeInTheDocument();
    });
  });

  test('form validation shows error for invalid email format', async () => {
    render(
      <Router>
        <Login />
      </Router>
    );

    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole('button', { name: /login/i });

    // Fill with invalid email
    fireEvent.change(emailInput, { target: { value: 'invalid-email' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/please enter a valid email address/i)).toBeInTheDocument();
    });
  });

  test('successful login with valid credentials', async () => {
    // Mock successful API response
    mockLoginService.mockResolvedValueOnce({
      data: { token: 'fake-jwt-token' }
    });

    render(
      <Router>
        <Login />
      </Router>
    );

    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole('button', { name: /login/i });

    // Fill form with valid data
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });
    fireEvent.click(submitButton);

    // Wait for loading state to appear and then disappear
    await waitFor(() => {
      expect(screen.getByText(/logging in/i)).toBeInTheDocument();
    });

    await waitFor(() => {
      expect(mockLoginService).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123'
      });
      expect(mockNavigate).toHaveBeenCalledWith('/dashboard');
    });
  });

  test('failed login with wrong credentials', async () => {
    // Mock failed API response
    mockLoginService.mockRejectedValueOnce({
      response: {
        status: 401,
        data: { message: 'Invalid credentials' }
      }
    });

    render(
      <Router>
        <Login />
      </Router>
    );

    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole('button', { name: /login/i });

    // Fill form with invalid data
    fireEvent.change(emailInput, { target: { value: 'wrong@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'wrongpassword' } });
    fireEvent.click(submitButton);

    // Wait for error to appear
    await waitFor(() => {
      expect(screen.getByText(/invalid credentials/i)).toBeInTheDocument();
    });

    expect(mockLoginService).toHaveBeenCalledWith({
      email: 'wrong@example.com',
      password: 'wrongpassword'
    });
  });

  test('redirects to dashboard after successful login', async () => {
    mockLoginService.mockResolvedValueOnce({
      data: { token: 'fake-jwt-token' }
    });

    render(
      <Router>
        <Login />
      </Router>
    );

    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole('button', { name: /login/i });

    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockNavigate).toHaveBeenCalledWith('/dashboard');
    });
  });

  test('shows loading state during login process', async () => {
    // Mock API call to take some time
    mockLoginService.mockImplementationOnce(() => 
      new Promise(resolve => setTimeout(() => resolve({ data: { token: 'token' } }), 1000))
    );

    render(
      <Router>
        <Login />
      </Router>
    );

    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole('button', { name: /login/i });

    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });
    fireEvent.click(submitButton);

    // Check that loading text appears immediately
    expect(screen.getByText(/logging in/i)).toBeInTheDocument();

    // Wait for completion
    await waitFor(() => {
      expect(screen.queryByText(/logging in/i)).not.toBeInTheDocument();
    });
  });

  test('displays error messages for various failure scenarios', async () => {
    // Test network error
    mockLoginService.mockRejectedValueOnce({
      message: 'Network Error'
    });

    render(
      <Router>
        <Login />
      </Router>
    );

    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole('button', { name: /login/i });

    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/network error/i)).toBeInTheDocument();
    });

    // Reset mocks
    mockLoginService.mockClear();

    // Test server error with custom message
    mockLoginService.mockRejectedValueOnce({
      response: {
        status: 500,
        data: { message: 'Server Error' }
      }
    });

    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/server error/i)).toBeInTheDocument();
    });
  });
});