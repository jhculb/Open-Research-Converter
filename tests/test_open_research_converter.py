"""This file tests the frontend-facing elements of the open research converter."""

from __future__ import annotations

import logging
import queue
from logging.handlers import QueueHandler
from pathlib import Path
from uuid import uuid4

import pytest
from orc.backend.orc_backend.open_research_converter import OpenResearchConverter

LOGGING_FOLDER_LOCATION = Path(__file__).parent / "logs"
LOGGING_FOLDER_LOCATION.mkdir(exist_ok=True)


@pytest.fixture(name="log")
def create_logger():
    logging.basicConfig(
        level=logging.DEBUG,
        filename=LOGGING_FOLDER_LOCATION / "test_orc.log",
        filemode="w",
    )
    log_queue = queue.Queue()
    queue_handler = QueueHandler(log_queue)
    root_logger = logging.getLogger()
    root_logger.addHandler(queue_handler)
    return root_logger


@pytest.mark.integration
@pytest.mark.asyncio
async def test_init_healthcheck_sunny_day(log):
    orc = OpenResearchConverter(log)
    response, code = await orc.health_check()
    assert code == 418
    assert response == {"healthy": True, "error": False}


def test_generate_new_job(log):
    orc = OpenResearchConverter(log)
    identifier = orc.generate_new_job()
    assert isinstance(identifier, str)
    assert identifier in orc._jobs
    assert isinstance(orc._jobs[identifier], dict)
    assert "input_data" in orc._jobs[identifier]
    assert orc._jobs[identifier]["input_data"] is None
    assert "output_data" in orc._jobs[identifier]
    assert orc._jobs[identifier]["output_data"] is None
    assert "status" in orc._jobs[identifier]
    assert orc._jobs[identifier]["status"] == "initialised"
    assert "progress" in orc._jobs[identifier]
    assert orc._jobs[identifier]["progress"] == 0
    # Test new fields for DOI tracking
    assert "submitted_count" in orc._jobs[identifier]
    assert orc._jobs[identifier]["submitted_count"] == 0
    assert "found_count" in orc._jobs[identifier]
    assert orc._jobs[identifier]["found_count"] == 0
    assert "missing_dois" in orc._jobs[identifier]
    assert orc._jobs[identifier]["missing_dois"] == []
    assert "invalid_dois" in orc._jobs[identifier]
    assert orc._jobs[identifier]["invalid_dois"] == []


def test_validate_data(log):
    orc = OpenResearchConverter(log)
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
def test_check_ready_no_data(log):
    orc = OpenResearchConverter(log)
    userid = orc.generate_new_job()
    orc._check_ready(userid)


