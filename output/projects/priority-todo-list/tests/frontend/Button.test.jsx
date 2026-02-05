jsx
import React from 'react';
import { render, screen, fireEvent, userEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import Button from './Button';

// Mock any external dependencies if needed
jest.mock('./Button', () => {
  return jest.fn((props) => (
    <button 
      data-testid="button"
      {...props}
      onClick={props.onClick}
    >
      {props.children}
    </button>
  ));
});

describe('Button Component', () => {
  // Test 1: Component renders correctly
  test('renders button with correct text content', () => {
    const buttonText = 'Click me';
    render(<Button>{buttonText}</Button>);
    
    const button = screen.getByTestId('button');
    expect(button).toBeInTheDocument();
    expect(button).toHaveTextContent(buttonText);
  });

  // Test 2: Props are handled properly
  test('renders with different variants and sizes', () => {
    const variants = ['primary', 'secondary', 'danger', 'outline'];
    const sizes = ['small', 'medium', 'large'];

    variants.forEach(variant => {
      render(<Button variant={variant}>Test</Button>);
      const button = screen.getByTestId('button');
      expect(button).toHaveClass(`btn-${variant}`);
    });

    sizes.forEach(size => {
      render(<Button size={size}>Test</Button>);
      const button = screen.getByTestId('button');
      expect(button).toHaveClass(`btn-${size}`);
    });
  });

  test('handles disabled state correctly', () => {
    render(<Button disabled>Disabled Button</Button>);
    const button = screen.getByTestId('button');
    expect(button).toBeDisabled();
    expect(button).toHaveAttribute('disabled');
  });

  test('handles loading state correctly', () => {
    render(<Button loading>Loading...</Button>);
    const button = screen.getByTestId('button');
    expect(button).toHaveAttribute('aria-busy', 'true');
    expect(screen.getByRole('status')).toBeInTheDocument();
  });

  test('applies custom className', () => {
    render(<Button className="custom-class">Custom Button</Button>);
    const button = screen.getByTestId('button');
    expect(button).toHaveClass('custom-class');
  });

  // Test 3: User interactions work (clicks, input changes)
  test('calls onClick handler when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click Me</Button>);
    
    const button = screen.getByTestId('button');
    fireEvent.click(button);
    
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  test('supports keyboard interactions', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Keyboard Button</Button>);
    
    const button = screen.getByTestId('button');
    
    // Test Enter key
    fireEvent.keyDown(button, { key: 'Enter' });
    expect(handleClick).toHaveBeenCalledTimes(1);
    
    // Reset mock
    handleClick.mockClear();
    
    // Test Space key
    fireEvent.keyDown(button, { key: ' ' });
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  test('handles focus and blur events', () => {
    const handleFocus = jest.fn();
    const handleBlur = jest.fn();
    render(
      <Button 
        onFocus={handleFocus} 
        onBlur={handleBlur}
      >
        Focusable Button
      </Button>
    );
    
    const button = screen.getByTestId('button');
    
    fireEvent.focus(button);
    expect(handleFocus).toHaveBeenCalledTimes(1);
    
    fireEvent.blur(button);
    expect(handleBlur).toHaveBeenCalledTimes(1);
  });

  // Test 4: Conditional rendering works
  test('conditionally renders children based on props', () => {
    // Test with icon prop
    render(<Button icon="icon">Button with Icon</Button>);
    const button = screen.getByTestId('button');
    expect(button).toBeInTheDocument();
    
    // Test without icon
    render(<Button>Button without Icon</Button>);
    const buttonWithoutIcon = screen.getByTestId('button');
    expect(buttonWithoutIcon).toBeInTheDocument();
  });

  test('shows loading spinner when loading is true', () => {
    render(<Button loading>Submit</Button>);
    const button = screen.getByTestId('button');
    
    expect(button).toHaveAttribute('aria-busy', 'true');
    expect(screen.getByRole('status')).toBeInTheDocument();
    
    // Ensure the button text is still visible
    expect(button).toHaveTextContent('Submit');
  });

  test('hides loading spinner when loading is false', () => {
    render(<Button loading={false}>Submit</Button>);
    const button = screen.getByTestId('button');
    
    expect(button).not.toHaveAttribute('aria-busy', 'true');
    expect(screen.queryByRole('status')).not.toBeInTheDocument();
  });

  // Test 5: Accessibility attributes present
  test('has proper aria attributes', () => {
    render(<Button aria-label="Close dialog">Close</Button>);
    const button = screen.getByTestId('button');
    
    expect(button).toHaveAttribute('aria-label', 'Close dialog');
    expect(button).toHaveAttribute('role', 'button');
  });

  test('has accessible name when no aria-label provided', () => {
    render(<Button>Submit</Button>);
    const button = screen.getByTestId('button');
    
    // Should have accessible name from text content
    expect(button).toHaveAccessibleName('Submit');
  });

  test('has proper role attribute', () => {
    render(<Button>Test Button</Button>);
    const button = screen.getByTestId('button');
    
    expect(button).toHaveAttribute('role', 'button');
  });

  test('supports aria-describedby for complex interactions', () => {
    render(
      <Button 
        aria-describedby="help-text"
        aria-label="Submit form"
      >
        Submit
      </Button>
    );
    
    const button = screen.getByTestId('button');
    expect(button).toHaveAttribute('aria-describedby', 'help-text');
    expect(button).toHaveAttribute('aria-label', 'Submit form');
  });

  // Edge Cases
  test('handles null/undefined children gracefully', () => {
    render(<Button>{null}</Button>);
    const button = screen.getByTestId('button');
    expect(button).toBeInTheDocument();
    
    render(<Button>{undefined}</Button>);
    const button2 = screen.getByTestId('button');
    expect(button2).toBeInTheDocument();
  });

  test('handles empty string children', () => {
    render(<Button></Button>);
    const button = screen.getByTestId('button');
    expect(button).toBeInTheDocument();
    expect(button).toHaveTextContent('');
  });

  test('handles complex children', () => {
    render(
      <Button>
        <span data-testid="icon">✓</span>
        <span data-testid="text">Save</span>
      </Button>
    );
    
    const button = screen.getByTestId('button');
    expect(button).toBeInTheDocument();
    expect(screen.getByTestId('icon')).toBeInTheDocument();
    expect(screen.getByTestId('text')).toBeInTheDocument();
  });

  test('handles very long text content', () => {
    const longText = 'A'.repeat(1000);
    render(<Button>{longText}</Button>);
    const button = screen.getByTestId('button');
    expect(button).toHaveTextContent(longText);
  });

  test('maintains proper styling classes with multiple props', () => {
    render(
      <Button 
        variant="primary" 
        size="large" 
        disabled
        loading
        className="extra-class"
      >
        Complex Button
      </Button>
    );
    
    const button = screen.getByTestId('button');
    expect(button).toHaveClass('btn-primary');
    expect(button).toHaveClass('btn-large');
    expect(button).toHaveClass('extra-class');
    expect(button).toBeDisabled();
    expect(button).toHaveAttribute('aria-busy', 'true');
  });

  // Performance and behavior tests
  test('does not re-render unnecessarily', () => {
    const { rerender } = render(<Button>Initial</Button>);
    const initialButton = screen.getByTestId('button');
    
    rerender(<Button>Updated</Button>);
    const updatedButton = screen.getByTestId('button');
    
    // Should be the same element
    expect(initialButton).toBe(updatedButton);
    expect(updatedButton).toHaveTextContent('Updated');
  });

  test('handles event propagation correctly', () => {
    const parentHandler = jest.fn();
    const childHandler = jest.fn();
    
    render(
      <div onClick={parentHandler}>
        <Button onClick={childHandler}>Child Button</Button>
      </div>
    );
    
    const button = screen.getByTestId('button');
    fireEvent.click(button);
    
    expect(childHandler).toHaveBeenCalledTimes(1);
    expect(parentHandler).toHaveBeenCalledTimes(1);
  });
});