import React, { useState, useEffect, useRef } from 'react';
import PropTypes from 'prop-types';

/**
 * Modal component with overlay
 * @param {Object} props - Component props
 * @param {boolean} props.isOpen - Controls modal visibility
 * @param {Function} props.onClose - Callback function when modal is closed
 * @param {string} props.title - Modal title text
 * @param {ReactNode} props.children - Modal content
 * @param {string} props.className - Additional CSS classes
 * @param {boolean} props.closeOnOverlayClick - Whether to close on overlay click
 * @param {boolean} props.closeOnEscape - Whether to close on Escape key press
 * @param {string} props.size - Modal size ('sm', 'md', 'lg', 'xl', 'full')
 * @returns {JSX.Element} Modal component
 */
const Modal = ({
  isOpen,
  onClose,
  title,
  children,
  className = '',
  closeOnOverlayClick = true,
  closeOnEscape = true,
  size = 'md'
}) => {
  const [isMounted, setIsMounted] = useState(false);
  const modalRef = useRef(null);

  // Set mounted state for smooth transitions
  useEffect(() => {
    if (isOpen) {
      setIsMounted(true);
    } else {
      const timer = setTimeout(() => setIsMounted(false), 300);
      return () => clearTimeout(timer);
    }
  }, [isOpen]);

  // Handle escape key press
  useEffect(() => {
    const handleEscape = (event) => {
      if (closeOnEscape && event.key === 'Escape' && isOpen) {
        onClose();
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [onClose, isOpen, closeOnEscape]);

  // Handle click outside modal
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        closeOnOverlayClick &&
        modalRef.current &&
        !modalRef.current.contains(event.target) &&
        isOpen
      ) {
        onClose();
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [onClose, isOpen, closeOnOverlayClick]);

  // Prevent body scroll when modal is open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }

    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isOpen]);

  if (!isMounted) return null;

  // Size classes mapping
  const sizeClasses = {
    sm: 'max-w-md',
    md: 'max-w-lg',
    lg: 'max-w-2xl',
    xl: 'max-w-4xl',
    full: 'max-w-full'
  };

  return (
    <div
      className={`fixed inset-0 z-50 flex items-center justify-center p-4 transition-opacity duration-300 ${
        isOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'
      }`}
      role="dialog"
      aria-modal="true"
      aria-labelledby={title ? "modal-title" : undefined}
    >
      {/* Backdrop */}
      <div
        className={`absolute inset-0 bg-black transition-opacity duration-300 ${
          isOpen ? 'opacity-50' : 'opacity-0'
        }`}
        aria-hidden="true"
      />

      {/* Modal Content */}
      <div
        ref={modalRef}
        className={`relative bg-white rounded-lg shadow-xl w-full ${sizeClasses[size]} ${className}`}
        tabIndex="-1"
        role="document"
      >
        {/* Header */}
        {(title || onClose) && (
          <div className="flex items-center justify-between p-4 border-b border-gray-200">
            {title && (
              <h3
                id="modal-title"
                className="text-lg font-medium text-gray-900"
              >
                {title}
              </h3>
            )}
            {onClose && (
              <button
                onClick={onClose}
                type="button"
                className="text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 rounded-full p-1"
                aria-label="Close modal"
              >
                <svg
                  className="h-6 w-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            )}
          </div>
        )}

        {/* Body */}
        <div className="p-4 sm:p-6">
          {children}
        </div>

        {/* Footer */}
        {onClose && (
          <div className="flex justify-end p-4 border-t border-gray-200">
            <button
              onClick={onClose}
              type="button"
              className="inline-flex justify-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Close
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

// PropTypes for type checking
Modal.propTypes = {
  isOpen: PropTypes.bool.isRequired,
  onClose: PropTypes.func,
  title: PropTypes.string,
  children: PropTypes.node.isRequired,
  className: PropTypes.string,
  closeOnOverlayClick: PropTypes.bool,
  closeOnEscape: PropTypes.bool,
  size: PropTypes.oneOf(['sm', 'md', 'lg', 'xl', 'full'])
};

export default Modal;