"""
OpenAlex API Requester Module.

This module provides the OpenAlexRequester class for communicating with the
OpenAlex API. It handles rate limiting, request chunking, and response processing
for bulk DOI to OpenAlex ID conversion.

The module implements polite API usage following OpenAlex guidelines:
- Rate limiting to max 8 concurrent requests per second
- Exponential backoff on 429 (Too Many Requests) responses
- Email-based polite pool access for faster response times

Classes:
    OpenAlexRequester: Base class for OpenAlex API communication.

Constants:
    HEALTHCHECK_ADDR: URL for health check endpoint.
    HEALTH_CHECK_RESPONSE: Expected response from healthy OpenAlex API.

References:
    OpenAlex API Documentation: https://docs.openalex.org/how-to-use-the-api/api-overview
    OpenAlex Rate Limits: https://docs.openalex.org/how-to-use-the-api/rate-limits-and-authentication
"""

import asyncio
import functools
import logging
import re
from typing import Generator

import aiometer
import requests
from httpx import AsyncClient

#: URL for OpenAlex API health check endpoint
HEALTHCHECK_ADDR = "https://api.openalex.org/?mailto=jack.culbert@gesis.org"

#: Expected JSON response from a healthy OpenAlex API
HEALTH_CHECK_RESPONSE = {"documentation_url": "https://openalex.org/rest-api", "msg": "Don't panic", "version": "0.0.1"}


