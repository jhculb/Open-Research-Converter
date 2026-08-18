
# Open Research Converter
## Description
The [Open Research Converter (ORC)](https://orc-demo.gesis.org) is a tool designed to allow users to convert proprietary and licensed bibliometric datasets to a shareable format through [OpenAlex](https://openalex.org)'s API ([API documentation found here](https://docs.openalex.org/how-to-use-the-api/api-overview)).

The Open Research Converter has a demo running at [orc-demo.gesis.org](https://orc-demo.gesis.org) where you can trial the functionality. This url may be subject to change or to removal after a period of time.
## Statement of Need
Bibliometrics and in particular Scientometrics suffers from a lack of reproducibility, wherein the databases used to perform bibliometrics are often proprietary and therefore bound by copyright and access agreements which forbid sharing the underlying data used to create the scientific insights shared in papers.

OpenAlex released in 2022 and is a open-source bibliometric database compiled by [Our Research](https://ourresearch.org/) which releases its data with a maximally permissive copyright (specifically under the [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/) deed), allowing free sharing of all data. This has allowed bibliometric researchers to download and interrogate the data as they see fit, and enables sharing of data.

However, dealing with OpenAlex data can be cumbersome. The methods of access are currently via the [website](https://openalex.org/), [API](https://api.openalex.org/), or a [data dump](https://docs.openalex.org/download-all-data/openalex-snapshot), each of which have challenges for researchers associated with it. Namely, to use the website limits the amount of information available to be displayed and may require downloading and then processing the data further to achieve the desired insights, to use the API requires a level of technical knowledge and is rate limited by OpenAlex, and the data dumps are very large (approximately 300GB at time of writing) and also require technical knowledge in the processing and interrogation of the data.

Easing the barrier of access to OpenAlex is a current theme of work in the bibliometrics community, for example @massimo_2024 have created a tool in the R programming language, [openalexR](https://docs.ropensci.org/openalexR/), capable of bulk collection of OpenAlex data and processing this data from OpenAlex's JSON based data format to a tabular format. Similarly [OpenAlex Networks](https://github.com/filipinascimento/openalexnet) is a Python library for generation of OpenAlex datasets and processing of citation and coauthorship networks. [OpenAlexNet](https://www.nuget.org/packages/OpenAlexNet) is a C# wrapper for OpenAlex enabling searching of OpenAlex.

Currently OpenAlex has no easy method for researchers to convert their datasets from proprietary formats to OpenAlex. While it is possible to manually convert smaller datasets using OpenAlex's website, or download the OpenAlex data dump and process this to enable matching.

We provide here in the Open Research Coverter a tool utilising the OpenAlex API enabling simple bulk conversion of bilbiometric data to a shareable format.

## Table of Contents
- [Open Research Converter](#open-research-converter)
	- [Description](#description)
	- [Statement of Need](#statement-of-need)
	- [Table of Contents](#table-of-contents)
	- [How to Use the ORC](#how-to-use-the-orc)
		- [Online](#online)
		- [Local Installation (Docker)](#local-installation-docker)
		- [Local Installation (Without Docker)](#local-installation-without-docker)
		- [Please Note](#please-note)
	- [API Documentation](#api-documentation)
		- [Endpoints Summary](#endpoints-summary)
		- [Example Request](#example-request)
		- [Response Format](#response-format)
	- [Process Flow](#process-flow)
	- [Functionality](#functionality)
		- [NGINX Container](#nginx-container)
		- [Frontend Container](#frontend-container)
		- [Backend Container](#backend-container)
	- [Development](#development)
		- [CI/CD](#cicd)
			- [Testing](#testing)
				- [Frontend](#frontend)
				- [Backend](#backend)
			- [Dependency Management](#dependency-management)
			- [CI/CD Configuration](#cicd-configuration)
		- [Known Bugs](#known-bugs)
		- [Planned Features](#planned-features)
			- [Major](#major)
			- [Minor](#minor)
		- [Contributing](#contributing)
		- [Tips for Development](#tips-for-development)
		- [Support](#support)
	- [Credits](#credits)
		- [Developers](#developers)
		- [Funding](#funding)
	- [How to Cite](#how-to-cite)
		- [Thanks](#thanks)
	- [License](#license)

## How to Use the ORC
### Online
If you wish to use the ORC without installing locally:
1. Navigate to https://orc-demo.gesis.org
2. Input your DOI data:
	* The ORC expects a comma separated list of DOIs in the text box
	* The ORC does not mind whether DOIs are prefaced with "https://doi.org/"
	1. Via csv file
		* Browse to select a csv file, this shall be read into the text box
		* The ORC expects a single column of DOIs with a header
			* Therefore if the first row contains a DOI this will be not be parsed into the text box
	2. Via copy and paste into the text box
		* You can also manually copy and paste your DOI data into the text box
	* The ORC can accept thousands of DOIs, though this may take a few minutes.
3. Click Submit
	* A waiting animation should play in the right hand output box, if this flashes and then disappears your query may have been unsuccessful. Please try one more time, and then check your input.
4. Wait for Output
	* If your query is successful, then in the output box the first 50 OpenAlex IDs corresponding to your DOIs will be returned.
	* If you have more submitted than 50 DOIs, then click "download CSV" to download a csv file with the DOI in the first column and the corresponding OpenAlex ID in the second column.
### Local Installation (Docker)
Should you wish to run the ORC locally using Docker, please follow these steps:

**Prerequisites:** Docker and Docker Compose installed, an OpenAlex API key has been obtained ([see here](https://developers.openalex.org/api-reference/introduction))

**Step 1: Set up environment variables**

The root `.env` file is *required* as it configures which nginx configuration to use.

Via makefile (Linux/macOS):
```bash
make set_envs
```

Or manually:
```bash
# IMPORTANT: Copy the root .env.template first
cp .env.template .env

# Then copy the service-specific env files
cp src/env_templates/backend.env.template src/env/backend.env
cp src/env_templates/frontend.env.template src/env/frontend.env
cp src/env_templates/js.env.template src/env/js.env
cp src/env_templates/nginx.env.template src/env/nginx.env
```

**Note:** The root `.env` file sets `LOCAL_OR_PRODUCTION=local`, which tells Docker which nginx config to use (`local.default.conf` vs `prod.default.conf`). Without this file, docker-compose will fail with "`.default.conf`: not found".

**API Key:** An [OpenAlex API key](https://openalex.org/) is required. Replace the placeholder in `src/env/backend.env`:
```
OPENALEX_API_KEY=your-api-key
```

**Step 2: Build and run**
```bash
docker compose up --build -d
# Or via makefile: make run
```

**Step 3: Access the application**

Navigate to `http://localhost` or `http://127.0.0.1`
(Note, if your browser gives secure connection is not available, please check you are not using https)

### Local Installation (Without Docker)

For development without Docker, you can run the backend and frontend separately.

**Prerequisites:**
- Python 3.11+
- Node.js 16+ (or 22 for latest)
- Poetry (Python package manager)

**Backend Setup:**
```bash
# From project root
poetry install

# Set your OpenAlex API key
export OPENALEX_API_KEY=your-api-key  # Linux/macOS
# $env:OPENALEX_API_KEY="your-api-key"  # Windows (PowerShell)

# Run the backend server on port 8001
poetry run python -m quart --app src.orc.backend.orc_backend.app run --port 8001
```
If successful, browsing to http://127.0.0.1:8001 should present an HTML page with the heading: "ORC API using quart".

**Frontend Setup:**
```bash
cd src/orc/frontend/orc-demo

# Install dependencies
npm install

# Start the development server
npm start
```

**Note:** `src/orc/frontend/orc-demo/.env` is pre-configured with `REACT_APP_DEV_URL=http://localhost:8001` for local development. If you need to change the backend URL, edit that file directly in a text editor (do not use shell redirection such as `echo … > .env`, as this produces a BOM-encoded file that the React toolchain cannot read).

**CORS Configuration:**

When running frontend and backend separately, you may encounter CORS issues. Two solutions:

1. **Add proxy to package.json** (recommended for development):
   ```json
   {
     "proxy": "http://localhost:8001"
   }
   ```
   Then change `REACT_APP_DEV_URL` to empty string or `/`.

2. **Add CORS headers to backend** (for testing only - not recommended for production)
### Please Note
* The ORC is still in development and may contain bugs, for example:
	* If items are not found in OpenAlex, they may not be returned leading to a smaller number of items in the output
	* If an error happens on the backend it may not inform the frontend properly, leading to a failure (when the waiting ring disappears) without informing the user as to why.
## API Documentation

The ORC exposes a REST API for programmatic access. Full OpenAPI specification is available at `src/orc/backend/orc_backend/openapi.yaml`.

### Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information page (served directly at http://host:8001/) |
| GET | `/api/healthcheck` | Check OpenAlex API connectivity (returns 418 if healthy) |
| POST | `/api/start_processing` | Convert DOIs to OpenAlex IDs |
| POST | `/api/process_all` | Convert DOIs and get full OpenAlex metadata |

### Example Request

```bash
curl -X POST https://orc-demo.gesis.org/api/start_processing \
  -H "Content-Type: application/json" \
  -d '{"input_data": "10.1038/nature12373, 10.1126/science.1231143"}'
```

### Response Format

```json
{
  "job_id": "uuid-string",
  "output_data": ["https://openalex.org/W2102245935", "https://openalex.org/W2015936098"],
  "output_full": "doi, oa_id\n...",
  "submitted_count": 2,
  "found_count": 2,
  "missing_dois": [],
  "invalid_dois": ["not-a-doi"]
}
```

The response includes:
- `submitted_count`: Number of valid DOIs submitted for processing
- `found_count`: Number of DOIs found in OpenAlex
- `missing_dois`: List of valid DOIs not found in OpenAlex
- `invalid_dois`: List of input strings that failed DOI format validation

## Process Flow

This section describes the complete flow from when a user submits DOIs to when results are returned.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER INTERFACE                                 │
│  1. User enters DOIs (via text input or CSV upload)                         │
│  2. User clicks "Submit"                                                    │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           FRONTEND (React)                                  │
│  3. Sends POST request to /api/start_processing with DOI list               │
│  4. Displays loading animation while waiting                                │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      BACKEND API (app.py)                                   │
│  6. Receives request at /start_processing endpoint                          │
│  7. Creates OpenResearchConverter instance                                  │
│  8. Calls process() method with input data                                  │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│              ORCHESTRATOR (open_research_converter.py)                      │
│  9.  generate_new_job() - Creates unique job ID (UUID)                      │
│  10. _receive_data() - Stores raw input in job dictionary                   │
│  11. _validate_input_data() - Validates:                                    │
│      • Job ID exists                                                        │
│      • Partitions DOIs into valid and invalid (Step 11a)                    │
│      • Invalid DOIs are stored separately and reported to the user          │
│      • Processing continues with valid DOIs only                            │
│  12. Normalizes DOIs to standard format (https://doi.org/...)               │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    REQUESTER (requester.py)                                 │
│  13. _chunk_input_data() - Splits DOIs into chunks of 50                    │
│  14. _prepare_chunks() - Formats each chunk into OpenAlex API query         │
│      • Creates filter query: works?filter=doi:DOI1|DOI2|DOI3...             │
│  15. _process_aio() - Sends concurrent requests using aiometer              │
│      • Respects rate limits (max 10 requests/second)                        │
│      • Implements exponential backoff on failures                           │
│  16. Collects responses and extracts DOI → OpenAlex ID pairs                │
│  17. Compares returned DOIs against submitted DOIs                          │
│  18. Tracks missing DOIs (submitted but not found in OpenAlex)              │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         RESPONSE ASSEMBLY                                   │
│  19. return_data() - Formats final response:                                │
│      • output_data: List of OpenAlex IDs                                    │
│      • output_full: CSV string (doi, oa_id)                                 │
│      • submitted_count: Valid DOIs submitted for processing                 │
│      • found_count: DOIs successfully matched                               │
│      • missing_dois: DOIs not found in OpenAlex                             │
│      • invalid_dois: Input strings that failed DOI format validation        │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           FRONTEND (React)                                  │
│  20. Receives JSON response                                                 │
│  21. Displays counter: "Found X/Y" (found_count/submitted_count)            │
│  22. Shows first 50 OpenAlex IDs in output box                              │
│  23. Enables "Download CSV" button for full results                         │
│  24. If invalid DOIs exist, shows expandable section to view/download them  │
│  25. If missing DOIs exist, shows expandable section to view/download them  │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Functionality
The ORC functions in a containerised environment. To run this using the makefile type `make run`.

There are three containers that are initialised, a nginx container that acts as a reverse proxy, a frontend container that serves a JavaScript based website, and a backend container which has the processing and API interface.

### NGINX Container
Acts as reverse proxy for front- and back-end containers. Copies in robots and 404 html pages and has two potential configurations, local and prod. Which of these is chosen is selected by the .env in the TLD.

Local.default.conf is a simpler configuration designed for running the ORC locally. If you wish to deploy to a server to host ORC and wish to enable SSH, prod.default.conf allows for this configuration using certbot. The commands to trial and run the certbot authentication are in the makefile `certificates_dry_run` and `certificates_create_and_load` respectively. Further certbot configuration is found in the docker-compose.yml.

### Frontend Container
A separate README detailing the Frontend container can be found at `src/orc/frontend/orc-demo/README.md`

### Backend Container
Exposes port 8001 for app traffic.

Utilises Gunicorn for serving the app. Worker count and other parameters can be configured via `GUNICORN_NUM_WORKERS` in `src/env/backend.env` (defaults to 9). Additional parameters can be changed in the ENTRYPOINT command in the Dockerfile.

* app.py
	- Contains async API to interface with the JavaScript Application
	* Route ``/`` - hello_world
		- Returns root HTML with noindex Robots
	* Route ``/healthcheck``
		- Queries OpenAlex to check there is a working connection
	* Route ``/start_processing`` (Steps 6-8)
		- Queries OpenAlex for WorkIDs
	* Route ``/process_all`` (Steps 6-8)
		- Queries OpenAlex for full bibliographic records
* open_research_converter.py
	* OpenResearchConverter
		- Contains code to coordinate processing the input DOIs (data) and returned values from OpenAlex (superclass of OpenAlexRequester)
		* generate_new_job (Step 9)
			- Creates UUID for job and assigns memory in dictionary for data
		* process
			- Checks input data is correctly formatted and begins querying OpenAlex for WorkIDs
		* process_all
			- Checks input data is correctly formatted and begins querying OpenAlex for full bibliometric data
		* return_data (Step 19)
			- Formats and returns data to frontend
		* Private Functions:
			* _recieve_data (Step 10)
				- Stores input data with best effort to reformat correctly
			* _validate_input_data (Step 11)
				- Checks job exists and partitions DOIs into valid and invalid
			* _partition_dois (Step 11a)
				- Separates input strings into valid and invalid DOIs; invalid DOIs are stored and reported, valid DOIs proceed to processing
			* _validate_uuid
				- Checks the UUID is in the job dictionary
			* _validate_data
				- Checks the data is a list of valid dois (with or without `https://doi.org/` prefix).
			* _doi_list_formatter (Step 12)
				- Normalizes DOIs to include the https://doi.org/ prefix
			* _check_ready
				- Checks the formatted data (post _validate_data) is in the dictionary
* requester.py
	* OpenAlexRequester
		- Base class for accessing OpenAlex API using asynchronous httpx client and exponential backoff in case of rate limit breaking.
		* health_check
			- Tests connection to OpenAlex API
		* Private Functions
			* _process_aio (Steps 15-18)
				- Coordinates processing the data (chunking, formatting requests) and sending requests to OpenAlex to return WorkIDs with aiometer. Collects responses, compares returned DOIs against submitted, and tracks missing DOIs.
			* _process_all (Steps 15-18)
				- Coordinates processing the data (chunking, formatting requests) and sending requests to OpenAlex to return full bibliographic records with aiometer. Collects responses, compares returned DOIs against submitted, and tracks missing DOIs.
			* _prepare_chunks (Step 14)
				- Takes DOI chunk and formats into a request to OpenAlex API for WorkIDs
			* _prepare_chunks_full (Step 14)
				- Takes DOI chunk and formats into a request to OpenAlex API for full bibliographic data
			* _chunk_input_data (Step 13)
				- Splits data into 'chunks' of 50 DOIs
			* _doi_str_formatter (Step 12)
				- Regularises DOIs to https prefix and lowercase
			* _fetch
				- Sends requests to OpenAlex API using aioclient and implements exponential backoff


## Development
### CI/CD
The ORC was built with a Gitlab CI/CD specific to GESIS. We have included in v1.1.0 a thinner Github CI/CD template. The majority of commands and testing used can be replicated via the Makefile. We include the structure of the current Gitlab CI/CD here:
- Build
- Lint
  - Ruff
    - `ruff check ./src`
- Test
  - Coverage using Pytest
    - `poetry run coverage run -m pytest -m "" ./tests`
  - Bandit
    - `bandit -c pyproject.toml -r ./src/ --format txt > bandit.txt`
  - Pyright
    - `pyright ./src --outputjson > report_raw.json`
- Deploy
#### Testing
##### Frontend
Frontend Testing must be run from `src/orc/frontend/orc-demo/` with `npm test`.
##### Backend
Backend Tests can be found in `tests/`. A csv of DOIs from Jason Priem (founder of OpenAlex) and the associated OpenAlex WorkIDs can be found in `tests/fixtures/priem.csv`. Similarly in ``test_requester.py`` and ``test_open_research_converter.py`` in ``tests/`` one may find lists of DOIs and associated WorkIDs used for testing the ORC. A guide for creating your own test set is found in `tests/fixtures/extraction.md`.
#### Dependency Management
All dependency management for the backend is managed by poetry. For the frontend it is captured in ``package.json`` and `package-lock.json`.
#### CI/CD Configuration
Following PEP621, configuration for core project metadata is stored in the pyproject.toml where possible.
### Known Bugs
1. [B1] - Error handling is currently not performed on the frontend, leading to the process occasionally stopping without informing the user
2. ~~[B2] - Reports of DOI input string ending in comma failing.~~
### Planned Features
#### Major
1. [M1] - For items that may exist in other databases without a DOI but contain enough information to confidently match (e.g. author names, title, publishing date, &c.), extending the ORCs capability to match these records.
#### Minor
1. [m1] - ~~Better handling of items which do not exist in OpenAlex (return "Not found" or similar rather than dropping)~~
2. [m2] - Improving test coverage and quality
3. [m3] - Reinstating Typecheck for the backend
4. [m4] - ~~Implement frontend Testing~~
5. [m5] - ~~Standardising .env variable names and values (local/dev/prod/production)~~
6. [m6] - Implement frontend logging
7. [m7] - ~~Change the bind mount for certbot to a docker volume.~~
8. [m8] - ~~Adding ability to change gunicorn parameters via ARG/ENV in the backend container.(see ``Functionality/Backend Container``)~~
### Contributing
Please raise github issues with bugs. Any frontend development experience would be greatly appreciated.
### Tips for Development
* This project was configured for use on a development container - this will automatically install the project and install development dependencies inside it. (A template version of this project will shortly be publicly released)
* To add dependencies to the python module use poetry add
* To enable production change:
	* ```src/env/js.env``` REACT_APP_ENV: "dev" to "production"
	* ```.env``` LOCAL_OR_PRODUCTION: "local" to "prod"
* Most useful commands have been captured in the makefile, this also can assist with figuring out what fits where
* When docker compose up is run, the logs are captured in a newly created folder /logs/, this is bind mounted to your filesystem.
### Support
If you are having difficulties using the ORC locally or at [orc-demo.gesis.org](orc-demo.gesis.org) please reach out to Jack Culbert at [jack.culbert@gesis.org](mailto:jack.culbert@gesis.org?subject=ORC%20Support:%20)
## Credits
### Developers
* Jack H. Culbert - Lead Developer - [ORCID](https://orcid.org/0009-0000-1581-4021), [LinkedIn](https://www.linkedin.com/in/jack-c-2485989a/), [Github](https://github.com/jhculb)
* Muhammad Ahsan Shahid - Frontend Developer - [ORCID](https://orcid.org/0000-0002-7274-7934), [LinkedIn](https://www.linkedin.com/in/muhammad-ahsan-shahid/), [Github](https://github.com/MAhsanShahid)
* Philipp Mayr - Team Lead - [ORCID](https://orcid.org/0000-0002-6656-1658)
### Funding
This work was funded by the Federal Ministry of Research, Technology and Space (BMFTR)
via funding numbers: 16WIK2301B / 16WIK2301E, The OpenBib project. We
acknowledge support by the Federal Ministry of Research, Technology and Space (BMFTR), Germany under grant number 01PQ17001, the Competence Network for Bibliometrics.

Jack Culbert, and Philipp Mayr received additional funding by the European Union under the Horizon Europe grant OMINO – Overcoming Multilevel INformation Overload under grant number 101086321
## How to Cite

Please cite the JOSS paper:

Markdown:
[![DOI](https://joss.theoj.org/papers/10.21105/joss.08205/status.svg)](https://doi.org/10.21105/joss.08205)

HTML:
<a style="border-width:0" href="https://doi.org/10.21105/joss.08205">
  <img src="https://joss.theoj.org/papers/10.21105/joss.08205/status.svg" alt="DOI badge" >
</a>

reStructuredText:
.. image:: https://joss.theoj.org/papers/10.21105/joss.08205/status.svg
   :target: https://doi.org/10.21105/joss.08205
### Thanks
Please remember to also cite the OpenAlex work:
```bib
@article{priem2022openalex,
  title={OpenAlex: A fully-open index of scholarly works, authors, venues, institutions, and concepts},
  author={Priem, Jason and Piwowar, Heather and Orr, Richard},
  journal={arXiv preprint arXiv:2205.01833},
  year={2022}
}
```
## License
This code is licenced under [GPL-3.0](https://www.gnu.org/licenses/gpl-3.0-standalone.html), or later.
