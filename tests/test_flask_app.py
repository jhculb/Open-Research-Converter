#   ---------------------------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
"""This is a sample python file for testing functions from the source code."""

from __future__ import annotations

from orc.backend.app import hello_world, generate_new_job, send_data, start_processing, get_status, recieve_data


def hello_test():
    """
    This defines the expected usage, which can then be used in various test cases.
    Pytest will not execute this code directly, since the function does not contain the suffex "test"
    """
    hello_world()


def test_hello(unit_test_mocks: None):
    """
    This is a simple test, which can use a mock to override online functionality.
    unit_test_mocks: Fixture located in conftest.py, implicitly imported via pytest.
    """
    hello_test()


def test_init_hello():
    """
    This test is marked implicitly as an integration test because the name contains "_init_"
    https://docs.pytest.org/en/6.2.x/example/markers.html#automatically-adding-markers-based-on-test-names
    """
    hello_test()


def test_generate_new_job():
    pass
    return orc.generate_new_job()


def test_send_data():
    pass
    uuid = request.form["job_id"]
    text = request.form["input_data"]
    email = request.form["text"]
    return orc.recieve_data(uuid, text, email)


def test_start_processing():
    pass
    uuid = request.form["job_id"]
    return orc.process(uuid)


def test_get_status():
    pass
    uuid = request.form["job_id"]
    return orc.get_status(uuid)


def test_recieve_data():
    pass
    uuid = request.form["job_id"]
    return orc.return_data(uuid)
