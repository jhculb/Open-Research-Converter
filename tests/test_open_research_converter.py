"""This file tests the frontend-facing elements of the open research converter."""

from __future__ import annotations

import asyncio
from time import sleep
from uuid import uuid4

import pytest
from orc.backend.orc_backend.open_research_converter import OpenResearchConverter

from tests.fixtures.fixture_orc_dois import fixture_priem_culbert_dois


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
    assert orc._jobs[identifier]["input_data"] is None
    assert "output_data" in orc._jobs[identifier]
    assert orc._jobs[identifier]["output_data"] is None
    assert "email" in orc._jobs[identifier]
    assert orc._jobs[identifier]["email"] is None
    assert "status" in orc._jobs[identifier]
    assert orc._jobs[identifier]["status"] == "initialised"
    assert "progress" in orc._jobs[identifier]
    assert orc._jobs[identifier]["progress"] == 0


def test_get_status_initial():
    orc = OpenResearchConverter()
    new_user_uuid_response, _ = orc.generate_new_job()
    new_user_uuid = new_user_uuid_response["job_id"]
    check_response, code = orc.get_status(new_user_uuid)
    assert code == 200
    assert "status" in check_response
    assert "progress" in check_response
    assert check_response["status"] == "initialised"
    assert check_response["progress"] == 0


def test_get_status_incorrect_uuid():
    orc = OpenResearchConverter()
    response, code = orc.get_status("incorrectuuid")
    assert response["job_id"] == "incorrectuuid"
    assert code == 400


def test_get_status_incorrect_uuid_type():
    orc = OpenResearchConverter()
    response, code = orc.get_status(4)
    assert response["job_id"] == 4
    assert code == 400


def test_validate_data():
    orc = OpenResearchConverter()
    identifier = uuid4().__str__()
    valid_doi_list = ["10.48550/ARXIV.2406.15154"]
    assert orc._validate_data(identifier, valid_doi_list)
    valid_doi_list = [
        "https://doi.org/10.48550/ARXIV.2406.15154",
        "https://doi.org/10.5281/ZENODO.10997451",
        "https://doi.org/10.5281/ZENODO.10777334",
    ]
    assert orc._validate_data(identifier, valid_doi_list)
    invalid_doi_list = ["as"]
    assert not orc._validate_data(identifier, invalid_doi_list)


@pytest.mark.xfail()
def test_check_ready_no_data():
    orc = OpenResearchConverter()
    response, _ = orc.generate_new_job()
    userid = response["job_id"]
    orc._check_ready(userid)


def test_check_ready_wrong_uuid():
    orc = OpenResearchConverter()
    assert not orc._check_ready("incorrect_uuid")


# @pytest.mark.parametrize(
#     ["email", "data", "expected_output"],
#     [
#         [
#             "jack.culbert+orc@gesis.org",
#             "https://doi.org/10.48550/ARXIV.2406.15154",
#             ["https://openalex.org/W4399991117"],
#         ],
#         [
#             "jack.culbert+orc@gesis.org",
#             "fixture_priem_culbert_dois",
#             "fixture_priem_culbert_oa",
#         ],
#     ],
# )
# def test_init_process_sunny_day(email, data, expected_output):
#     orc = OpenResearchConverter()
#     gen_response, gen_code = orc.generate_new_job()
#     assert gen_code == 201
#     job_id = gen_response["job_id"]
#     _, proc_code = asyncio.run(orc.process(job_id, data, email))
#     # TODO Work out way to stall the response, or mock one of the many requests to view progress in the middle
#     assert proc_code == 201
#     finished = False
#     while finished is False:
#         sleep(0.1)
#         status_response, status_code = orc.get_status(job_id)
#         assert status_code == 200
#         if status_response["status"] != "processing":
#             finished = True
#         for task in orc._jobs[job_id]["_tasklist"]:
#             try:
#                 print(task.exception())
#             except asyncio.CancelledError as err:
#                 print(task.print_stack(), flush=True)
#                 raise err

#     output_response, output_code = orc.return_data(job_id)
#     assert output_code == 200
#     output_data = output_response["output_data"]
#     assert output_data == expected_output


def test_return_data():
    pass
