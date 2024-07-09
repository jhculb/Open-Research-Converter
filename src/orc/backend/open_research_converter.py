import pandas as pd
import uuid
# from validate_email import validate_email


class OpenResearchConverter:
    def __init__(self) -> None:
        self.jobs = {}

    def generate_new_job(self) -> tuple[dict, int]:
        new_uuid = uuid.uuid4().__str__()
        self.jobs[new_uuid] = {}
        self.jobs[new_uuid]["input_data"] = None
        self.jobs[new_uuid]["output_data"] = None
        self.jobs[new_uuid]["email"] = None
        self.jobs[new_uuid]["status"] = None
        self.jobs[new_uuid]["progress"] = None
        return {"job_id": new_uuid}, 201

    def get_status(self, uuid: str) -> tuple[dict, int]:
        self._parse_uuid(uuid=uuid)
        if uuid in self.jobs.keys():
            return {"job_id": uuid, "status": self.jobs[uuid]["status"], "progress": self.jobs[uuid]["progress"]}, 200
        else:
            return {
                "job_id": uuid,
            }, 400

    def _recieve_data(self, uuid, data: str, email: str) -> tuple[dict, int]:
        self._parse_uuid(uuid=uuid)

        if isinstance(email, str):
            if isinstance(data, str):
                try:
                    self.jobs["uuid"]["input_data"] = pd.DataFrame(data.split(","))
                    self.email = email
                    return {"job_id": uuid}, 202
                except Exception as err:
                    print(err)  # this may be a log file
                    return {"job_id": uuid}, 400
        else:
            return {"job_id": uuid}, 400

    def _parse_input_data(self, uuid=None, data=None, email=None):
        uuid_is_valid = None
        email_is_valid = None
        data_is_valid = None
        if uuid is not None:
            uuid_is_valid = self._parse_uuid(uuid)
        if email is not None:
            email_is_valid = self._parse_email(email)
        if data is not None:
            data_is_valid = self._parse_data(data)
        return False

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

    def _parse_data(self, data):
        pass

    def _check_ready(self) -> bool:
        if self.jobs["input_data"] is None:
            raise TypeError
        return True

    def process(self, uuid, data, email) -> tuple[dict, int]:
        self._recieve_data(uuid, data, email)
        if self._check_ready():
            self._process(uuid)
            return {"job_id": uuid, "status": self.jobs[uuid]["status"], "progress": self.jobs[uuid]["progress"]}, 201
        else:
            return {"job_id": uuid, "status": self.jobs[uuid]["status"], "progress": self.jobs[uuid]["progress"]}, 400

    def _process(self, uuid):
        pass

    def return_data(self, uuid) -> tuple[dict, int]:
        self._parse_uuid(uuid=uuid)
        if self.jobs[uuid]["status"] == "complete":
            return {
                "job_id": uuid,
                "output_data": self.jobs[uuid]["output_data"],
            }, 200
        else:
            return {
                "job_id": uuid,
                "status": self.jobs[uuid]["status"],
            }, 204
