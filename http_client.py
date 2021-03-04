import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import Timeout, ConnectionError
from urllib3.util.retry import Retry

class TimeoutHTTPAdapter(HTTPAdapter):

    def __init__(self, *args, **kwargs):
        self.timeout = kwargs.pop('timeout', 15)
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)

class HTTP_CLIENT():
    def client(self):
        retry_strategy = Retry(
            total=3,
            backoff_factor=1.0,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        timeout = 15
        adapter = TimeoutHTTPAdapter(max_retries=retry_strategy, timeout=timeout)
        http = requests.Session()
        http.mount("https://", adapter)
        http.mount("http://", adapter)
        return http
