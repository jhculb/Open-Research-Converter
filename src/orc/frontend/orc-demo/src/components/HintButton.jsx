import React, { useState } from 'react';
import input_template from '../images/input_template.PNG';
import './styles/HintButton.sass';

const HintButton = ({ imageName }) => {
    const [showImage, setShowImage] = useState(false);

    return (
        <div style={{ position: 'relative', display: 'inline-block' }}>
            <button
                className="btn btn-style"
                data-testid="hint-button"
                onMouseEnter={() => setShowImage(true)}
                onMouseLeave={() => setShowImage(false)}
            >
                ?
            </button>

            {/* Conditional Rendering of the Image */}
            {showImage && (
                <div className='image-style d-flex flex-column align-items-center'>
                    <b className='txt-color text-center'>Example input file format with header:</b>
                    <img src={imageName === 'input_template' ? input_template : null} alt="Hint" style={{ height: '400px', maxWidth: '600' }} />
                </div>
            )}
        </div>
    );
};

export default HintButton;
