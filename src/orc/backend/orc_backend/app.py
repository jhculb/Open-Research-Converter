from __future__ import annotations

from flask import Flask, request
from orc.backend.orc_backend.open_research_converter import OpenResearchConverter

app = Flask(__name__)
orc = OpenResearchConverter()


@app.route("/", methods=["GET"])
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
async def healthcheck():
    return await orc.health_check()


@app.route("/start_processing", methods=["POST"])
async def start_processing():
    job_id = orc.generate_new_job()
    text = request.form["input_data"]
    email = request.form["email"]
    return await orc.process(job_id, text, email)


@app.route("/get_status", methods=["POST"])
def get_status():
    job_id = request.form["job_id"]
    return orc.get_status(job_id)


@app.route("/get_data", methods=["GET"])
def send_data():
    job_id = request.form["job_id"]
    return orc.return_data(job_id)
