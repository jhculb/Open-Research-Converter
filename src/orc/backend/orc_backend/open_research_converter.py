from __future__ import annotations

import re
import uuid

import pandas as pd

# from validate_email import validate_email


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
        self._parse_uuid(uuid=uuid)
        if uuid in self._jobs.keys():
            return {"job_id": uuid, "status": self._jobs[uuid]["status"], "progress": self._jobs[uuid]["progress"]}, 200
        else:
            return {
                "job_id": uuid,
            }, 400

    def _recieve_data(self, uuid, data: str, email: str) -> tuple[dict, int]:
        self._parse_uuid(uuid=uuid)

        if isinstance(email, str):
            if isinstance(data, str):
                try:
                    self._jobs["uuid"]["input_data"] = pd.DataFrame(data.split(","))
                    self.email = email
                    return {"job_id": uuid}, 202
                except Exception as err:
                    print(err)  # this may be a log file
                    return {"job_id": uuid}, 400
        else:
            return {"job_id": uuid}, 400

    def _parse_input_data(self, uuid=None, data=None, email=None):
        uuid_is_valid = False
        uuid_is_present = False if uuid is None else True
        email_is_valid = False
        email_is_present = False if email is None else True
        data_is_valid = False
        data_is_present = False if data is None else True
        if uuid_is_present:
            uuid_is_valid = self._parse_uuid(uuid)
        if email_is_present:
            email_is_valid = self._parse_email(email)
        if data_is_present:
            data_is_valid = self._parse_data(data)
        return uuid_is_valid and email_is_valid and data_is_valid

    def _parse_input_string(self, string: str) -> bool:
        correct = False
        return correct

    def _parse_uuid(self, uuid):
        pass

    def _parse_email(self, email):
        # is_valid = validate_email(
        #     email_address=email,
        #     check_regex=True,
        #     check_mx=True,
        #     from_address="my@from.addr.ess",
        #     helo_host="my.host.name",
        #     smtp_timeout=10,
        #     dns_timeout=10,
        #     use_blacklist=True,
        # )
        pass

    def _parse_data(self, data: list) -> bool:
        if not isinstance(data, list):
            raise TypeError("Data passed was not a list")
        else:
            list(map(lambda x: isinstance(x, str), data))
        # Assumes list of strings containing dois
        doi_regex_str = r"^10.\d{4,9}\/[-._;()/:A-Z0-9]+$"
        regex = re.compile(doi_regex_str)
        return len(list(filter(regex.match, data))) == len(data)

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
        self._parse_uuid(uuid=uuid)
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
