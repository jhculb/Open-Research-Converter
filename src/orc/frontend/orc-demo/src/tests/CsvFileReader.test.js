import { render, screen, fireEvent, waitFor, createEvent } from '@testing-library/react';
import CsvFileReader from '../components/CsvFileReader';

describe('CsvFileReader Component', () => {
    const setTextMock = jest.fn(); // Mock function to simulate setText prop

    beforeEach(() => {
        jest.clearAllMocks(); // Clear previous mocks
    });

    test('renders file input', () => {
        render(<CsvFileReader setText={setTextMock} />);

        const fileInput = screen.getByTestId('upload-csv');
        expect(fileInput).toBeInTheDocument();
    });

    test('processes a valid CSV file and extracts DOIs', async () => {
        render(<CsvFileReader setText={setTextMock} />);

        const file = new Blob(
            [`dois\nhttps://doi.org/10.48550/ARXIV.2406.15154\n10.7717/peerj.4375\nhttps://doi.org/10.5210/fm.v15i7.2874`], // Mock CSV data
            { type: 'text/csv' }
        );

        const fileInput = screen.getByTestId('upload-csv');
        Object.defineProperty(fileInput, 'files', {
            value: [file],
        });
        fireEvent.change(fileInput); // Simulate file selection

        // Ensure the setTextMock is called with the expected comma-separated DOIs
        await waitFor(() => {
            expect(setTextMock).toHaveBeenCalledWith('https://doi.org/10.48550/ARXIV.2406.15154,10.7717/peerj.4375,https://doi.org/10.5210/fm.v15i7.2874');
        });
    });

    test('displays error message for oversized file', () => {
        render(<CsvFileReader setText={setTextMock} />);

        const oversizedFile = new Blob(['a'.repeat(2 * 1024 * 1024)], { type: 'text/csv' }); // 2 MB file

        const fileInput = screen.getByTestId('upload-csv');
        Object.defineProperty(fileInput, 'files', {
            value: [oversizedFile],
        });
        fireEvent.change(fileInput); // Simulate file selection

        const errorMessage = screen.getByText(/File size exceeds the limit/i);
        expect(errorMessage).toBeInTheDocument(); // Expect the error message to be displayed
    });

    test('clears error message when a valid file is uploaded after an error', async () => {
        render(<CsvFileReader setText={setTextMock} />);

        // Simulate oversized file selection
        const oversizedFile = new Blob(['a'.repeat(2 * 1024 * 1024)], { type: 'text/csv' });
        const fileInput = screen.getByTestId('upload-csv');

        // Create the event for file input change
        const oversizedFileEvent = createEvent.change(fileInput, {
            target: {
                files: [oversizedFile],
            },
        });
        fireEvent(fileInput, oversizedFileEvent); // Fire the change event with the oversized file

        expect(screen.getByText(/File size exceeds the limit/i)).toBeInTheDocument(); // Error is displayed

        // Now simulate valid file selection
        const validFile = new Blob([`dois\nhttps://doi.org/10.48550/ARXIV.2406.15154\n10.7717/peerj.4375\nhttps://doi.org/10.5210/fm.v15i7.2874`], { type: 'text/csv' });

        // Create the event for file input change with valid file
        const validFileEvent = createEvent.change(fileInput, {
            target: {
                files: [validFile],
            },
        });
        fireEvent(fileInput, validFileEvent); // Fire the change event with the valid file

        // Wait for the error message to be cleared and the mock function to be called
        await waitFor(() => {
            expect(setTextMock).toHaveBeenCalledWith('https://doi.org/10.48550/ARXIV.2406.15154,10.7717/peerj.4375,https://doi.org/10.5210/fm.v15i7.2874');
            expect(screen.queryByText(/File size exceeds the limit/i)).not.toBeInTheDocument(); // Error message should be cleared
        });
    });
});
