import React from 'react';
import './styles/Footer.sass'
const Footer = () => {
    return (
        <footer className="footer-bg-color text-color text-center py-3">
            <div className="container">
                <a href="https://www.gesis.org/en/institute/imprint" className="mb-0 link-color">GESIS - Imprint </a> &nbsp;|&nbsp;
                <a href="https://bibliometrie.info/en/research" className="mb-0 link-color">Project Website </a> &nbsp;|&nbsp;
                <a href="https://github.com/jhculb/Open-Research-Converter" className="mb-0 link-color">About </a>
                <p className="mb-0 text-color">E-mail:
                    <span className="email-color mx-2">john.culbert@gesis.org</span>|
                    <span className="email-color mx-2">ahsan.shahid@gesis.org</span>
                </p>
            </div>
        </footer>
    );
}

export default Footer;
