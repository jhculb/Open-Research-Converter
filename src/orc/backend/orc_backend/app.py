from __future__ import annotations

import logging

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from orc.backend.orc_backend.open_research_converter import OpenResearchConverter

# from https://stackoverflow.com/questions/67741946/how-to-validate-fields-raw-in-flask-marshmallow?rq=1

app = Flask(__name__)
cors = CORS(app)

gunicorn_error_logger = logging.getLogger("gunicorn.error")
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.DEBUG)

log = app.logger

orc = OpenResearchConverter(log)


@app.route("/", methods=["GET"])
@cross_origin()
def hello_world():
    log.debug("app.py: API root page called")
    description = """
                <!DOCTYPE html>
                <head>
                <title>API Landing</title>
                </head>
                <body>
                    <h3>ORC API using Flask</h3>
                </body>
                """
    return description
    # <a href="http://localhost:5000/api?value=2">sample request</a>


@app.route("/healthcheck", methods=["GET"])
async def healthcheck():
    log.debug("app.py: healthcheck called")
    return await orc.health_check()


@app.route("/start_processing", methods=["POST"])
@cross_origin()
def start_processing():
    log.debug("app.py: start_processing called")
    json_data = request.get_json()
    job_id = orc.generate_new_job()
    text = json_data["input_data"]
    email = json_data["email"]
    log.debug(f"start_processing input: job_id: {job_id}, text:{text}, email: {email}")
    orc.process(job_id, text, email)
    log.debug(f"finished processing {job_id}")
    response = jsonify(orc.return_data(job_id))
    response.headers.add("Access-Control-Allow-Origin", "*")
    log.debug(f"get_data response: {response}")
    return response


# @app.route("/get_status", methods=["POST"])
# @cross_origin()
# def get_status():
#     log.debug("app.py: get_status called")
#     job_id = request.form["job_id"]
#     log.debug(f"get_status job_id: {job_id}")
#     response = jsonify(orc.get_status(job_id))
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     log.debug(f"get_status response: {response}")
#     return response


# @app.route("/get_data", methods=["GET"])
# @cross_origin()
# def send_data():
#     log.debug("app.py: get_data called")
#     job_id = request.form["job_id"]
#     log.debug(f"get_data job_id: {job_id}")
#     response = jsonify(orc.return_data(job_id))
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     log.debug(f"get_data response: {response}")
#     return response
