import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import App from '../App';

test('renders the header with title', () => {
  render(
      <MemoryRouter>
        <App />
      </MemoryRouter>
  );

  // Check if the header renders with the correct title
  const headerElement = screen.getByText(/Open Research Converter/i);
  expect(headerElement).toBeInTheDocument();
});

test('renders the home page by default', () => {
  render(
      <MemoryRouter>
        <App />
      </MemoryRouter>
  );

  // Check for content that appears on the Home page
  const homePageElement = screen.getByText(/Clear Input/i); // Adjust this if "Home" is not the actual text
  expect(homePageElement).toBeInTheDocument();
});

test('navigates to the about page', () => {
  render(
      <MemoryRouter initialEntries={['/about']}>
        <App />
      </MemoryRouter>
  );

  // Check for content that appears on the About page
  const aboutPageElement = screen.getByText(/About ORC/i); // Adjust this to match the actual content in About.js
  expect(aboutPageElement).toBeInTheDocument();
});
