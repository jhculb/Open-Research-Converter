import asyncio
import datetime as dt
import functools
import itertools
import logging
import re
from typing import Generator

import aiometer
import requests
from httpx import AsyncClient

HEALTHCHECK_ADDR = "https://api.openalex.org/?mailto=jack.culbert@gesis.org"
HEALTH_CHECK_RESPONSE = {"documentation_url": "https://openalex.org/rest-api", "msg": "Don't panic", "version": "0.0.1"}
# Can do healthcheck every 90 seconds and not break politeness

# unless you keep a strong reference to a running task, it can be dropped during execution
# https://docs.python.org/3/library/asyncio-task.html#asyncio.create_task
_background_tasks = set()


class RateLimitedClient(AsyncClient):
    """httpx.AsyncClient with a rate limit."""

    # Thanks go to clbarnes: https://github.com/encode/httpx/issues/815

    def __init__(self, interval: dt.timedelta | float, count=1, **kwargs):
        """
        Parameters
        ----------
        interval : Union[dt.timedelta, float]
            Length of interval.
            If a float is given, seconds are assumed.
        numerator : int, optional
            Number of requests which can be sent in any given interval (default 1).
        """
        if isinstance(interval, dt.timedelta):
            interval = interval.total_seconds()

        self.interval = interval
        self.semaphore = asyncio.Semaphore(count)
        super().__init__(**kwargs)

    def _schedule_semaphore_release(self):
        wait = asyncio.create_task(asyncio.sleep(self.interval))
        _background_tasks.add(wait)

        def wait_cb(task):
            self.semaphore.release()
            _background_tasks.discard(task)

        wait.add_done_callback(wait_cb)


class openalex_requester:
    def __init__(self) -> None:
        logging.basicConfig(level=logging.DEBUG)
        self._logger = logging.getLogger(__name__)
        self._jobs = {}
        self._rate_limit_interval = 1
        self._max_concurrent_per_second_aio = 8
        self._client = RateLimitedClient(1.0, 9)
        self._aio_client = AsyncClient()

    async def health_check(self) -> tuple:
        try:
            response = await self._client.get(HEALTHCHECK_ADDR)
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
        chunked_data = self._chunk_input_data(job_id)
        if chunked_data is not None:
            chunked_data = list(chunked_data)
            return [
                f'https://api.openalex.org/works?filter=doi:{"|".join(chunks)}&per-page={chunklen}&mailto={self._jobs[job_id]["email"]}&select=id,doi'
                for chunks, chunklen in chunked_data
            ]

        else:
            self._logger.error(f"job_id: {job_id}: _prepare chunks failed ")
            return None

    async def _fetch(self, request: str):
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

    async def _process_aio(self, job_id: str):
        oa_requests = self._prepare_chunks(job_id)
        if oa_requests is not None:
            self._logger.info(f"job_id: {job_id}: Requesting via aiometer")
            responses = await aiometer.run_all(
                [functools.partial(self._fetch, query) for query in oa_requests],
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

    async def _process(self, job_id: str):
        self._jobs[job_id]["status"] = "processing"
        self._jobs[job_id]["_tasklist"] = []
        chunked_data = self._chunk_input_data(job_id)
        if chunked_data is not None:
            chunked_data = list(chunked_data)
            tasks = set()
            for pos, (chunks, chunklen) in enumerate(chunked_data):
                tasks.add(asyncio.create_task(self._request(chunks, job_id, chunklen, pos)))
                self._logger.debug(f"job_id: {job_id}: Request task added for chunk {pos} of {job_id}")
            await asyncio.gather(*tasks)
            results = [self._jobs[job_id]["responses"][pos_iter] for pos_iter in range(0, len(chunked_data))]
            csv_results = [self._jobs[job_id]["csv_responses"][pos_iter] for pos_iter in range(0, len(chunked_data))]
            self._logger.info(f"job_id: {job_id}: results completed for {job_id}")
        else:
            self._logger.error(f"job_id: {job_id}: Chunking failed in process for {job_id}, returning False")
        output = list(itertools.chain.from_iterable(results))
        csv_output = list(itertools.chain.from_iterable(csv_results))
        self._logger.debug(csv_output)
        self._logger.debug(csv_results)
        self._jobs[job_id]["output_data"] = output
        self._jobs[job_id]["output_csv_data"] = "doi, oa_id\n" + "".join(
            [f"{doi_val},{oi_val}\n" for csv_inner in csv_results for (doi_val, oi_val) in csv_inner]
        )
        self._jobs[job_id]["status"] = "complete"

    def _chunk_input_data(
        self, job_id: str, chunksize: int = 50
    ) -> Generator[tuple[list[str], int], None, None] | None:
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

    async def _request(self, chunked_data: list[str], job_id: str, chunklen: int, pos: int) -> None:
        self._logger.info(f"job_id: {job_id}: sending request {pos}")
        formatted_chunk = "|".join(chunked_data)
        response = await self._client.get(
            f'https://api.openalex.org/works?filter=doi:{formatted_chunk}&per-page={chunklen}&mailto={self._jobs[job_id]["email"]}&select=id,doi'
        )
        # TODO: add Nina Request functionality for searching the title && Year && Surname / All authors
        shuffled_ids = [work["id"] for work in response.json()["results"]]
        dois = [work["doi"] for work in response.json()["results"]]
        filtered_chunk = list(map(self._doi_str_formatter, chunked_data))
        positions = [list(map(str.lower, filtered_chunk)).index(doi) for doi in dois]
        ids = [x for _, x in sorted(zip(positions, shuffled_ids, strict=True), key=lambda pair: pair[0])]
        csv_ids = [
            ([list(map(str.lower, chunked_data)) for doi in dois][pos][y], x)
            for y, x in sorted(zip(positions, shuffled_ids, strict=True), key=lambda pair: pair[0])
        ]
        self._jobs[job_id]["responses"][pos] = ids
        self._jobs[job_id]["csv_responses"][pos] = csv_ids
        self._jobs[job_id]["progress"] += chunklen
        self._logger.info(f"job_id: {job_id}: _request {pos} complete")
