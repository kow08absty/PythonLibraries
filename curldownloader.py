import io
import pycurl
import time
from urllib.parse import urlencode
from collections import Iterable

import certifi


class HTTPResult:
    def __init__(self, status_code: int, body_buffer: io.BufferedIOBase, heads: tuple = None):
        self._status_code = status_code
        self._body_buffer = body_buffer
        self._heads = heads

    def get_status_code(self) -> int:
        return self._status_code

    def get_body(self) -> io.BufferedIOBase:
        return self._body_buffer

    def get_head(self) -> tuple:
        return self._heads


class CurlDownloader:
    def __init__(self):
        self._wait_secs = 0
        self._curl = pycurl.Curl()
        self._cache_body = None
        self._cache_head = None
        self._heads = None

    def _prep(self):
        self._cache_body = io.BytesIO()
        self._cache_head = io.BytesIO()
        self._curl.setopt(pycurl.CAINFO, certifi.where())
        self._curl.setopt(pycurl.WRITEFUNCTION, self._cache_body.write)
        self._curl.setopt(pycurl.HEADERFUNCTION, self._cache_head.write)
        time.sleep(self._wait_secs)

    def _perform(self) -> HTTPResult:
        self._curl.perform()
        self._cache_body.seek(0)
        self._cache_head.seek(0)
        _headers = []
        for _item in self._cache_head.read().decode('ascii').split('\r\n'):
            if _item:
                _headers.append(_item)
        return HTTPResult(self._curl.getinfo(pycurl.HTTP_CODE), self._cache_body, tuple(_headers))

    def get(self, url: str) -> HTTPResult:
        self._prep()
        self._curl.setopt(pycurl.URL, url)
        return self._perform()

    def post(self, url: str, data: Iterable) -> HTTPResult:
        self._prep()
        self._curl.setopt(pycurl.URL, url)
        self._curl.setopt(pycurl.CUSTOMREQUEST, 'POST')
        self._curl.setopt(pycurl.POSTFIELDS, urlencode(data))
        return self._perform()

    def implicitly_wait(self, sec: int):
        self._wait_secs = sec
