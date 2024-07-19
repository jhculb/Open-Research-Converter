#   ---------------------------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
"""This is a sample python file for testing functions from the source code."""

from __future__ import annotations

import pytest
from orc.backend.orc_backend.open_research_converter import OpenResearchConverter


@pytest.fixture
def arrange_blank_orc():
    yield OpenResearchConverter()


def hello_world():
    return "hello world"


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
    orc = OpenResearchConverter()
    response = orc.generate_new_job()
    assert isinstance(response, tuple)
    content, code = response
    assert isinstance(code, int)
    assert code == 201
    assert isinstance(content, dict)
    assert "job_id" in content
    id = content["job_id"]
    assert isinstance(id, str)
    assert id in orc._jobs
    assert isinstance(orc._jobs[id], dict)
    assert "input_data" in orc._jobs[id]
    assert "output_data" in orc._jobs[id]
    assert "email" in orc._jobs[id]
    assert "status" in orc._jobs[id]
    assert "progress" in orc._jobs[id]


def test_process():
    pass


def test_return_data():
    pass
