import {Component} from "react";
import './styles/Header.sass'
import orc_logo from '../images/orc-logo.png'

class Header extends Component {
    render() {
        return <>
            <h1 className="col-12 d-flex justify-content-center">
                {this.props.title}
            </h1>
            <div className="col-12 d-flex justify-content-center">
                <img className='img-header' src={orc_logo} alt="orc" onClick={()=>window.open("http://localhost:3000/", "_self")}/>
            </div>
        </>;
    }
}

export default Header;
