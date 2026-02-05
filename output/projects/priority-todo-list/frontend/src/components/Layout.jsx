import React, { useState } from 'react';
import PropTypes from 'prop-types';

/**
 * Layout component with Header, Sidebar (optional), and Footer
 * @param {Object} props - Component props
 * @param {React.ReactNode} props.children - Main content to render
 * @param {React.ReactNode} props.header - Header content
 * @param {React.ReactNode} props.sidebar - Sidebar content (optional)
 * @param {React.ReactNode} props.footer - Footer content
 * @param {boolean} props.hasSidebar - Whether to show sidebar
 * @param {string} props.sidebarPosition - Position of sidebar ('left' or 'right')
 * @param {string} props.className - Additional CSS classes
 * @returns {JSX.Element} Layout component
 */
const Layout = ({
  children,
  header,
  sidebar,
  footer,
  hasSidebar = false,
  sidebarPosition = 'left',
  className = ''
}) => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  /**
   * Toggle sidebar visibility on mobile
   */
  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  return (
    <div className={`flex flex-col min-h-screen ${className}`}>
      {/* Header */}
      <header 
        className="bg-white shadow-md py-4 px-6 z-10"
        role="banner"
        aria-label="Main header"
      >
        {header}
      </header>

      {/* Main Content Area */}
      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar */}
        {hasSidebar && (
          <>
            {/* Mobile sidebar overlay */}
            {isSidebarOpen && (
              <div 
                className="fixed inset-0 bg-black bg-opacity-50 z-20 lg:hidden"
                onClick={toggleSidebar}
                aria-hidden="true"
              />
            )}

            {/* Sidebar */}
            <aside 
              className={`
                fixed lg:static z-30 h-full bg-white shadow-lg transform transition-transform duration-300 ease-in-out
                ${sidebarPosition === 'left' ? 'left-0' : 'right-0'}
                ${isSidebarOpen ? 'translate-x-0' : sidebarPosition === 'left' ? '-translate-x-full' : 'translate-x-full'}
                lg:translate-x-0 lg:w-64 w-64
              `}
              role="complementary"
              aria-label="Main navigation"
            >
              <div className="h-full flex flex-col">
                {/* Sidebar header for mobile */}
                <div className="lg:hidden p-4 border-b">
                  <button
                    onClick={toggleSidebar}
                    className="text-gray-500 hover:text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 rounded"
                    aria-label="Close sidebar"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
                
                {/* Sidebar content */}
                <div className="flex-1 overflow-y-auto p-4">
                  {sidebar}
                </div>
              </div>
            </aside>

            {/* Sidebar toggle button for mobile */}
            <div className="fixed top-16 left-4 z-20 lg:hidden">
              <button
                onClick={toggleSidebar}
                className="bg-white rounded-full p-2 shadow-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                aria-label={isSidebarOpen ? "Close sidebar" : "Open sidebar"}
                aria-expanded={isSidebarOpen}
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
            </div>
          </>
        )}

        {/* Main content */}
        <main 
          className={`
            flex-1 overflow-y-auto p-4
            ${hasSidebar ? 'lg:ml-0' : ''}
            ${sidebarPosition === 'right' && hasSidebar ? 'lg:mr-64' : ''}
          `}
          role="main"
          aria-label="Main content"
        >
          {children}
        </main>
      </div>

      {/* Footer */}
      <footer 
        className="bg-white border-t py-6 px-4 z-10"
        role="contentinfo"
        aria-label="Site footer"
      >
        {footer}
      </footer>
    </div>
  );
};

// PropTypes for type checking
Layout.propTypes = {
  children: PropTypes.node.isRequired,
  header: PropTypes.node,
  sidebar: PropTypes.node,
  footer: PropTypes.node,
  hasSidebar: PropTypes.bool,
  sidebarPosition: PropTypes.oneOf(['left', 'right']),
  className: PropTypes.string
};

export default Layout;