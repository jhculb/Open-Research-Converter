import React, { useState, useEffect } from 'react';
import '../App.css';
import TextBox from './TextBox';
import CsvFileReader from './CsvFileReader';
import HintButton from './HintButton';

function Home() {
    const [email, setEmail] = useState('');
    const [validEmail, setValidEmail] = useState(false);
    const [text, setText] = useState('');
    const [result, setResult] = useState('');
    const [limitedResult, setLimitedResult] = useState('');
    const [jobId, setjobId] = useState('');
    const [isDownloadAll, setIsDownloadAll] = useState(false);
    const [isDownloadDisabled, setIsDownloadDisabled] = useState(true);
    const [isLoading, setIsLoading] = useState(false);
    // State for tracking DOI matching results
    const [foundCount, setFoundCount] = useState(0);
    const [submittedCount, setSubmittedCount] = useState(0);
    const [missingDois, setMissingDois] = useState([]);
    const [showMissing, setShowMissing] = useState(false);
    const blockedEmails = ['john.culbert@gesis.org', 'ahsan.shahid@gesis.org'];

    let apiUrl = process.env.REACT_APP_DEV_URL;
    if (process.env.REACT_APP_ENV === "production") {
        apiUrl = process.env.REACT_APP_PROD_URL;
    }

    const handleTextChange = (event) => {
        setText(event.target.value);
    };
    const handleEmailChange = (event) => {
        let email = event.target.value;
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        setEmail(email);
        // Check if email is valid
        if (!emailRegex.test(email)) {
            setValidEmail(false);
            return;
        }
        // Check if email is blocked
        if (blockedEmails.includes(email.toLowerCase())) {
            setValidEmail(false);
            setEmail('');
            alert('Oops! Smart move! Please insert your personal e-mail address.');
        } else {
            setValidEmail(true);
        }
    };

    //---- function called on Download IDS/Full Records button press
    const downloadResult = () => {
        setIsDownloadDisabled(true);
        setLimitedResult('');
        setIsDownloadAll(false);
        let outputData = isDownloadAll ? result[0]["output_full"][0] : result[0]["output_full"];
        const lines = outputData.trim().split('\n');
        const header = lines[0];
        const rows = lines.slice(1).join('\n');
        const csvContent = `${header}\n${rows}`;
        const blob = new Blob([csvContent], { type: 'text/csv' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        // Set the the desired file name
        link.download = 'orc_output.csv';
        link.click();
        URL.revokeObjectURL(link.href);
    };

    const clearInput = () => {
        setText('');
        setLimitedResult('');
        setFoundCount(0);
        setSubmittedCount(0);
        setMissingDois([]);
        setShowMissing(false);
        setIsDownloadDisabled(true);
    }

    //---- function called on Convert DOIs to IDs button press
    const onGetIds = () => {
        let url = apiUrl + '/api/start_processing';
        let data = { "email": email, "input_data": text };
        setIsLoading(true);
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
            .then((response) => {
                if (!response.ok) {
                    setLimitedResult('Oops, something went wrong! Please check your input and try again.');
                    setIsDownloadDisabled(true);
                    setIsLoading(false);  // Stop loading
                    // Read the response as text to capture HTML or error message
                    return response.text().then((text) => {
                        // Log the HTML/error message
                        console.error('Error response body:', text);
                        // Optionally, throw an error or return a custom object
                        throw new Error('Network response was not ok');
                    });
                }
                return response.json();  // Assuming the response is JSON
            })
            .then(result => {
                let outputData = result[0]["output_data"];
                setjobId(result[0]["job_id"]);
                setResult(result);
                // Extract counter data
                setFoundCount(result[0]["found_count"] || outputData.length);
                setSubmittedCount(result[0]["submitted_count"] || outputData.length);
                setMissingDois(result[0]["missing_dois"] || []);
                setShowMissing(false);
                if (outputData.length) {
                    setIsDownloadDisabled(false);
                    let formattedText = outputData
                        .slice(0, 50)  // Take only the first 50 items
                        .map((item, index) => `${index + 1}. ${item}`)  // Create a numbered list
                        .join('\n');  // Join with new line characters for display in textarea
                    setLimitedResult(formattedText);
                }
            })
            .catch(error => console.log(error))
            .finally(() => {
                setIsLoading(false);  // Stop loading
            });
    }

    //---- function called on Download Full Records button press
    const onGetAll = () => {
        let url = apiUrl + '/api/process_all';
        let data = { "email": email, "input_data": text };
        setIsLoading(true);
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
            .then((response) => {
                if (!response.ok) {
                    // Read the response as text to capture HTML or error message
                    return response.text().then((text) => {
                        // Log the HTML/error message
                        console.error('Error response body:', text);
                        // Optionally, throw an error or return a custom object
                        throw new Error('Network response was not ok');
                    });
                }
                return response.json();  // Assuming the response is JSON
            })
            .then(result => {
                setjobId(result[0]["job_id"]);
                setResult(result);
                // Extract counter data
                let outputData = result[0]["output_data"] || [];
                setFoundCount(result[0]["found_count"] || outputData.length);
                setSubmittedCount(result[0]["submitted_count"] || outputData.length);
                setMissingDois(result[0]["missing_dois"] || []);
                setShowMissing(false);
                setIsDownloadAll(true);
            })
            .catch(error => console.log(error))
            .finally(() => {
                setIsLoading(false);  // Stop loading
            });
    }

    // Using useEffect to trigger isDownloadAll when "Download Full Records" is pressed
    useEffect(() => {
        if (isDownloadAll) {
            downloadResult();  // Call the download function
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [isDownloadAll]);  // Dependency array ensures this effect runs when `isDownloadAll` changes

    return (
        <div className="row">
            <div className="col-12 col-md-6 d-flex flex-column">
                <div className="mt-2">
                    <TextBox
                        customClass={email === "" ? "" : (validEmail ? "custom-valid-focus" : "custom-invalid-focus")}
                        title={"Email"}
                        rows={1}
                        placeholder={'Please enter your email address'}
                        value={email}
                        type="email"
                        onChange={handleEmailChange}
                    />
                </div>
                <div className="mt-2 d-flex flex-grow-0 align-items-center upload-border">
                    <CsvFileReader className="m-1 w-100" setText={setText} />
                    <HintButton className="ml-2" imageName='input_template'></HintButton>
                </div>
                <div className="mt-2 flex-grow-1">
                    <TextBox
                        title={"Input Box"}
                        rows={16}
                        placeholder={'Please enter comma separated DOIs or upload a csv file (max. size 1 MB) containing DOIs in the first column'}
                        value={text}
                        onChange={handleTextChange}
                    />
                    <div className="d-flex justify-content-center">
                        <button type="button" className={`btn ${(!(text) || isLoading) ? 'btn-disabled' : 'btn-color'}`} disabled={(!(text) || isLoading)} onClick={() => clearInput()}>Clear Input</button>
                        &nbsp;&nbsp;&nbsp;&nbsp;
                        <button type="button" className={`btn ${(!(text && validEmail) || isLoading) ? 'btn-disabled' : 'btn-color'}`} disabled={(!(text && validEmail) || isLoading)} onClick={() => onGetIds()}>Convert DOIs to IDs</button>
                    </div>
                </div>
            </div>
            <div className="col-12 col-md-6 mt-2 d-flex flex-column position-relative" style={{ height: '100%' }}>
                {
                    isLoading &&
                    <div className="spinner-border spinner-color spinner-position large-spinner" role="status">
                        <span className="sr-only"></span>
                    </div>
                }
                {/* Counter display */}
                {submittedCount > 0 && (
                    <div className="d-flex justify-content-between align-items-center mb-2 px-1">
                        <span className={`badge ${foundCount === submittedCount ? 'bg-success' : 'bg-warning text-dark'}`}>
                            Found: {foundCount} / {submittedCount}
                        </span>
                        {missingDois.length > 0 && (
                            <button
                                type="button"
                                className="btn btn-sm btn-outline-secondary"
                                onClick={() => setShowMissing(!showMissing)}
                            >
                                {showMissing ? 'Hide' : 'Show'} Missing DOIs ({missingDois.length})
                            </button>
                        )}
                    </div>
                )}
                {/* Missing DOIs collapsible section */}
                {showMissing && missingDois.length > 0 && (
                    <div className="alert alert-warning mb-2 p-2">
                        <div className="d-flex justify-content-between align-items-center mb-1">
                            <strong>DOIs not found in OpenAlex ({missingDois.length}):</strong>
                            <div>
                                <button
                                    type="button"
                                    className="btn btn-sm btn-outline-primary me-1"
                                    onClick={() => navigator.clipboard.writeText(missingDois.join('\n'))}
                                >
                                    Copy
                                </button>
                                <button
                                    type="button"
                                    className="btn btn-sm btn-outline-secondary"
                                    onClick={() => {
                                        const csvContent = "doi\n" + missingDois.join('\n');
                                        const blob = new Blob([csvContent], { type: 'text/csv' });
                                        const link = document.createElement('a');
                                        link.href = URL.createObjectURL(blob);
                                        link.download = 'missing_dois.csv';
                                        link.click();
                                        URL.revokeObjectURL(link.href);
                                    }}
                                >
                                    Download CSV
                                </button>
                            </div>
                        </div>
                        <textarea
                            className="form-control"
                            rows={Math.min(missingDois.length, 5)}
                            readOnly
                            value={missingDois.join('\n')}
                        />
                    </div>
                )}
                <TextBox
                    title={"Result Box"}
                    rows={20}
                    placeholder={'OpenAlex IDs for the first 50 DOIs will be shown\n\nPlease download for all IDs or full records'}
                    value={limitedResult}
                    readOnly={true}
                    style={{ height: '100%' }}
                />
                <div className="d-flex justify-content-center mb-1">
                    <button type="button" className={`btn ${isDownloadDisabled ? 'btn-disabled' : 'btn-color'}`} disabled={isDownloadDisabled} onClick={() => downloadResult()}>Download IDs</button>
                    &nbsp;&nbsp;&nbsp;&nbsp;
                    <button type="button" className={`btn ${(!(text && validEmail) || isLoading) ? 'btn-disabled' : 'btn-color'}`} disabled={(!(text && validEmail) || isLoading)} onClick={() => onGetAll()}>Download Full Records</button>
                </div>
            </div>
        </div>
    );
}

export default Home;
