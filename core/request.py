from time import perf_counter

from requests import Response

from core.client import HttpClient


def send_get_request(
    url: str,
    timeout: float = 10.0,
) -> tuple[Response, float]:
    """
    Send a GET request and measure the total request time.

    Returns:
        A tuple containing the response and response time
        in milliseconds.
    """
    client = HttpClient(timeout=timeout)

    start_time = perf_counter()

    try:
        response = client.get(url)
    finally:
        client.close()

    response_time_ms = round(
        (perf_counter() - start_time) * 1000,
        2,
    )

    return response, response_time_ms