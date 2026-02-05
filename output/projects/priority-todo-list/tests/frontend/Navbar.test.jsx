jsx
// Navbar.test.jsx
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Navbar from './Navbar'; // Adjust import path as needed

// Mock the useNavigate hook if using react-router-dom
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => jest.fn(),
}));

describe('Navbar Component', () => {
  const defaultProps = {
    logo: 'My App',
    navItems: [
      { id: 'home', label: 'Home', href: '/' },
      { id: 'about', label: 'About', href: '/about' },
      { id: 'contact', label: 'Contact', href: '/contact' },
    ],
    user: null,
    onLogout: jest.fn(),
    onLogin: jest.fn(),
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders correctly with default props', () => {
    render(<Navbar {...defaultProps} />);
    
    // Check that the logo is rendered
    expect(screen.getByText(defaultProps.logo)).toBeInTheDocument();
    
    // Check that all navigation items are rendered
    defaultProps.navItems.forEach(item => {
      expect(screen.getByRole('link', { name: item.label })).toBeInTheDocument();
    });
    
    // Check that login button is visible
    expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
  });

  test('renders user profile when user is provided', () => {
    const user = { name: 'John Doe', email: 'john@example.com' };
    render(<Navbar {...defaultProps} user={user} />);
    
    // Check that user profile elements are rendered
    expect(screen.getByText(user.name)).toBeInTheDocument();
    expect(screen.getByText(user.email)).toBeInTheDocument();
    
    // Check that logout button is visible
    expect(screen.getByRole('button', { name: /logout/i })).toBeInTheDocument();
  });

  test('handles login click correctly', async () => {
    render(<Navbar {...defaultProps} />);
    
    const loginButton = screen.getByRole('button', { name: /login/i });
    
    // Click the login button
    await userEvent.click(loginButton);
    
    // Verify that onLogin was called
    expect(defaultProps.onLogin).toHaveBeenCalledTimes(1);
  });

  test('handles logout click correctly', async () => {
    const user = { name: 'John Doe', email: 'john@example.com' };
    render(<Navbar {...defaultProps} user={user} />);
    
    const logoutButton = screen.getByRole('button', { name: /logout/i });
    
    // Click the logout button
    await userEvent.click(logoutButton);
    
    // Verify that onLogout was called
    expect(defaultProps.onLogout).toHaveBeenCalledTimes(1);
  });

  test('navigates to correct links when clicked', async () => {
    render(<Navbar {...defaultProps} />);
    
    // Click on Home link
    const homeLink = screen.getByRole('link', { name: 'Home' });
    await userEvent.click(homeLink);
    
    // Since we're mocking useNavigate, we can't verify actual navigation
    // But we can check that the link exists and has correct attributes
    expect(homeLink).toHaveAttribute('href', '/');
    
    // Click on About link
    const aboutLink = screen.getByRole('link', { name: 'About' });
    await userEvent.click(aboutLink);
    expect(aboutLink).toHaveAttribute('href', '/about');
  });

  test('conditional rendering works correctly', () => {
    // Test with no user - should show login button
    render(<Navbar {...defaultProps} user={null} />);
    expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /logout/i })).not.toBeInTheDocument();
    
    // Test with user - should show user profile and logout button
    const user = { name: 'Jane Smith', email: 'jane@example.com' };
    render(<Navbar {...defaultProps} user={user} />);
    expect(screen.getByText(user.name)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /logout/i })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /login/i })).not.toBeInTheDocument();
  });

  test('accessibility attributes are present', () => {
    render(<Navbar {...defaultProps} />);
    
    // Check that logo has appropriate aria-label
    const logoElement = screen.getByText(defaultProps.logo);
    expect(logoElement).toHaveAttribute('aria-label', 'Logo');
    
    // Check that navigation has role="navigation"
    const navElement = screen.getByRole('navigation');
    expect(navElement).toBeInTheDocument();
    
    // Check that navigation items have proper roles and labels
    defaultProps.navItems.forEach(item => {
      const navItem = screen.getByRole('link', { name: item.label });
      expect(navItem).toBeInTheDocument();
      expect(navItem).toHaveAttribute('href', item.href);
    });
    
    // Check that login button has appropriate aria-label
    const loginButton = screen.getByRole('button', { name: /login/i });
    expect(loginButton).toHaveAttribute('aria-label', 'Login');
  });

  test('handles empty nav items gracefully', () => {
    const propsWithEmptyNav = {
      ...defaultProps,
      navItems: [],
    };
    
    render(<Navbar {...propsWithEmptyNav} />);
    
    // Should still render logo and login button
    expect(screen.getByText(defaultProps.logo)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
    
    // Should not render any navigation links
    expect(screen.queryByRole('link')).not.toBeInTheDocument();
  });

  test('handles undefined user gracefully', () => {
    render(<Navbar {...defaultProps} user={undefined} />);
    
    // Should behave same as null user
    expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /logout/i })).not.toBeInTheDocument();
  });

  test('handles null user gracefully', () => {
    render(<Navbar {...defaultProps} user={null} />);
    
    // Should show login button
    expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /logout/i })).not.toBeInTheDocument();
  });

  test('handles invalid navigation items gracefully', () => {
    const invalidNavItems = [
      { id: 'invalid', label: '', href: '' }, // Empty label
      { id: 'missing-href', label: 'Missing Href' }, // Missing href
    ];
    
    const propsWithInvalidNav = {
      ...defaultProps,
      navItems: invalidNavItems,
    };
    
    render(<Navbar {...propsWithInvalidNav} />);
    
    // Should render without crashing
    expect(screen.getByText(defaultProps.logo)).toBeInTheDocument();
  });

  test('handles click events on navigation items', async () => {
    render(<Navbar {...defaultProps} />);
    
    // Simulate clicking a navigation item
    const aboutLink = screen.getByRole('link', { name: 'About' });
    await userEvent.click(aboutLink);
    
    // Verify the element was clicked (no crash)
    expect(aboutLink).toBeInTheDocument();
  });

  test('renders with custom className', () => {
    const customClassName = 'custom-navbar';
    render(<Navbar {...defaultProps} className={customClassName} />);
    
    const navbarElement = screen.getByRole('navigation');
    expect(navbarElement).toHaveClass(customClassName);
  });

  test('handles special characters in navigation labels', () => {
    const specialNavItems = [
      { id: 'special', label: 'Special & Important', href: '/special' },
      { id: 'unicode', label: 'Unicode: café', href: '/unicode' },
    ];
    
    render(<Navbar {...defaultProps} navItems={specialNavItems} />);
    
    // Should render without issues
    expect(screen.getByRole('link', { name: 'Special & Important' })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: 'Unicode: café' })).toBeInTheDocument();
  });

  test('maintains accessibility when user is logged in', () => {
    const user = { name: 'Test User', email: 'test@example.com' };
    render(<Navbar {...defaultProps} user={user} />);
    
    // Check that user profile elements are accessible
    expect(screen.getByText(user.name)).toBeInTheDocument();
    expect(screen.getByText(user.email)).toBeInTheDocument();
    
    // Check that logout button is accessible
    const logoutButton = screen.getByRole('button', { name: /logout/i });
    expect(logoutButton).toBeInTheDocument();
    expect(logoutButton).toHaveAttribute('aria-label', 'Logout');
  });

  test('handles rapid successive clicks', async () => {
    render(<Navbar {...defaultProps} />);
    
    const loginButton = screen.getByRole('button', { name: /login/i });
    
    // Simulate rapid clicks
    await userEvent.click(loginButton);
    await userEvent.click(loginButton);
    await userEvent.click(loginButton);
    
    // Should handle multiple clicks without errors
    expect(defaultProps.onLogin).toHaveBeenCalledTimes(3);
  });
});