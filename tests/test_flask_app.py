#   ---------------------------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
"""This is a sample python file for testing functions from the source code."""

from __future__ import annotations

import pytest
from flask import current_app
from orc.backend.orc_backend.app import app, hello_world


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_index_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"ORC API using Flask" in response.data


def test_generate_new_job(client):
    pass
    # return orc.generate_new_job()


def test_send_data(client):
    pass
    # uuid = request.form["job_id"]
    # text = request.form["input_data"]
    # email = request.form["text"]
    # return orc.recieve_data(uuid, text, email)


def test_start_processing(client):
    pass
    # uuid = request.form["job_id"]
    # return orc.process(uuid)


def test_get_status(client):
    pass
    # uuid = request.form["job_id"]
    # return orc.get_status(uuid)


def test_recieve_data(client):
    pass
    # uuid = request.form["job_id"]
    # return orc.return_data(uuid)
