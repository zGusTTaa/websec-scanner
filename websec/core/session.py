import requests

from websec.utils.logger import get_logger

logger = get_logger(__name__)


class Session:
    """Wrapper da requests.Session com defaults seguros."""

    def __init__(
        self,
        user_agent: str = "WebSecScanner/0.1",
        timeout: int = 10,
        retries: int = 2,
    ):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": user_agent})

        adapter = requests.adapters.HTTPAdapter(max_retries=retries)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def get(self, url: str, **kwargs) -> requests.Response | None:
        return self._request("GET", url, **kwargs)

    def post(self, url: str, **kwargs) -> requests.Response | None:
        return self._request("POST", url, **kwargs)

    def _request(self, method: str, url: str, **kwargs) -> requests.Response | None:
        kwargs.setdefault("timeout", self.timeout)
        kwargs.setdefault("allow_redirects", True)
        try:
            response = self.session.request(method, url, **kwargs)
            logger.debug(f"{method} {url} → {response.status_code}")
            return response
        except requests.RequestException as e:
            logger.warning(f"Falha em {method} {url}: {e}")
            return None