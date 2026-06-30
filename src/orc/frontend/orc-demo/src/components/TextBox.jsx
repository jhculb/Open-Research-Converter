const TextBox = ({ customClass = "", wrapperClassName = "", wrapperStyle, title = "Text Box", rows = 10, placeholder = "Paste your text here...", value, readOnly, onChange, style }) => {
    return (
        <div className={wrapperClassName} style={wrapperStyle}>
            <textarea
                className={"form-control mb-2 " + customClass + " "}
                rows={rows}
                title={title}
                placeholder={placeholder}
                value={value}
                readOnly={readOnly}
                onChange={onChange}
                style={style}
            ></textarea>
        </div>
    );
};

export default TextBox;
