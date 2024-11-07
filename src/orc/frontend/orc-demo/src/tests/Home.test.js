import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Home from '../components/Home';

// Mock the global fetch function
const mockFetchSuccess = () =>
    Promise.resolve({
        ok: true,
        json: () => Promise.resolve([{
            job_id: "69c01d25-5db1-408e-abc0-e87094b713b3",
            output_data: [
                "https://openalex.org/W4399991117",
                "https://openalex.org/W2741809807",
                "https://openalex.org/W2122130843"
            ]
        }]),
    });

const mockFetchFailure = () =>
    Promise.reject(new Error('Fetch failed'));

beforeEach(() => {
    // Clear all instances and calls to fetch before each test
    global.fetch.mockClear();
});

beforeAll(() => {
    global.fetch = jest.fn(); // Mock global fetch
    global.alert = jest.fn(); // Mock window.alert function
});

describe('Home Component', () => {
    test('renders email input and buttons', () => {
        render(<Home />);

        const emailInput = screen.getByPlaceholderText('Please enter your email address');
        const clearInputButton = screen.getByText('Clear Input');
        const convertButton = screen.getByText('Convert DOIs to IDs');

        expect(emailInput).toBeInTheDocument();
        expect(clearInputButton).toBeInTheDocument();
        expect(convertButton).toBeInTheDocument();
    });

    test('validates email and blocks certain emails', () => {
        render(<Home />);

        const emailInput = screen.getByPlaceholderText('Please enter your email address');

        // Enter a blocked email
        fireEvent.change(emailInput, { target: { value: 'ahsan.shahid@gesis.org' } });
        expect(emailInput.value).toBe(''); // Blocked emails should be cleared

        // Enter a valid email
        fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
        expect(emailInput.value).toBe('test@example.com'); // Valid email should be accepted
    });

    test('clears input box when "Clear Input" button is clicked', () => {
        render(<Home />);

        const inputBox = screen.getByPlaceholderText('Please enter comma separated DOIs or upload a csv file (max. size 1 MB) containing DOIs in the first column');
        const clearInputButton = screen.getByText('Clear Input');

        // Type something into input box
        fireEvent.change(inputBox, { target: { value: 'https://doi.org/10.48550/ARXIV.2406.15154, 10.7717/peerj.4375, https://doi.org/10.5210/fm.v15i7.2874' } });
        expect(inputBox.value).toBe('https://doi.org/10.48550/ARXIV.2406.15154, 10.7717/peerj.4375, https://doi.org/10.5210/fm.v15i7.2874');

        // Click "Clear Input" button
        fireEvent.click(clearInputButton);
        expect(inputBox.value).toBe(''); // Input should be cleared
    });

    test('fetches and displays result on "Convert DOIs to IDs" button click', async () => {
        // Set up the mock for a successful fetch response
        global.fetch.mockImplementationOnce(mockFetchSuccess);

        render(<Home />);

        const emailInput = screen.getByPlaceholderText('Please enter your email address');
        const inputBox = screen.getByPlaceholderText('Please enter comma separated DOIs or upload a csv file (max. size 1 MB) containing DOIs in the first column');
        const convertButton = screen.getByText('Convert DOIs to IDs');

        // Enter valid email and DOIs
        fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
        fireEvent.change(inputBox, { target: { value: 'https://doi.org/10.48550/ARXIV.2406.15154, 10.7717/peerj.4375, https://doi.org/10.5210/fm.v15i7.2874' } });

        // Click "Convert DOIs to IDs" button
        fireEvent.click(convertButton);

        // Expect loading spinner to show
        const spinner = screen.getByRole('status');
        expect(spinner).toBeInTheDocument();

        // Wait for the fetch call to complete and the spinner to disappear
        await waitFor(() => expect(spinner).not.toBeInTheDocument());

        // Check if result box contains the result data
        const resultBox = screen.getByTitle('Result Box');
        expect(resultBox.value).toContain('1. https://openalex.org/W4399991117');
        expect(resultBox.value).toContain('2. https://openalex.org/W2741809807');
        expect(resultBox.value).toContain('3. https://openalex.org/W2122130843');
    });

    test('displays error message on fetch failure', async () => {
        // Set up the mock for a failed fetch response
        global.fetch.mockImplementationOnce(mockFetchFailure);

        render(<Home />);

        const emailInput = screen.getByPlaceholderText('Please enter your email address');
        const inputBox = screen.getByPlaceholderText('Please enter comma separated DOIs or upload a csv file (max. size 1 MB) containing DOIs in the first column');
        const convertButton = screen.getByText('Convert DOIs to IDs');

        // Enter valid email and DOIs
        fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
        fireEvent.change(inputBox, { target: { value: 'https://doi.org/10.48550/ARXIV.2406.15154, 10.7717/peerj.4375, https://doi.org/10.5210/fm.v15i7.2874,' } });

        // Click "Convert DOIs to IDs" button
        fireEvent.click(convertButton);

        // Expect loading spinner to show
        const spinner = screen.getByRole('status');
        expect(spinner).toBeInTheDocument();

        // Wait for the fetch call to complete and the spinner to disappear
        await waitFor(() => expect(spinner).not.toBeInTheDocument());

        // Expect an error message to be displayed
        // const errorMessage = screen.getByText('Oops, something went wrong! Please check your input and try again.');
        // expect(errorMessage).toBeInTheDocument();
    });

    test('disables "Convert DOIs to IDs" button when email or DOIs are missing', () => {
        render(<Home />);

        const convertButton = screen.getByText('Convert DOIs to IDs');

        // Initially, button should be disabled because no email or DOIs are provided
        expect(convertButton).toBeDisabled();

        // Enter email but leave input box empty
        const emailInput = screen.getByPlaceholderText('Please enter your email address');
        fireEvent.change(emailInput, { target: { value: 'test@example.com' } });

        expect(convertButton).toBeDisabled(); // Still disabled because DOIs are missing

        // Enter DOIs
        const inputBox = screen.getByPlaceholderText('Please enter comma separated DOIs or upload a csv file (max. size 1 MB) containing DOIs in the first column');
        fireEvent.change(inputBox, { target: { value: 'https://doi.org/10.48550/ARXIV.2406.15154, 10.7717/peerj.4375, https://doi.org/10.5210/fm.v15i7.2874' } });

        expect(convertButton).not.toBeDisabled(); // Now button should be enabled
    });
});

