const TextBox = ({ customClass = "", title = "Text Box", rows = 10, placeholder = "Paste your text here...", value, readOnly, onChange }) => {
    return (
        <div>
            <textarea
                className={"form-control mb-2 " + customClass + " "}
                rows={rows}
                title={title}
                placeholder={placeholder}
                value={value}
                readOnly={readOnly}
                onChange={onChange}
            ></textarea>
        </div>
    );
};

export default TextBox;
