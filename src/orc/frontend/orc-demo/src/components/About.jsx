import React from 'react';
import './styles/About.sass';

const About = () => {
    return <div className="row align-items-center justify-content-center">
        <div className="col-md-11">
            <h2 className="text-center headings-color">About ORC</h2>
            <p>
                The <a href="https://orc-demo.gesis.org" target="_blank" rel="noopener noreferrer">
                Open Research Converter (ORC)</a> is a tool designed to allow users to convert proprietary and licensed
                bibliometric datasets to a shareable format through&nbsp;
                <a href="https://openalex.org" target="_blank" rel="noopener noreferrer">OpenAlex</a>'s API
                (<a href="https://docs.openalex.org/how-to-use-the-api/api-overview" target="_blank" rel="noopener noreferrer">API documentation</a>).
            </p>
            <p>
                Try out the ORC demo where you can trial the functionality.
                This URL may be subject to change or to removal after a period of time.
            </p>

            <h4 className="headings-color mt-3">How to use it?</h4>
            <h5 className="headings-color"><i className="fas fa-book me-2"></i>Instructions</h5>
            <ol>
                <li>Navigate to <a href="https://orc-demo.gesis.org" target="_blank" rel="noopener noreferrer">https://orc-demo.gesis.org</a></li>
                <li>Fill in your email address into the email box. This is so that OpenAlex can monitor traffic and places your requests in the "polite pool," where responses are faster and more consistent.</li>
                <li>Input your DOI data:</li>
                <ul>
                    <li><strong>Via text box:</strong> The ORC expects a comma-separated list of DOIs. It does not mind whether DOIs are prefaced with "https://doi.org/"</li>
                    <li><strong>Via CSV file:</strong> Browse to select a CSV file with maximum size of 1 Megabyte, which will be read into the text box. The ORC expects a single column of DOIs with a header. If the first row contains a DOI, it will not be parsed.</li>
                    <li><strong>Via copy-paste:</strong> You can also manually copy and paste your DOI data into the text box. The ORC can accept thousands of DOIs, but it may take a few minutes to process.</li>
                </ul>
                <li>Click Submit</li>
                <ul>
                    <li>A waiting animation should appear in the right-hand output box. If it flashes and disappears, your query may have been unsuccessful. Please try again or check your input. </li>
                </ul>
                <li>Wait for Output</li>
                <ul>
                    <li>If successful, the first 50 OpenAlex IDs corresponding to your DOIs will appear in the output box. If you submitted more than 50 DOIs, click "download CSV" to download a file containing the DOI in the first column and the OpenAlex ID in the second.</li>
                </ul>
            </ol>

            <h6 className="headings-color"><i className="fas fa-tools me-2"></i>Local Installation</h6>
            <p>
                If you wish to run the ORC locally, please go to <a href="https://github.com/jhculb/Open-Research-Converter?tab=readme-ov-file#local-installation" target="_blank" rel="noopener noreferrer">Local Installation </a>
            </p>

            <h6 className="headings-color"><i className="fas fa-pen me-2"></i>Want to Cite?</h6>
            <p>
                As of release on the 16th of September 2024: This software is being submitted to <a href="https://joss.theoj.org/" target="_blank" rel="noopener noreferrer">JOSS</a>, citation details pending.
            </p>

            <h6 className="headings-color"><i className="fas fa-bug me-2"></i>Report an issue</h6>
            <p>
                You are welcome to report a problem or to open a new ticket, kindly go to <a href="https://github.com/jhculb/Open-Research-Converter/issues" target="_blank" rel="noopener noreferrer">Open Issue </a>
            </p>

            <h4 className="headings-color"><i className="fas fa-lightbulb me-2"></i>How it works?</h4>
            <p>
                The input is being processed after sending the request to the respective API endpoint on the ORC server which further calls OpenAlex's API to process the input and provide the output.
            </p>
            <p>
                This output data is returned and displayed as a response to your request.
            </p>
            <p>
                We also log the request data for our record and further processing like calculating the number of users and successful requests.
            </p>

            <h6 className="headings-color"><i className="fas fa-exclamation-triangle me-2"></i>OpenAlex Request Limits</h6>
            <p>
                OpenAlex has a limit of 500 items per 10 seconds, therefore the users requests might be slow.
            </p>

            <h6 className="headings-color"><i className="fas fa-sticky-note me-2"></i>Note</h6>
            This tool is in development and may not perform perfectly:
            <ul>
                <li>If items are not found in OpenAlex, they may not be returned, leading to a smaller number of items in the output.</li>
                <li>
                    If an error happens on the backend it may not inform the frontend properly, leading to a failure (when the waiting ring disappears) without informing the user why.
                </li>
            </ul>

            <h4 className="headings-color"><i className="fas fa-users me-2 mt-3"></i>Team</h4>
            <ul className="list-unstyled mt-2">
                <li>
                    <i className="fas fa-user me-2 headings-color"></i>
                    Jack H. Culbert - Lead Developer
                    <span className="ms-2">
                        <a href="https://orcid.org/0009-0000-1581-4021" target="_blank" rel="noopener noreferrer">ORCID</a> <a href="https://www.linkedin.com/in/jack-c-2485989a/" target="_blank" rel="noopener noreferrer">LinkedIn</a> <a href="https://github.com/jhculb" target="_blank" rel="noopener noreferrer">GitHub</a>
                    </span>
                </li>
                <li className="mt-1">
                    <i className="fas fa-user me-2 headings-color"></i>
                    Muhammad Ahsan Shahid - Frontend Developer
                    <span className="ms-2">
                        <a href="https://orcid.org/0000-0002-7274-7934" target="_blank" rel="noopener noreferrer">ORCID</a> <a href="https://www.linkedin.com/in/muhammad-ahsan-shahid/" target="_blank" rel="noopener noreferrer">LinkedIn</a> <a href="https://github.com/MAhsanShahid" target="_blank" rel="noopener noreferrer">GitHub</a>
                    </span>
                </li>
                <li className="mt-1">
                    <i className="fas fa-user me-2 headings-color"></i>
                    Philipp Mayr - Team Lead
                    <span className="ms-2">
                        <a href="https://orcid.org/0000-0002-6656-1658" target="_blank" rel="noopener noreferrer">ORCID</a>
                    </span>
                </li>
            </ul>

            <h4 className="headings-color"><i className="fas fa-certificate me-2 mt-3"></i>License</h4>
            <p>
                This work is licenced under <a href="https://www.gnu.org/licenses/gpl-3.0-standalone.html" target="_blank" rel="noopener noreferrer">GPL-3.0</a>, or later.
            </p>

            <h4 className="headings-color"><i className="fas fa-dollar-sign me-2 mt-3"></i>Funding</h4>
            <p>
                This work was funded by the <a href="https://www.bmbf.de/bmbf/en/home/home_node.html" target="_blank" rel="noopener noreferrer">
                Federal Ministry of Education and Research (BMBF)
            </a> via funding numbers: 16WIK2301B /
                16WIK2301E, The <a href="https://bibliometrie.info/forschung/" target="_blank" rel="noopener noreferrer">
                OPENBIB
                </a> project.
                We acknowledge support by Federal Ministry of Education and Research, Germany under grant number
                01PQ17001, the Competence Network for Bibliometrics.
            </p>
            <p>
                Jack Culbert and Philipp Mayr received additional funding by the European Union under the Horizon Europe
                grant OMINO – Overcoming Multilevel INformation Overload under grant number 101086321.
            </p>
        </div>
    </div>;
};

export default About;