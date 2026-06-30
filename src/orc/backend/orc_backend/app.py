"""
Open Research Converter (ORC) API Module.

This module provides the REST API endpoints for the Open Research Converter,
a tool for converting DOIs (Digital Object Identifiers) to OpenAlex IDs.

The API enables researchers to:
- Convert lists of DOIs to OpenAlex identifiers
- Retrieve full bibliometric metadata from OpenAlex
- Check API health status

Endpoints:
    GET  /              : API information page
    GET  /healthcheck   : Check OpenAlex API connectivity
    POST /start_processing : Convert DOIs to OpenAlex IDs
    POST /process_all   : Convert DOIs and retrieve full OpenAlex metadata

Example:
    To convert DOIs to OpenAlex IDs::

        POST /start_processing
        Content-Type: application/json
        {
            "input_data": "10.1038/nature12373, 10.1126/science.1231143"
        }

For more information, see the OpenAPI specification at openapi.yaml.

References:
    - OpenAlex API: https://docs.openalex.org/how-to-use-the-api/api-overview
    - ORC Documentation: https://github.com/jhculb/OpenResearchConverter
"""

from __future__ import annotations

import logging

from orc.backend.orc_backend.open_research_converter import OpenResearchConverter
from quart import Blueprint, Quart, jsonify, request
from quart_cors import cors

app = Quart(__name__)
cors = cors(app)

api_bp = Blueprint("api", __name__, url_prefix="/api")

gunicorn_error_logger = logging.getLogger("gunicorn.error")
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.DEBUG)

log = app.logger

orc = OpenResearchConverter(log)


@app.route("/", methods=["GET"])
def hello_world():
    """
    Return the API root page.

    Provides a simple HTML page indicating the API is running.
    Includes a noindex robots directive to prevent search engine indexing.

    Returns:
        str: HTML content describing the API.

    HTTP Status Codes:
        200: Success
    """
    log.debug("app.py: API root page called")
    description = """
                <!DOCTYPE html>
                <head>
                <title>ORC-API</title>
                <meta name="robots" content="noindex" />
                </head>
                <body>
                    <h3>ORC API using quart</h3>
                </body>
                """
    return description


@api_bp.route("/healthcheck", methods=["GET"])
async def healthcheck():
    """
    Check the health status of the OpenAlex API connection.

    Verifies that the ORC can successfully communicate with the OpenAlex API.
    This endpoint is useful for monitoring and ensuring service availability.

    Returns:
        tuple: A tuple containing:
            - dict: Health status with keys 'healthy' (bool) and 'error' (bool or str)
            - int: HTTP status code

    HTTP Status Codes:
        418: Healthy (OpenAlex API is accessible)
        200: Unhealthy (OpenAlex API is not accessible or returned unexpected response)

    Note:
        The unconventional use of 418 for healthy status allows easy differentiation
        between healthy and unhealthy states in monitoring systems.

    Example Response (healthy)::

        {"healthy": true, "error": false}

    Example Response (unhealthy)::

        {"healthy": false, "error": "Connection error"}
    """
    log.debug("app.py: healthcheck called")
    return await orc.health_check()


