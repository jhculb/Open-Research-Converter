import asyncio
import datetime as dt
import itertools
import logging
import typing
from functools import wraps

import requests
from httpx import AsyncClient, Response

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

    @wraps(AsyncClient.send)
    async def send(self, *args, **kwargs) -> Response:
        await self.semaphore.acquire()
        send = asyncio.create_task(super().send(*args, **kwargs))
        self._schedule_semaphore_release()
        return await send


class openalex_requester:
    def __init__(self) -> None:
        logging.basicConfig(level=logging.DEBUG)
        self._logger = logging.getLogger(__name__)
        self._jobs = {}
        self._client = RateLimitedClient(1, 9)

    def health_check(self) -> bool:
        return True
        try:
            response = self._session.get(HEALTHCHECK_ADDR)
            if response.json() != HEALTH_CHECK_RESPONSE:
                self._logger.error("Health check failed - response not as expected")
                return False
        except requests.ConnectionError as conn_err:
            self._logger.error("Health check failed - Connection error")
            self._logger.error(conn_err)
            return False
        except requests.JSONDecodeError as decode_err:
            self._logger.error("Health check failed - JSON decode error")
            self._logger.error(decode_err)
            return False
        return True

    async def _process(self, job_id: str):
        self._jobs[job_id]["status"] = "processing"
        self._jobs[job_id]["_tasklist"] = []
        chunked_data = self._chunk_input_data(job_id)
        if chunked_data is not None:
            chunked_data = list(chunked_data)
            async with asyncio.TaskGroup() as tg:
                for pos, (chunks, chunklen) in enumerate(chunked_data):
                    self._jobs[job_id]["_tasklist"].append(tg.create_task(self._request(chunks, job_id, chunklen, pos)))
                    self._logger.debug(f"Request task added for chunk {pos}")
        else:
            self._logger.error(f"Chunking failed in process for {job_id}, returning False")
        results = [task.result() for task in self._jobs[job_id]["_tasklist"]]
        output = list(itertools.chain.from_iterable(results))
        self._jobs[job_id]["output_data"] = output
        self._jobs[job_id]["status"] = "complete"

    def _chunk_input_data(
        self, job_id: str, chunksize: int = 50
    ) -> typing.Generator[tuple[str, int], None, None] | None:
        if not isinstance(chunksize, int):
            self._logger.error("Non-int passed as chunk")
            return None
        if 0 < chunksize and chunksize < 51:
            for i in range(0, len(self._jobs[job_id]["input_data"]), chunksize):
                yield (
                    "|".join(self._jobs[job_id]["input_data"][i : i + chunksize]),
                    len(self._jobs[job_id]["input_data"][i : i + chunksize]),
                )
        else:
            self._logger.error("Chunksize parameter was outside range [1,50]")
            return None

    async def _request(self, chunked_data: str, job_id: str, chunklen: int, pos: int) -> list[str]:
        self._logger.info(f"sending request {pos} for job {job_id}")
        async with AsyncClient() as client:
            response = await client.get(
                f'https://api.openalex.org/works?filter=doi:{chunked_data}&per-page={chunklen}&mailto={self._jobs[job_id]["email"]}'
            )
        # TODO: add functionality for searching the title && Year && Surname / All authors
        ids = [work["id"] for work in response.json()["results"]]
        async with self._jobs[job_id]["lock"]:
            if self._jobs[job_id]["output_data"] is None:
                self._jobs[job_id]["output_data"] = ids
            else:
                self._jobs[job_id]["output_data"].extend(ids)
        self._jobs[job_id]["progress"] += chunklen
        return ids
