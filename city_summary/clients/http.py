import requests
from requests.exceptions import Timeout, ConnectionError as ReqConnectionError
import time

def http_get(url: str, params: dict | None, timeout: float = 10, retries: int = 3) -> requests.Response:

    RETRY_STATUSES = {500, 502, 503, 504}

    for attempt in range(retries):
        wait = 1

        try:
            resp = requests.get(url=url, params=params, timeout=timeout)
        except (Timeout, ReqConnectionError):
            pass

        else:
            if resp.status_code == 429:
                retry_after = resp.headers.get("Retry-After", "")
                if retry_after.isdigit():
                    wait = int(retry_after)
            elif resp.status_code not in RETRY_STATUSES:
                return resp

        if attempt < retries - 1:
            time.sleep(wait)

    raise ConnectionError(f"{url} недоступен после {retries} попыток")

