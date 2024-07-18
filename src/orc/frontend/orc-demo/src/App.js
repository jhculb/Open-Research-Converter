// import logo from './logo.svg';
import React, { useState } from 'react';
import './App.css';
import './components/styles/Header.sass'
import Header from './components/Header';
import TextBox from './components/TextBox';
import UploadFile from "./components/UploadFile";

function App() {
    const [email, setEmail] = useState('');
    const [validEmail, setValidEmail] = useState(false);
    const [text, setText] = useState('');
    const [result, setResult] = useState('');

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
        let domain = 'https://demo-outcite.gesis.org:443/users/_search';
        let params = '?q=_id:0bc9160f0359aeb3e2b766e9cc4a33bc';
        let url = domain + params;

        fetch(url, { method: 'GET'})
            .then(response => response.json())
            .then(result => {
                setResult(JSON.stringify(result));
                console.log('Download Result button pressed: ', result);
            })
            .catch(error => console.log('Download Result button', error));
        //---- in case of sending POST request comment out the upper request (all lines from fetch... till .catch)
        //---- and uncomment the below fetch method
        // fetch(domain, {
        //     method: 'POST',
        //     headers: {
        //         'Content-Type': 'application/json'
        //     },
        //     // for example, data = {sample_json: {field1: ['',...], field2: {...}, ...}, ...}
        //     body: JSON.stringify(data)
        // })
        //     .then(response => response.json())
        //     .then(result => {
        //         setResult(JSON.stringify(result));
        //         console.log('Download Result button pressed: ', result);
        //     })
        //     .catch(error => console.log('Download Result button error', error));
    }

    //---- function called on Submit button press
    const onSubmit = () => {
        //---- endpoint receiving the GET request upon the button press
        let domain = 'https://demo-outcite.gesis.org:443/users/_search';
        let params = '?q=_id:0bc9160f0359aeb3e2b766e9cc4a33bc';
        let url = domain + params;

        fetch(url, { method: 'GET'})
            .then(response => response.json())
            .then(result => {
                setText(JSON.stringify(result));
                console.log('Submit button pressed: ', result);
            })
            .catch(error => console.log('Submit button error', error));
        //---- in case of sending POST request comment out the upper request (all lines from fetch... till .catch)
        //---- and uncomment the below fetch method
        // fetch(domain, {
        //     method: 'POST',
        //     headers: {
        //         'Content-Type': 'application/json'
        //     },
        //     // for example, data = {sample_json: {data: ['',...], data2: {...}, ...}, ...}
        //     body: JSON.stringify(data)
        // })
        //     .then(response => response.json())
        //     .then(result => {
        //         setText(JSON.stringify(result));
        //         console.log('Submit button pressed: ', result);
        //     })
        //     .catch(error => console.log('Submit button error', error));
    }

    return (
    <div className="container">
        <div className="row header">
            <Header title="Open Research Converter - Demo"/>
        </div>
        <div className="row">
            <div className="col-6">
                <TextBox customClass={email===""?"":(validEmail?"custom-valid-focus":"custom-invalid-focus")} title={"Email"} rows={1} placeholder={'Enter your email address!'} value={email} type="email" onChange={handleEmailChange}/>
            </div>
            <div className="col-6 upload-border mt-1 mb-2">
                <UploadFile/>
            </div>
            <div className="col-6">
                <TextBox title={"Text Box"} rows={7} placeholder={'Enter or paste your comma separated strings here!'} value={text} onChange={handleTextChange}/>
                <div className="d-flex justify-content-end mt-2">
                    <button type="button" className="btn btn-secondary" onClick={() => onSubmit()}>Submit</button>
                </div>
            </div>
            <div className="col-6">
                <TextBox title={"Text Box"} rows={7} placeholder={'Here are the first N results returned!'} value={result} readOnly={true}/>
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
