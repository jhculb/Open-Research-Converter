import React from 'react';
import './styles/Footer.sass'
import kb_logo from '../images/KB_logo.svg';
import Bmbf from '../images/bmbf.svg';
const Footer = () => {
    return (
        <footer className="footer-bg-color text-color text-center">
            <div className="container mt-3">
                <a href="https://www.gesis.org/en/institute/imprint" className="mb-0 link-color">GESIS - Imprint </a> &nbsp;|&nbsp;
                <a href="https://bibliometrie.info/en/research" className="mb-0 link-color">Project Website </a> &nbsp;|&nbsp;
                <a href="https://github.com/jhculb/Open-Research-Converter" className="mb-0 link-color">Codebase </a>
                <p className="mb-0 text-color">E-mail:
                    <span className="email-color ms-1"> john.culbert@gesis.org</span> &nbsp;|
                    <span className="email-color ms-1"> ahsan.shahid@gesis.org</span>
                </p>
                <p className="mt-2">
                    <a href="https://www.bmbf.de/bmbf/en/home/home_node.html" target="_blank" rel="noopener noreferrer">
                        <img src={Bmbf} alt="Bmbf" style={{height: '120px', maxWidth:'180px', verticalAlign: 'middle'}}/>
                    </a>
                    &nbsp;&nbsp;
                    <a href="https://bibliometrie.info/forschung/" target="_blank" rel="noopener noreferrer">
                        <img src={kb_logo} alt="Kb" style={{backgroundColor:'#2596be', height: '120px', maxWidth:'180px', verticalAlign: 'middle', padding:'5px'}}/>
                    </a>
                </p>
            </div>
        </footer>
    );
}

export default Footer;
