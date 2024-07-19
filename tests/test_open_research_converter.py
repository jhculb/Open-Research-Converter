#   ---------------------------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
"""This is a sample python file for testing functions from the source code."""

from __future__ import annotations

from uuid import uuid4

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
    identifier = content["job_id"]
    assert isinstance(identifier, str)
    assert identifier in orc._jobs
    assert isinstance(orc._jobs[identifier], dict)
    assert "input_data" in orc._jobs[identifier]
    assert "output_data" in orc._jobs[identifier]
    assert "email" in orc._jobs[identifier]
    assert "status" in orc._jobs[identifier]
    assert "progress" in orc._jobs[identifier]


def test_validate_data():
    orc = OpenResearchConverter()
    identifier = uuid4().__str__()
    valid_doi_list = ["10.48550/ARXIV.2406.15154"]
    assert orc._validate_data(identifier, valid_doi_list)
    valid_doi_list = ["10.48550/ARXIV.2406.15154", "10.5281/ZENODO.10997451", "10.5281/ZENODO.10777334"]
    assert orc._validate_data(identifier, valid_doi_list)
    invalid_doi_list = ["as"]
    assert not orc._validate_data(identifier, invalid_doi_list)


def test_process():
    pass


def test_return_data():
    pass
