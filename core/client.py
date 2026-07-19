import requests


class HttpClient:
    """
    HTTP client used to send requests to target websites.
    """

    def __init__(self, timeout: float = 10.0) -> None:
        self.timeout = timeout
        self.session = requests.Session()

        self.session.headers.update(
            {
                "User-Agent": "MyRecon/1.0",
            }
        )

    def get(self, url: str) -> requests.Response:
        """
        Send a GET request and automatically follow redirects.
        """
        return self.session.get(
            url,
            timeout=self.timeout,
            allow_redirects=True,
        )

    def close(self) -> None:
        """
        Close the underlying HTTP session.
        """
        self.session.close()