class OpenAlexRequester:
    """
    Base class for making requests to the OpenAlex API.

    Provides functionality for:
    - Async HTTP requests with rate limiting via aiometer
    - Chunking large DOI lists into API-compliant batches (max 50 per request)
    - Exponential backoff retry logic for rate limit errors
    - DOI normalization to consistent format

    This class is designed to be inherited by OpenResearchConverter, which
    adds job management and validation logic.

    Attributes:
        _logger: Logger instance for debug and error messages.
        _jobs (dict): Dictionary storing job data, keyed by job_id.
        _rate_limit_interval (int): Seconds between rate limit checks.
        _max_concurrent_per_second_aio (int): Maximum concurrent requests per second.
        _aio_client (AsyncClient): httpx async client for API requests.

    Example:
        >>> requester = OpenAlexRequester()
        >>> healthy, status = await requester.health_check()
        >>> print(f"OpenAlex API healthy: {healthy['healthy']}")
    """

    def __init__(self) -> None:
        """
        Initialize the OpenAlexRequester with default configuration.

        Sets up logging, initializes the jobs dictionary, and creates an
        async HTTP client for API communication.
        """
        logging.basicConfig(level=logging.DEBUG)
        self._logger = logging.getLogger(__name__)
        self._jobs = {}
        self._rate_limit_interval = 1
        self._max_concurrent_per_second_aio = 8
        self._aio_client = AsyncClient()

    async def _process_aio(self, job_id: str):
        """
        Process DOIs and retrieve OpenAlex IDs using async concurrent requests.

        Chunks the input DOIs, makes parallel requests to OpenAlex API,
        and stores the results. Tracks which DOIs were found vs missing.

        Args:
            job_id: The UUID string identifying the job to process.

        Side Effects:
            Updates the job dictionary with:
            - aio_responses: List of (doi, openalex_id) tuples, sorted by input order
            - output_csv_data: CSV string with doi,oa_id columns
            - submitted_count: Total DOIs submitted
            - found_count: DOIs successfully matched
            - missing_dois: List of DOIs not found in OpenAlex
            - status: Set to "complete" on success

        Note:
            Uses aiometer for rate-limited concurrent requests (max 8/second).
            Results are re-sorted to match the original input order.
        """
        oa_requests = self._prepare_chunks(job_id)
        if oa_requests is not None:
            self._logger.info(f"job_id: {job_id}: Requesting via aiometer")
            responses = await aiometer.run_all(
                [functools.partial(self._request, query) for query in oa_requests],
                max_per_second=self._max_concurrent_per_second_aio,
                max_at_once=self._max_concurrent_per_second_aio,
            )
            self._logger.info(f"job_id: {job_id}: Requests via aiometer successful")
            shuffled_responses = [(work["doi"], work["id"]) for response in responses for work in response["results"]]
            formatted_input_dois = list(map(self._doi_str_formatter, self._jobs[job_id]["input_data"]))
            # Only include DOIs that were found in the response
            returned_dois = {pair[0] for pair in shuffled_responses}
            found_input_dois = [doi for doi in formatted_input_dois if doi in returned_dois]
            self._jobs[job_id]["aio_responses"] = sorted(
                shuffled_responses, key=lambda pair: found_input_dois.index(pair[0])
            )
            self._logger.info(f"job_id: {job_id}: aiometer sorting successful")
            # Track missing DOIs
            missing_dois = [doi for doi in formatted_input_dois if doi not in returned_dois]
            self._jobs[job_id]["submitted_count"] = len(formatted_input_dois)
            self._jobs[job_id]["found_count"] = len(shuffled_responses)
            self._jobs[job_id]["missing_dois"] = missing_dois
            self._logger.info(f"job_id: {job_id}: Found {len(shuffled_responses)}/{len(formatted_input_dois)} DOIs")
            self._jobs[job_id]["output_csv_data"] = "doi, oa_id\n" + "".join(
                [f"{doi_val},{oi_val}\n" for (doi_val, oi_val) in self._jobs[job_id]["aio_responses"]]
            )
            self._logger.info(f"job_id: {job_id}: aiometer csv string creation successful")
            self._jobs[job_id]["status"] = "complete"
        else:
            self._logger.error(f"job_id: {job_id}: Chunking failed in process for {job_id}, returning False")

    async def _process_all(self, job_id: str):
        """
        Process DOIs and retrieve full OpenAlex metadata using async concurrent requests.

        Similar to _process_aio but retrieves comprehensive bibliometric metadata
        for each work instead of just the OpenAlex ID.

        Args:
            job_id: The UUID string identifying the job to process.

        Side Effects:
            Updates the job dictionary with:
            - aio_responses: List of tuples containing all metadata fields
            - output_csv_data: TSV string with 47+ metadata columns
            - submitted_count: Total DOIs submitted
            - found_count: DOIs successfully matched
            - missing_dois: List of DOIs not found in OpenAlex
            - status: Set to "complete" on success

        Note:
            The output TSV includes fields such as: doi, oa_id, ids, title,
            language, display_name, is_retracted, authorships, publication_date,
            publication_year, open_access, primary_topic, topics, concepts,
            keywords, cited_by_count, referenced_works, and many more.
        """
        oa_requests = self._prepare_chunks_full(job_id)
        if oa_requests is not None:
            self._logger.info(f"job_id: {job_id}: Requesting bulk data via aiometer")
            responses = await aiometer.run_all(
                [functools.partial(self._request, query) for query in oa_requests],
                max_per_second=self._max_concurrent_per_second_aio,
                max_at_once=self._max_concurrent_per_second_aio,
            )
            self._logger.info(f"job_id: {job_id}: Bulk Requests via aiometer successful")
            # OpenAlex metadata fields to extract for each work
            keys = [
                "ids",
                "title",
                "language",
                "display_name",
                "is_retracted",
                "is_paratext",
                "corresponding_author_ids",
                "authorships",
                "publication_date",
                "publication_year",
                "created_date",
                "updated_date",
                "versions",
                "biblio",
                "type",
                "type_crossref",
                "indexed_in",
                "open_access",
                "best_oa_location",
                "primary_topic",
                "topics",
                "concepts",
                "keywords",
                "mesh",
                "cited_by_api_url",
                "cited_by_count",
                "counts_by_year",
                "cited_by_percentile_year",
                "citation_normalized_percentile",
                "fwci",
                "institutions_distinct_count",
                "corresponding_institution_ids",
                "institution_assertions",
                "primary_location",
                "locations",
                "locations_count",
                "countries_distinct_count",
                "sustainable_development_goals",
                "referenced_works",
                "referenced_works_count",
                "related_works",
                "apc_paid",
                "apc_list",
                "datasets",
                "grants",
                "has_fulltext",
                "fulltext_origin",
                "abstract_inverted_index",
            ]
            shuffled_responses = [
                (work["doi"], work["id"]) + tuple(work[key] if key in work.keys() else "" for key in keys)
                for response in responses
                for work in response["results"]
            ]
            formatted_input_dois = list(map(self._doi_str_formatter, self._jobs[job_id]["input_data"]))
            # Only include DOIs that were found in the response
            returned_dois = {pair[0] for pair in shuffled_responses}
            found_input_dois = [doi for doi in formatted_input_dois if doi in returned_dois]
            self._jobs[job_id]["aio_responses"] = sorted(
                shuffled_responses, key=lambda pair: found_input_dois.index(pair[0])
            )
            self._logger.info(f"job_id: {job_id}: aiometer sorting successful")
            # Track missing DOIs
            missing_dois = [doi for doi in formatted_input_dois if doi not in returned_dois]
            self._jobs[job_id]["submitted_count"] = len(formatted_input_dois)
            self._jobs[job_id]["found_count"] = len(shuffled_responses)
            self._jobs[job_id]["missing_dois"] = missing_dois
            self._logger.info(f"job_id: {job_id}: Found {len(shuffled_responses)}/{len(formatted_input_dois)} DOIs")
            self._jobs[job_id]["output_csv_data"] = (
                "sep=\t\n"
                + "doi\toa_id\t"
                + "\t".join(keys)
                + "\n"
                + "".join(
                    [
                        "\t".join(
                            [
                                str(x).replace("\n", "\\n").replace("\r", "\\r").replace("\t", "    ")
                                for x in aio_response
                            ]
                        )
                        + "\n"
                        for aio_response in self._jobs[job_id]["aio_responses"]
                    ]
                ),
            )
            self._logger.info(f"job_id: {job_id}: aiometer bulk csv string creation successful")
            self._jobs[job_id]["status"] = "complete"
        else:
            self._logger.error(f"job_id: {job_id}: Chunking failed in process_all for {job_id}, returning False")

    async def health_check(self) -> tuple[dict, int]:
        """
        Check connectivity to the OpenAlex API.

        Makes a test request to the OpenAlex API root endpoint and verifies
        the response matches the expected format.

        Returns:
            tuple: A tuple containing:
                - dict: Health status with keys:
                    - healthy (bool): True if API is accessible and responding correctly
                    - error (bool or str): False if healthy, error message otherwise
                - int: HTTP status code (418 if healthy, 200 if unhealthy)

        Note:
            The unconventional use of 418 (I'm a teapot) for healthy status
            allows easy differentiation in monitoring systems. This endpoint
            can be called every 90 seconds without breaking OpenAlex politeness rules.

        Example:
            >>> result, status = await requester.health_check()
            >>> if status == 418:
            ...     print("OpenAlex API is healthy")
        """
        try:
            response = await self._aio_client.get(HEALTHCHECK_ADDR)
            if response.json() != HEALTH_CHECK_RESPONSE:
                self._logger.error("Health check failed - response not as expected")
                return {"healthy": False, "error": "unknown"}, 200
        except requests.ConnectionError as conn_err:
            self._logger.error("Health check failed - Connection error")
            self._logger.error(conn_err)
            return {"healthy": False, "error": conn_err.__str__}, 200
        except requests.JSONDecodeError as decode_err:
            self._logger.error("Health check failed - JSON decode error")
            self._logger.error(decode_err)
            return {"healthy": False, "error": decode_err.__str__}, 200
        return {"healthy": True, "error": False}, 418

    def _prepare_chunks(self, job_id: str) -> list[str] | None:
        """
        Prepare OpenAlex API request URLs for lightweight (ID-only) queries.

        Chunks the input DOIs and constructs API URLs with the 'select' parameter
        to retrieve only doi and id fields (faster response).

        Args:
            job_id: The UUID string identifying the job.

        Returns:
            list[str] | None: List of OpenAlex API URLs, or None if chunking failed.

        Note:
            Uses the 'select=id,doi' parameter to minimize response size.
            Each URL queries up to 50 DOIs using the pipe-separated filter syntax.
        """
        chunked_data = self._chunk_input_data(job_id)
        if chunked_data is not None:
            chunked_data = list(chunked_data)
            return [
                f"https://api.openalex.org/works?filter=doi:{'|'.join(chunks)}&per-page={chunklen}&mailto={self._jobs[job_id]['email']}&select=id,doi"
                for chunks, chunklen in chunked_data
            ]

        else:
            self._logger.error(f"job_id: {job_id}: _prepare chunks failed ")
            return None

    def _prepare_chunks_full(self, job_id: str) -> list[str] | None:
        """
        Prepare OpenAlex API request URLs for full metadata queries.

        Chunks the input DOIs and constructs API URLs that retrieve all
        available metadata fields for each work.

        Args:
            job_id: The UUID string identifying the job.

        Returns:
            list[str] | None: List of OpenAlex API URLs, or None if chunking failed.

        Note:
            Does not use the 'select' parameter, so OpenAlex returns all fields.
            Response includes 47+ metadata fields per work.
        """
        chunked_data = self._chunk_input_data(job_id)
        if chunked_data is not None:
            chunked_data = list(chunked_data)
            return [
                f"https://api.openalex.org/works?filter=doi:{'|'.join(chunks)}&per-page={chunklen}&mailto={self._jobs[job_id]['email']}"
                for chunks, chunklen in chunked_data
            ]

        else:
            self._logger.error(f"job_id: {job_id}: _prepare chunks failed ")
            return None

    def _chunk_input_data(
        self, job_id: str, chunksize: int = 50
    ) -> Generator[tuple[list[str], int], None, None] | None:
        """
        Split input DOIs into chunks for API requests.

        OpenAlex API has a limit on the number of items that can be queried
        in a single request. This method splits large DOI lists into
        manageable chunks.

        Args:
            job_id: The UUID string identifying the job.
            chunksize: Maximum DOIs per chunk (default 50, max allowed by OpenAlex).

        Yields:
            tuple[list[str], int]: Tuple of (DOI list, chunk length) for each chunk.

        Returns:
            None: If chunksize is invalid (not int or outside range 1-50).

        Note:
            The OpenAlex API allows a maximum of 50 items per filter query.
            Chunk length is included in the yield to set the per-page parameter.
        """
        if not isinstance(chunksize, int):
            self._logger.error(f"job_id: {job_id}: Non-int passed as chunk")
            return None
        if 0 < chunksize and chunksize < 51:
            for i in range(0, len(self._jobs[job_id]["input_data"]), chunksize):
                yield (
                    self._jobs[job_id]["input_data"][i : i + chunksize],
                    len(self._jobs[job_id]["input_data"][i : i + chunksize]),
                )
        else:
            self._logger.error(f"job_id: {job_id}: Chunksize parameter was outside range [1,50]")
            return None

    def _doi_str_formatter(self, input_str: str) -> str:
        """
        Normalize a DOI string to consistent https://doi.org/ format.

        Handles various input formats:
        - Raw DOI: "10.1234/abc" -> "https://doi.org/10.1234/abc"
        - HTTP URL: "http://doi.org/10.1234/abc" -> "https://doi.org/10.1234/abc"
        - HTTPS URL: "https://doi.org/10.1234/abc" -> unchanged

        Args:
            input_str: DOI string in any supported format.

        Returns:
            str: Normalized DOI URL in lowercase with https://doi.org/ prefix.

        Example:
            >>> _doi_str_formatter("10.1038/nature12373")
            "https://doi.org/10.1038/nature12373"
            >>> _doi_str_formatter("HTTP://DOI.ORG/10.1038/NATURE12373")
            "https://doi.org/10.1038/nature12373"
        """
        https_regex_str = r"^https:\/\/doi\.org\/"
        with_regex = re.compile(https_regex_str)
        http_regex_str = r"^http:\/\/doi\.org\/"
        with_http_regex = re.compile(http_regex_str)
        if not bool(with_regex.match(input_str)):
            if bool(with_http_regex.match(input_str)):
                output_str = input_str[0:4] + "s" + input_str[4:]
            else:
                output_str = "https://doi.org/" + input_str
        else:
            output_str = input_str
        return output_str.lower()

    async def _request(self, request: str) -> dict:
        """
        Make an async HTTP GET request to OpenAlex with retry logic.

        Implements exponential backoff for rate limit (429) responses,
        retrying up to 5 times with delays of 1, 2, 4, 8, 16 seconds.

        Args:
            request: The full URL to request.

        Returns:
            dict: JSON response from the API.

        Note:
            This method is designed to be used with aiometer for concurrent
            rate-limited requests. The exponential backoff ensures compliance
            with OpenAlex rate limits even under heavy load.
        """
        self._logger.debug(request)
        self._logger.debug("DEBUG: aiometer request sent to openalex")
        response = await self._aio_client.get(request)
        self._logger.debug(f"DEBUG: aiometer request returned from openalex, response code: {response.status_code}")
        retries = 0
        while response.status_code == 429 and retries < 5:
            await asyncio.sleep(pow(2, retries))  # Exponential backoff
            self._logger.debug(f"DEBUG: RETRY aiometer request, retries: {retries}")
            response = await self._aio_client.get(request)
            retries += 1
        return response.json()