@api_bp.route("/start_processing", methods=["POST"])
async def start_processing():
    """
    Convert a list of DOIs to OpenAlex IDs.

    Process Flow Steps 6-8: Receives the API request, creates the converter
    instance, and initiates processing.

    Accepts a JSON payload containing DOIs and an email address, queries the
    OpenAlex API, and returns the corresponding OpenAlex identifiers.

    Request Body:
        JSON object with the following fields:
            - input_data (str or list): DOIs to convert. Can be:
                - A comma-separated string: "10.1234/abc, 10.5678/def"
                - An array of strings: ["10.1234/abc", "10.5678/def"]
                DOIs can include or omit the https://doi.org/ prefix.

    Returns:
        Response: JSON response containing:
            - job_id (str): Unique identifier for this processing job
            - output_data (list): List of OpenAlex IDs (URLs)
            - output_full (str): CSV formatted string with DOI to OpenAlex ID mappings
            - submitted_count (int): Number of valid DOIs submitted for processing
            - found_count (int): Number of DOIs found in OpenAlex
            - missing_dois (list): DOIs not found in OpenAlex
            - invalid_dois (list): Input strings that failed DOI format validation

    HTTP Status Codes:
        200: Processing complete, results returned
        204: Processing not yet complete (status returned instead)

    Note:
        Incorrectly formatted DOIs are separated out and returned in invalid_dois.
        The remaining valid DOIs are still processed normally.

    Example Request::

        POST /start_processing
        Content-Type: application/json
        {
            "input_data": "10.1038/nature12373, not-a-doi, 10.1126/science.1231143"
        }

    Example Response::

        [{
            "job_id": "550e8400-e29b-41d4-a716-446655440000",
            "output_data": ["https://openalex.org/W2102245935"],
            "output_full": "doi, oa_id\\nhttps://doi.org/10.1038/nature12373,...",
            "submitted_count": 2,
            "found_count": 1,
            "missing_dois": ["https://doi.org/10.1126/science.1231143"],
            "invalid_dois": ["not-a-doi"]
        }]
    """
    log.debug("app.py: start_processing called")
    json_data = await request.get_json()
    job_id = orc.generate_new_job()
    text = json_data["input_data"]
    log.debug(f"app.py: start_processing input: job_id: {job_id}, text:{text}")
    await orc.process(job_id, text)
    log.debug(f"app.py: finished processing {job_id}")
    response = jsonify(orc.return_data(job_id))
    response.headers.add("Access-Control-Allow-Origin", "*")
    log.debug(f"app.py: get_data response: {response}")
    return response


@api_bp.route("/process_all", methods=["POST"])
async def start_processing_all():
    """
    Convert DOIs to OpenAlex IDs and retrieve full bibliometric metadata.

    Similar to /start_processing, but returns comprehensive OpenAlex metadata
    for each work, including citations, authors, topics, and more.

    Request Body:
        JSON object with the following fields:
            - input_data (str or list): DOIs to convert (same format as /start_processing).

    Returns:
        Response: JSON response containing:
            - job_id (str): Unique identifier for this processing job
            - output_data (list): List of OpenAlex IDs (URLs)
            - output_full (str): TSV formatted string with full metadata (47+ fields)
            - submitted_count (int): Number of valid DOIs submitted for processing
            - found_count (int): Number of DOIs found in OpenAlex
            - missing_dois (list): DOIs not found in OpenAlex
            - invalid_dois (list): Input strings that failed DOI format validation

    HTTP Status Codes:
        200: Processing complete, results returned
        204: Processing not yet complete

    Note:
        Incorrectly formatted DOIs are separated out and returned in invalid_dois.
        The remaining valid DOIs are still processed normally.

        The output_full field contains tab-separated values (TSV) with fields including:
        doi, oa_id, ids, title, language, display_name, is_retracted, authorships,
        publication_date, publication_year, open_access, primary_topic, topics,
        concepts, keywords, cited_by_count, referenced_works, and many more.

    Example Request::

        POST /process_all
        Content-Type: application/json
        {
            "input_data": ["10.1038/nature12373"]
        }
    """
    log.debug("app.py: start_processing called")
    json_data = await request.get_json()
    job_id = orc.generate_new_job()
    text = json_data["input_data"]
    log.debug(f"app.py: start_processing input: job_id: {job_id}, text:{text}")
    await orc.process_all(job_id, text)
    log.debug(f"app.py: finished processing {job_id}")
    response = jsonify(orc.return_data(job_id))
    response.headers.add("Access-Control-Allow-Origin", "*")
    log.debug(f"app.py: get_data response: {response}")
    return response


app.register_blueprint(api_bp)
