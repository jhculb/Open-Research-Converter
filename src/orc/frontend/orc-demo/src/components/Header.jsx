import { Component } from "react";
import './styles/Header.sass';
import gesis_logo from '../images/logo_gesis_en.svg';

class Header extends Component {
    render() {
        return <>
            <div className="col-12 col-md-2 d-flex justify-content-center justify-content-md-start">
                <img className="mt-2 img-fluid img-header" src={gesis_logo} alt="gesis" onClick={() => window.open(this.props.href, "_self")} />
            </div>
            <div className="col-12 col-md-9 mt-2 d-flex justify-content-center justify-content-md-center">
                <h1 className="title-color text-center mr-md-75">
                    {this.props.title}
                </h1>
            </div>
            <div className="col-12 col-md-1 mt-2 d-flex justify-content-center justify-content-md-end align-self-end">
                {
                    this.props.isHome ?
                        <a data-testid="is-home" href="/about" className="mb-0 link-color" style={{ fontSize: '22px' }}>
                            About
                        </a>
                        :
                        <a data-testid="is-not-home" href="/" className="mb-0 link-color">
                            <i className="fas fa-home fa-2x"></i>
                        </a>
                }
            </div>
        </>;
    }
}

export default Header;
