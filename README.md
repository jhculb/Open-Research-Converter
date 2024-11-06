<!-- TOC --><a name="open-research-converter"></a>
# Open Research Converter
<!-- TOC --><a name="description"></a>
## Description
The [Open Research Converter (ORC)](https://orc-demo.gesis.org) is a tool designed to allow users to convert proprietary and licensed bibliometric datasets to a shareable format through [OpenAlex](https://openalex.org)'s API ([API documentation found here](https://docs.openalex.org/how-to-use-the-api/api-overview)).

The Open Research Converter has a demo running at [orc-demo.gesis.org](https://orc-demo.gesis.org) where you can trial the functionality. This url may be subject to change or to removal after a period of time.
<!-- TOC --><a name="statement-of-need"></a>
## Statement of Need
Bibliometrics and in particular Scientometrics suffers from a lack of reproducibility, wherein the databases used to perform bibliometrics are often proprietary and therefore bound by copyright and access agreements which forbid sharing the underlying data used to create the scientific insights shared in papers.

OpenAlex released in 2022 and is a open-source bibliometric database compiled by [Our Research](https://ourresearch.org/) which releases its data with a maximally permissive copyright (specifically under the [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/) deed), allowing free sharing of all data. This has allowed bibliometric researchers to download and interrogate the data as they see fit, and enables sharing of data.

However, dealing with OpenAlex data can be cumbersome. The methods of access are currently via the [website](https://openalex.org/), [API](https://api.openalex.org/), or a [data dump](https://docs.openalex.org/download-all-data/openalex-snapshot), each of which have challenges for researchers associated with it. Namely, to use the website limits the amount of information available to be displayed and may require downloading and then processing the data further to achieve the desired insights, to use the API requires a level of technical knowledge and is rate limited by OpenAlex, and the data dumps are very large (approximately 300GB at time of writing) and also require technical knowledge in the processing and interrogation of the data.

Easing the barrier of access to OpenAlex is a current theme of work in the bibliometrics community, for example @massimo_2024 have created a tool in the R programming language, [openalexR](https://docs.ropensci.org/openalexR/), capable of bulk collection of OpenAlex data and processing this data from OpenAlex's JSON based data format to a tabular format. Similarly [OpenAlex Networks](https://github.com/filipinascimento/openalexnet) is a Python library for generation of OpenAlex datasets and processing of citation and coauthorship networks. [OpenAlexNet](https://www.nuget.org/packages/OpenAlexNet) is a C# wrapper for OpenAlex enabling searching of OpenAlex.

Currently OpenAlex has no easy method for researchers to convert their datasets from proprietary formats to OpenAlex. While it is possible to manually convert smaller datasets using OpenAlex's website, or download the OpenAlex data dump and process this to enable matching.

We provide here in the Open Research Coverter a tool utilising the OpenAlex API enabling simple bulk conversion of bilbiometric data to a shareable format.

<!-- TOC --><a name="table-of-contents"></a>
## Table of Contents
<!-- TOC start (generated with https://github.com/derlin/bitdowntoc) -->

- [Open Research Converter](#open-research-converter)
   * [Description](#description)
   * [Statement Of Need](#statement-of-need)
   * [Table of Contents](#table-of-contents)
   * [How to Use the ORC](#how-to-use-the-orc)
      + [Online](#online)
      + [Local Installation](#local-installation)
      + [Please Note](#please-note)
   * [Development](#development)
      + [Known Bugs](#known-bugs)
      + [Planned Features](#planned-features)
         - [Major](#major)
         - [Minor](#minor)
      + [Contributing](#contributing)
      + [Tips for Development](#tips-for-development)
	  + [Support](#support)
   * [Credits](#credits)
      + [Developers](#developers)
	  + [Funding](#funding)
   * [How to Cite](#how-to-cite)
      + [Thanks](#thanks)
   * [License](#license)

<!-- TOC end -->
<!-- TOC --><a name="how-to-use-the-orc"></a>
## How to Use the ORC
<!-- TOC --><a name="online"></a>
### Online
If you wish to use the ORC without installing locally:
1. Navigate to https://orc-demo.gesis.org
2. Fill your the email address into the email box
	* This is so that OpenAlex can monitor traffic, and places your requests in the "polite pool", where responses are faster and more consistent.
3. Input your DOI data:
	* The ORC expects a comma separated list of DOIs in the text box
	* The ORC does not mind whether DOIs are prefaced with "https://doi.org/"
	1. Via csv file
		* Browse to select a csv file, this shall be read into the text box
		* The ORC expects a single column of DOIs with a header
			* Therefore if the first row contains a DOI this will be not be parsed into the text box
	2. Via copy and paste into the text box
		* You can also manually copy and paste your DOI data into the text box
	* The ORC can accept thousands of DOIs, though this may take a few minutes.
4. Click Submit
	* A waiting animation should play in the right hand output box, if this flashes and then disappears your query may have been unsuccessful. Please try one more time, and then check your input.
5. Wait for Output
	* If your query is successful, then in the output box the first 50 OpenAlex IDs corresponding to your DOIs will be returned.
	* If you have more submitted than 50 DOIs, then click "download CSV" to download a csv file with the DOI in the first column and the corresponding OpenAlex ID in the second column.
<!-- TOC --><a name="local-installation"></a>
### Local Installation
If you wish to run the ORC locally please follow these steps:
1. Install docker and docker compose
2. Transform the environment variable templates to environment variables
	* The environment variable templates are the ```.env.template``` files
	1. Via makefile command (on Linux):
		1. Run  ```make set_envs```
	2. Manually:
		1. Copy the ```.env.template``` file to ```.env``` in the top level directory
		2. Copy the environment variable template files in src/env/templates to src/env, and remove the ```.template``` suffix for each
		* These are ```backend.env.template```, ```frontend.env.template```, ```js.env.template``` and ```nginx.env.template```
		* The corresponding .env files should be named ```backend.env```, ```frontend.env```, ```js.env``` and ```nginx.env```
3. Run ```docker compose up --build -d```
	* Or via makefile command ```make run```
	* This will build the containers and run the code. This may take some time
4. Use your browser to navigate to ```localhost```, or ```127.0.0.1```
5. Follow the instructions in the Online section from instruction 2.
<!-- TOC --><a name="please-note"></a>
### Please Note
* The ORC is still in development and may contain bugs, for example:
	* If items are not found in OpenAlex, they may not be returned leading to a smaller number of items in the output
	* If an error happens on the backend it may not inform the frontend properly, leading to a failure (when the waiting ring disappears) without informing the user as to why.
<!-- TOC --><a name="functionality"></a>
## Functionality
The ORC functions in a containerised environment. To run this using the makefile
<!-- TOC --><a name="development"></a>
## Development
<!-- TOC --><a name="known-bugs"></a>
### Known Bugs
1. [B1] - Error handling is currently not performed on the frontend, leading to the process stopping without informing the user
<!-- TOC --><a name="planned-features"></a>
### Planned Features
<!-- TOC --><a name="major"></a>
#### Major
1. [Maj1] - For items that may exist in other databases without a DOI but contain enough information to confidently match (e.g. author names, title, publishing date, &c.), extending the ORCs capability to match these records.
<!-- TOC --><a name="minor"></a>
#### Minor
1. [Min1] - Better handling of items which do not exist in OpenAlex (return "Not found" or similar rather than dropping)
2. [Min2] - Improving test coverage and quality
3. [Min3] - Reinstating Typecheck for the backend and refactoring so it passes
4. [Min4] - Implement frontend Testing
5. [Min5] - Standardising .env variable names and values (local/dev/prod/production)
6. [Min6] - Implement frontend logging
7. [Min7] - Change the bind mount for certbot to a docker volume.
<!-- TOC --><a name="contributing"></a>
### Contributing
Please raise github issues with bugs. Any frontend development experience would be greatly appreciated.
<!-- TOC --><a name="tips-for-development"></a>
### Tips for Development
* This project was configured for use on a development container - this will automatically install the project and install development dependencies inside it. (A template version of this project will shortly be publicly released)
* To add dependencies to the python module use poetry add
* To enable production change:
	* ```src/env/js.env``` REACT_APP_ENV: "dev" to "production"
	* ```.env``` LOCAL_OR_PRODUCTION: "local" to "prod"
* Most useful commands have been captured in the makefile, this also can assist with figuring out what fits where
* When docker compose up is run, the logs are captured in a newly created folder /logs/, this is bind mounted to your filesystem.
<!-- TOC --><a name="support"></a>
### Support
If you are having difficulties using the ORC locally or at [orc-demo.gesis.org](orc-demo.gesis.org) please reach out to Jack Culbert at [john.culbert@gesis.org](mailto:john.culbert@gesis.org?subject=ORC%20Support:%20)
<!-- TOC --><a name="support"></a>
## Credits
<!-- TOC --><a name="developers"></a>
### Developers
* Jack H. Culbert - Lead Developer - [ORCID](https://orcid.org/0009-0000-1581-4021), [LinkedIn](https://www.linkedin.com/in/jack-c-2485989a/), [Github](https://github.com/jhculb)
* Muhammad Ahsan Shahid - Frontend Developer - [ORCID](https://orcid.org/0000-0002-7274-7934), [LinkedIn](https://www.linkedin.com/in/muhammad-ahsan-shahid/), [Github](https://github.com/MAhsanShahid)
* Philipp Mayr - Team Lead - [ORCID](https://orcid.org/0000-0002-6656-1658)
<!-- TOC --><a name="funding"></a>
### Funding
This work was funded by the Federal Ministry of Education and Research
via funding numbers: 16WIK2301B / 16WIK2301E, The OpenBib project. We
acknowledge support by Federal Ministry of Education and Research, Germany under grant number 01PQ17001, the Competence Network for Bibliometrics.

Jack Culbert, and Philipp Mayr received additional funding by the European Union under the Horizon Europe grant OMINO – Overcoming Multilevel INformation Overload under grant number 101086321
<!-- TOC --><a name="how-to-cite"></a>
## How to Cite
As of release of v1.1.0 on the 5th of November 2024: This software has been submitted to [JOSS](https://joss.theoj.org/), citation details pending.
<!-- TOC --><a name="thanks"></a>
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
<!-- TOC --><a name="license"></a>
## License
This code is licenced under [GPL-3.0](https://www.gnu.org/licenses/gpl-3.0-standalone.html), or later.
