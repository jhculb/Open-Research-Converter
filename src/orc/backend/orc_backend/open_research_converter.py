from __future__ import annotations

import asyncio
import re
import uuid

from orc.backend.orc_backend.requester import openalex_requester


class OpenResearchConverter(openalex_requester):
    def __init__(self, log) -> None:
        super().__init__()
        self._logger = log

    def generate_new_job(self) -> str:
        new_job_id = uuid.uuid4().__str__()
        self._logger.debug(f"orc.py: new job created with id: {new_job_id}")
        self._jobs[new_job_id] = {}
        self._jobs[new_job_id]["input_data"] = None
        self._jobs[new_job_id]["responses"] = {}
        self._jobs[new_job_id]["csv_responses"] = {}
        self._jobs[new_job_id]["aio_responses"] = None
        self._jobs[new_job_id]["output_data"] = None
        self._jobs[new_job_id]["output_csv_data"] = None
        self._jobs[new_job_id]["lock"] = asyncio.Lock()
        self._jobs[new_job_id]["email"] = None
        self._jobs[new_job_id]["status"] = "initialised"
        self._jobs[new_job_id]["progress"] = 0
        self._jobs[new_job_id]["task_group"] = None
        return new_job_id

    def _recieve_data(self, job_id: str, data: list[str], email: str):
        if isinstance(data, str):
            data = list(map(str.strip, data.split(",")))
        if isinstance(data, list):
            data = list(map(str.strip, data))
        if self._validate_input_data(job_id, data, email):
            try:
                self._jobs[job_id]["input_data"] = data
                self._jobs[job_id]["email"] = email
                self._jobs[job_id]["status"] = "ready"
            except Exception as err:
                self._logger.error(err)
        else:
            self._logger.error("job_id: {job_id}: _validate_input_data failed")

    def _validate_input_data(self, job_id: str, data: list[str], email: str) -> bool:
        job_id_is_valid = False
        email_is_valid = False
        data_is_valid = False
        if job_id is not None:
            job_id_is_valid = self._validate_uuid(job_id)
            self._logger.debug(f"job_id: {job_id}: job:{job_id_is_valid}")
        if email is not None:
            email_is_valid = self._validate_email(job_id, email)
            self._logger.debug(f"job_id: {job_id}: email:{email_is_valid}")
        if data is not None:
            data_is_valid = self._validate_data(job_id, data)
        else:
            data_is_valid = False
        self._logger.debug(f"job_id: {job_id}: data:{data_is_valid}")
        return job_id_is_valid and email_is_valid and data_is_valid

    def _validate_uuid(self, job_id: str) -> bool:
        try:
            if not isinstance(job_id, str):
                raise AssertionError("uuid must be a string")
        except AssertionError as err:
            self._logger.error("job_id: {job_id}: uuid passed to _validate_uuid was not a string")
            self._logger.error(err)
            return False
        try:
            if job_id not in self._jobs.keys():
                raise KeyError(f"job_id: {job_id}: uuid {job_id} not in job keys")
        except KeyError as err:
            self._logger.error("job_id: {job_id}: uuid not in Jobs")
            self._logger.error(err)
            return False
        return True

    def _validate_email(self, job_id: str, email: str) -> bool:
        try:
            if not isinstance(email, str):
                raise AssertionError("email passed to _validate_email must be a string")
        except AssertionError as err:
            self._logger.error(f"job_id: {job_id}: email not string for uuid")
            self._logger.error(err)
            return False
        return True

    def _doi_list_formatter(self, data: list[str]) -> list[str]:
        https_regex_str = r"^https:\/\/doi\.org\/"
        with_regex = re.compile(https_regex_str)
        for pos, potential_doi in enumerate(data):
            if not bool(with_regex.match(potential_doi)):
                data[pos] = "https://doi.org/" + potential_doi
        return data

    def _validate_data(self, job_id: str, data: list[str]) -> bool:
        # Assumes list of strings containing dois
        self._logger.debug(f"job_id: {job_id}: validating data")
        doi_regex_str = r"10.\d{4,9}\/[-._;()/:A-Za-z0-9]+"
        doi_regex = re.compile(doi_regex_str)
        https_regex_str = r"^https:\/\/doi\.org\/"
        with_regex = re.compile(https_regex_str)
        try:
            ret_val = len(list(filter(doi_regex.search, data))) == len(data)
            if not ret_val:
                for pos, potential_doi in enumerate(data):
                    if not bool(with_regex.match(potential_doi)):
                        data[pos] = "https://doi.org/" + potential_doi
                ret_val = len(list(filter(doi_regex.search, data))) == len(data)
            self._logger.debug(f"job_id: {job_id}: return value for validating data {ret_val}")
            return ret_val
        except TypeError as err:
            self._logger.error(
                f"job_id: {job_id}: Incorrect type passed to _validate_data - validation failed for uuid"
            )
            self._logger.error(err)
            return False

    def _check_ready(self, job_id: str) -> bool:
        if self._validate_uuid(job_id):
            if self._jobs[job_id]["input_data"] is None:
                raise ValueError("No input data given")
            return True
        return False

    def process_old(self, job_id, data, email) -> None:
        self._logger.info(f"job_id: {job_id}: orc: processing")
        self._recieve_data(job_id, data, email)
        self._logger.info(f"job_id: {job_id}: orc: data received")
        if self._check_ready(job_id):
            self._logger.info(f"job_id: {job_id}: orc: data was suitable, creating task")
            asyncio.run(self._process(job_id))

    async def process(self, job_id, data, email) -> None:
        self._logger.info(f"job_id: {job_id}: orc: processing")
        self._recieve_data(job_id, data, email)
        self._logger.info(f"job_id: {job_id}: orc: data received")
        if self._check_ready(job_id):
            self._logger.info(f"job_id: {job_id}: orc: data was suitable, creating task")
            await self._process_aio(job_id)

    def return_data_old(self, job_id) -> tuple[dict, int]:
        self._validate_uuid(job_id=job_id)
        if self._jobs[job_id]["status"] == "complete":
            del self._jobs[job_id]["_tasklist"]
            return {
                "job_id": job_id,
                "output_data": self._jobs[job_id]["output_data"],
                "output_full": self._jobs[job_id]["output_csv_data"],
            }, 200
        else:
            return {
                "job_id": job_id,
                "status": self._jobs[job_id]["status"],
            }, 204

    def return_data(self, job_id) -> tuple[dict, int]:
        self._validate_uuid(job_id=job_id)
        if self._jobs[job_id]["status"] == "complete":
            return {
                "job_id": job_id,
                "output_data": [doi_oa_pair[1] for doi_oa_pair in self._jobs[job_id]["aio_responses"]],
                "output_full": self._jobs[job_id]["output_csv_data"],
            }, 200
        else:
            return {
                "job_id": job_id,
                "status": self._jobs[job_id]["status"],
            }, 204
