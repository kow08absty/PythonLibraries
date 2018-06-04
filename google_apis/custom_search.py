from ..curldownloader import CurlDownloader
from urllib.parse import urlencode
import json


class GoogleCustomSearch:
    def __init__(self, api_key: str, engine_id: str):
        self._API_KEY = api_key
        self._ENGINE_ID = engine_id
        self._downloader = CurlDownloader()

    def exec(self, keyword: str, site: str = ''):
        _queries = {
            'key': self._API_KEY,
            'cx': self._ENGINE_ID,
            'q': keyword
        }
        if len(site) > 0:
            _queries['q'] += ' site:' + site
        _url = 'https://www.googleapis.com/customsearch/v1?' + urlencode(_queries)
        return json.loads(self._downloader.get(_url).get_body().read().decode('UTF-8'))
