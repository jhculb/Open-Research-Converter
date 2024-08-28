from __future__ import annotations

import asyncio
import re
import uuid

from orc.backend.orc_backend.requester import openalex_requester


class OpenResearchConverter(openalex_requester):
    def __init__(self) -> None:
        super().__init__()

    def generate_new_job(self) -> str:
        new_job_id = uuid.uuid4().__str__()
        self._jobs[new_job_id] = {}
        self._jobs[new_job_id]["input_data"] = None
        self._jobs[new_job_id]["responses"] = {}
        self._jobs[new_job_id]["output_data"] = None
        self._jobs[new_job_id]["lock"] = asyncio.Lock()
        self._jobs[new_job_id]["email"] = None
        self._jobs[new_job_id]["status"] = "initialised"
        self._jobs[new_job_id]["progress"] = 0
        self._jobs[new_job_id]["task_group"] = None
        return new_job_id

    def get_status(self, job_id: str) -> tuple[dict[str, str | int], int]:
        if self._validate_uuid(job_id=job_id):
            return {
                "job_id": job_id,
                "status": self._jobs[job_id]["status"],
                "progress": self._jobs[job_id]["progress"],
            }, 200
        else:
            return {
                "job_id": job_id,
            }, 400

    def _recieve_data(self, job_id: str, data: list[str], email: str):
        if isinstance(data, str):
            data = data.split(",")
        if self._validate_input_data(job_id, data, email):
            try:
                self._jobs[job_id]["input_data"] = data
                self._jobs[job_id]["email"] = email
                self._jobs[job_id]["status"] = "ready"
            except Exception as err:
                print(err)
                self._logger.error(err)
        else:
            print("DEBUG: _validate_input_data failed")

    def _validate_input_data(self, job_id: str, data: list[str], email: str) -> bool:
        job_id_is_valid = False
        email_is_valid = False
        data_is_valid = False
        if job_id is not None:
            job_id_is_valid = self._validate_uuid(job_id)
            print(f"job:{job_id_is_valid}")
        if email is not None:
            email_is_valid = self._validate_email(job_id, email)
            print(f"email:{email_is_valid}")
        if data is not None:
            data_is_valid = self._validate_data(job_id, data)
        else:
            data_is_valid = False
        print(f"data:{data_is_valid}")
        return job_id_is_valid and email_is_valid and data_is_valid

    def _validate_uuid(self, job_id: str) -> bool:
        try:
            if not isinstance(job_id, str):
                raise AssertionError("uuid must be a string")
        except AssertionError as err:
            self._logger.error("uuid passed to _validate_uuid was not a string")
            self._logger.error(err)
            return False
        try:
            if job_id not in self._jobs.keys():
                raise KeyError(f"uuid {job_id} not in job keys")
        except KeyError as err:
            self._logger.error("uuid not in Jobs")
            self._logger.error(err)
            return False
        return True

    def _validate_email(self, job_id: str, email: str) -> bool:
        try:
            if not isinstance(email, str):
                raise AssertionError("email passed to _validate_email must be a string")
        except AssertionError as err:
            self._logger.error(f"email not string for uuid {job_id}")
            self._logger.error(err)
            return False
        return True

    def _validate_data(self, job_id: str, data: list[str]) -> bool:
        # Assumes list of strings containing dois
        print(f"validating data for job {job_id}")
        print(f"type(data): {type(data)}")
        doi_regex_str = r"10.\d{4,9}\/[-._;()/:A-Za-z0-9]+"
        doi_regex = re.compile(doi_regex_str)
        https_regex_str = r"^https:\/\/doi\.org\/"
        with_regex = re.compile(https_regex_str)
        try:
            print(data)
            ret_val = len(list(filter(doi_regex.search, data))) == len(data)
            if not ret_val:
                for pos, potential_doi in enumerate(data):
                    if not bool(with_regex.match(potential_doi)):
                        data[pos] = "https://doi.org/" + potential_doi
                print("DATA ADJUSTED")
                print(data)
                ret_val = len(list(filter(doi_regex.search, data))) == len(data)
                print(list(filter(doi_regex.search, data)))
                print(f"RET VAL NOW {ret_val}")
            print(f"return value for validating data {ret_val}")
            return ret_val
        except TypeError as err:
            self._logger.error(f"Incorrect type passed to _validate_data - validation failed for uuid {job_id}")
            self._logger.error(err)
            print(err)
            return False

    def _check_ready(self, job_id: str) -> bool:
        if self._validate_uuid(job_id):
            if self._jobs[job_id]["input_data"] is None:
                raise ValueError("No input data given")
            return True
        return False

    async def process(self, job_id, data, email) -> tuple[dict, int]:
        self._recieve_data(job_id, data, email)
        if self._check_ready(job_id):
            print("READY TO GO")
            try:
                await self._process(job_id)
            except asyncio.CancelledError as err:
                self._jobs[job_id]["progress"] = "failed"
                self._logger.error(err)
                return {
                    "job_id": job_id,
                    "status": self._jobs[job_id]["progress"],
                }, 500
            except asyncio.TimeoutError as err:
                self._jobs[job_id]["progress"] = "failed"
                self._logger.error(err)
                return {
                    "job_id": job_id,
                    "status": self._jobs[job_id]["progress"],
                }, 500
            return {
                "job_id": job_id,
                "status": self._jobs[job_id]["status"],
                "progress": self._jobs[job_id]["progress"],
            }, 201
        else:
            print("NOT READY TO GO")
            return {
                "job_id": job_id,
                "status": self._jobs[job_id]["status"],
                "progress": self._jobs[job_id]["progress"],
            }, 400

    def return_data(self, job_id) -> tuple[dict, int]:
        self._validate_uuid(job_id=job_id)
        if self._jobs[job_id]["status"] == "complete":
            del self._jobs[job_id]["_tasklist"]
            return {
                "job_id": job_id,
                "output_data": self._jobs[job_id]["output_data"],
            }, 200
        else:
            return {
                "job_id": job_id,
                "status": self._jobs[job_id]["status"],
            }, 204
