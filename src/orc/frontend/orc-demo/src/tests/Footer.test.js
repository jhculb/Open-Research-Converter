import { render, screen } from '@testing-library/react';
import Footer from '../components/Footer';
import kb_logo from '../images/KB_logo.svg';
import bmftr from '../images/bmftr.svg';


describe('Footer Component', () => {
    test('renders the GESIS imprint link', () => {
        render(<Footer />);

        const gesisLink = screen.getByText('GESIS - Imprint');
        expect(gesisLink).toBeInTheDocument();
        expect(gesisLink).toHaveAttribute('href', 'https://www.gesis.org/en/institute/imprint');
    });

    test('renders the project website link', () => {
        render(<Footer />);

        const projectWebsiteLink = screen.getByText('Project Website');
        expect(projectWebsiteLink).toBeInTheDocument();
        expect(projectWebsiteLink).toHaveAttribute('href', 'https://bibliometrie.info/en/research');
    });

    test('renders the codebase link', () => {
        render(<Footer />);

        const codebaseLink = screen.getByText('Codebase');
        expect(codebaseLink).toBeInTheDocument();
        expect(codebaseLink).toHaveAttribute('href', 'https://github.com/jhculb/Open-Research-Converter');
    });

    test('renders email addresses correctly', () => {
        render(<Footer />);

        const emailJohn = screen.getByText('john.culbert@gesis.org');
        const emailAhsan = screen.getByText('ahsan.shahid@gesis.org');

        expect(emailJohn).toBeInTheDocument();
        expect(emailAhsan).toBeInTheDocument();
    });

    test('renders BMFTR image with correct src and alt attributes', () => {
        render(<Footer />);

        const bmftrImage = screen.getByAltText('BMFTR');
        expect(bmftrImage).toBeInTheDocument();
        expect(bmftrImage).toHaveAttribute('src', bmftr);
        expect(bmftrImage).toHaveAttribute('alt', 'BMFTR');
    });

    test('renders KB image with correct src and alt attributes', () => {
        render(<Footer />);

        const KbImage = screen.getByAltText('Kb');
        expect(KbImage).toBeInTheDocument();
        expect(KbImage).toHaveAttribute('src', kb_logo);
        expect(KbImage).toHaveAttribute('alt', 'Kb');
    });

    test('BMFTR and KB links open in a new tab with correct rel attribute', () => {
        render(<Footer />);

        const bmftrLink = screen.getByAltText('BMFTR').closest('a');
        const KbLink = screen.getByAltText('Kb').closest('a');

        expect(bmftrLink).toHaveAttribute('target', '_blank');
        expect(bmftrLink).toHaveAttribute('rel', 'noopener noreferrer');

        expect(KbLink).toHaveAttribute('target', '_blank');
        expect(KbLink).toHaveAttribute('rel', 'noopener noreferrer');
    });
});
