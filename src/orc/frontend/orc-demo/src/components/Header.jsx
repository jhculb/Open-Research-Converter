import {Component} from "react";
import './styles/Header.sass';
// import orc_logo from '../images/orc-logo.png';
import gesis_logo from '../images/logo_gesis.svg';

class Header extends Component {
    render() {
        return <>
            <div className="col-12 col-md-2 d-flex justify-content-center justify-content-md-start">
                <img className="mt-2 img-fluid img-header" src={gesis_logo} alt="gesis" onClick={()=>window.open(this.props.href, "_self")}/>
            </div>
            <div className="col-12 col-md-9 mt-2 d-flex justify-content-center justify-content-md-center">
                <h1 className="title-color text-center mr-md-75">
                    {this.props.title}
                </h1>
            </div>
            <div className="col-12 col-md-1 mt-2 d-flex justify-content-center justify-content-md-end align-self-end">
                {
                    this.props.isHome?
                        <a href="/about" className="mb-0 link-color">
                            <i className="fas fa-info-circle fa-2x"></i>
                        </a>
                        :
                        <a href="/" className="mb-0 link-color">
                            <i className="fas fa-home fa-2x"></i>
                        </a>
                }
            </div>
        </>;
    }
}

export default Header;
