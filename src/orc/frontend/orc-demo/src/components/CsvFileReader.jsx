import React, { useState } from 'react';
import Papa from 'papaparse';
import './styles/CsvFileReader.sass'

function CsvFileReader({ setText, className }) {
    const [fileName, setFileName] = useState(''); // Holds the name of the selected file
    const [error, setError] = useState('');
    // Set your file size limit here (in bytes)
    const FILE_SIZE_LIMIT = 1 * 1024 * 1024; // 1 MB

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        setFileName(file.name);
        if (file) {
            // Check if file size exceeds the limit
            if (file.size > FILE_SIZE_LIMIT) {
                setError(`File size exceeds the limit of ${FILE_SIZE_LIMIT / (1024 * 1024)} MB`);
                event.target.value = ''; // Reset the input value to allow re-uploading the same file
                return;
            }
            setError(''); // Clear any previous errors

            const reader = new FileReader();
            // When the file is read, parse it using PapaParse
            reader.onload = (e) => {
                const csv = Papa.parse(e.target.result, {
                    header: true, // Set this to true if the CSV file has a header row
                    skipEmptyLines: true, // Skip empty lines
                    complete: (result) => {
                        // Extract the DOIs from the parsed data
                        let dois = result.data.map((row) => Object.values(row)[0]); // Get the first value from each row
                        // Join them into a single comma-separated string
                        setText(dois.join(','));
                    },
                });
            };
            // Read the file as text
            reader.readAsText(file);
            event.target.value = ''; // Reset the input value to allow re-uploading the same file
        }
    };

    return (
        <div className={className}>
            <input data-testid="upload-csv" type="file" accept=".csv" onChange={handleFileChange} />
            {error && <p style={{ color: 'red' }}>{error}</p>}
        </div>
    );
}

export default CsvFileReader;