def test_check_ready_wrong_uuid(log):
    orc = OpenResearchConverter(log)
    assert not orc._check_ready("incorrect_uuid")


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["data", "expected_output"],
    [
        [
            "https://doi.org/10.48550/ARXIV.2406.15154",
            ["https://openalex.org/W4399991117"],
        ],
        [
            ["https://doi.org/10.48550/ARXIV.2406.15154", "https://doi.org/10.7717/peerj.4375"],
            [
                "https://openalex.org/W4399991117",
                "https://openalex.org/W2741809807",
            ],
        ],
        [
            [
                "https://doi.org/10.48550/ARXIV.2406.15154",
                "https://doi.org/10.7717/peerj.4375",
                "https://doi.org/10.5210/fm.v15i7.2874",
                "https://doi.org/10.1007/s11192-013-1221-3",
                "https://doi.org/10.1371/journal.pone.0048753",
                "https://doi.org/10.48550/arxiv.2205.01833",
                "https://doi.org/10.1002/meet.14504701201",
                "https://doi.org/10.48550/arxiv.1203.4745",
                "https://doi.org/10.1038/495437a",
                "https://doi.org/10.1101/795310",
                "https://doi.org/10.1016/j.iheduc.2008.03.002",
                "https://doi.org/10.1002/bult.2013.1720390405",
                "https://doi.org/10.3389/fncom.2012.00019",
                "https://doi.org/10.7287/peerj.preprints.3119",
                "https://doi.org/10.48550/arxiv.1205.5611",
                "https://doi.org/10.7287/peerj.preprints.3119v1",
                "https://doi.org/10.5860/crln.74.6.8960",
                "https://doi.org/10.1145/3462204.3482889",
                "https://doi.org/10.59350/89wpz-hpz32",
                "https://doi.org/10.3998/3336451.0017.301",
                "https://doi.org/10.1002/meet.14504901155",
                "https://doi.org/10.6084/m9.figshare.104629.v1",
                "https://doi.org/10.5281/zenodo.837902",
                "https://doi.org/10.48550/arxiv.1507.01328",
                "https://doi.org/10.6084/m9.figshare.790651.v1",
                "https://doi.org/10.1002/meet.2011.14504801205",
                "https://doi.org/10.15200/winn.140813.35294",
                "https://doi.org/10.48550/arxiv.2009.04281",
                "https://doi.org/10.5281/zenodo.8200678",
                "https://doi.org/10.5281/zenodo.8170024",
                "https://doi.org/10.5281/zenodo.8170023",
                "https://doi.org/10.5281/zenodo.8189450",
                "https://doi.org/10.5281/zenodo.8189449",
                "https://doi.org/10.5281/zenodo.8200679",
                "https://doi.org/10.48550/arxiv.2009.04287",
                "https://doi.org/10.6084/m9.figshare.1461749.v1",
                "https://doi.org/10.6084/m9.figshare.4214037.v2",
                "https://doi.org/10.1002/meet.2011.14504801327",
                "https://doi.org/10.6084/m9.figshare.729080.v1",
                "https://doi.org/10.17615/bzx4-n933",
                "https://doi.org/10.17615/t6x2-d431",
                "https://doi.org/10.48550/arxiv.1305.3328",
                "https://doi.org/10.48550/arxiv.1304.7300",
                "https://doi.org/10.6084/m9.figshare.729080",
                "https://doi.org/10.5281/zenodo.837901",
                "https://doi.org/10.5281/zenodo.1041791",
                "https://doi.org/10.5281/zenodo.1041788",
                "https://doi.org/10.5281/zenodo.3474007",
                "https://doi.org/10.5281/zenodo.3474006",
                "https://doi.org/10.5860/crln.81.7.341",
                "https://doi.org/10.5281/zenodo.6936227",
            ],
            [
                "https://openalex.org/W4399991117",
                "https://openalex.org/W2741809807",
                "https://openalex.org/W2122130843",
                "https://openalex.org/W2038196424",
                "https://openalex.org/W2396414759",
                "https://openalex.org/W4229010617",
                "https://openalex.org/W2041540760",
                "https://openalex.org/W1553564559",
                "https://openalex.org/W2059275568",
                "https://openalex.org/W2980172586",
                "https://openalex.org/W2104791248",
                "https://openalex.org/W2051771537",
                "https://openalex.org/W2144816075",
                "https://openalex.org/W4245410681",
                "https://openalex.org/W1519117689",
                "https://openalex.org/W4235038322",
                "https://openalex.org/W2109312864",
                "https://openalex.org/W3208256308",
                "https://openalex.org/W4391560706",
                "https://openalex.org/W2017292130",
                "https://openalex.org/W2143461694",
                "https://openalex.org/W87230806",
                "https://openalex.org/W4393631545",
                "https://openalex.org/W854896339",
                "https://openalex.org/W2244341329",
                "https://openalex.org/W2110180658",
                "https://openalex.org/W4230863633",
                "https://openalex.org/W3084303366",
                "https://openalex.org/W4393520745",
                "https://openalex.org/W4393612922",
                "https://openalex.org/W4393657389",
                "https://openalex.org/W4393689549",
                "https://openalex.org/W4393735424",
                "https://openalex.org/W4393829228",
                "https://openalex.org/W4287670050",
                "https://openalex.org/W2227647665",
                "https://openalex.org/W2550999367",
                "https://openalex.org/W2154768595",
                "https://openalex.org/W2287991258",
                "https://openalex.org/W4299872130",
                "https://openalex.org/W4299955488",
                "https://openalex.org/W4301303362",
                "https://openalex.org/W4301494992",
                "https://openalex.org/W4394076148",
                "https://openalex.org/W4393426114",
                "https://openalex.org/W4393568106",
                "https://openalex.org/W4393628136",
                "https://openalex.org/W3206844309",
                "https://openalex.org/W4393718594",
                "https://openalex.org/W3041578807",
                "https://openalex.org/W4288680697",
            ],
        ],
    ],
)
async def test_init_process_sunny_day(log, data, expected_output):
    orc = OpenResearchConverter(log)
    job_id = orc.generate_new_job()
    await orc.process(job_id, data)
    output_response, output_code = orc.return_data(job_id)
    assert output_code == 200
    output_data = output_response["output_data"]
    assert output_data == expected_output
    # Verify new counter fields are present in response
    assert "submitted_count" in output_response
    assert "found_count" in output_response
    assert "missing_dois" in output_response
    assert isinstance(output_response["submitted_count"], int)
    assert isinstance(output_response["found_count"], int)
    assert isinstance(output_response["missing_dois"], list)
    assert isinstance(output_response["invalid_dois"], list)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_missing_dois_tracking(log):
    """Test that DOIs not found in OpenAlex are tracked correctly."""
    orc = OpenResearchConverter(log)
    job_id = orc.generate_new_job()
    # Include a valid DOI and an invalid/nonexistent DOI
    data = [
        "https://doi.org/10.48550/ARXIV.2406.15154",  # Valid - exists in OpenAlex
        "https://doi.org/10.99999/this-doi-does-not-exist-12345",  # Invalid - won't be found
    ]
    await orc.process(job_id, data)
    output_response, output_code = orc.return_data(job_id)
    assert output_code == 200
    # Verify submitted count matches input
    assert output_response["submitted_count"] == 2
    # Verify found count is 1 (only the valid DOI)
    assert output_response["found_count"] == 1
    # Verify the invalid DOI is in missing_dois
    assert len(output_response["missing_dois"]) == 1
    assert "10.99999/this-doi-does-not-exist-12345" in output_response["missing_dois"][0].lower()
    # Verify only the valid DOI is in output_data
    assert len(output_response["output_data"]) == 1
    assert output_response["output_data"][0] == "https://openalex.org/W4399991117"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_all_dois_found(log):
    """Test that when all DOIs are found, missing_dois is empty."""
    orc = OpenResearchConverter(log)
    job_id = orc.generate_new_job()
    data = [
        "https://doi.org/10.48550/ARXIV.2406.15154",
        "https://doi.org/10.7717/peerj.4375",
    ]
    await orc.process(job_id, data)
    output_response, output_code = orc.return_data(job_id)
    assert output_code == 200
    assert output_response["submitted_count"] == 2
    assert output_response["found_count"] == 2
    assert output_response["missing_dois"] == []
    assert output_response["invalid_dois"] == []


