import React from 'react';
import PropTypes from 'prop-types';

/**
 * Reusable Button component with multiple variants
 * @param {Object} props - Component props
 * @param {'primary' | 'secondary' | 'danger'} props.variant - Button variant style
 * @param {boolean} props.disabled - Whether the button is disabled
 * @param {string} props.className - Additional CSS classes
 * @param {React.ReactNode} props.children - Button content
 * @param {string} props.type - Button type (button, submit, reset)
 * @param {Function} props.onClick - Click handler function
 * @param {string} props ariaLabel - ARIA label for accessibility
 * @returns {JSX.Element} Rendered button component
 */
const Button = ({
  variant = 'primary',
  disabled = false,
  className = '',
  children,
  type = 'button',
  onClick,
  ariaLabel,
  ...rest
}) => {
  // Define base styles
  const baseStyles = 'inline-flex items-center justify-center px-4 py-2 text-sm font-medium rounded-md transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed';

  // Define variant-specific styles
  const variantStyles = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500',
    secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300 focus:ring-gray-500',
    danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500'
  };

  // Combine all styles
  const combinedClassName = `${baseStyles} ${variantStyles[variant]} ${className}`;

  return (
    <button
      type={type}
      className={combinedClassName}
      disabled={disabled}
      onClick={onClick}
      aria-label={ariaLabel}
      {...rest}
    >
      {children}
    </button>
  );
};

// PropTypes for type checking
Button.propTypes = {
  variant: PropTypes.oneOf(['primary', 'secondary', 'danger']),
  disabled: PropTypes.bool,
  className: PropTypes.string,
  children: PropTypes.node.isRequired,
  type: PropTypes.oneOf(['button', 'submit', 'reset']),
  onClick: PropTypes.func,
  ariaLabel: PropTypes.string
};

export default Button;