import {Component} from "react";
import './styles/Header.sass';
import orc_logo from '../images/orc-logo.png';
import gesis_logo from '../images/logo_gesis.svg';

class Header extends Component {
    render() {
        return <>
            <div className="col-12 col-md-2 d-flex justify-content-center justify-content-md-start">
                <img className="mt-2 img-fluid img-header" src={gesis_logo} alt="gesis" onClick={()=>window.open(this.props.href, "_self")}/>
            </div>
            <div className="col-12 col-md-10 mt-2 d-flex justify-content-center justify-content-md-center">
                <h1 className="title-color text-center mr-md-100">
                    {this.props.title}
                </h1>
            </div>
        </>;
    }
}

export default Header;
