"""This file tests the frontend-facing elements of the open research converter."""

from __future__ import annotations

import asyncio
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
        filename=LOGGING_FOLDER_LOCATION / "test_requester.log",
        filemode="w",
    )
    log_queue = queue.Queue()
    queue_handler = QueueHandler(log_queue)
    root_logger = logging.getLogger()
    root_logger.addHandler(queue_handler)
    return root_logger


# TODO add longer doi list test case
@pytest.mark.parametrize(
    ["valid_doi_list", "valid_output"],
    [
        [
            ["10.48550/ARXIV.2406.15154", "10.5281/ZENODO.10997451", "10.5281/ZENODO.10777334"],
            [["10.48550/ARXIV.2406.15154", "10.5281/ZENODO.10997451", "10.5281/ZENODO.10777334"]],
        ],
        [
            ["10.48550/ARXIV.2406.15154"],
            [["10.48550/ARXIV.2406.15154"]],
        ],
    ],
)
def test_chunk_input_data(log, valid_doi_list, valid_output):
    orc = OpenResearchConverter(log)
    job_id = orc.generate_new_job()
    orc._jobs[job_id]["input_data"] = valid_doi_list
    response = orc._chunk_input_data(job_id)
    assert response is not None
    results = list(response)
    for i, pos in enumerate(results):
        result, chunksize = pos
        assert result == valid_output[i]
        assert chunksize == min(len(valid_doi_list), 50)


@pytest.mark.parametrize(
    "invalid_chunksize",
    [0, -1, 0.3, 51, 5555],
)
def test_chunk_input_data_invalid_chunksize(log, invalid_chunksize):
    valid_doi_list = ["10.48550/ARXIV.2406.15154", "10.5281/ZENODO.10997451", "10.5281/ZENODO.10777334"]
    orc = OpenResearchConverter(log)
    job_id = orc.generate_new_job()
    orc._jobs[job_id]["input_data"] = valid_doi_list
    result = orc._chunk_input_data(job_id, invalid_chunksize)
    assert result is not None
    result = list(result)
    assert result == []


@pytest.mark.parametrize(
    ["chunk_data", "chunk_len", "email", "expected_ids"],
    [
        [
            ["https://doi.org/10.48550/ARXIV.2406.15154"],
            1,
            "jack.culbert+orc@gesis.org",
            ["https://openalex.org/W4399991117"],
        ],
        [
            ["https://doi.org/10.48550/ARXIV.2406.15154", "https://doi.org/10.5281/zenodo.6936227"],
            2,
            "jack.culbert+orc@gesis.org",
            ["https://openalex.org/W4399991117", "https://openalex.org/W4288680697"],
        ],
        [
            ["https://doi.org/10.5281/zenodo.6936227", "https://doi.org/10.48550/ARXIV.2406.15154"],
            2,
            "jack.culbert+orc@gesis.org",
            ["https://openalex.org/W4288680697", "https://openalex.org/W4399991117"],
        ],
    ],
)
def test_request(log, chunk_data, chunk_len, email, expected_ids):
    orc = OpenResearchConverter(log)
    job_id = orc.generate_new_job()
    orc._jobs[job_id]["email"] = email
    asyncio.run(orc._request(chunk_data, job_id, chunk_len, 0))
    assert orc._jobs[job_id]["responses"][0] == expected_ids  # TODO Fix the bodge with chunk_len-1
