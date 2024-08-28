from __future__ import annotations

from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from orc.backend.orc_backend.open_research_converter import OpenResearchConverter

# from https://stackoverflow.com/questions/67741946/how-to-validate-fields-raw-in-flask-marshmallow?rq=1

app = Flask(__name__)
orc = OpenResearchConverter()
cors = CORS(app)
LOGGING_FOLDER_LOCATION = Path("/app/logs")


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
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/start_processing", methods=["POST"])
@cross_origin()
async def start_processing():
    json_data = request.get_json()
    job_id = orc.generate_new_job()
    text = json_data["input_data"]
    email = json_data["email"]
    response = await orc.process(job_id, text, email)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/get_status", methods=["POST"])
@cross_origin()
def get_status():
    job_id = request.form["job_id"]
    response = jsonify(orc.get_status(job_id))
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/get_data", methods=["GET"])
@cross_origin()
def send_data():
    job_id = request.form["job_id"]
    response = jsonify(orc.return_data(job_id))
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
