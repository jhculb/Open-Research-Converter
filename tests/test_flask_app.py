#   ---------------------------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
"""This is a sample python file for testing functions from the source code."""

from __future__ import annotations

import pytest
from orc.backend.orc_backend.app import app, hello_world
from quart import current_app


@pytest.fixture
@pytest.mark.asyncio
async def client():
    async with app.test_client() as client:
        yield client


# @pytest.mark.asyncio
# async def test_index_page(client):
#     response = await client.get("/")
#     assert response.status_code == 200
#     assert b"ORC API using quart" in response.data


@pytest.mark.asyncio
async def test_generate_new_job(client):
    pass
    # return orc.generate_new_job()


@pytest.mark.asyncio
async def test_send_data(client):
    pass
    # uuid = request.form["job_id"]
    # text = request.form["input_data"]
    # email = request.form["text"]
    # return orc.recieve_data(uuid, text, email)


@pytest.mark.asyncio
async def test_start_processing(client):
    pass
    # uuid = request.form["job_id"]
    # return orc.process(uuid)


@pytest.mark.asyncio
async def test_get_status(client):
    pass
    # uuid = request.form["job_id"]
    # return orc.get_status(uuid)


@pytest.mark.asyncio
async def test_recieve_data(client):
    pass
    # uuid = request.form["job_id"]
    # return orc.return_data(uuid)
