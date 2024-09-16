const TextBox = ({ customClass="", title="Text Box", rows=10, placeholder="Paste your text here...", value, type="text", readOnly, onChange }) => {
    return (
        <div>
            {/*<h1 className="mb-4">{title}</h1>*/}
            {type==="email"?(
                <input
                    type="email"
                    className={"form-control " + customClass + " "}
                    placeholder={placeholder}
                    value={value}
                    onChange={onChange}
                    readOnly={readOnly}
                />
            ):(
                <textarea
                    className={"form-control mb-2 " + customClass + " "}
                    rows={rows}
                    placeholder={placeholder}
                    value={value}
                    readOnly={readOnly}
                    onChange={onChange}
                ></textarea>
            )}
        </div>
    );
};

export default TextBox;
