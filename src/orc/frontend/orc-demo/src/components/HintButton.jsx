import React, { useState } from 'react';
import input_template from '../images/input_template.PNG';
import './styles/HintButton.sass';

const HintButton = ({ imageName }) => {
    const [showImage, setShowImage] = useState(false);

    return (
        <div style={{ position: 'relative', display: 'inline-block' }}>
            <button
                className="btn btn-style"
                onMouseEnter={() => setShowImage(true)}
                onMouseLeave={() => setShowImage(false)}
            >
                ?
            </button>

            {/* Conditional Rendering of the Image */}
            {showImage && (
                <div className='image-style d-flex flex-column align-items-center'>
                    <b className='txt-color text-center'>Input file format:</b>
                    <img src={imageName==='input_template'? input_template : null} alt="Hint" style={{ width: '500px' }} />
                </div>
            )}
        </div>
    );
};

export default HintButton;
