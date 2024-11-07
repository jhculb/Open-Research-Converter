from __future__ import annotations

import logging

from orc.backend.orc_backend.open_research_converter import OpenResearchConverter
from quart import Quart, jsonify, request
from quart_cors import cors

# from https://stackoverflow.com/questions/67741946/how-to-validate-fields-raw-in-flask-marshmallow?rq=1

app = Quart(__name__)
cors = cors(app)

gunicorn_error_logger = logging.getLogger("gunicorn.error")
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.DEBUG)

log = app.logger

orc = OpenResearchConverter(log)


@app.route("/", methods=["GET"])
def hello_world():
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


@app.route("/healthcheck", methods=["GET"])
async def healthcheck():
    log.debug("app.py: healthcheck called")
    return await orc.health_check()


@app.route("/start_processing", methods=["POST"])
async def start_processing():
    log.debug("app.py: start_processing called")
    json_data = await request.get_json()
    job_id = orc.generate_new_job()
    text = json_data["input_data"]
    email = json_data["email"]
    log.debug(f"app.py: start_processing input: job_id: {job_id}, text:{text}, email: {email}")
    await orc.process(job_id, text, email)
    log.debug(f"app.py: finished processing {job_id}")
    response = jsonify(orc.return_data(job_id))
    response.headers.add("Access-Control-Allow-Origin", "*")
    log.debug(f"app.py: get_data response: {response}")
    return response


@app.route("/process_all", methods=["POST"])
async def start_processing_all():
    log.debug("app.py: start_processing called")
    json_data = await request.get_json()
    job_id = orc.generate_new_job()
    text = json_data["input_data"]
    email = json_data["email"]
    log.debug(f"app.py: start_processing input: job_id: {job_id}, text:{text}, email: {email}")
    await orc.process_all(job_id, text, email)
    log.debug(f"app.py: finished processing {job_id}")
    response = jsonify(orc.return_data(job_id))
    response.headers.add("Access-Control-Allow-Origin", "*")
    log.debug(f"app.py: get_data response: {response}")
    return response
