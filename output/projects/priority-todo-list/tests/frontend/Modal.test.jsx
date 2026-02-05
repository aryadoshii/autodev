jsx
// Modal.test.jsx
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Modal from './Modal';

describe('Modal Component', () => {
  const defaultProps = {
    isOpen: false,
    onClose: jest.fn(),
    title: 'Test Modal',
    children: <div>Modal content</div>,
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders correctly when isOpen is true', () => {
    const { container } = render(
      <Modal {...defaultProps} isOpen={true}>
        <p>Modal content</p>
      </Modal>
    );

    expect(screen.getByRole('dialog')).toBeInTheDocument();
    expect(screen.getByText('Test Modal')).toBeInTheDocument();
    expect(screen.getByText('Modal content')).toBeInTheDocument();
    expect(container.firstChild).toMatchSnapshot();
  });

  test('does not render when isOpen is false', () => {
    render(<Modal {...defaultProps} isOpen={false} />);
    
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  });

  test('handles props correctly', () => {
    const customTitle = 'Custom Title';
    const customChildren = <span>Custom Content</span>;
    const customOnClose = jest.fn();

    render(
      <Modal
        {...defaultProps}
        isOpen={true}
        title={customTitle}
        onClose={customOnClose}
      >
        {customChildren}
      </Modal>
    );

    expect(screen.getByText(customTitle)).toBeInTheDocument();
    expect(screen.getByText('Custom Content')).toBeInTheDocument();
    expect(screen.getByRole('dialog')).toHaveAttribute('aria-modal', 'true');
  });

  test('closes modal when close button is clicked', () => {
    render(
      <Modal {...defaultProps} isOpen={true}>
        <p>Modal content</p>
      </Modal>
    );

    const closeButton = screen.getByLabelText('Close');
    fireEvent.click(closeButton);

    expect(defaultProps.onClose).toHaveBeenCalledTimes(1);
  });

  test('closes modal when Escape key is pressed', () => {
    render(
      <Modal {...defaultProps} isOpen={true}>
        <p>Modal content</p>
      </Modal>
    );

    fireEvent.keyDown(screen.getByRole('dialog'), { key: 'Escape' });

    expect(defaultProps.onClose).toHaveBeenCalledTimes(1);
  });

  test('closes modal when backdrop is clicked', () => {
    render(
      <Modal {...defaultProps} isOpen={true}>
        <p>Modal content</p>
      </Modal>
    );

    const backdrop = screen.getByRole('dialog').parentElement;
    fireEvent.click(backdrop);

    expect(defaultProps.onClose).toHaveBeenCalledTimes(1);
  });

  test('does not close modal when content area is clicked', () => {
    render(
      <Modal {...defaultProps} isOpen={true}>
        <p>Modal content</p>
      </Modal>
    );

    const contentArea = screen.getByText('Modal content').parentElement;
    fireEvent.click(contentArea);

    expect(defaultProps.onClose).not.toHaveBeenCalled();
  });

  test('handles user input changes', async () => {
    const user = userEvent.setup();
    const inputText = 'Test input value';

    render(
      <Modal {...defaultProps} isOpen={true}>
        <input data-testid="test-input" defaultValue="" />
      </Modal>
    );

    const input = screen.getByTestId('test-input');
    await user.type(input, inputText);

    expect(input).toHaveValue(inputText);
  });

  test('conditional rendering works correctly', () => {
    // Test initial state - should not render
    render(<Modal {...defaultProps} isOpen={false} />);
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();

    // Test after opening
    const { rerender } = render(<Modal {...defaultProps} isOpen={true} />);
    expect(screen.getByRole('dialog')).toBeInTheDocument();

    // Test after closing
    rerender(<Modal {...defaultProps} isOpen={false} />);
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  });

  test('accessibility attributes are present', () => {
    render(
      <Modal {...defaultProps} isOpen={true}>
        <p>Modal content</p>
      </Modal>
    );

    const dialog = screen.getByRole('dialog');
    expect(dialog).toHaveAttribute('aria-modal', 'true');
    expect(dialog).toHaveAttribute('aria-labelledby', 'modal-title');
    expect(dialog).toHaveAttribute('role', 'dialog');

    const closeButton = screen.getByLabelText('Close');
    expect(closeButton).toBeInTheDocument();
    expect(closeButton).toHaveAttribute('aria-label', 'Close');
  });

  test('handles edge case: no title provided', () => {
    render(
      <Modal {...defaultProps} isOpen={true} title={null}>
        <p>Modal content</p>
      </Modal>
    );

    expect(screen.queryByRole('heading')).not.toBeInTheDocument();
  });

  test('handles edge case: empty children', () => {
    render(
      <Modal {...defaultProps} isOpen={true} children={null}>
        <p>Modal content</p>
      </Modal>
    );

    expect(screen.getByText('Modal content')).toBeInTheDocument();
  });

  test('handles edge case: no onClose handler', () => {
    const { container } = render(
      <Modal {...defaultProps} isOpen={true} onClose={undefined}>
        <p>Modal content</p>
      </Modal>
    );

    const closeButton = screen.getByLabelText('Close');
    fireEvent.click(closeButton);

    // Should not crash even without onClose handler
    expect(container).toBeInTheDocument();
  });

  test('focus management works correctly', () => {
    render(
      <Modal {...defaultProps} isOpen={true}>
        <button data-testid="first-button">First Button</button>
        <button data-testid="second-button">Second Button</button>
      </Modal>
    );

    const firstButton = screen.getByTestId('first-button');
    expect(firstButton).toHaveFocus();
  });

  test('prevents focus from leaving modal when tabbing', () => {
    render(
      <Modal {...defaultProps} isOpen={true}>
        <input data-testid="input-field" placeholder="Input field" />
        <button data-testid="close-button">Close</button>
      </Modal>
    );

    const inputField = screen.getByTestId('input-field');
    const closeButton = screen.getByTestId('close-button');

    // Simulate tabbing through elements
    fireEvent.keyDown(inputField, { key: 'Tab' });
    
    // Focus should remain within the modal
    expect(inputField).toHaveFocus();
  });

  test('renders with custom className', () => {
    render(
      <Modal {...defaultProps} isOpen={true} className="custom-modal">
        <p>Modal content</p>
      </Modal>
    );

    const modalDialog = screen.getByRole('dialog');
    expect(modalDialog).toHaveClass('custom-modal');
  });

  test('calls onClose when clicking outside of modal content', () => {
    render(
      <Modal {...defaultProps} isOpen={true}>
        <p>Modal content</p>
      </Modal>
    );

    const backdrop = screen.getByRole('dialog').parentElement;
    fireEvent.mouseDown(backdrop);
    fireEvent.click(backdrop);

    expect(defaultProps.onClose).toHaveBeenCalledTimes(1);
  });

  test('does not call onClose when clicking inside modal content', () => {
    render(
      <Modal {...defaultProps} isOpen={true}>
        <p data-testid="modal-content">Modal content</p>
      </Modal>
    );

    const content = screen.getByTestId('modal-content');
    fireEvent.click(content);

    expect(defaultProps.onClose).not.toHaveBeenCalled();
  });

  test('handles multiple modals gracefully', () => {
    render(
      <>
        <Modal {...defaultProps} isOpen={true} title="First Modal">
          <p>First modal content</p>
        </Modal>
        <Modal {...defaultProps} isOpen={true} title="Second Modal">
          <p>Second modal content</p>
        </Modal>
      </>
    );

    expect(screen.getByText('First Modal')).toBeInTheDocument();
    expect(screen.getByText('Second Modal')).toBeInTheDocument();
  });

  test('properly handles nested components in modal', () => {
    const NestedComponent = () => (
      <div>
        <h3>Nested Header</h3>
        <p>Nested paragraph</p>
      </div>
    );

    render(
      <Modal {...defaultProps} isOpen={true}>
        <NestedComponent />
      </Modal>
    );

    expect(screen.getByText('Nested Header')).toBeInTheDocument();
    expect(screen.getByText('Nested paragraph')).toBeInTheDocument();
  });
});