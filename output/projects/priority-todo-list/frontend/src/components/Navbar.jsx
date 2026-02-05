import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';

/**
 * Navbar component for navigation with logo, links, and user menu
 * @param {Object} props - Component props
 * @param {string} props.logoSrc - URL to the logo image
 * @param {string} props.logoAlt - Alt text for the logo
 * @param {Array} props.links - Array of link objects with text and href properties
 * @param {Array} props.userMenuItems - Array of menu items for user dropdown
 * @param {Function} props.onLogoClick - Callback function when logo is clicked
 * @param {Function} props.onLinkClick - Callback function when a link is clicked
 * @param {Function} props.onMenuItemClick - Callback function when a menu item is clicked
 * @returns {JSX.Element} Navbar component
 */
const Navbar = ({
  logoSrc,
  logoAlt,
  links,
  userMenuItems,
  onLogoClick,
  onLinkClick,
  onMenuItemClick
}) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  // Handle scroll effect for navbar
  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Close menus when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (!event.target.closest('.navbar-container')) {
        setIsMenuOpen(false);
        setIsUserMenuOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  /**
   * Toggle mobile menu visibility
   */
  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  /**
   * Toggle user menu visibility
   */
  const toggleUserMenu = () => {
    setIsUserMenuOpen(!isUserMenuOpen);
  };

  /**
   * Handle link click with optional callback
   * @param {Object} link - Link object
   * @param {Event} event - Click event
   */
  const handleLinkClick = (link, event) => {
    if (onLinkClick) {
      onLinkClick(link, event);
    }
    setIsMenuOpen(false); // Close mobile menu after selection
  };

  /**
   * Handle menu item click with optional callback
   * @param {Object} item - Menu item object
   * @param {Event} event - Click event
   */
  const handleMenuItemClick = (item, event) => {
    if (onMenuItemClick) {
      onMenuItemClick(item, event);
    }
    setIsUserMenuOpen(false); // Close user menu after selection
  };

  return (
    <nav 
      className={`fixed w-full z-50 transition-all duration-300 ${
        scrolled ? 'bg-white shadow-md py-2' : 'bg-white/90 backdrop-blur-sm py-4'
      } navbar-container`}
      role="navigation"
      aria-label="Main navigation"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center">
          {/* Logo */}
          <div className="flex items-center">
            <button
              onClick={onLogoClick}
              className="flex items-center focus:outline-none focus:ring-2 focus:ring-blue-500 rounded"
              aria-label={`Go to home page`}
            >
              {logoSrc && (
                <img 
                  src={logoSrc} 
                  alt={logoAlt || 'Company Logo'} 
                  className="h-8 w-auto"
                />
              )}
            </button>
          </div>

          {/* Desktop Links */}
          <div className="hidden md:flex items-center space-x-8">
            {links?.map((link, index) => (
              <a
                key={index}
                href={link.href}
                onClick={(e) => handleLinkClick(link, e)}
                className="text-gray-700 hover:text-blue-600 font-medium transition-colors duration-200 px-3 py-2 rounded-md text-sm"
                aria-label={`Navigate to ${link.text}`}
              >
                {link.text}
              </a>
            ))}
          </div>

          {/* User Menu */}
          <div className="hidden md:flex items-center">
            <div className="relative">
              <button
                onClick={toggleUserMenu}
                className="flex items-center space-x-2 focus:outline-none focus:ring-2 focus:ring-blue-500 rounded-md"
                aria-haspopup="true"
                aria-expanded={isUserMenuOpen}
                aria-label="User menu"
              >
                <div className="h-8 w-8 rounded-full bg-blue-500 flex items-center justify-center text-white font-medium">
                  U
                </div>
                <span className="text-gray-700 font-medium hidden lg:block">User</span>
              </button>

              {/* User Menu Dropdown */}
              {isUserMenuOpen && (
                <div 
                  className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-50 border border-gray-200"
                  role="menu"
                >
                  {userMenuItems?.map((item, index) => (
                    <button
                      key={index}
                      onClick={(e) => handleMenuItemClick(item, e)}
                      className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 focus:outline-none focus:bg-gray-100 transition-colors duration-150"
                      role="menuitem"
                      aria-label={item.text}
                    >
                      {item.text}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={toggleMenu}
              className="inline-flex items-center justify-center p-2 rounded-md text-gray-700 hover:text-blue-600 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500"
              aria-expanded="false"
              aria-label="Toggle navigation menu"
            >
              <svg
                className={`${isMenuOpen ? 'hidden' : 'block'} h-6 w-6`}
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
              <svg
                className={`${isMenuOpen ? 'block' : 'hidden'} h-6 w-6`}
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMenuOpen && (
        <div className="md:hidden">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
            {links?.map((link, index) => (
              <a
                key={index}
                href={link.href}
                onClick={(e) => handleLinkClick(link, e)}
                className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
                aria-label={`Navigate to ${link.text}`}
              >
                {link.text}
              </a>
            ))}
            
            {/* Mobile User Menu */}
            <div className="pt-4 pb-2 border-t border-gray-200">
              <div className="flex items-center px-4">
                <div className="h-10 w-10 rounded-full bg-blue-500 flex items-center justify-center text-white font-medium">
                  U
                </div>
                <div className="ml-3">
                  <p className="text-base font-medium text-gray-700">User</p>
                </div>
              </div>
              <div className="mt-2 px-4">
                {userMenuItems?.map((item, index) => (
                  <button
                    key={index}
                    onClick={(e) => handleMenuItemClick(item, e)}
                    className="block w-full text-left px-3 py-2 text-base font-medium text-gray-700 hover:text-blue-600 hover