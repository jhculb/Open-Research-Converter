from __future__ import annotations

import logging
import queue
from logging.handlers import QueueHandler
from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from orc.backend.orc_backend.open_research_converter import OpenResearchConverter

# from https://stackoverflow.com/questions/67741946/how-to-validate-fields-raw-in-flask-marshmallow?rq=1

app = Flask(__name__)
orc = OpenResearchConverter()
cors = CORS(app)

LOGGING_FOLDER_LOCATION = Path(__file__).parents[4] / "logs" / "backend"

logging.basicConfig(
    level=logging.DEBUG,
    filename=LOGGING_FOLDER_LOCATION / "orc.log",
    filemode="w",
)
log_queue = queue.Queue()
queue_handler = QueueHandler(log_queue)
root_logger = logging.getLogger()
root_logger.addHandler(queue_handler)

log = logging.getLogger(__name__)


@app.route("/", methods=["GET"])
@cross_origin()
def hello_world():
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
@cross_origin()
async def healthcheck():
    response = jsonify(await orc.health_check())
    log.debug("healthcheck called")
    response.headers.add("Access-Control-Allow-Origin", "*")
    log.debug(f"healthcheck response: {response}")
    return response


@app.route("/start_processing", methods=["POST"])
@cross_origin()
async def start_processing():
    log.debug("start_processing called")
    json_data = request.get_json()
    job_id = orc.generate_new_job()
    text = json_data["input_data"]
    email = json_data["email"]
    log.debug(f"start_processing input: job_id: {job_id}, text:{text}, email: {email}")
    response = await orc.process(job_id, text, email)
    response.headers.add("Access-Control-Allow-Origin", "*")
    log.debug(f"start_processing response: {response}")
    return response


@app.route("/get_status", methods=["POST"])
@cross_origin()
def get_status():
    log.debug("get_status called")
    job_id = request.form["job_id"]
    log.debug(f"get_status job_id: {job_id}")
    response = jsonify(orc.get_status(job_id))
    response.headers.add("Access-Control-Allow-Origin", "*")
    log.debug(f"get_status response: {response}")
    return response


@app.route("/get_data", methods=["GET"])
@cross_origin()
def send_data():
    log.debug("get_data called")
    job_id = request.form["job_id"]
    log.debug(f"get_data job_id: {job_id}")
    response = jsonify(orc.return_data(job_id))
    response.headers.add("Access-Control-Allow-Origin", "*")
    log.debug(f"get_data response: {response}")
    return response
