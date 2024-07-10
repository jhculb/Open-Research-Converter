from __future__ import annotations

from flask import Flask, request

from .open_research_converter import OpenResearchConverter

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
                    <a href="http://localhost:5000/api?value=2">sample request</a>
                </body>
                """
    return description


@app.route("/new", methods=["GET"])
def generate_new_job():
    return orc.generate_new_job()


def send_data():
    return


@app.route("/start_processing", methods=["POST"])
def start_processing():
    uuid = request.form["job_id"]
    text = request.form["input_data"]
    email = request.form["email"]
    return orc.process(uuid, text, email)


@app.route("/get_status", methods=["POST"])
def get_status():
    uuid = request.form["job_id"]
    return orc.get_status(uuid)


@app.route("/recieve_data", methods=["POST"])
def recieve_data():
    uuid = request.form["job_id"]
    return orc.return_data(uuid)
