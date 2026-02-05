import React from 'react';
import PropTypes from 'prop-types';

/**
 * Card component for displaying content in a structured container
 * @param {Object} props - Component props
 * @param {React.ReactNode} props.children - Content to be displayed inside the card
 * @param {string} props.title - Optional title for the card
 * @param {string} props.subtitle - Optional subtitle for the card
 * @param {string} props.className - Additional CSS classes for customization
 * @param {boolean} props.isClickable - Makes the card clickable with hover effects
 * @param {Function} props.onClick - Callback function when card is clicked
 * @param {string} props.role - ARIA role for accessibility
 * @param {string} props.ariaLabel - ARIA label for accessibility
 * @returns {JSX.Element} Card component
 */
const Card = ({
  children,
  title,
  subtitle,
  className = '',
  isClickable = false,
  onClick,
  role = 'region',
  ariaLabel,
  ...restProps
}) => {
  const handleClick = (event) => {
    if (onClick && !event.defaultPrevented) {
      onClick(event);
    }
  };

  // Determine if card should be clickable
  const clickableClass = isClickable ? 'cursor-pointer hover:shadow-lg transition-shadow duration-200' : '';
  
  // Build base classes
  const baseClasses = 'bg-white rounded-xl shadow-md overflow-hidden';
  const combinedClasses = `${baseClasses} ${clickableClass} ${className}`;

  return (
    <div
      className={combinedClasses}
      role={role}
      aria-label={ariaLabel}
      onClick={handleClick}
      {...restProps}
    >
      {/* Card header with title and subtitle */}
      {(title || subtitle) && (
        <div className="px-6 py-4 border-b border-gray-100">
          {title && (
            <h3 
              className="text-lg font-semibold text-gray-900 leading-tight"
              aria-level="3"
            >
              {title}
            </h3>
          )}
          {subtitle && (
            <p className="mt-1 text-sm text-gray-600">
              {subtitle}
            </p>
          )}
        </div>
      )}

      {/* Card body */}
      <div className="p-6">
        {children}
      </div>
    </div>
  );
};

// PropTypes for type checking
Card.propTypes = {
  children: PropTypes.node.isRequired,
  title: PropTypes.string,
  subtitle: PropTypes.string,
  className: PropTypes.string,
  isClickable: PropTypes.bool,
  onClick: PropTypes.func,
  role: PropTypes.string,
  ariaLabel: PropTypes.string
};

export default Card;