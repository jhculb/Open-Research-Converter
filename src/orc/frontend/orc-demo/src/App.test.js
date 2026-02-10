import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import App from './App';

test('renders application title', () => {
  render(
    <MemoryRouter>
      <App />
    </MemoryRouter>
  );
  const titleElement = screen.getByText(/Open Research Converter/i);
  expect(titleElement).toBeInTheDocument();
});
