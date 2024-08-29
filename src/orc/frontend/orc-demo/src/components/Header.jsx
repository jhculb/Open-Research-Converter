import {Component} from "react";
import './styles/Header.sass'
import orc_logo from '../images/orc-logo.png'
import gesis_logo from '../images/logo_gesis.svg'

class Header extends Component {
    render() {
        return <>
            {/*<div className="col-2">*/}
            {/*    <img className="mt-2 justify-content-center" src={gesis_logo} alt="gesis" onClick={()=>window.open("http://localhost/", "_self")}/>*/}
            {/*</div>*/}
            {/*<h1 className="col-10 mt-2 d-flex justify-content-center">*/}
            {/*    {this.props.title}*/}
            {/*</h1>*/}
            <h1 className="col-12 d-flex justify-content-center">
                {this.props.title}
            </h1>
            <div className="col-12 d-flex justify-content-center">
                <img className='img-header' src={orc_logo} alt="orc" onClick={()=>window.open("http://localhost/", "_self")}/>
            </div>
        </>;
    }
}

export default Header;
