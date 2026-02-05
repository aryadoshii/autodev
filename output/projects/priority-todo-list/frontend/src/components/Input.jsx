import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';

/**
 * Reusable Input component with validation, error handling, and accessibility features
 * @param {Object} props - Component props
 * @param {string} props.id - Unique identifier for the input
 * @param {string} props.label - Label text for the input
 * @param {string} props.type - Input type (text, email, password, etc.)
 * @param {string} props.value - Current value of the input
 * @param {function} props.onChange - Callback function when input value changes
 * @param {function} props.onBlur - Callback function when input loses focus
 * @param {string} props.placeholder - Placeholder text
 * @param {boolean} props.required - Whether the input is required
 * @param {RegExp} props.pattern - Regular expression for validation
 * @param {string} props.errorMessage - Custom error message
 * @param {string} props.className - Additional CSS classes
 * @param {boolean} props.disabled - Whether the input is disabled
 * @param {boolean} props.autoComplete - Whether to enable autocomplete
 * @returns {JSX.Element} Input component
 */
const Input = ({
  id,
  label,
  type = 'text',
  value,
  onChange,
  onBlur,
  placeholder,
  required = false,
  pattern,
  errorMessage,
  className = '',
  disabled = false,
  autoComplete = 'off'
}) => {
  const [error, setError] = useState('');
  const [touched, setTouched] = useState(false);

  // Validate input when value or touched state changes
  useEffect(() => {
    if (touched) {
      validateInput(value);
    }
  }, [value, touched]);

  /**
   * Validates the input based on required field and pattern
   * @param {string} inputValue - Current input value
   */
  const validateInput = (inputValue) => {
    let newError = '';

    if (required && !inputValue) {
      newError = `${label} is required`;
    } else if (pattern && inputValue && !pattern.test(inputValue)) {
      newError = errorMessage || `Please enter a valid ${label.toLowerCase()}`;
    }

    setError(newError);
  };

  /**
   * Handles input change event
   * @param {Object} e - Event object
   */
  const handleChange = (e) => {
    onChange(e.target.value);
  };

  /**
   * Handles input blur event
   */
  const handleBlur = () => {
    setTouched(true);
    if (onBlur) onBlur();
  };

  // Generate unique ID if not provided
  const inputId = id || `input-${Math.random().toString(36).substr(2, 9)}`;

  return (
    <div className={`mb-4 ${className}`}>
      {label && (
        <label 
          htmlFor={inputId}
          className="block text-sm font-medium text-gray-700 mb-1"
        >
          {label} {required && <span className="text-red-500">*</span>}
        </label>
      )}
      
      <input
        id={inputId}
        type={type}
        value={value}
        onChange={handleChange}
        onBlur={handleBlur}
        placeholder={placeholder}
        disabled={disabled}
        autoComplete={autoComplete}
        aria-invalid={!!error}
        aria-describedby={error ? `${inputId}-error` : undefined}
        className={`
          w-full px-3 py-2 border rounded-md shadow-sm
          focus:outline-none focus:ring-2
          ${error 
            ? 'border-red-500 focus:ring-red-500' 
            : 'border-gray-300 focus:border-blue-500 focus:ring-blue-500'
          }
          ${disabled ? 'bg-gray-100 cursor-not-allowed' : 'bg-white'}
          transition-colors duration-200
        `}
      />
      
      {error && (
        <p 
          id={`${inputId}-error`}
          className="mt-1 text-sm text-red-600"
          role="alert"
        >
          {error}
        </p>
      )}
    </div>
  );
};

// PropTypes for type checking
Input.propTypes = {
  id: PropTypes.string,
  label: PropTypes.string,
  type: PropTypes.string,
  value: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired,
  onBlur: PropTypes.func,
  placeholder: PropTypes.string,
  required: PropTypes.bool,
  pattern: PropTypes.instanceOf(RegExp),
  errorMessage: PropTypes.string,
  className: PropTypes.string,
  disabled: PropTypes.bool,
  autoComplete: PropTypes.string
};

export default Input;