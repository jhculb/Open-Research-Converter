// import logo from './logo.svg';
import React, { useState } from 'react';
import './App.css';
import './components/styles/Header.sass';
import Header from './components/Header';
import TextBox from './components/TextBox';
// import UploadFile from "./components/UploadFile";
import CsvFileReader from './components/CsvFileReader';
import HintButton from './components/HintButton';
import Footer from './components/Footer';

function App() {
    const [email, setEmail] = useState('');
    const [validEmail, setValidEmail] = useState(false);
    const [text, setText] = useState('');
    const [result, setResult] = useState('');
    const [limitedResult, setLimitedResult] = useState('');
    const [jobId, setjobId] = useState('');
    const [isDownloadDisabled, setIsDownloadDisabled] = useState(true);
    const [isLoading, setIsLoading] = useState(false);
    const blockedEmails = ['john.culbert@gesis.org', 'ahsan.shahid@gesis.org'];

    let apiUrl = process.env.REACT_APP_DEV_URL;
    if (process.env.REACT_APP_ENV === "production") {
        apiUrl = process.env.REACT_APP_PROD_URL;
    }
    // console.log("API URL:", apiUrl);

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

    //---- function called on Download Result button press
    const downloadResult = () => {
        let outputData = result[0]["output_full"];
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

    //---- function called on Submit button press
    const onSubmit = () => {
        // let url = 'https://orc-demo.gesis.org/api/start_processing';
        let url = apiUrl + '/api/start_processing';
        let data ={"email": email, "input_data": text};
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
                let outputData = result[0]["output_data"];
                setjobId(result[0]["job_id"]);
                setResult(result);
                setText('');
                if(outputData.length){
                    setIsDownloadDisabled(false);
                    let formattedText = outputData
                        .slice(0, 50)  // Take only the first 50 items
                        .map((item, index) => `${index + 1}. ${item}`)  // Create a numbered list
                        .join('\n');  // Join with new line characters for display in textarea
                    setLimitedResult(formattedText);
                }
                // setResult(JSON.stringify(result[0]["output_data"], null, 2));
                // console.log('Submit button pressed: ', result);
            })
            .catch(error => console.log(error))
            .finally(() => {
                setIsLoading(false);  // Stop loading
            });
    }
    return (
        <div className="container">
            <div className="row header-border mb-4 mt-2 align-items-center">
                <Header title="Open Research Converter" href="https://www.gesis.org/" />
            </div>
            <div className="row">
                <div className="col-12 col-md-6 d-flex flex-column">
                    <div className="mt-2">
                        <TextBox
                            customClass={email === "" ? "" : (validEmail ? "custom-valid-focus" : "custom-invalid-focus")}
                            title={"Email"}
                            rows={1}
                            placeholder={'Enter your email address!'}
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
                            placeholder={'DOIs from selected CSV file are displayed here! (OR) Enter comma separated DOIs!'}
                            value={text}
                            onChange={handleTextChange}
                        />
                        <div className="d-flex justify-content-center">
                            {/*<button type="button" className="btn btn-color" onClick={() => onSubmit()}>Submit</button>*/}
                            <button type="button" className={`btn ${!(text && validEmail) ? 'btn-disabled' : 'btn-color'}`} disabled={!(text && validEmail)} onClick={() => onSubmit()}>Submit</button>
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
                    <TextBox
                        title={"Result Box"}
                        rows={20}
                        placeholder={'OpenAlex DOIs for the first 50 inputs will be shown. Download the file for full results!'}
                        value={limitedResult}
                        readOnly={true}
                        style={{ height: '100%' }}
                    />
                    <div className="d-flex justify-content-center mb-1">
                        {/*<button type="button" className="btn btn-color" onClick={() => downloadResult()}>Download Result</button>*/}
                        <button type="button" className={`btn ${isDownloadDisabled ? 'btn-disabled' : 'btn-color'}`} disabled={isDownloadDisabled} onClick={() => downloadResult()}>Download Result</button>
                    </div>
                </div>
            </div>
            <div className="row mt-4">
                <Footer></Footer>
            </div>
        </div>
    );
}

export default App;


// .then(result => {
//     console.log(JSON.stringify(result));
//     let outputData = result[0]["output_full"];
//     setjobId(result[0]["job_id"]);
//     setResult(result);
//     setText('');
//     if(outputData.length){
//         setIsDownloadDisabled(false);
//         const lines = outputData.trim().split('\n').slice(0, 51);
//
//         // Extract the headers (first line) and the data (remaining lines)
//         const headers = lines[0].split(',');
//         const rows = lines.slice(1).map(line => line.split(','));
//
//         // Create a text representation with proper alignment using tabs
//         let formattedText = headers.join('\t\t\t\t\t\t\t\t\t\t\t\t') + '\n';  // Join headers with tabs
//         rows.forEach(row => {
//             formattedText += row.join('\t') + '\n';  // Join each row with tabs
//         });
//
//         setLimitedResult(formattedText);
//     }
//     // setResult(JSON.stringify(result[0]["output_data"], null, 2));
//     // console.log('Submit button pressed: ', result);
// })

// const downloadResult = () => {
//     let outputData = result[0]["output_data"];
//     let csvContent = "openalex_dois\n"; // Header
//     // Append each item in the outputData array as a new line in the CSV
//     outputData.forEach(item => {
//         csvContent += `${item}\n`;
//     });
//     // Create a Blob from the CSV string
//     const blob = new Blob([csvContent], { type: 'text/csv' });
//     // Create a temporary anchor element
//     const link = document.createElement('a');
//     // Set the download URL as the Blob's URL
//     link.href = URL.createObjectURL(blob);
//     // Set the download attribute with a file name
//     link.download = 'openalex_dois.csv';
//     // Programmatically click the link to trigger the download
//     link.click();
//     // Clean up by revoking the Blob URL
//     URL.revokeObjectURL(link.href);
// };
