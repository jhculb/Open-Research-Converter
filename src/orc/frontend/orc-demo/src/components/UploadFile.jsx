import React from 'react';
import './styles/UploadFile.sass';
// import {v4 as uuidv4} from 'uuid';
import SparkMD5 from 'spark-md5'

class UploadFile extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            files: [],
            msg: '',
            fileName: '',
            hashName: ''
        };
        this.onFileChange = this.onFileChange.bind(this)
        this.uploadFileData = this.uploadFileData.bind(this)
        this.md5HashForFile = this.md5HashForFile.bind(this)
    }


    onFileChange = (event) => {
        this.setState({
            // files: event.target.files[0]
            files: event.target.files
        }, function (){
            for (let i = 0; i < this.state.files.length; i++) {
                this.md5HashForFile(this.state.files[i])
            }
        });
    }

    md5HashForFile(file) {
        let blobSlice = File.prototype.slice || File.prototype.mozSlice || File.prototype.webkitSlice,
            chunkSize = 2097152,                             // Read in chunks of 2MB
            chunks = Math.ceil(file.size / chunkSize),
            currentChunk = 0,
            hash = '',
            spark = new SparkMD5.ArrayBuffer(),
            fileReader = new FileReader();

        fileReader.onload = function (e) {
            // console.log('read chunk nr', currentChunk + 1, 'of', chunks);
            spark.append(e.target.result);                   // Append array buffer
            currentChunk++;

            if (currentChunk < chunks) {
                loadNext();
            } else {
                hash = spark.end()
                // console.log('finished loading');
                // console.info('computed hash', hash, typeof (hash));  // Compute hash
                this.setState({
                    hashName: hash
                });
            }
        }.bind(this);

        fileReader.onerror = function () {
            console.warn('oops, something went wrong.');
        };

        function loadNext() {
            let start = currentChunk * chunkSize,
                end = ((start + chunkSize) >= file.size) ? file.size : start + chunkSize;

            fileReader.readAsArrayBuffer(blobSlice.call(file, start, end));

        }

        loadNext();
    }

    uploadFileData = (event) => {
        event.preventDefault();
        this.setState({
            msg: '',
        });
        // let newFileNames = []
        let data = new FormData();
        for (let i = 0; i < this.state.files.length; i++) {
            // let origFileName = this.state.files[i]['name']
            // let newFileName = uuidv4()
            let blob = this.state.files[i].slice(0, this.state.files[i].size, 'application/csv');
            let renamedFile = new File([blob], this.state.hashName + '.csv', {type: 'application/csv'});
            console.log(renamedFile)
            // let renamedFile = new File([blob], origFileName.substring(0, origFileName.indexOf('.pdf')) + '-oc-' + uuidv4() + '.pdf', {type: 'application/pdf'});
            data.append('file', renamedFile)
            // newFileNames.push(this.state.hashName)
        }
        // data.append('file', this.state.files);
        if(this.state.hashName) {
            // fetch('http://localhost:8001/', {
            // fetch('http://193.175.238.110:8001/', {
            // fetch('https://demo-outcite.gesis.org:8001/', {
            // fetch('https://demo-outcite.gesis.org/_upload/', {
            fetch('https://demo-orc.gesis.org/_upload/', {
                method: 'POST',
                body: data
            }).then(response => {
                if (response.status === 200) {
                    this.setState({
                        msg: "File uploaded successfully!",
                        fileName: this.state.hashName
                        // fileName: newFileNames.length > 0 ? newFileNames[0] : ''
                    });
                } else {
                    this.setState({
                        msg: "File uploading failed!"
                    });
                }
                // console.log(this.state.files, data)
            }).catch(err => {
                this.setState({error: err});
            });
        }

    }

    render() {
        let resultURL = 'https://demo-orc.gesis.org/users/';
        // http://outcite.gesis.org:80/users/
            // 'http://193.175.238.110:8003/users/'
        // let resultURL = 'http://localhost:3000/users/'
        return (
            <div className="upload-container mt-3">
                {/*<input multiple="multiple" name="file" onChange={this.onFileChange} type="file" accept=".pdf"/>*/}
                <input name="file" onChange={this.onFileChange} type="file" accept=".csv"/>
                <button className="btn btn-outline-secondary btn-sm" disabled={!this.state.files.length}
                        onClick={this.uploadFileData}>Upload
                </button>
                {this.state.msg==="File uploaded successfully!" ?
                    <div className="alert alert-success alert-dismissible" role="alert">
                        {this.state.msg} <br/>
                        <b>Follow-up ID to Result:</b> {this.state.fileName} <b>OR</b> <br/>
                        <span key={'id'}><b>Hit it for Result: </b>
                            <a className='wrap' href={resultURL+this.state.fileName}
                               target='_blank' rel='noreferrer'>{resultURL+this.state.fileName}</a><br/>
                            <b>Note:</b>Complete process may take a while for new upload, refresh the result page in few minutes. Thank you :)
                        </span>
                    </div> :
                    this.state.msg==="File uploading failed!"?
                        <div className="alert alert-danger alert-dismissible" role="alert">
                            {this.state.msg}
                        </div>
                        :
                        <h6>{this.state.msg}</h6>
                }
            </div>
        )
    }

}

export default UploadFile;
