from __future__ import annotations

from flask import CORS, Flask, cross_origin, request
from orc.backend.orc_backend.open_research_converter import OpenResearchConverter

app = Flask(__name__)
orc = OpenResearchConverter()
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


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
    return await orc.health_check()


@app.route("/start_processing", methods=["POST"])
@cross_origin()
async def start_processing():
    json_data = request.get_json()
    job_id = orc.generate_new_job()
    text = json_data["input_data"]
    email = json_data["email"]
    return await orc.process(job_id, text, email)


@app.route("/get_status", methods=["POST"])
@cross_origin()
def get_status():
    job_id = request.form["job_id"]
    return orc.get_status(job_id)


@app.route("/get_data", methods=["GET"])
@cross_origin()
def send_data():
    job_id = request.form["job_id"]
    return orc.return_data(job_id)
