Given the provided details, here are comprehensive test cases for the Button component using Jest and React Testing Library, ensuring functionality, correctness, and validation of props:

Path: src/tests/Button.test.js
Code:
'''
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Button from '../components/Button';

describe('Button Component Tests', () => {
  it('renders button with the provided text', () => {
    const text = "Click me";
    render(<Button text={text} onClick={() => {}} />);
    const buttonElement = screen.getByRole('button', { name: text });
    expect(buttonElement).toBeInTheDocument();
    expect(buttonElement).toHaveTextContent(text);
  });

  it('calls the onClick function when clicked', () => {
    const onClickMock = jest.fn();
    const text = "Click me";
    render(<Button text={text} onClick={onClickMock} />);
    const buttonElement = screen.getByRole('button', { name: text });
    fireEvent.click(buttonElement);
    expect(onClickMock).toHaveBeenCalled();
  });

  it('is disabled when disabled prop is true', () => {
    const text = "Click me";
    render(<Button text={text} onClick={() => {}} disabled={true} />);
    const buttonElement = screen.getByRole('button', { name: text });
    expect(buttonElement).toBeDisabled();
  });

  it('has type submit when submit prop is set', () => {
    const text = "Submit";
    render(<Button text={text} onClick={() => {}} submit={true} />);
    const buttonElement = screen.getByRole('button', { name: text });
    expect(buttonElement.getAttribute('type')).toBe('submit');
  });
});
'''
This code tests various functionalities of the Button component, such as rendering with the correct text, invoking callbacks on user interaction, handling disabled state, and specific attributes like 'type' based on props. These tests ensure the Button behaves as expected under different conditions.