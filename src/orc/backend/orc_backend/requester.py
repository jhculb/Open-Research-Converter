import asyncio
import functools
import logging
import re
from typing import Generator

import aiometer
import requests
from httpx import AsyncClient

HEALTHCHECK_ADDR = "https://api.openalex.org/?mailto=jack.culbert@gesis.org"
HEALTH_CHECK_RESPONSE = {"documentation_url": "https://openalex.org/rest-api", "msg": "Don't panic", "version": "0.0.1"}
# Can do healthcheck every 90 seconds and not break politeness


class OpenAlexRequester:
    """This class contains code to interface and process requests to the OpenAlex API"""

    def __init__(self) -> None:
        """Instantiate a requester, initialising the parameters"""
        logging.basicConfig(level=logging.DEBUG)
        self._logger = logging.getLogger(__name__)
        self._jobs = {}
        self._rate_limit_interval = 1
        self._max_concurrent_per_second_aio = 8
        self._aio_client = AsyncClient()

    async def _process_aio(self, job_id: str):
        """4. Orchestrates the asynchronous requests for OpenAlex WorkIDs"""
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
            self._jobs[job_id]["aio_responses"] = sorted(
                shuffled_responses, key=lambda pair: formatted_input_dois.index(pair[0])
            )
            self._logger.info(f"job_id: {job_id}: aiometer sorting successful")
            self._jobs[job_id]["output_csv_data"] = "doi, oa_id\n" + "".join(
                [f"{doi_val},{oi_val}\n" for (doi_val, oi_val) in self._jobs[job_id]["aio_responses"]]
            )
            self._logger.info(f"job_id: {job_id}: aiometer csv string creation successful")
            self._jobs[job_id]["status"] = "complete"
        else:
            self._logger.error(f"job_id: {job_id}: Chunking failed in process for {job_id}, returning False")

    async def _process_all(self, job_id: str):
        """4. Orchestrates the asynchronous requests for OpenAlex full records"""
        oa_requests = self._prepare_chunks_full(job_id)
        if oa_requests is not None:
            self._logger.info(f"job_id: {job_id}: Requesting bulk data via aiometer")
            responses = await aiometer.run_all(
                [functools.partial(self._request, query) for query in oa_requests],
                max_per_second=self._max_concurrent_per_second_aio,
                max_at_once=self._max_concurrent_per_second_aio,
            )
            self._logger.info(f"job_id: {job_id}: Bulk Requests via aiometer successful")
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
            self._jobs[job_id]["aio_responses"] = sorted(
                shuffled_responses, key=lambda pair: formatted_input_dois.index(pair[0])
            )
            self._logger.info(f"job_id: {job_id}: aiometer sorting successful")
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

    async def health_check(self) -> tuple:
        """Hook"""
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
        """5. Splits the DOIs into chunks of length ._chunklen and formats them into URLs requesting the ID and DOI"""
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
        """5. Splits the DOIs into chunks of length ._chunklen and formats them into URLs requesting the full record"""
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
        """5.1 Does the chunking of a list into smaller lists of length chunksize or less"""
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
        """7. Checks the input string is a DOI and returns a regularised lower case format"""
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

    async def _request(self, request: str):
        """6. Requests data from OpenAlex via the request string"""
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
