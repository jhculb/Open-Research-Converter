import { render, screen, fireEvent } from '@testing-library/react';
import HintButton from '../components/HintButton';
import input_template from '../images/input_template.PNG'; // Mock the image file

describe('HintButton Component', () => {
    test('renders the hint button', () => {
        render(<HintButton imageName="input_template" />);

        // Assert that the button with "?" is in the document
        const buttonElement = screen.getByTestId('hint-button');
        expect(buttonElement).toBeInTheDocument();
    });

    test('displays the image when mouse enters the button', () => {
        render(<HintButton imageName="input_template" />);

        const buttonElement = screen.getByTestId('hint-button');

        // Fire the mouse enter event to display the image
        fireEvent.mouseEnter(buttonElement);

        // Assert that the image is displayed
        const imageElement = screen.getByAltText('Hint');
        expect(imageElement).toBeInTheDocument();
        expect(imageElement).toHaveAttribute('src', input_template); // Ensure the correct image is rendered
    });

    test('hides the image when mouse leaves the button', () => {
        render(<HintButton imageName="input_template" />);

        const buttonElement = screen.getByTestId('hint-button');

        // Fire the mouse enter event to display the image
        fireEvent.mouseEnter(buttonElement);

        // Assert that the image is displayed
        const imageElement = screen.getByAltText('Hint');
        expect(imageElement).toBeInTheDocument();

        // Fire the mouse leave event to hide the image
        fireEvent.mouseLeave(buttonElement);

        // Assert that the image is no longer in the document
        expect(screen.queryByAltText('Hint')).not.toBeInTheDocument();
    });
});
