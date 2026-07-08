"""
Open Research Converter Core Module.

This module contains the OpenResearchConverter class, which orchestrates the
conversion of DOIs to OpenAlex identifiers. It handles job management, input
validation, and coordinates with the OpenAlex API requester.

The OpenResearchConverter is designed to support bibliometric research by enabling
bulk conversion of DOIs from proprietary databases to the open OpenAlex format,
facilitating reproducibility in scientometric studies.

Classes:
    OpenResearchConverter: Main class for managing DOI to OpenAlex ID conversion jobs.

Example:
    Basic usage::

        from orc.backend.orc_backend.open_research_converter import OpenResearchConverter

        orc = OpenResearchConverter(logger)
        job_id = orc.generate_new_job()
        await orc.process(job_id, ["10.1038/nature12373"])
        result, status_code = orc.return_data(job_id)
"""

from __future__ import annotations

import asyncio
import re
import uuid

from orc.backend.orc_backend.requester import OpenAlexRequester


class OpenResearchConverter(OpenAlexRequester):
    """
    Orchestrator for converting DOIs to OpenAlex identifiers.

    This class manages the lifecycle of conversion jobs, including:
    - Job creation and tracking
    - Input validation (DOIs)
    - Coordination with the OpenAlex API
    - Result formatting and retrieval

    Inherits from OpenAlexRequester to leverage async API communication capabilities.

    Attributes:
        _logger: Logger instance for debugging and error reporting.
        _jobs (dict): Dictionary storing job data, keyed by job_id (UUID string).

    Example:
        Processing a list of DOIs::

            orc = OpenResearchConverter(app.logger)
            job_id = orc.generate_new_job()
            await orc.process(
                job_id,
                "10.1038/nature12373, 10.1126/science.1231143",
            )
            result, status = orc.return_data(job_id)
            print(f"Found {result['found_count']} of {result['submitted_count']} DOIs")
    """

    def __init__(self, log) -> None:
        """
        Initialize the OpenResearchConverter.

        Args:
            log: Logger instance for logging debug information and errors.
                Typically passed from the Flask/Quart application logger.
        """
        super().__init__()
        self._logger = log

    def generate_new_job(self) -> str:
        """
        Create a new processing job with a unique identifier.

        Process Flow Step 9: Creates unique job ID (UUID).

        Initializes all required data structures for tracking the job through
        its lifecycle from creation to completion.

        Returns:
            str: A UUID string uniquely identifying this job.

        Note:
            The job is created with status "initialised" and must go through
            the process() or process_all() method to be completed.

        Job Data Structure:
            - input_data: List of DOIs to process (None until data received)
            - status: One of "initialised", "ready", "complete"
            - submitted_count: Total DOIs submitted
            - found_count: DOIs successfully matched in OpenAlex
            - missing_dois: List of DOIs not found in OpenAlex
            - invalid_dois: List of input strings that failed DOI format validation
        """
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
        self._jobs[new_job_id]["status"] = "initialised"
        self._jobs[new_job_id]["progress"] = 0
        self._jobs[new_job_id]["task_group"] = None
        # Fields for tracking DOI matching results
        self._jobs[new_job_id]["submitted_count"] = 0
        self._jobs[new_job_id]["found_count"] = 0
        self._jobs[new_job_id]["missing_dois"] = []
        self._jobs[new_job_id]["invalid_dois"] = []
        return new_job_id

    def _recieve_data(self, job_id: str, data: list[str]):
        """
        Receive and store input data for a job.

        Process Flow Step 10: Stores raw input in job dictionary.

        Normalizes input data format (handles both comma-separated strings and lists),
        validates the data, and stores it in the job dictionary if valid.

        Args:
            job_id: The UUID string identifying the job.
            data: DOIs to process. Can be:
                - A comma-separated string: "10.1234/abc, 10.5678/def"
                - A list of strings: ["10.1234/abc", "10.5678/def"]

        Side Effects:
            - Updates job status to "ready" if validation passes
            - Stores normalized DOI list in job's input_data field
            - Logs errors if validation fails
        """
        if isinstance(data, str):
            data = list(map(str.strip, data.strip(",").split(",")))
        if isinstance(data, list):
            data = list(map(str.strip, data))
        if self._validate_input_data(job_id, data):
            try:
                self._jobs[job_id]["input_data"] = data
                self._jobs[job_id]["status"] = "ready"
            except Exception as err:
                self._logger.error(err)
        else:
            self._logger.error("job_id: {job_id}: _validate_input_data failed")

    def _validate_input_data(self, job_id: str, data: list[str]) -> bool:
        """
        Validate all input data for a processing request.

        Process Flow Step 11: Validates job ID exists and DOIs are present and
        correctly formatted. Incorrectly formatted DOIs are separated out and
        stored as invalid_dois; valid DOIs proceed to processing.

        Args:
            job_id: The UUID string identifying the job (must exist in _jobs).
            data: List of DOI strings to validate.

        Returns:
            bool: True if job_id is valid and at least one valid DOI exists,
                False otherwise.

        Note:
            For DOI data, the method partitions into valid and invalid DOIs
            rather than rejecting the entire request.
            Invalid DOIs are stored in the job's invalid_dois field.
        """
        job_id_is_valid = False
        data_has_valid = False
        if job_id is not None:
            job_id_is_valid = self._validate_uuid(job_id)
            self._logger.debug(f"job_id: {job_id}: job:{job_id_is_valid}")
        if data is not None:
            valid_dois, invalid_dois = self._partition_dois(job_id, data)
            self._jobs[job_id]["invalid_dois"] = invalid_dois
            if len(invalid_dois) > 0:
                self._logger.info(f"job_id: {job_id}: {len(invalid_dois)} invalid DOIs separated out")
            data_has_valid = len(valid_dois) > 0
            # Replace data in-place so _recieve_data stores only valid DOIs
            data.clear()
            data.extend(valid_dois)
        self._logger.debug(f"job_id: {job_id}: data_has_valid:{data_has_valid}")
        return job_id_is_valid and data_has_valid

    def _validate_uuid(self, job_id: str) -> bool:
        """
        Validate that a job_id exists and is properly formatted.

        Process Flow Step 11 (sub-step): Verifies the job ID is a valid string
        and exists in the jobs dictionary.

        Args:
            job_id: The UUID string to validate.

        Returns:
            bool: True if job_id is a string and exists in _jobs, False otherwise.
        """
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

    def _doi_list_formatter(self, data: list[str]) -> list[str]:
        """
        Normalize DOIs to include the https://doi.org/ prefix.

        Process Flow Step 12: Normalizes DOIs to standard format (https://doi.org/...).

        Args:
            data: List of DOI strings, with or without prefix.

        Returns:
            list[str]: List of DOIs with https://doi.org/ prefix.

        Example:
            >>> _doi_list_formatter(["10.1234/abc", "https://doi.org/10.5678/def"])
            ["https://doi.org/10.1234/abc", "https://doi.org/10.5678/def"]
        """
        https_regex_str = r"^https:\/\/doi\.org\/"
        with_regex = re.compile(https_regex_str)
        for pos, potential_doi in enumerate(data):
            if not bool(with_regex.match(potential_doi)):
                data[pos] = "https://doi.org/" + potential_doi
        return data

    def _validate_data(self, job_id: str, data: list[str]) -> bool:
        """
        Validate that all items in data are valid DOI strings.

        Process Flow Step 11 (sub-step): Checks all items against the DOI regex
        pattern. Superseded by _partition_dois (Step 11a) for the main pipeline.

        Checks each string against the DOI regex pattern. If DOIs are missing
        the https://doi.org/ prefix, it will be added automatically.

        Args:
            job_id: The job identifier (for logging purposes).
            data: List of potential DOI strings to validate.

        Returns:
            bool: True if all items are valid DOIs, False otherwise.

        Note:
            DOI format validated: 10.XXXX/suffix where XXXX is 4-9 digits
            and suffix contains alphanumeric characters and common punctuation.
        """
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

    def _partition_dois(self, job_id: str, data: list[str]) -> tuple[list[str], list[str]]:
        """
        Partition input strings into valid and invalid DOIs.

        Process Flow Step 11a: Separates incorrectly formatted DOIs from valid ones
        so that valid DOIs can proceed to processing while invalid DOIs are reported
        back to the user.

        Checks each string against the DOI regex pattern. If a DOI is missing
        the https://doi.org/ prefix, it is added before validation.

        Args:
            job_id: The job identifier (for logging purposes).
            data: List of potential DOI strings to partition.

        Returns:
            tuple[list[str], list[str]]: A tuple of (valid_dois, invalid_dois).

        Note:
            DOI format validated: 10.XXXX/suffix where XXXX is 4-9 digits
            and suffix contains alphanumeric characters and common punctuation.
        """
        self._logger.debug(f"job_id: {job_id}: partitioning DOIs into valid/invalid")
        doi_regex_str = r"10.\d{4,9}\/[-._;()/:A-Za-z0-9]+"
        doi_regex = re.compile(doi_regex_str)
        https_regex_str = r"^https:\/\/doi\.org\/"
        with_regex = re.compile(https_regex_str)
        valid_dois = []
        invalid_dois = []
        try:
            for potential_doi in data:
                # Add prefix if missing before validation
                normalized = potential_doi
                if not bool(with_regex.match(normalized)):
                    normalized = "https://doi.org/" + normalized
                if doi_regex.search(normalized):
                    valid_dois.append(potential_doi)
                else:
                    invalid_dois.append(potential_doi)
            self._logger.debug(
                f"job_id: {job_id}: partitioned {len(valid_dois)} valid, {len(invalid_dois)} invalid DOIs"
            )
        except TypeError as err:
            self._logger.error(f"job_id: {job_id}: Incorrect type passed to _partition_dois - validation failed")
            self._logger.error(err)
        return valid_dois, invalid_dois

    def _check_ready(self, job_id: str) -> bool:
        """
        Check if a job has received input data and is ready for processing.

        Process Flow between Steps 11 and 13: Gate check before sending DOIs
        to the requester for API processing.

        Args:
            job_id: The job identifier to check.

        Returns:
            bool: True if job exists and has input data, False otherwise.

        Raises:
            ValueError: If job exists but has no input data.
        """
        if self._validate_uuid(job_id):
            if self._jobs[job_id]["input_data"] is None:
                raise ValueError("No input data given")
            return True
        return False

    async def process(self, job_id: str, data: str | list[str]) -> None:
        """
        Process DOIs and retrieve their OpenAlex identifiers.

        Process Flow Steps 9-18: Orchestrates the full ID conversion pipeline
        from receiving data through to storing results.

        This is the main entry point for lightweight DOI conversion. It validates
        the input, queries the OpenAlex API, and stores the results in the job.

        Args:
            job_id: The UUID string identifying the job (from generate_new_job()).
            data: DOIs to process. Can be a comma-separated string or list of strings.

        Side Effects:
            - Updates job status from "initialised" -> "ready" -> "complete"
            - Populates job with output_data, submitted_count, found_count, missing_dois

        Example:
            >>> job_id = orc.generate_new_job()
            >>> await orc.process(job_id, "10.1038/nature12373")
            >>> result, status = orc.return_data(job_id)
        """
        self._logger.info(f"job_id: {job_id}: orc: processing")
        self._recieve_data(job_id, data)
        self._logger.info(f"job_id: {job_id}: orc: data received")
        if self._check_ready(job_id):
            self._logger.info(f"job_id: {job_id}: orc: data was suitable, creating task")
            await self._process_aio(job_id)  # A OpenAlexRequester function

    async def process_all(self, job_id: str, data: str | list[str]) -> None:
        """
        Process DOIs and retrieve full OpenAlex metadata.

        Process Flow Steps 9-18: Orchestrates the full metadata conversion pipeline
        from receiving data through to storing results.

        Similar to process(), but retrieves comprehensive bibliometric metadata
        for each work including citations, authors, topics, open access status, etc.

        Args:
            job_id: The UUID string identifying the job (from generate_new_job()).
            data: DOIs to process. Can be a comma-separated string or list of strings.

        Side Effects:
            - Updates job status from "initialised" -> "ready" -> "complete"
            - Populates job with full metadata in TSV format (47+ fields)

        Note:
            The output includes fields such as: doi, oa_id, title, authors,
            publication_date, cited_by_count, open_access, topics, concepts,
            keywords, referenced_works, and many more.
        """
        self._logger.info(f"job_id: {job_id}: orc: processing")
        self._recieve_data(job_id, data)
        self._logger.info(f"job_id: {job_id}: orc: data received")
        if self._check_ready(job_id):
            self._logger.info(f"job_id: {job_id}: orc: data was suitable, creating task")
            await self._process_all(job_id)  # A OpenAlexRequester function

    def return_data(self, job_id: str) -> tuple[dict, int]:
        """
        Retrieve the results of a completed processing job.

        Process Flow Step 19: Formats final response with output_data, output_full,
        submitted_count, found_count, missing_dois, and invalid_dois.

        Returns the processed data including OpenAlex IDs, CSV/TSV output,
        and statistics about the conversion (found count, missing DOIs, invalid DOIs).

        Args:
            job_id: The UUID string identifying the job.

        Returns:
            tuple: A tuple containing:
                - dict: Job results with the following keys:
                    - job_id (str): The job identifier
                    - output_data (list): List of OpenAlex IDs (if complete)
                    - output_full (str): CSV/TSV formatted results (if complete)
                    - submitted_count (int): Number of DOIs submitted
                    - found_count (int): Number of DOIs found in OpenAlex
                    - missing_dois (list): DOIs not found in OpenAlex
                    - invalid_dois (list): Input strings that failed DOI format validation
                    - status (str): Job status (if not complete)
                - int: HTTP status code (200 if complete, 204 if still processing)

        Example:
            >>> result, status_code = orc.return_data(job_id)
            >>> if status_code == 200:
            ...     print(f"Found {result['found_count']} of {result['submitted_count']} DOIs")
            ...     for doi in result['missing_dois']:
            ...         print(f"Not found: {doi}")
            ...     for doi in result['invalid_dois']:
            ...         print(f"Invalid format: {doi}")
        """
        self._validate_uuid(job_id=job_id)
        if self._jobs[job_id]["status"] == "complete":
            out_csv_data = None
            if isinstance(self._jobs[job_id]["output_csv_data"], list):
                if len(self._jobs[job_id]["output_csv_data"]) == 1:
                    out_csv_data = self._jobs[job_id]["output_csv_data"][0]
            else:
                out_csv_data = self._jobs[job_id]["output_csv_data"]
            return {
                "job_id": job_id,
                "output_data": [doi_oa_pair[1] for doi_oa_pair in self._jobs[job_id]["aio_responses"]],
                "output_full": out_csv_data,
                "submitted_count": self._jobs[job_id]["submitted_count"],
                "found_count": self._jobs[job_id]["found_count"],
                "missing_dois": self._jobs[job_id]["missing_dois"],
                "invalid_dois": self._jobs[job_id]["invalid_dois"],
            }, 200
        else:
            return {
                "job_id": job_id,
                "status": self._jobs[job_id]["status"],
            }, 204
