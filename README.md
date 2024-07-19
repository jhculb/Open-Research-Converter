# Open Research Converter
## Description
## Table of Contents
## Installation and Running
## How to Use
## Credits
## License
## Internal
### Flow
Hi Ahsan,

I have architected the backend to have a rest interface. I'll work out the url to send it to, but for the moment use a dummy url followed by the address.

E.g. "my.dummy.url/new_user"

For details, see the src/orc/backend/app.py file, and for types expected see src/orc/backend/open_research_converter.py.


The user experience flow between the interface and the application should be as follows:


1. Initialisation
	- Description: A new user has arrived at the website and starts a session
	- Call Location:
		- my.dummy.url/new
	- Request Type:
		- GET
	- Returns:
		- If successful:
			- {"content":{"job_id":uuid}, "status_code":201}
			- This is the identifier that will be used for this session's data
2. User Inputs Data
	- Description: The user inputs their email (required), and data in the frontend
3. Processing Begins
	- Description: User has input data and email, and clicks button for processing.
	- Call Location:
		- my.dummy.url/start_processing
	- Request Type:
		- POST
			- CONTENT:
				- "job_id": The uuid of the session returned from my.dummy.url/new
				- "input_data": (IN DEVELOPMENT) A string containing comma separated DOIs
				- "email": A string containing an email
	- Returns:
		- If successful:
			- {"content":{"job_id": uuid, "status": status, "progress":progress}, "status_code":201}
		- If uuid invalid:
			- TODO (HTTP-400)
		- If email invalid
			- TODO (HTTP-400)
		- If data invalid
			- TODO (HTTP-400)
4. Checking on progress
	- Description: The user is waiting for the ORC to process the data, and the website is updating every so often (1 second?) to let them know how it is going
	- Call Location:
		- my.dummy.url/get_status
	- Request Type:
		- POST
			- CONTENT:
				- "job_id": The uuid of the session returned from my.dummy.url/new
	- Returns:
		- If uuid valid:
			- {"content":{"job_id": uuid, "status": status, "progress": progress}, status_code":200}
			- status may be ["waiting", "processing", "finished", "failed"]
			- progress is a dictionary of {"valid_dois":integer, "completed_dois":integer}
		- If uuid invalid:
			- TODO
5. Returning completed data to user
	- Description: The data has processed, which is signified by a call to /get_status having "status" variable == "finished", so now is time to return that data to the frontend.
	- Call Location:
		- my.dummy.url/recieve_data
	- Request Type:
		- POST
			- CONTENT:
				- "job_id": The uuid of the session returned from my.dummy.url/new
	- Returns:
		- If uuid valid and status == finished:
			- {"content":{
                "job_id": uuid,
                "output_data": output_data,
            }, status_code":200}
			- status may be ["waiting", "processing", "finished", "failed"]
			- output_data is a list of 2-tuples of strings
				- e.g. [\(input_doi_1, output_oa_work_id_1\),\(input_doi_2, output_oa_work_id_2\)]
		- If uuid valid and status == processing:
			- {"content":{
                "job_id": uuid,
                "status": status,
            }, status_code":204}
		- If uuid invalid:
			- TODO
