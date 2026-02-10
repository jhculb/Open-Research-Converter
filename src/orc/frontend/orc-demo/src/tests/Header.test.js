import { render, screen, fireEvent } from '@testing-library/react';
import Header from '../components/Header';
import gesis_logo from '../images/logo_gesis_en.svg';

describe('Header Component', () => {
    test('renders the GESIS logo with correct src and alt', () => {
        render(<Header href="https://www.gesis.org" title="Open Research Converter" isHome={true} />);

        const logo = screen.getByAltText('gesis');
        expect(logo).toBeInTheDocument();
        expect(logo).toHaveAttribute('src', gesis_logo);
        expect(logo).toHaveAttribute('alt', 'gesis');
    });

    test('clicking the logo opens the correct URL', () => {
        // Mock window.open
        const openMock = jest.spyOn(window, 'open').mockImplementation(() => {});

        render(<Header href="https://www.gesis.org" title="Open Research Converter" isHome={true} />);

        const logo = screen.getByAltText('gesis');
        fireEvent.click(logo);  // Simulate clicking the logo

        expect(openMock).toHaveBeenCalledWith("https://www.gesis.org", "_self");

        // Clean up the mock
        openMock.mockRestore();
    });

    test('renders the title correctly', () => {
        render(<Header href="https://www.gesis.org" title="Open Research Converter" isHome={true} />);

        const title = screen.getByText('Open Research Converter');
        expect(title).toBeInTheDocument();
    });

    test('renders "About" link when isHome is true', () => {
        render(<Header href="https://www.gesis.org" title="Open Research Converter" isHome={true} />);

        const aboutLink = screen.getByTestId('is-home');
        expect(aboutLink).toBeInTheDocument();
        expect(aboutLink).toHaveAttribute('href', '/about');
    });

    test('renders "Home" text link when isHome is false', () => {
        render(<Header href="https://www.gesis.org" title="Open Research Converter" isHome={false} />);

        const homeLink = screen.getByTestId('is-not-home');
        expect(homeLink).toBeInTheDocument();
        expect(homeLink).toHaveAttribute('href', '/');
        expect(homeLink).toHaveTextContent('Home');
    });
});
