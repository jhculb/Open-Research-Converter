# ORC project
## Table of Contents
1. [Demo](#demo)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Running the App](#running-the-app)
6. [Technologies Used](#technologies-used)
7. [Folder Structure](#folder-structure)
8. [License](#license)
9. [Contributing](#contributing)
10. [Developers](#developers)
11. [Acknowledgements](#acknowledgements)

## Demo
URL: https://orc-demo.gesis.org/

## Features
Main features of the app:
- Users provided input DOIs (as a comma separated string or single column CSV file upto max. size of 1 Mb) are converted to OpenAlex IDs
- For the input provided, the IDs or Full Records could be downloaded as a CSV file.

## Prerequisites
List the necessary requirements to run the React app:
- node=22.9.0 and npm=10.8.3

## Installation
- install node.js and npm (for me the working versions are node=22.9.0 and npm=10.8.3)
- go to directory: `cd /src/orc/frontend/orc-demo`
- `npm install` to install required modules/packages before running

## Running the App
- `npm start` to run the app in the development mode
- view running app using `http://localhost:3000/`
- `npm run build` to create a production build

## Technologies Used
- ReactJS ([Create React App](https://github.com/facebook/create-react-app))
- react-router-dom (for routing)
- Bootstrap
- Fetch API
- Sass: Syntactically Awesome Style Sheets

## Folder Structure
```
src/ 
├── orc/ 
    ├── frontend/ 
        ├── orc-demo/ 
            ├── src/ 
                ├── components/ # Reusable UI components
                    ├── styles/ # Style sheets for each component  
                ├── images/ # Contains the logos and images used  
                ├── App.js # Main application component and entry point
                └── App.css # Style sheet for main application
```

## License
This work is licenced under [GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.de.html), or later.

## Contributing
Your suggestions and feedback are welcome. Kindly explore project's [GitHub Repository](https://github.com/jhculb/Open-Research-Converter/issues) to report a problem or to open a new issue.

## Developers
- Jack H. Culbert - Lead Developer [ORCID](https://orcid.org/0009-0000-1581-4021) [LinkedIn](https://www.linkedin.com/in/jack-c-2485989a/) [GitHub](https://github.com/jhculb)
- Muhammad Ahsan Shahid - Frontend Developer [ORCID](https://orcid.org/0000-0002-7274-7934) [LinkedIn](https://www.linkedin.com/in/muhammad-ahsan-shahid/) [GitHub](https://github.com/MAhsanShahid)
- Philipp Mayr - Team Lead [ORCID](https://orcid.org/0000-0002-6656-1658)

## Acknowledgements
- The Open Research Converter (ORC) is a tool designed to allow users to convert proprietary and licensed bibliometric datasets to a shareable format through [OpenAlex](https://openalex.org/)'s [API](https://docs.openalex.org/how-to-use-the-api/api-overview).
- This work was funded by the [Federal Ministry of Education and Research (BMBF)](https://www.bmbf.de/bmbf/en/home/home_node.html) via funding numbers: 16WIK2301B / 16WIK2301E, the [OpenBib](https://www.openbib.org/) project. We acknowledge support by Federal Ministry of Education and Research, Germany under grant number 01PQ17001, the Competence Network for Bibliometrics.
- Jack Culbert and Philipp Mayr received additional funding by the European Union under the Horizon Europe grant OMINO – Overcoming Multilevel INformation Overload under grant number 101086321.
