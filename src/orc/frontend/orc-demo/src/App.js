// import logo from './logo.svg';
import React, { useState } from 'react';
import './App.css';
import './components/styles/Header.sass'
import Header from './components/Header';
import TextBox from './components/TextBox';
import UploadFile from "./components/UploadFile";
import CsvFileReader from './components/CsvFileReader';

function App() {
    const [email, setEmail] = useState('');
    const [validEmail, setValidEmail] = useState(false);
    const [text, setText] = useState('');
    const [result, setResult] = useState('');
    const [jobId, setjobId] = useState('');

    const handleTextChange = (event) => {
        setText(event.target.value);
    };
    const handleEmailChange = (event) => {
        let email = event.target.value;
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (emailRegex.test(email)) {
            setValidEmail(true);
        } else {
            setValidEmail(false);
        }
        setEmail(email);
    };
    // const handleResultChange = (event) => {
    //     setResult(event.target.value);
    // };

    // Function to update the result value
    // const updateResult = (newResult) => {
    //     setResult(newResult);
    // };

    //---- function called on Download Result button press
    const getResult = () => {
        //---- endpoint receiving the GET request upon the button press
        let domain = 'http://localhost/api/healthcheck';
        let params = '';
        let url = domain + params;

        fetch(url, { method: 'GET' })
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
                setResult(JSON.stringify(result));
                console.log('Download Result button pressed: ', result);
            })
            .catch(error => console.log('Download Result button', error));
    }

    //---- function called on Submit button press
    const onSubmit = () => {
        //---- endpoint receiving the GET request upon the button press
        let url = 'http://localhost/api/start_processing';
        let data ={"email": email, "input_data": text}
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            // body: data
            body: JSON.stringify(data)
            })
            .then((response) => {
                console.log(url, data);
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
                setText(JSON.stringify(result));
                console.log('Submit button pressed: ', result);
            })
            .catch(error => console.log('Submit button error', error));
    }

    return (
        <div className="container">
            <div className="row header">
                <Header title="Open Research Converter" />
            </div>
            <div className="row">
                <div className="col-6 mt-2">
                    <TextBox customClass={email === "" ? "" : (validEmail ? "custom-valid-focus" : "custom-invalid-focus")} title={"Email"} rows={1} placeholder={'Enter your email address!'} value={email} type="email" onChange={handleEmailChange} />
                </div>
                <div className="col-6 mt-2 upload-border">
                    <CsvFileReader className="mt-1" setText={setText}/>
                    {/*<UploadFile />*/}
                </div>
                <div className="col-6 mt-2">
                    <TextBox title={"Input Box"} rows={7} placeholder={'DOIs from selected CSV file are displayed here! (OR) Enter comma separated DOIs!'} value={text} onChange={handleTextChange} />
                    <div className="d-flex justify-content-end mt-2">
                        <button type="button" className="btn btn-secondary" onClick={() => onSubmit()}>Submit</button>
                    </div>
                </div>
                <div className="col-6 mt-2">
                    <TextBox title={"Result Box"} rows={7} placeholder={'Here are the first N results returned!'} value={result} readOnly={true} />
                    {/*onChange={handleResultChange}*/}
                    <div className="d-flex justify-content-end mt-2">
                        <button type="button" className="btn btn-secondary" onClick={() => getResult()}>Download Result</button>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default App;



// const handleDownload = () => {
//     // Step 1: Create the JSON data
//     const jsonData = {
//         name: "John Doe",
//         age: 30,
//         city: "New York"
//     };
//
//     // Step 2: Convert JSON data to string
//     const jsonString = JSON.stringify(jsonData, null, 2); // Pretty print with 2 spaces
//
//     // Step 3: Create a Blob from the JSON string
//     const blob = new Blob([jsonString], { type: 'application/json' });
//
//     // Step 4: Create a temporary anchor element
//     const link = document.createElement('a');
//
//     // Step 5: Set the download URL as the Blob's URL
//     link.href = URL.createObjectURL(blob);
//
//     // Step 6: Set the download attribute with a file name
//     link.download = 'data.json';
//
//     // Step 7: Programmatically click the link to trigger the download
//     link.click();
//
//     // Step 8: Clean up by revoking the Blob URL
//     URL.revokeObjectURL(link.href);
// };

// <div className="container">
//     <div className="row header">
//         <Header title="Open Research Converter" />
//     </div>
//     <div className="row">
//         <div className="col-6 d-flex flex-column">
//             <div className="mt-2">
//                 <TextBox
//                     customClass={email === "" ? "" : (validEmail ? "custom-valid-focus" : "custom-invalid-focus")}
//                     title={"Email"}
//                     rows={1}
//                     placeholder={'Enter your email address!'}
//                     value={email}
//                     type="email"
//                     onChange={handleEmailChange}
//                 />
//             </div>
//             <div className="mt-2 flex-grow-0 upload-border">
//                 <CsvFileReader className="m-1" setText={setText}/>
//             </div>
//             <div className="mt-2 flex-grow-1">
//                 <TextBox
//                     title={"Input Box"}
//                     rows={10}
//                     placeholder={'DOIs from selected CSV file are displayed here! (OR) Enter comma separated DOIs!'}
//                     value={text}
//                     onChange={handleTextChange}
//                 />
//                 <div className="d-flex justify-content-end">
//                     <button type="button" className="btn btn-secondary" onClick={() => onSubmit()}>Submit</button>
//                 </div>
//             </div>
//         </div>
//         <div className="col-6 mt-2 d-flex flex-column" style={{height: '100%'}}>
//             <TextBox
//                 title={"Result Box"}
//                 rows={14}
//                 placeholder={'Here are the first N results returned!'}
//                 value={jobId}
//                 readOnly={true}
//                 style={{height: '100%'}}
//             />
//             <div className="d-flex justify-content-end mb-1">
//                 <button type="button" className="btn btn-secondary" onClick={() => getResult()}>Download Result</button>
//             </div>
//         </div>
//     </div>
// </div>