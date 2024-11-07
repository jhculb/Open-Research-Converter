import { Route, Routes } from 'react-router-dom';
import '@fortawesome/fontawesome-free/css/all.css';
import './App.css';
import Header from './components/Header';
import About from './components/About';
import Home from './components/Home';
import Footer from './components/Footer';

function App() {
    const pathName = window.location.pathname; // Access the current path
    // Check the current path
    const isHome = pathName === '/';

    return (
        <div className="container">
            <div className="row header-border mb-4 mt-2 align-items-center">
                <Header title="Open Research Converter" href="https://www.gesis.org/" isHome={isHome} />
            </div>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/about" element={<About />} />
            </Routes>
            <div className="row mt-4">
                <Footer></Footer>
            </div>
        </div>
    );
}

export default App;
