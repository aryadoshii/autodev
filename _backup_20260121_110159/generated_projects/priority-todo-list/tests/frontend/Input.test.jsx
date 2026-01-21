jsx
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Input from './Input';

// Mock any dependencies if needed
jest.mock('@testing-library/user-event', () => ({
  ...jest.requireActual('@testing-library/user-event'),
  click: jest.fn(),
}));

describe('Input Component', () => {
  const defaultProps = {
    id: 'test-input',
    label: 'Test Input',
    placeholder: 'Enter text...',
    value: '',
    onChange: jest.fn(),
    type: 'text',
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders correctly with default props', () => {
    render(<Input {...defaultProps} />);
    
    // Check that the input element is rendered
    const inputElement = screen.getByRole('textbox', { name: /test input/i });
    expect(inputElement).toBeInTheDocument();
    
    // Check that the label is rendered
    const labelElement = screen.getByText(/test input/i);
    expect(labelElement).toBeInTheDocument();
    
    // Check placeholder
    expect(inputElement).toHaveAttribute('placeholder', 'Enter text...');
    
    // Check initial value
    expect(inputElement).toHaveValue('');
  });

  test('renders correctly with custom props', () => {
    const customProps = {
      ...defaultProps,
      id: 'custom-input',
      label: 'Custom Label',
      placeholder: 'Custom placeholder',
      value: 'Initial value',
      disabled: true,
      required: true,
      ariaLabel: 'Custom ARIA label',
    };
    
    render(<Input {...customProps} />);
    
    const inputElement = screen.getByRole('textbox', { name: /custom label/i });
    expect(inputElement).toBeInTheDocument();
    
    // Check all custom props
    expect(inputElement).toHaveAttribute('id', 'custom-input');
    expect(inputElement).toHaveAttribute('placeholder', 'Custom placeholder');
    expect(inputElement).toHaveValue('Initial value');
    expect(inputElement).toBeDisabled();
    expect(inputElement).toBeRequired();
    expect(inputElement).toHaveAttribute('aria-label', 'Custom ARIA label');
  });

  test('handles user input changes correctly', async () => {
    const handleChange = jest.fn();
    const user = userEvent.setup();
    
    render(<Input {...defaultProps} onChange={handleChange} />);
    
    const inputElement = screen.getByRole('textbox', { name: /test input/i });
    
    // Simulate typing in the input
    await user.type(inputElement, 'Hello World');
    
    // Verify the change was called with correct value
    expect(handleChange).toHaveBeenCalledTimes(11); // 11 characters typed
    expect(inputElement).toHaveValue('Hello World');
    
    // Test with specific value
    fireEvent.change(inputElement, { target: { value: 'New Value' } });
    expect(handleChange).toHaveBeenCalledTimes(12);
    expect(inputElement).toHaveValue('New Value');
  });

  test('handles click events properly', () => {
    const handleClick = jest.fn();
    render(<Input {...defaultProps} onClick={handleClick} />);
    
    const inputElement = screen.getByRole('textbox', { name: /test input/i });
    
    // Simulate click
    fireEvent.click(inputElement);
    
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  test('conditional rendering based on props', () => {
    // Test with showLabel = false
    render(<Input {...defaultProps} showLabel={false} />);
    
    const labelElement = screen.queryByText(/test input/i);
    expect(labelElement).not.toBeInTheDocument();
    
    // Test with showLabel = true (default)
    render(<Input {...defaultProps} showLabel={true} />);
    
    const visibleLabel = screen.getByText(/test input/i);
    expect(visibleLabel).toBeInTheDocument();
  });

  test('accessibility attributes are present', () => {
    render(<Input {...defaultProps} />);
    
    const inputElement = screen.getByRole('textbox', { name: /test input/i });
    
    // Check required accessibility attributes
    expect(inputElement).toHaveAttribute('id', 'test-input');
    expect(inputElement).toHaveAttribute('aria-labelledby', 'test-input-label');
    
    // Check that label has correct htmlFor attribute
    const labelElement = screen.getByText(/test input/i);
    expect(labelElement).toHaveAttribute('htmlFor', 'test-input');
  });

  test('handles different input types', () => {
    const types = ['text', 'email', 'password', 'number', 'search'];
    
    types.forEach(type => {
      render(<Input {...defaultProps} type={type} />);
      
      const inputElement = screen.getByRole('textbox', { name: /test input/i });
      expect(inputElement).toHaveAttribute('type', type);
    });
  });

  test('handles error state and validation', () => {
    render(<Input {...defaultProps} error="This field is required" />);
    
    const inputElement = screen.getByRole('textbox', { name: /test input/i });
    
    // Should have error class or attribute
    expect(inputElement).toHaveClass('error'); // Assuming error styling
    
    // Error message should be visible
    const errorMessage = screen.getByText(/this field is required/i);
    expect(errorMessage).toBeInTheDocument();
  });

  test('handles disabled state properly', () => {
    render(<Input {...defaultProps} disabled={true} />);
    
    const inputElement = screen.getByRole('textbox', { name: /test input/i });
    expect(inputElement).toBeDisabled();
    
    // Try to interact - should not trigger onChange
    fireEvent.change(inputElement, { target: { value: 'Should not change' } });
    expect(defaultProps.onChange).not.toHaveBeenCalled();
  });

  test('handles required state properly', () => {
    render(<Input {...defaultProps} required={true} />);
    
    const inputElement = screen.getByRole('textbox', { name: /test input/i });
    expect(inputElement).toBeRequired();
  });

  test('handles autoFocus prop', () => {
    render(<Input {...defaultProps} autoFocus={true} />);
    
    const inputElement = screen.getByRole('textbox', { name: /test input/i });
    expect(inputElement).toHaveFocus();
  });

  test('handles multiline textarea input', () => {
    render(<Input {...defaultProps} multiline={true} rows={5} />);
    
    const textareaElement = screen.getByRole('textbox', { name: /test input/i });
    expect(textareaElement).toBeInTheDocument();
    expect(textareaElement).toHaveAttribute('rows', '5');
  });

  test('handles autocomplete prop', () => {
    render(<Input {...defaultProps} autoComplete="off" />);
    
    const inputElement = screen.getByRole('textbox', { name: /test input/i });
    expect(inputElement).toHaveAttribute('autocomplete', 'off');
  });

  test('handles maxLength prop', () => {
    render(<Input {...defaultProps} maxLength={10} />);
    
    const inputElement = screen.getByRole('textbox', { name: /test input/i });
    expect(inputElement).toHaveAttribute('maxlength', '10');
  });

  test('handles custom className prop', () => {
    render(<Input {...defaultProps} className="custom-input-class" />);
    
    const inputElement = screen.getByRole('textbox', { name: /test input/i });
    expect(inputElement).toHaveClass('custom-input-class');
  });

  test('handles focus and blur events', () => {
    const handleFocus = jest.fn();
    const handleBlur = jest.fn();
    
    render(<Input {...defaultProps} onFocus={handleFocus} onBlur={handleBlur} />);
    
    const inputElement = screen.getByRole('textbox', { name: /test input/i });
    
    // Test focus
    fireEvent.focus(inputElement);
    expect(handleFocus).toHaveBeenCalledTimes(1);
    
    // Test blur
    fireEvent.blur(inputElement);
    expect(handleBlur).toHaveBeenCalledTimes(1);
  });

  test('handles special characters in input', async () => {
    const handleChange = jest.fn();
    const user = userEvent.setup();
    
    render(<Input {...defaultProps} onChange={handleChange} />);
    
    const inputElement = screen.getByRole('textbox', { name: /test input/i });
    
    // Test with special characters
    await user.type(inputElement, 'Special chars: !@#$%^&*()_+-=[]{}|;:,.<>?');
    
    expect(inputElement).toHaveValue('Special chars: !@#$%^&*()_+-=[]{}|;:,.<>?');
  });

  test('handles empty string values correctly', () => {
    render(<Input {...defaultProps} value="" />);
    
    const inputElement = screen.getByRole('textbox', { name: /test input/i });
    expect(inputElement).toHaveValue('');
  });

  test('handles null and undefined values gracefully', () => {
    render(<Input {...defaultProps} value={null} />);
    
    const inputElement = screen.getByRole('textbox', { name: /test input/i });
    expect(inputElement).toHaveValue('');
    
    render(<Input {...defaultProps} value={undefined} />);
    
    expect(inputElement).toHaveValue('');
  });

  test('renders with no label when label is empty string', () => {
    render(<Input {...defaultProps} label="" />);
    
    const inputElement = screen.getByRole('textbox', { name: /test input/i });
    expect(inputElement).toBeInTheDocument();
    
    // No label should be rendered
    const labelElement = screen.queryByText('');
    expect(labelElement).not.toBeInTheDocument();
  });

  test('handles form submission context', () => {
    const handleSubmit = jest.fn();
    
    render(
      <form onSubmit={handleSubmit}>
        <Input {...defaultProps} />
        <button type="submit">Submit</button>
      </form>
    );
    
    const submitButton = screen.getByText('Submit');
    fireEvent.click(submitButton);
    
    // Form submission should occur
    expect(handleSubmit).toHaveBeenCalledTimes(1);
  });

  test('handles keyboard events properly', () => {
    const handleKeyDown = jest.fn();
    render(<Input {...defaultProps} onKeyDown={handleKeyDown} />);
    
    const inputElement = screen.getByRole('textbox', { name: /test input/i });
    
    // Test key down event
    fireEvent.keyDown(inputElement, { key: 'Enter' });
    expect(handleKeyDown).toHaveBeenCalledTimes(1);
    
    // Test key press event
    fireEvent.keyPress(inputElement, { key: 'a' });
    expect(handleKeyDown).toHaveBeenCalledTimes(2);
  });
});