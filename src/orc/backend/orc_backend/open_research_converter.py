from __future__ import annotations

import logging
import re
import uuid

import pandas as pd

logger = logging.getLogger(__name__)


class OpenResearchConverter:
    def __init__(self) -> None:
        self._jobs = {}

    def generate_new_job(self) -> tuple[dict, int]:
        new_uuid = uuid.uuid4().__str__()
        self._jobs[new_uuid] = {}
        self._jobs[new_uuid]["input_data"] = None
        self._jobs[new_uuid]["output_data"] = None
        self._jobs[new_uuid]["email"] = None
        self._jobs[new_uuid]["status"] = None
        self._jobs[new_uuid]["progress"] = None
        return {"job_id": new_uuid}, 201

    def get_status(self, uuid: str) -> tuple[dict, int]:
        self._validate_uuid(uuid=uuid)
        if uuid in self._jobs.keys():
            return {"job_id": uuid, "status": self._jobs[uuid]["status"], "progress": self._jobs[uuid]["progress"]}, 200
        else:
            return {
                "job_id": uuid,
            }, 400

    def _recieve_data(self, uuid, data: list[str], email: str) -> tuple[dict, int]:
        if self._validate_input_data(uuid, data, email):
            try:
                self._jobs[uuid]["input_data"] = pd.DataFrame(data)
                self._jobs[uuid]["email"] = email
                self._jobs[uuid]["status"] = "Ready"
                return {"job_id": uuid, "status": self._jobs[uuid]["status"]}, 202
            except Exception as err:
                logger.error(err)
                return {"job_id": uuid}, 400
        else:
            return {"job_id": uuid}, 400

    def _validate_input_data(self, uuid: str | None = None, data: list | None = None, email: str | None = None) -> bool:
        uuid_is_valid = False
        email_is_valid = False
        data_is_valid = False
        if uuid is not None:
            uuid_is_valid = self._validate_uuid(uuid)
        if email is not None:
            email_is_valid = self._validate_email(uuid, email)
        if data is not None:
            data_is_valid = self._validate_data(uuid, data)
        return uuid_is_valid and email_is_valid and data_is_valid

    def _validate_uuid(self, uuid: str) -> bool:
        try:
            if not isinstance(uuid, str):
                raise AssertionError("uuid must be a string")
        except AssertionError as err:
            logger.error("uuid passed to _validate_uuid was not a string")
            logger.error(err)
            return False
        try:
            if uuid in self._jobs.keys():
                raise KeyError(f"uuid {uuid} not in job keys")
        except KeyError as err:
            logger.error("uuid not in Jobs")
            logger.error(err)
            return False
        return True

    def _validate_email(self, uuid: str, email: str) -> bool:
        try:
            if not isinstance(email, str):
                raise AssertionError("email passed to _validate_email must be a string")
        except AssertionError as err:
            logger.error(f"email not string for uuid {uuid}")
            logger.error(err)
            return False
        return True

    def _validate_data(self, uuid: str, data: list[str]) -> bool:
        # Assumes list of strings containing dois
        doi_regex_str = r"^10.\d{4,9}\/[-._;()/:A-Z0-9]+$"
        try:
            regex = re.compile(doi_regex_str)
            return len(list(filter(regex.match, data))) == len(data)
        except TypeError as err:
            logger.error(f"Incorrect type passed to _validate_data - validation failed for uuid {uuid}")
            logger.error(err)
            return False

    def _check_ready(self) -> bool:
        if self._jobs["input_data"] is None:
            raise TypeError
        return True

    def process(self, uuid, data, email) -> tuple[dict, int]:
        self._recieve_data(uuid, data, email)
        if self._check_ready():
            self._process(uuid)
            return {"job_id": uuid, "status": self._jobs[uuid]["status"], "progress": self._jobs[uuid]["progress"]}, 201
        else:
            return {"job_id": uuid, "status": self._jobs[uuid]["status"], "progress": self._jobs[uuid]["progress"]}, 400

    def _process(self, uuid):
        pass

    def return_data(self, uuid) -> tuple[dict, int]:
        self._validate_uuid(uuid=uuid)
        if self._jobs[uuid]["status"] == "complete":
            return {
                "job_id": uuid,
                "output_data": self._jobs[uuid]["output_data"],
            }, 200
        else:
            return {
                "job_id": uuid,
                "status": self._jobs[uuid]["status"],
            }, 204
