import React from 'react';
import PropTypes from 'prop-types';

/**
 * LoadingSpinner component displays a circular loading indicator
 * @param {Object} props - Component props
 * @param {string} [props.size='md'] - Size of the spinner ('sm', 'md', 'lg')
 * @param {string} [props.color='blue'] - Color of the spinner ('blue', 'gray', 'red', 'green', 'yellow')
 * @param {boolean} [props.visible=true] - Whether the spinner is visible
 * @param {string} [props.label='Loading...'] - Accessible label for screen readers
 * @param {string} [props.className=''] - Additional CSS classes
 * @returns {JSX.Element} LoadingSpinner component
 */
const LoadingSpinner = ({
  size = 'md',
  color = 'blue',
  visible = true,
  label = 'Loading...',
  className = ''
}) => {
  // Size mapping for Tailwind classes
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12'
  };

  // Color mapping for Tailwind classes
  const colorClasses = {
    blue: 'text-blue-500',
    gray: 'text-gray-500',
    red: 'text-red-500',
    green: 'text-green-500',
    yellow: 'text-yellow-500'
  };

  // Return null if not visible
  if (!visible) {
    return null;
  }

  return (
    <div 
      className={`flex items-center justify-center ${className}`}
      role="status"
      aria-label={label}
    >
      <svg
        className={`${sizeClasses[size]} ${colorClasses[color]} animate-spin`}
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        aria-hidden="true"
      >
        <circle
          className="opacity-25"
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          strokeWidth="4"
        ></circle>
        <path
          className="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
        ></path>
      </svg>
      <span className="sr-only">{label}</span>
    </div>
  );
};

// PropTypes for type checking
LoadingSpinner.propTypes = {
  size: PropTypes.oneOf(['sm', 'md', 'lg']),
  color: PropTypes.oneOf(['blue', 'gray', 'red', 'green', 'yellow']),
  visible: PropTypes.bool,
  label: PropTypes.string,
  className: PropTypes.string
};

export default LoadingSpinner;