def test_partition_dois(log):
    """Test that _partition_dois correctly separates valid and invalid DOIs."""
    orc = OpenResearchConverter(log)
    job_id = orc.generate_new_job()
    data = [
        "https://doi.org/10.48550/ARXIV.2406.15154",  # Valid
        "not-a-doi",  # Invalid
        "10.7717/peerj.4375",  # Valid (without prefix)
        "hello world",  # Invalid
        "",  # Invalid (empty string)
    ]
    valid, invalid = orc._partition_dois(job_id, data)
    assert len(valid) == 2
    assert len(invalid) == 3
    assert "https://doi.org/10.48550/ARXIV.2406.15154" in valid
    assert "10.7717/peerj.4375" in valid
    assert "not-a-doi" in invalid
    assert "hello world" in invalid
    assert "" in invalid


@pytest.mark.integration
@pytest.mark.asyncio
async def test_invalid_dois_continue_processing(log):
    """Test that invalid DOIs are separated out and valid DOIs are still processed."""
    orc = OpenResearchConverter(log)
    job_id = orc.generate_new_job()
    # Mix of valid DOIs and invalid strings
    data = [
        "https://doi.org/10.48550/ARXIV.2406.15154",  # Valid - exists in OpenAlex
        "not-a-doi",  # Invalid format
        "hello world",  # Invalid format
    ]
    await orc.process(job_id, data)
    output_response, output_code = orc.return_data(job_id)
    assert output_code == 200
    # Only the valid DOI should be submitted for processing
    assert output_response["submitted_count"] == 1
    assert output_response["found_count"] == 1
    assert output_response["output_data"] == ["https://openalex.org/W4399991117"]
    # Invalid DOIs should be reported
    assert len(output_response["invalid_dois"]) == 2
    assert "not-a-doi" in output_response["invalid_dois"]
    assert "hello world" in output_response["invalid_dois"]
    assert output_response["missing_dois"] == []
